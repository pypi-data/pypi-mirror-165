from __future__ import annotations

import math
import os
from datetime import datetime
from functools import partial
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, Tuple

import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe
from hyperopt.pyll.base import scope
from keras import backend as K
from keras import callbacks
from keras.layers import Dense, Input, InputSpec, Wrapper, concatenate
from keras.models import Model
from keras.optimizers import Optimizer
from sklearn.model_selection import train_test_split
from tensorflow import keras

import nemo_bo.utils.logger as logging_nemo
import nemo_bo.utils.perf_metrics as pm
from nemo_bo.models.base.base_model import Base_Model
from nemo_bo.models.base.nn_save_checkpoint import SaveModelCheckPoint
from nemo_bo.utils.data_proc import sort_train_test_split_shuffle

if TYPE_CHECKING:
    from nemo_bo.opt.objectives import RegressionObjective
    from nemo_bo.opt.variables import VariablesList

try:
    logging_nemo.logging_path
    logger = logging_nemo.logging_nemo_child(os.path.basename(__file__))
except AttributeError:
    logger = logging_nemo.logging_nemo_master(os.path.basename(__file__))


tfpl = tfp.layers
tfd = tfp.distributions

gpus = tf.config.list_physical_devices("GPU")
if gpus:
    try:
        # Memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.list_logical_devices("GPU")
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        print(e)


class ConcreteDropout(Wrapper):
    """

    Code copied from:
    João Caldeira, Brian Nord, Deeply Uncertain: Comparing Methods of Uncertainty Quantification in Deep Learning
    Algorithms, arXiv:2004.10710, https://github.com/deepskies/DeeplyUncertain-Public

    """

    def __init__(
        self,
        layer,
        weight_regularizer=0,
        dropout_regularizer=1e-5,
        init_min=0.1,
        init_max=0.1,
        is_mc_dropout=True,
        **kwargs,
    ):
        assert "kernel_regularizer" not in kwargs
        super(ConcreteDropout, self).__init__(layer, **kwargs)
        self.weight_regularizer = weight_regularizer
        self.dropout_regularizer = dropout_regularizer
        self.is_mc_dropout = is_mc_dropout
        self.supports_masking = True
        self.p_logit = None
        self.init_min = np.log(init_min) - np.log(1.0 - init_min)
        self.init_max = np.log(init_max) - np.log(1.0 - init_max)

    def build(self, input_shape=None):
        self.input_spec = InputSpec(shape=input_shape)
        if not self.layer.built:
            self.layer.build(input_shape)
            self.layer.built = True
        super(ConcreteDropout, self).build()

        # initialise p
        self.p_logit = self.add_weight(
            name="p_logit",
            shape=(1,),
            initializer=tf.random_uniform_initializer(self.init_min, self.init_max),
            dtype=tf.dtypes.float64,
            trainable=True,
        )

    def compute_output_shape(self, input_shape):
        return self.layer.compute_output_shape(input_shape)

    def concrete_dropout(self, x, p):
        eps = 1e-07
        temp = 0.1

        unif_noise = tf.random.uniform(shape=tf.shape(x))
        drop_prob = (
            tf.math.log(p + eps)
            - tf.math.log(1.0 - p + eps)
            + tf.math.log(unif_noise + eps)
            - tf.math.log(1.0 - unif_noise + eps)
        )
        drop_prob = tf.math.sigmoid(drop_prob / temp)
        random_tensor = 1.0 - drop_prob

        retain_prob = 1.0 - p
        x *= random_tensor
        x /= retain_prob
        return x

    def call(self, inputs, training=None):
        p = tf.math.sigmoid(self.p_logit)

        # initialise regulariser / prior KL term
        input_dim = inputs.shape[-1]  # last dim
        weight = self.layer.kernel
        kernel_regularizer = self.weight_regularizer * tf.reduce_sum(tf.square(weight)) / (1.0 - p)
        dropout_regularizer = p * tf.math.log(p) + (1.0 - p) * tf.math.log(1.0 - p)
        dropout_regularizer *= self.dropout_regularizer * input_dim
        regularizer = tf.reduce_sum(kernel_regularizer + dropout_regularizer)
        if self.is_mc_dropout:
            return self.layer.call(self.concrete_dropout(inputs, p)), regularizer
        else:

            def relaxed_dropped_inputs():
                return self.layer.call(self.concrete_dropout(inputs, p)), regularizer

            return (
                tf.keras.backend.in_train_phase(relaxed_dropped_inputs, self.layer.call(inputs), training=training),
                regularizer,
            )


