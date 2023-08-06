# Based on forest-confidence-interval: Confidence intervals for Forest algorithms, Kivan Polimis, Ariel Rokem, Bryna Hazelton, The University of Washington, https://github.com/scikit-learn-contrib/forest-confidence-interval

from __future__ import annotations

import os
from functools import partial
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, Tuple

import forestci as fci
import numpy as np
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe
from hyperopt.pyll.base import scope
from sklearn.ensemble import RandomForestRegressor

import nemo_bo.utils.logger as logging_nemo
import nemo_bo.utils.perf_metrics as pm
from nemo_bo.models.base.base_model import Base_Model

if TYPE_CHECKING:
    from nemo_bo.opt.objectives import RegressionObjective
    from nemo_bo.opt.variables import VariablesList

try:
    logging_nemo.logging_path
    logger = logging_nemo.logging_nemo_child(os.path.basename(__file__))
except AttributeError:
    logger = logging_nemo.logging_nemo_master(os.path.basename(__file__))


class RFModel(Base_Model):
    """

    Used to create a Random Forest model for the RegressionObjective

    See docstring for Base_Model __init__ function for information

    """

    def __init__(
        self, variables: VariablesList, objective: RegressionObjective, always_hyperparam_opt: bool = True, **kwargs
    ):
        super().__init__(variables, objective, always_hyperparam_opt)
        self.default_X_transform_type = "none"
        self.default_Y_transform_type = "none"
        self.include_validation = False
        self.name = "rf"

    def fit(self, X: np.ndarray, Y: np.ndarray, **params) -> None:
        """

        Function that is called to start the Random Forest model fitting procedure

        Parameters
        ----------
        X: np.ndarray,
            X array that contains the unprocessed variables data to be fitted to the model, i.e. The data has not yet
            undergone any transformations related to converted categorical variables to their respective descriptors
            or transformations related to standardisation/normalisation
        Y: np.ndarray,
            Y array that contains the unprocessed objective data, i.e. The data has not yet undergone any
            transformations related to standardisation/normalisation
        params: Dict[str, Any]
            Dictionary that contains the hyperparameters for the model

        """
        if self.variables.num_cat_var > 0:
            self.X_train = self.variables.categorical_transform(X).astype("float")
        else:
            self.X_train = X

        self.X_train, self.Y_train = self.transform_by_predictor_type(self.X_train, Y=Y)

        self.fit_model(params)

        self.Y_pred, self.Y_pred_stddev = self.predict(X)
        self.performance_metrics = pm.all_performance_metrics(Y, self.Y_pred)

        self.Y_pred_error = 1.96 * self.Y_pred_stddev

    def fit_model(self, params: Dict[str, Any]) -> None:
        """

        Called by the fit and cv-related functions for fitting the Random Forest model using pre-processed X and Y
        training data in the class instance

        """
        for key in params:
            if key == "max_depth":
                params["max_depth"] = int(params["max_depth"])
            if key == "n_estimators":
                params["n_estimators"] = int(params["n_estimators"])

        # Create RandomForestRegressor
        self.model = RandomForestRegressor(random_state=1, **params)
        self.model.fit(self.X_train, self.Y_train.flatten())

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

        Y_mean = self.model.predict(X.astype(float))

        Y_var = np.absolute(
            fci.random_forest_error(self.model, self.X_train, X, calibrate=False if X.shape[0] <= 20 else True)
        )
        Y_pred_upper = Y_mean + (1.96 * np.sqrt(Y_var))

        Y_pred = self.objective.inverse_transform(Y_mean)
        Y_pred_upper = self.objective.inverse_transform(Y_pred_upper)
        Y_pred_stddev = (np.subtract(Y_pred_upper, Y_pred)) / 1.96

        return Y_pred.flatten(), Y_pred_stddev.flatten()

    @staticmethod
    def default_params():
        """

        Function that returns the default hyperparameters to use for the hyperparameter optimisation of Random Forest
        models using the hyperopt package. Returns a dictionary that is used for the space argument in the hyperopt.fmin
        function

        """
        return {
            "max_depth": scope.int(hp.quniform("max_depth", 5, 100, 1)),
            "min_samples_leaf": hp.uniform("min_samples_leaf", 0.01, 0.5),
            "min_samples_split": hp.uniform("min_samples_split", 0.01, 0.75),
            "n_estimators": scope.int(hp.quniform("n_estimators", 40, 2000, 20)),
        }

    def hyperparam_opt(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        test_ratio: float,
        predictor_params_dict: Optional[Dict[str, Dict[str, Callable]]] = None,
        **kwargs,
    ) -> Tuple[RFModel, Dict[str, Any]]:
        """

        Function to be called for performing hyperparameter optimisation for Random Forest models using the hyperopt
        package. Returns the model fitted with the best hyperparameters and a dictionary containing the best
        hyperparameters

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
        predictor_params_dict: Dict[str, Dict[str, Callable]], Default = None
            Dictionary with a key 'rf' and a corresponding value that is a dictionary that is used for the space
            argument in the hyperopt.fmin function

        Returns
        -------
        model: RFModel
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
            cv_results = self.cv(X, Y, model_params, test_ratio=test_ratio, **kwargs)

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
