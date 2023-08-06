# Tony Duan, Anand Avati, Daisy Yi Ding, Khanh K. Thai, Sanjay Basu, Andrew Y. Ng, Alejandro Schuler. 2019. NGBoost: Natural Gradient Boosting for Probabilistic Prediction.
# https://arxiv.org/abs/1910.03225
# https://github.com/stanfordmlgroup/ngboost

from __future__ import annotations

import os
from functools import partial
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, Tuple

import numpy as np
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe
from hyperopt.pyll.base import scope
from ngboost import NGBRegressor
from ngboost.distns import Normal
from ngboost.scores import LogScore
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

import nemo_bo.utils.logger as logging_nemo
import nemo_bo.utils.perf_metrics as pm
from nemo_bo.models.base.base_model import Base_Model
from nemo_bo.utils.data_proc import sort_train_test_split_shuffle

if TYPE_CHECKING:
    from nemo_bo.opt.objectives import RegressionObjective
    from nemo_bo.opt.variables import VariablesList

try:
    logging_nemo.logging_path
    logger = logging_nemo.logging_nemo_child(os.path.basename(__file__))
except AttributeError:
    logger = logging_nemo.logging_nemo_master(os.path.basename(__file__))


class NGBoostModel(Base_Model):
    """

    Used to create a NGBoost model for the RegressionObjective

    See docstring for Base_Model __init__ function for information

    """

    def __init__(
        self, variables: VariablesList, objective: RegressionObjective, always_hyperparam_opt: bool = True, **kwargs
    ):
        super().__init__(variables, objective, always_hyperparam_opt)
        self.default_X_transform_type = "none"
        self.default_Y_transform_type = "none"
        self.include_validation = True
        self.name = "ngb"

    def fit(
        self, X: np.ndarray, Y: np.ndarray, test_ratio: float = 0.2, sort_before_split: bool = True, **params
    ) -> None:
        """

        Function that is called to start the NGBoost model fitting procedure

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

        Called by the fit and cv-related functions for fitting the NGBoost model using pre-processed X and Y training
        data in the class instance

        """
        decision_tree_params = {
            "criterion": params.get("criterion", "friedman_mse"),
            "splitter": params.get("splitter", "best"),
            "max_depth": int(params.get("max_depth")),
            "min_samples_split": params.get("min_samples_split", 2),
            "min_samples_leaf": params.get("min_samples_leaf", 1),
            "min_weight_fraction_leaf": params.get("min_weight_fraction_leaf", 0.0),
            "max_features": params.get("max_features"),
            "max_leaf_nodes": params.get("max_leaf_nodes"),
            "min_impurity_decrease": params.get("min_impurity_decrease", 0.0),
            "ccp_alpha": params.get("ccp_alpha", 0.0),
        }
        if decision_tree_params["max_leaf_nodes"] is not None:
            decision_tree_params["max_leaf_nodes"] = int(decision_tree_params["max_leaf_nodes"])

        regressor_params = {
            "Dist": params.get("Dist", Normal),
            "Score": params.get("Score", LogScore),
            "Base": params.get("base", DecisionTreeRegressor(**decision_tree_params)),
            "natural_gradient": params.get("natural_gradient", True),
            "n_estimators": int(params.get("n_estimators", 2000)),
            "learning_rate": params.get("learning_rate", 0.01),
            "minibatch_frac": params.get("minibatch_frac", 1.0),
            "col_sample": params.get("col_sample", 1.0),
            "tol": params.get("tol", 1e-4),
        }

        self.model = NGBRegressor(verbose=True, verbose_eval=20, random_state=1, **regressor_params)

        # Re-attempts fitting
        for x in range(10):
            try:
                self.model.fit(
                    self.X_train,
                    self.Y_train.flatten(),
                    X_val=self.X_val,
                    Y_val=self.Y_val.flatten(),
                    early_stopping_rounds=10,
                )
                break
            except np.linalg.LinAlgError as e:
                print(e)
            except TypeError as e:
                print(e)

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
        Y_mean: np.ndarray
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

        Y_pred = self.model.pred_dist(X.astype(float))
        Y_mean = Y_pred.loc
        Y_pred_upper = Y_mean + (1.96 * Y_pred.scale)

        Y_pred = self.objective.inverse_transform(Y_mean)
        Y_pred_upper = self.objective.inverse_transform(Y_pred_upper)
        Y_pred_stddev = (np.subtract(Y_pred_upper, Y_pred)) / 1.96

        return Y_mean.flatten(), Y_pred_stddev.flatten()

    @staticmethod
    def default_params():
        """

        Function that returns the default hyperparameters to use for the hyperparameter optimisation of NGBoost models
        using the hyperopt package. Returns a dictionary that is used for the space argument in the hyperopt.fmin
        function

        """
        return {
            "learning_rate": hp.uniform("learning_rate", 0.005, 0.02),
            "max_depth": scope.int(hp.quniform("max_depth", 3, 10, 1)),
            "min_samples_split": hp.uniform("min_samples_split", 0.01, 0.75),
            "col_sample": hp.uniform("col_sample", 0.5, 1.0),
        }

    def hyperparam_opt(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        test_ratio: float,
        sort_before_split: bool = True,
        predictor_params_dict: Optional[Dict[str, Dict[str, Callable]]] = None,
        **kwargs,
    ) -> Tuple[NGBoostModel, Dict[str, Any]]:
        """

        Function to be called for performing hyperparameter optimisation for NGBoost models using the hyperopt package.
        Returns the model fitted with the best hyperparameters and a dictionary containing the best hyperparameters

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
            Dictionary with a key 'ngb' and a corresponding value that is a dictionary that is used for the space
            argument in the hyperopt.fmin function

        Returns
        -------
        model: NGBoostModel
            The model fitted with the best hyperparameters found using the hyperopt package

        model_params: Dict[str, Any]
            Dictionary containing the best hyperparameters found using the hyperopt package

        """
        if predictor_params_dict is None:
            predictor_params_dict = self.default_params()
        else:
            predictor_params_dict = predictor_params_dict.get(self.name, self.default_params())

        if self.objective.hyperopt_evals is None:
            hyperopt_evals = 1
        else:
            hyperopt_evals = self.objective.hyperopt_evals.get(self.name, 1)
        # if self.objective.hyperopt_evals is None:
        #     hyperopt_evals = 30
        # else:
        #     hyperopt_evals = self.objective.hyperopt_evals.get(f"{self.name}", 30)

        def func(X: np.ndarray, Y: np.ndarray, model_params: Dict[str, Any]) -> Dict[str, Any]:
            cv_results = self.cv(
                X, Y, model_params, test_ratio=test_ratio, sort_before_split=sort_before_split, **kwargs
            )

            return {
                "loss": cv_results["Mean Test RMSE"],
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