class NNConcreteDropoutModel(Base_Model):
    """

    Used to create a neural network model with self-learned dropout probability for the RegressionObjective

    See docstring for Base_Model __init__ function for information

    """

    def __init__(
        self,
        variables: VariablesList,
        objective: RegressionObjective,
        always_hyperparam_opt: bool = False,
        es_patience: int = 300,  # normally 300
    ):
        super().__init__(variables, objective, always_hyperparam_opt)
        self.default_X_transform_type = "standardisation"
        self.default_Y_transform_type = "standardisation"
        self.include_validation = True
        self.name = "nn_concrete"

        # Creates the callback method to stop fitting before the all epochs are completed based on the prediction
        # accuracy of the validation set
        self.earlystopping = callbacks.EarlyStopping(
            monitor="val_loss", min_delta=0.001, patience=es_patience, verbose=0, mode="min",
        )

        # The directory to save the model parameters when it detects a model with better prediction accuracy of the
        # validation set
        self.dirname_checkpoint = os.path.join(os.getcwd(), "ML Models", f"{self.name}", "Checkpoints")
        if not os.path.exists(self.dirname_checkpoint):
            os.makedirs(self.dirname_checkpoint)

    @staticmethod
    def mse_loss(true, pred):
        """

        Function to calculate the mean squared error (MSE) during training as a monitoring metric

        """
        n_outputs = pred.shape[1] // 2
        mean = pred[:, :n_outputs]
        return tf.reduce_mean((true - mean) ** 2, -1)

    @staticmethod
    def heteroscedastic_loss(true, pred):
        """

        Function to calculate the heteroscedastic uncertainty during training as the loss function

        """
        n_outputs = pred.shape[1] // 2
        mean = pred[:, :n_outputs]
        log_var = pred[:, n_outputs:]
        precision = tf.math.exp(-log_var)
        return tf.reduce_sum(precision * (true - mean) ** 2.0 + log_var, -1)

    def structure(
        self,
        learning_rate: float,
        hidden_units: int,
        hidden_layers: int,
        act_func: str,
        optimizer: Optimizer,
        wd: float = 0.0,
    ) -> Model:
        """

        Function that defines the structure of the input, hidden layers, and output for a neural network model with
        self-learned dropout probability

        Parameters
        ----------
        learning_rate: float
            Assigns the learning rate for the optimiser
        hidden_units: int
            The number of hidden units within every hidden layer. Currently, all hidden layers will have this number of hidden units
        hidden_layers: int
            The number of hidden layers in the neural network
        dropout_proba: float
            The dropout probability to be applied to the hidden layers
        act_func: str
            The activation function to apply on every hidden layer
        optimizer: Optimizer
            The type of optimiser to use to fit the model
        wd: float
            The weight regulariser to use in the model

        Returns
        -------
        model:
            The neural network model that can learn the dropout probability

        """
        K.clear_session()
        tf.random.set_seed(1)
        tf.random.uniform([1], seed=1)
        dropout_reg = 2 / self.X_train.shape[0]
        losses = []
        inputs = Input(shape=(self.X_train.shape[1],))
        x = inputs
        for i in range(hidden_layers):
            x, loss = ConcreteDropout(
                Dense(hidden_units, activation=act_func), weight_regularizer=wd, dropout_regularizer=dropout_reg,
            )(x)
            losses.append(loss)
        mean, loss = ConcreteDropout(
            Dense(self.Y_train.shape[1]), weight_regularizer=wd, dropout_regularizer=dropout_reg,
        )(x)
        losses.append(loss)
        log_var, loss = ConcreteDropout(
            Dense(self.Y_train.shape[1]), weight_regularizer=wd, dropout_regularizer=dropout_reg,
        )(x)
        losses.append(loss)
        out = concatenate([mean, log_var])
        model = Model(inputs, out)

        for loss in losses:
            model.add_loss(loss)

        model.summary()

        model.compile(
            optimizer=optimizer(learning_rate=learning_rate), loss=self.heteroscedastic_loss, metrics=[self.mse_loss],
        )
        assert len(model.layers[1].trainable_weights) == 3

        return model

    def fit(
        self, X: np.ndarray, Y: np.ndarray, test_ratio: float = 0.2, sort_before_split: bool = None, **params
    ) -> None:
        """

        Function that is called to start the concrete dropout neural network model fitting procedure

        Parameters
        ----------
        X: np.ndarray,
            X array that contains the unprocessed variables data to be fitted to the model, i.e. The data has not yet
            undergone any transformations related to converted categorical variables to their respective descriptors
            or transformations related to standardisation/normalisation
        Y: np.ndarray,
            Y array that contains the unprocessed objective data, i.e. The data has not yet undergone any
            transformations related to standardisation/normalisation
        test_ratio: float, Default = 0.2,
            The proportion of inputted X and Y arrays to be split for the validation set where applicable
        sort_before_split: bool, Default = True,
            Whether the inputted X and Y arrays should be sorted such that the Y-values are in ascending order before
            splitting into the training and test sets (and validation sets if applicable)
        params: Dict[str, Any]
            Dictionary that contains the hyperparameters for the model

        """
        if sort_before_split:
            (X_train, X_val, Y_train, Y_val,) = sort_train_test_split_shuffle(X, Y, test_ratio=test_ratio, seed=1)
        else:
            X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=test_ratio, random_state=1)

        Y_train = Y_train.astype("float")
        Y_val = Y_val.astype("float")

        self.X_train, self.X_val, self.Y_train, self.Y_val = (
            X_train,
            X_val,
            Y_train,
            Y_val,
        )
        if self.variables.num_cat_var > 0:
            self.X_train = self.variables.categorical_transform(self.X_train).astype("float")
            self.X_val = self.variables.categorical_transform(self.X_val).astype("float")

        self.X_train, self.Y_train = self.transform_by_predictor_type(self.X_train, Y=self.Y_train)
        self.X_val, self.Y_val = self.transform_only_by_predictor_type(self.X_val, self.Y_val)

        self.fit_model(params)

        self.Y_train_pred, self.Y_train_pred_stddev = self.predict(X_train)
        self.Y_val_pred, self.Y_val_pred_stddev = self.predict(X_val)
        self.performance_metrics = pm.all_performance_metrics_train_val(
            Y_train, self.Y_train_pred, Y_val, self.Y_val_pred
        )

        self.Y_train_error = 1.96 * self.Y_train_pred_stddev
        self.Y_val_error = 1.96 * self.Y_val_pred_stddev

    def fit_model(self, params: Dict[str, Any]) -> None:
        """

        Called by the fit and cv-related functions for fitting the neural network model with self-learned dropout
        probability using pre-processed X and Y training data in the class instance

        """
        hidden_units = int(params.get("hidden_units", self.X_train.shape[1] + 1))
        hidden_layers = int(params.get("hidden_layers", 2))
        batch_size = int(params.get("batch_size", 32))
        learning_rate = params.get("learning_rate", 0.001)
        max_epochs = int(params.get("max_epochs", 4000))
        act_func = params.get("act_func", "relu")
        optimizer = params.get("optimizer", keras.optimizers.Adam)

        self.filepath = os.path.join(
            self.dirname_checkpoint,
            f"Checkpoint, Concrete Dropout, {datetime.now().strftime('%d-%m-%Y, %H-%M-%S')}.h5",
        )

        self.model = self.structure(learning_rate, hidden_units, hidden_layers, act_func, optimizer,)
        self.savemodelcheckpoint = SaveModelCheckPoint(self.model, self.filepath)  # A Simon Original
        self.history = self.model.fit(
            self.X_train,
            self.Y_train,
            validation_data=(self.X_val, self.Y_val),
            epochs=max_epochs,
            verbose=2,
            batch_size=batch_size,
            callbacks=[
                callbacks.LambdaCallback(on_epoch_end=self.savemodelcheckpoint.save_weights),
                self.earlystopping,
            ],
        )

        self.model = self.structure(learning_rate, hidden_units, hidden_layers, act_func, optimizer,)
        self.model.load_weights(self.filepath)

    def predict(self, X: np.ndarray, X_transform: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        """

        Determines the model output and its standard deviation of the X array passed into the function

        Parameters
        ----------
        X: np.ndarray,
            X array that contains the unprocessed variables data to be used in the prediction, i.e. The data has not
            yet undergone any transformations related to converted categorical variables to their respective
            descriptors or transformations related to standardisation/normalisation
        X_transform: bool, Default = True
            For the default models provided natively in NEMO, the initial transformation of categorical variables and
            transformations related to standardisation/normalisation can be switched off by passing X_transform = False

        Returns
        ----------
        Y_pred: np.ndarray
            The predictive mean of the objective calculated using the model and the inputted X array. The outputted
            values have been un-transformed
        Y_pred_stddev: np.ndarray
            The predictive standard deviation of the objective calculated using the model and the inputted X array. The
            outputted values have been un-transformed

        """
        # X needs to be a 2D array
        if X.ndim == 1:
            X = X.reshape(1, -1)

        if X_transform:
            if self.variables.num_cat_var > 0:
                X = self.variables.categorical_transform(X).astype("float")
            X = self.transform_only_by_predictor_type(X)

        observed_Y_pred = np.array([self.model.predict(X) for _ in range(10)])
        Y_pred = observed_Y_pred[:, :, :1]
        Y_pred_stddev = np.sqrt(np.exp(observed_Y_pred[:, :, 1:]))

        # Code adapted from:
        #     1. João Caldeira, Brian Nord, Deeply Uncertain: Comparing Methods of Uncertainty Quantification in Deep Learning Algorithms, arXiv:2004.10710, https://github.com/deepskies/DeeplyUncertain-Public,
        #     2. Yarin Gal, Jiri Hron, Alex Kendall, Concrete Dropout, arXiv:1705.07832, https://github.com/yaringal/ConcreteDropout
        Y_val_epistemic_unc = np.std(np.array(Y_pred), axis=0)
        Y_val_aleatoric_unc = np.sqrt(np.mean(np.array(Y_pred_stddev) * np.array(Y_pred_stddev), axis=0))
        Y_val_total_unc = np.sqrt(Y_val_aleatoric_unc ** 2 + Y_val_epistemic_unc ** 2)

        Y_pred = np.mean(Y_pred, axis=0)
        Y_pred_upper = Y_pred + (1.96 * Y_val_total_unc)

        Y_pred = self.objective.inverse_transform(Y_pred)
        Y_pred_upper = self.objective.inverse_transform(Y_pred_upper)
        Y_pred_stddev = (np.subtract(Y_pred_upper, Y_pred)) / 1.96

        return Y_pred.flatten(), Y_pred_stddev.flatten()

    @staticmethod
    def default_params(X: np.ndarray):
        """

        Function that returns the default hyperparameters to use for the hyperparameter optimisation of a neural
        network model that can self-learn dropout probability using the hyperopt package. Returns a dictionary that is
        used for the space argument in the hyperopt.fmin function

        """
        return {
            "learning_rate": hp.uniform("learning_rate", 0.001, 0.01),
            "hidden_units": scope.int(hp.quniform("hidden_units", math.ceil(X.shape[1] / 2), (X.shape[1] + 1), 1)),
            "hidden_layers": scope.int(hp.quniform("hidden_layers", 1, 2, 1)),
            "batch_size": scope.int(hp.quniform("batch_size", math.ceil(X.shape[0] / 10), X.shape[0], 1)),
        }

    def hyperparam_opt(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        test_ratio: float,
        sort_before_split: bool = True,
        predictor_params_dict: Optional[Dict[str, Dict[str, Callable]]] = None,
        **kwargs,
    ) -> Tuple[NNConcreteDropoutModel, Dict[str, Any]]:
        """

        Function to be called for performing hyperparameter optimisation for neural network models with self-learned
        dropout probability using the hyperopt package. Returns the model fitted with the best hyperparameters and a
        dictionary containing the best hyperparameters

        Parameters
        ----------
        X: np.ndarray,
            X array that contains the unprocessed variables data to be fitted to the model, i.e. The data has not yet
            undergone any transformations related to converted categorical variables to their respective descriptors
            or transformations related to standardisation/normalisation
        Y: np.ndarray,
            Y array that contains the unprocessed objective data, i.e. The data has not yet undergone any
            transformations related to standardisation/normalisation
        test_ratio: float
            The proportion of inputted X and Y arrays to be split for the validation set where applicable
        sort_before_split: bool, Default = True,
            Whether the inputted X and Y arrays should be sorted such that the Y-values are in ascending order before
            splitting into the training and test sets (and validation sets if applicable)
        predictor_params_dict: Dict[str, Dict[str, Callable]], Default = None
            Dictionary with a key 'nn_concrete' and a corresponding value that is a dictionary that is used for the space
            argument in the hyperopt.fmin function

        Returns
        -------
        model: NNBayesianModel
            The model fitted with the best hyperparameters found using the hyperopt package

        model_params: Dict[str, Any]
            Dictionary containing the best hyperparameters found using the hyperopt package

        """
        if predictor_params_dict is None:
            predictor_params_dict = self.default_params(X)
        else:
            predictor_params_dict = predictor_params_dict.get(self.name, self.default_params(X))

        if self.objective.hyperopt_evals is None:
            hyperopt_evals = 1
        else:
            hyperopt_evals = self.objective.hyperopt_evals.get(self.name, 1)
        # if self.objective.hyperopt_evals is None:
        #     hyperopt_evals = 20
        # else:
        #     hyperopt_evals = self.objective.hyperopt_evals.get(f"{self.name}", 20)

        def func(X: np.ndarray, Y: np.ndarray, model_params: Dict[str, Any]) -> Dict[str, Any]:
            loss = self.non_cv_train_val_test(
                X, Y, model_params, test_ratio=test_ratio, sort_before_split=sort_before_split, **kwargs
            )

            return {
                "loss": loss,
                "status": STATUS_OK,
            }

        trials = Trials()
        model_params = fmin(
            fn=partial(func, X, Y),
            space=predictor_params_dict,
            algo=tpe.suggest,
            max_evals=hyperopt_evals,
            trials=trials,
        )

        model = self.new_instance(self.__class__, **kwargs)
        model.fit(X, Y, test_ratio=test_ratio, **model_params, **kwargs)

        logger.info(f"Completed hyperparameter opt")
        return model, model_params
