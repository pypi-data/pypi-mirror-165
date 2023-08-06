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
from keras.layers import Dense, Dropout, Input
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


class NNEnsembleModel(Base_Model):
    """

    Used to create an ensemble of neural network models for the RegressionObjective

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
        self.name = "nn_ensemble"

        # Creates the callback method to stop fitting before the all epochs are completed based on the prediction
        # accuracy of the validation set
        self.earlystopping = callbacks.EarlyStopping(
            monitor="val_loss", min_delta=0.001, patience=es_patience, verbose=0, mode="min",
        )

        # The directory to save the model parameters when it detects a model with better prediction accuracy of the
        # validation set
        self.dirname_checkpoint = os.path.join(os.getcwd(), "ML Models", "nn_ensemble", "Checkpoints")
        if not os.path.exists(self.dirname_checkpoint):
            os.makedirs(self.dirname_checkpoint)

    @staticmethod
    def negloglik(y_data, rv_y):
        """

        Function to calculate the value of the negative loglikelihood function

        """
        return -rv_y.log_prob(y_data)

    # function for creating a fully connected neural network of any architecture
    # the number of neurons in each layer is defined by layers_shape
    # the droupout_proba indicates if dropout layers should be added
    def structure(
        self,
        learning_rate: float,
        hidden_units: int,
        hidden_layers: int,
        dropout_proba: float,
        act_func: str,
        optimizer: Optimizer,
    ) -> Model:
        """

        Function that defines the structure of the input, hidden layers, and output for the neural network models in
        the ensemble

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

        Returns
        -------
        model:
            The neural network model with specified hidden layers

        """
        K.clear_session()
        tf.random.set_seed(1)
        tf.random.uniform([1], seed=1)
        input_data = Input((self.X_train.shape[1],))
        x = input_data
        for _ in range(hidden_layers):
            x = Dense(hidden_units, activation=act_func)(x)
            if dropout_proba > 0:
                x = Dropout(dropout_proba)(x)

        x = Dense(2)(x)
        x = tfpl.DistributionLambda(lambda t: tfd.Normal(loc=t[..., :1], scale=1e-3 + tf.math.softplus(t[..., 1:])))(x)
        model = Model(input_data, x)
        model.summary()

        model.compile(
            optimizer=optimizer(learning_rate=learning_rate), loss=self.negloglik, metrics=["mse"],
        )

        return model

    def fit(
        self, X: np.ndarray, Y: np.ndarray, test_ratio: float = 0.2, sort_before_split: bool = None, **params
    ) -> None:
        """

        Function that is called to start the probabilistic neural network model fitting procedure

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

        Called by the fit and cv-related functions for fitting the neural network models in the ensemble using
        pre-processed X and Y training data in the class instance

        """
        hidden_units = int(params.get("hidden_units", self.X_train.shape[1] + 1))
        hidden_layers = int(params.get("hidden_layers", 2))
        batch_size = int(params.get("batch_size", 32))
        learning_rate = params.get("learning_rate", 0.001)
        dropout_proba = params.get("dropout_proba", 0.001)
        ensemble_size = int(params.get("ensemble_size", 5))
        max_epochs = int(params.get("max_epochs", 4000))
        act_func = params.get("act_func", "relu")
        optimizer = params.get("optimizer", keras.optimizers.Adam)

        self.filepath = os.path.join(
            self.dirname_checkpoint, f"Checkpoint, Ensemble, {datetime.now().strftime('%d-%m-%Y, %H-%M-%S')}.h5",
        )

        self.ensemble_model_list = []
        for _ in range(ensemble_size):
            self.model = self.structure(learning_rate, hidden_units, hidden_layers, dropout_proba, act_func, optimizer,)
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

            self.model = self.structure(learning_rate, hidden_units, hidden_layers, dropout_proba, act_func, optimizer,)
            self.model.load_weights(self.filepath)
            self.ensemble_model_list.append(self.model)

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

        observed_Y_pred = [ensemble_model(X) for ensemble_model in self.ensemble_model_list]
        Y_pred = np.array([prediction.loc.numpy() for prediction in observed_Y_pred])
        Y_pred_stddev = np.array([prediction.scale.numpy() for prediction in observed_Y_pred])

        # Code adapted from:
        #     1. João Caldeira, Brian Nord, Deeply Uncertain: Comparing Methods of Uncertainty Quantification in Deep Learning Algorithms, arXiv:2004.10710, https://github.com/deepskies/DeeplyUncertain-Public,
        #     2. Yarin Gal, Jiri Hron, Alex Kendall, Concrete Dropout, arXiv:1705.07832, https://github.com/yaringal/ConcreteDropout
        Y_val_epistemic_unc = np.std(np.array(Y_pred), axis=0)  # Equation 4 from paper
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

        Function that returns the default hyperparameters to use for the hyperparameter optimisation of ensemble
        neural network models using the hyperopt package. Returns a dictionary that is used for the space argument in
        the hyperopt.fmin function

        """
        return {
            "learning_rate": hp.uniform("learning_rate", 0.001, 0.01),
            "hidden_units": scope.int(hp.quniform("hidden_units", math.ceil(X.shape[1] / 2), (X.shape[1] + 1), 1)),
            "hidden_layers": scope.int(hp.quniform("hidden_layers", 1, 2, 1)),
            "batch_size": scope.int(hp.quniform("batch_size", math.ceil(X.shape[0] / 10), X.shape[0], 1)),
            "dropout_proba": hp.uniform("dropout_proba", 0.001, 0.05),
        }

    def hyperparam_opt(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        test_ratio: float,
        sort_before_split: bool = True,
        predictor_params_dict: Optional[Dict[str, Dict[str, Callable]]] = None,
        **kwargs,
    ) -> Tuple[NNEnsembleModel, Dict[str, Any]]:
        """

        Function to be called for performing hyperparameter optimisation for ensemble neural network models using
        the hyperopt package. Returns the model fitted with the best hyperparameters and a dictionary containing the
        best hyperparameters

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
            Dictionary with a key 'nn_ensemble' and a corresponding value that is a dictionary that is used for the space
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
        #     hyperopt_evals = 15
        # else:
        #     hyperopt_evals = self.objective.hyperopt_evals.get(f"{self.name}", 15)

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
