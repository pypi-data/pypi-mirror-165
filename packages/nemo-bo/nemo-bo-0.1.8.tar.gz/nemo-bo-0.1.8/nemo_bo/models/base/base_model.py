from __future__ import annotations

import copy
import os
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold, train_test_split

import nemo_bo.utils.logger as logging_nemo
import nemo_bo.utils.perf_metrics as pm
import nemo_bo.utils.plotter as plotter
from nemo_bo.utils.data_proc import *

if TYPE_CHECKING:
    from nemo_bo.opt.objectives import RegressionObjective
    from nemo_bo.opt.variables import VariablesList

try:
    logging_nemo.logging_path
    logger = logging_nemo.logging_nemo_child(os.path.basename(__file__))
except AttributeError:
    logger = logging_nemo.logging_nemo_master(os.path.basename(__file__))


class Base_Model:
    """

    Base class for ML models in NEMO

    Parameters
    ----------
    variables: VariablesList
        VariablesList object that contains information about all variables
    objective: RegressionObjective
        RegressionObjective object that contains information about the objective to be modelled
    always_hyperparam_opt: bool, Default = True
        Whether optimisation of the model hyperparameters should be performed every iteration of the optimisation
        procedure. An example of when 'False' is suitable could be if hyperparameter optimisation takes such a
        long amount of time that it is not practical to do it every iteration

    """

    def __init__(
        self, variables: VariablesList, objective: RegressionObjective, always_hyperparam_opt: bool = True, **kwargs
    ):
        self.variables = variables
        self.objective = objective
        self.always_hyperparam_opt = always_hyperparam_opt

        # Creates copies of the variables and objective before they are altered by any fitting process
        self.input_variables = copy.copy(variables)
        self.input_objective = copy.copy(objective)

        # Four variables that need to be pre-defined by the author in the child classes that inherit Base_Model:
        # The name given to the type of model
        self.name = None

        # Boolean for whether a validation set is used for the model fitting process
        self.include_validation = None

        # The default X and Y transform types to use during the fit and predict processes when the
        # transformation_type attributes in any self.variables.variables and/or self.objective are None
        self.default_X_transform_type = None
        self.default_Y_transform_type = None

    def new_instance(self, cls: Base_Model, **kwargs):
        """

        Returns a new instance of the model class that is passed into the function

        """
        return cls(
            copy.copy(self.input_variables), copy.copy(self.input_objective), self.always_hyperparam_opt, **kwargs
        )

    def fit(
        self, X: np.ndarray, Y: np.ndarray, test_ratio: float = 0.2, sort_before_split: bool = True, **params,
    ) -> None:
        """

        Function that is called to start the fitting procedure. For example, the typical order steps here could include
        firstly data transformations and splitting, followed by fitting the model using the self.fit_model function,
        and then testing the model quality

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
        pass

    def fit_model(self, *args, **kwargs) -> None:
        """

        Called by the fit and cv-related functions for fitting the model. Ideally, nothing other than fitting should
        occur here

        """
        pass

    def predict(self, X: np.ndarray, X_transform: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        """

        Determines the model output and its standard deviation of the X array passed into the function. For example,
        the typical order steps here could include firstly data transformations, followed by passing the transformed
        X array, and then un-transforming the predicted outputs

        Parameters
        ----------
        X: np.ndarray,
            X array that contains the unprocessed variables data to be used in the prediction, i.e. The data has not
            yet undergone any transformations related to converted categorical variables to their respective
            descriptors or transformations related to standardisation/normalisation
        X_transform: bool, Default = True
            For the default models provided natively in NEMO, the initial transformation of categorical variables and
            transformations related to standardisation/normalisation can be switched off by passing X_transform = False

        """
        pass

    def cv(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        model_params: Dict[str, Any],
        test_ratio: float = 0.2,
        sort_before_split: bool = True,
        **kwargs,
    ) -> Dict[str, Any]:
        """

        Function that is called to start the cross validation procedure for a provided set of model hyperparameters and
        returns a dictionary containing the fitting results with emphasis on the test results. The number of k-folds is
        determined by the reciprocal of the test_ratio

        Parameters
        ----------
        X: np.ndarray,
            X array that contains the unprocessed variables data to be fitted to the model, i.e. The data has not yet
            undergone any transformations related to converted categorical variables to their respective descriptors
            or transformations related to standardisation/normalisation
        Y: np.ndarray,
            Y array that contains the unprocessed objective data, i.e. The data has not yet undergone any
            transformations related to standardisation/normalisation
        model_params: Dict[str, Any]
            Dictionary that contains the hyperparameters for the model
        test_ratio: float, Default = 0.2,
            The proportion of inputted X and Y arrays to be split into the validation and test sets where applicable
        sort_before_split: bool, Default = True,
            Whether the inputted X and Y arrays should be sorted such that the Y-values are in ascending order before
            splitting into the training and test sets (and validation sets if applicable)

        Returns
        -------
        Dict[str, Any]
        Dictionary containing the models, their respective prediction quality for all k-folds and average cv statistics
        across all k-folds

        """
        if self.include_validation:
            return self.cv_train_val_test(
                X, Y, model_params, test_ratio=test_ratio, sort_before_split=sort_before_split, **kwargs
            )
        else:
            return self.cv_train_test(X, Y, model_params, test_ratio=test_ratio, **kwargs)

    def hyperparam_opt(self, *args, **kwargs) -> Tuple[Base_Model, Dict[str, Any]]:
        """

        Function to be called for performing hyperparameter optimisation for a given model using the hyperopt package.
        Returns the model fitted with the best hyperparameters and a dictionary containing the best hyperparameters

        """
        pass

    def default_params(self, *args, **kwargs) -> Dict[str, Any]:
        """

        Function that returns the default hyperparameters to use for the hyperparameter optimisation using the
        hyperopt package. Returns a dictionary that is used for the space argument in the hyperopt.fmin function

        """
        pass

    def cv_train_test(
        self, X: np.ndarray, Y: np.ndarray, model_params: Dict[str, Any], test_ratio: float = 0.2, **kwargs
    ) -> Dict[str, Any]:
        """

        This function is called from the self.cv function. Cross validation process that involves splitting the X and
        Y array into training and test sets (no validation set)

        Parameters
        ----------
        X: np.ndarray,
            X array that contains the unprocessed variables data to be fitted to the model, i.e. The data has not yet
            undergone any transformations related to converted categorical variables to their respective descriptors
            or transformations related to standardisation/normalisation
        Y: np.ndarray,
            Y array that contains the unprocessed objective data, i.e. The data has not yet undergone any
            transformations related to standardisation/normalisation
        model_params: Dict[str, Any]
            Dictionary that contains the hyperparameters for the model
        test_ratio: float, Default = 0.2,
            The proportion of inputted X and Y arrays to be split into the validation and test sets where applicable

        Returns
        -------
        Dict[str, Any]
        Dictionary containing the models, their respective prediction quality for all k-folds and average cv statistics
        across all k-folds

        """
        self.model_params = model_params

        cv_results = {}
        test_rmse_list = []
        test_r2_list = []
        fold_number = 0

        kf = KFold(n_splits=int(1 / test_ratio), shuffle=True, random_state=1)

        # Split the data
        X_temp = copy.copy(X)
        Y_temp = copy.copy(Y)

        # remainder = X.shape[0] % int(1 / test_ratio)
        # if remainder > 0:
        #     X_temp = X_temp[: (-1 * remainder)]
        #     Y_temp = Y_temp[: (-1 * remainder)]

        for train_index, test_index in kf.split(X_temp):
            fold_number += 1
            X_train, X_test = X_temp[train_index], X_temp[test_index]
            Y_train, Y_test = (
                Y_temp[train_index].astype("float"),
                Y_temp[test_index].astype("float"),
            )

            # Create copy for the model
            model = self.new_instance(self.__class__, **kwargs)

            # Transform the data
            model.X_train, model.Y_train, model.X_test, model.Y_test = (
                X_train,
                Y_train,
                X_test,
                Y_test,
            )
            if model.variables.num_cat_var > 0:
                model.X_train = model.variables.categorical_transform(model.X_train).astype("float")
                model.X_test = model.variables.categorical_transform(model.X_test).astype("float")

            model.X_train, model.Y_train = model.transform_by_predictor_type(model.X_train, Y=model.Y_train)
            model.X_test, model.Y_test = model.transform_only_by_predictor_type(model.X_test, Y=model.Y_test)

            model.fit_model(self.model_params)

            # Make predictions and calculate model performance
            model.Y_train_pred, model.Y_train_pred_stddev = model.predict(X_train)
            model.Y_test_pred, model.Y_test_pred_stddev = model.predict(X_test)
            model.performance_metrics = pm.all_performance_metrics_train_val(
                Y_train, model.Y_train_pred, Y_test, model.Y_test_pred
            )

            cv_results[f"Fold {fold_number}"] = {
                "Performance Metrics": model.performance_metrics,
                "Model": model.model,
            }
            test_rmse_list.append(model.performance_metrics["Validation RMSE"])
            test_r2_list.append(model.performance_metrics["Validation r2"])

        cv_results["Mean Test RMSE"] = np.mean(test_rmse_list)
        cv_results["Mean Test r2"] = np.mean(test_r2_list)

        logger.info(
            f"Completed {self.name} CV (k = {int(1/test_ratio)}) model checking | Mean Test Loss: {cv_results['Mean Test RMSE']}"
        )

        return cv_results

    def cv_train_val_test(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        model_params: Dict[str, Any],
        test_ratio: float = 0.2,
        sort_before_split: bool = True,
        **kwargs,
    ) -> Dict[str, Any]:
        """

        This function is called from the self.cv function. Cross validation process that involves splitting the X and
        Y array into training, validation, and test sets

        Parameters
        ----------
        X: np.ndarray,
            X array that contains the unprocessed variables data to be fitted to the model, i.e. The data has not yet
            undergone any transformations related to converted categorical variables to their respective descriptors
            or transformations related to standardisation/normalisation
        Y: np.ndarray,
            Y array that contains the unprocessed objective data, i.e. The data has not yet undergone any
            transformations related to standardisation/normalisation
        model_params: Dict[str, Any]
            Dictionary that contains the hyperparameters for the model
        test_ratio: float, Default = 0.2,
            The proportion of inputted X and Y arrays to be split into the validation and test sets where applicable
        sort_before_split: bool, Default = True,
            Whether the inputted X and Y arrays should be sorted such that the Y-values are in ascending order before
            splitting into the training, validation, and test sets

        Returns
        -------
        Dict[str, Any]
        Dictionary containing the models, their respective prediction quality for all k-folds and average cv statistics
        across all k-folds

        """
        self.model_params = model_params

        cv_results = {}
        test_rmse_list = []
        test_r2_list = []
        test_pred_list = []
        test_error_list = []
        fold_number = 0

        kf = KFold(n_splits=int(1 / test_ratio), shuffle=True, random_state=1)

        if sort_before_split:
            (X_train_val, X_test, Y_train_val, Y_test,) = sort_train_test_split_shuffle(
                X, Y, test_ratio=test_ratio, seed=1
            )
        else:
            X_train_val, X_test, Y_train_val, Y_test = train_test_split(X, Y, test_size=test_ratio, random_state=1)
        Y_test = Y_test.astype("float")

        for train_index, test_index in kf.split(X_train_val):
            fold_number += 1
            X_train, X_val = X_train_val[train_index], X_train_val[test_index]
            Y_train, Y_val = (
                Y_train_val[train_index].astype("float"),
                Y_train_val[test_index].astype("float"),
            )

            # Create copy for the model
            model = self.new_instance(self.__class__, **kwargs)

            # Transform the data
            (model.X_train, model.Y_train, model.X_val, model.Y_val, model.X_test, model.Y_test,) = (
                X_train,
                Y_train,
                X_val,
                Y_val,
                X_test,
                Y_test,
            )
            if model.variables.num_cat_var > 0:
                model.X_train = model.variables.categorical_transform(model.X_train).astype("float")
                model.X_val = model.variables.categorical_transform(model.X_val).astype("float")
                model.X_test = model.variables.categorical_transform(model.X_test).astype("float")
            else:
                model.X_train = X_train
                model.X_val = X_val
                model.X_test = X_test

            model.X_train, model.Y_train = model.transform_by_predictor_type(model.X_train, model.Y_train)
            model.X_val, model.Y_val = model.transform_only_by_predictor_type(model.X_val, model.Y_val)
            (model.X_test, model.Y_test,) = model.transform_only_by_predictor_type(model.X_test, model.Y_test)

            model.fit_model(self.model_params)

            # Make predictions and calculate model performance
            model.Y_train_pred, model.Y_train_pred_stddev = model.predict(X_train)
            model.Y_val_pred, model.Y_val_pred_stddev = model.predict(X_val)
            model.Y_test_pred, model.Y_test_pred_stddev = model.predict(X_test)
            model.performance_metrics = pm.all_performance_metrics_train_val_test(
                Y_train, model.Y_train_pred, Y_val, model.Y_val_pred, Y_test, model.Y_test_pred,
            )
            model.Y_test_error = 1.96 * model.Y_test_pred_stddev

            cv_results[f"Fold {fold_number}"] = {
                "Performance Metrics": model.performance_metrics,
                "Model": model.model,
            }
            test_rmse_list.append(model.performance_metrics["Test RMSE"])
            test_r2_list.append(model.performance_metrics["Test r2"])
            test_pred_list.append(model.Y_test_pred.flatten())
            test_error_list.append(model.Y_test_error.flatten())

        cv_results["Mean Test RMSE"] = np.mean(test_rmse_list)
        cv_results["Mean Test r2"] = np.mean(test_r2_list)
        cv_results["Mean Y Test Parity Data"] = pm.paritydata(Y_test, np.mean(test_pred_list, axis=0))
        cv_results["Mean Y Test Error (CI 95%)"] = np.mean(test_error_list, axis=0)

        logger.info(
            f"Completed {self.name} CV (k = {int(1/test_ratio)}) model checking | Mean Test Loss: {cv_results['Mean Test RMSE']}"
        )

        return cv_results

    def non_cv_train_test(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        model_params: Dict[str, Any],
        test_ratio: float = 0.2,
        sort_before_split: bool = True,
        **kwargs,
    ) -> float:
        """

        This function can be called from the self.hyperparam_opt function to assess the quality of the model fitting
        against a test set, i.e. as an alternative to using cross validation for assessing model fittings. For example,
        this could be used as a compromise if the time taken for cross validation is prohibitively long. No validation
        set is used here for the model training

        Parameters
        ----------
        X: np.ndarray,
            X array that contains the unprocessed variables data to be fitted to the model, i.e. The data has not yet
            undergone any transformations related to converted categorical variables to their respective descriptors
            or transformations related to standardisation/normalisation
        Y: np.ndarray,
            Y array that contains the unprocessed objective data, i.e. The data has not yet undergone any
            transformations related to standardisation/normalisation
        model_params: Dict[str, Any]
            Dictionary that contains the hyperparameters for the model
        test_ratio: float, Default = 0.2,
            The proportion of inputted X and Y arrays to be split into the validation and test sets where applicable
        sort_before_split: bool, Default = True,
            Whether the inputted X and Y arrays should be sorted such that the Y-values are in ascending order before
            splitting into the training, validation, and test sets

        Returns
        -------
        float
        The RMSE of the test set prediction

        """
        self.model_params = model_params

        # Split the dataset
        if sort_before_split:
            (X_train, X_test, Y_train, Y_test,) = sort_train_test_split_shuffle(X, Y, test_ratio=test_ratio, seed=1)
        else:
            X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_ratio, random_state=1)

        # Create copy for the model
        model = self.new_instance(self.__class__, **kwargs)

        # Transform the data
        model.X_train, model.Y_train, model.X_test, model.Y_test = (
            X_train,
            Y_train,
            X_test,
            Y_test,
        )
        if model.variables.num_cat_var > 0:
            model.X_train = model.variables.categorical_transform(model.X_train).astype("float")
            model.X_test = model.variables.categorical_transform(model.X_test).astype("float")

        model.X_train, model.Y_train = model.transform_by_predictor_type(model.X_train, Y=model.Y_train)
        model.X_test, model.Y_test = model.transform_only_by_predictor_type(model.X_test, Y=model.Y_test)

        model.fit_model(self.model_params)

        # Make predictions and calculate model performance
        model.Y_train_pred, model.Y_train_pred_stddev = model.predict(X_train)
        model.Y_test_pred, model.Y_test_pred_stddev = model.predict(X_test)
        model.performance_metrics = pm.all_performance_metrics_train_val(
            Y_train, model.Y_train_pred, Y_test, model.Y_test_pred
        )

        return model.performance_metrics["Test RMSE"]

    def non_cv_train_val_test(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        model_params: Dict[str, Any],
        test_ratio: float = 0.2,
        sort_before_split: bool = True,
        **kwargs,
    ) -> float:
        """

        This function can be called from the self.hyperparam_opt function to assess the quality of the model fitting
        against a test set, i.e. as an alternative to using cross validation for assessing model fittings. For example,
        this could be used as a compromise if the time taken for cross validation is prohibitively long.  A validation
        set is used here to support the model training

        Parameters
        ----------
        X: np.ndarray,
            X array that contains the unprocessed variables data to be fitted to the model, i.e. The data has not yet
            undergone any transformations related to converted categorical variables to their respective descriptors
            or transformations related to standardisation/normalisation
        Y: np.ndarray,
            Y array that contains the unprocessed objective data, i.e. The data has not yet undergone any
            transformations related to standardisation/normalisation
        model_params: Dict[str, Any]
            Dictionary that contains the hyperparameters for the model
        test_ratio: float, Default = 0.2,
            The proportion of inputted X and Y arrays to be split into the validation and test sets where applicable
        sort_before_split: bool, Default = True,
            Whether the inputted X and Y arrays should be sorted such that the Y-values are in ascending order before
            splitting into the training, validation, and test sets

        Returns
        -------
        float
        The RMSE of the test set prediction

        """
        self.model_params = model_params

        # Split the dataset
        if sort_before_split:
            (X_train, X_val, X_test, Y_train, Y_val, Y_test,) = sort_train_val_test_split_shuffle(
                X, Y, test_ratio=test_ratio, seed=1
            )
        else:
            X_train_val, X_test, Y_train_val, Y_test = train_test_split(X, Y, test_size=test_ratio, random_state=1)
            X_train, X_val, Y_train, Y_val = train_test_split(
                X_train_val, Y_train_val, test_size=test_ratio, random_state=1
            )

        # Create copy for the model
        model = self.new_instance(self.__class__, **kwargs)

        # Transform the data
        if model.variables.num_cat_var > 0:
            model.X_train = model.variables.categorical_transform(X_train).astype("float")
            model.X_val = model.variables.categorical_transform(X_val).astype("float")
            model.X_test = model.variables.categorical_transform(X_test).astype("float")
        else:
            model.X_train = X_train
            model.X_val = X_val
            model.X_test = X_test

        model.X_train, model.Y_train = model.transform_by_predictor_type(model.X_train, Y=Y_train)
        model.X_val, model.Y_val = model.transform_only_by_predictor_type(model.X_val, Y=Y_val)
        model.X_test, model.Y_test = model.transform_only_by_predictor_type(model.X_test, Y=Y_test)

        model.fit_model(self.model_params)

        # Make predictions and calculate model performance
        model.Y_train_pred, model.Y_train_pred_stddev = model.predict(X_train)
        model.Y_val_pred, model.Y_val_pred_stddev = model.predict(X_val)
        model.Y_test_pred, model.Y_test_pred_stddev = model.predict(X_test)
        model.performance_metrics = pm.all_performance_metrics_train_val_test(
            Y_train, model.Y_train_pred, Y_val, model.Y_val_pred, Y_test, model.Y_test_pred
        )

        return model.performance_metrics["Test RMSE"]

    def y_scrambling_cv(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        model_params: Dict[str, Any],
        test_ratio: float = 0.2,
        sort_before_split: bool = True,
        plot_parity: bool = True,
        inc_error_bars: bool = False,
        **kwargs,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """

        Compares the model fitting and accuracy of test data using cross validation for the supplied X and Y data set
        and a Y-scrambled array

        Parameters
        ----------
        X: np.ndarray,
            X array that contains the unprocessed variables data to be fitted to the model, i.e. The data has not yet
            undergone any transformations related to converted categorical variables to their respective descriptors
            or transformations related to standardisation/normalisation
        Y: np.ndarray,
            Y array that contains the unprocessed objective data, i.e. The data has not yet undergone any
            transformations related to standardisation/normalisation
        model_params: Dict[str, Any]
            Dictionary that contains the hyperparameters for the model
        test_ratio: float, Default = 0.2,
            The proportion of inputted X and Y arrays to be split into the validation and test sets where applicable
        sort_before_split: bool, Default = True,
            Whether the inputted X and Y arrays should be sorted such that the Y-values are in ascending order before
            splitting into the training and test sets (and validation sets if applicable)
        plot_parity: bool, Default = True,
            Whether to plot a scatter plot of the Y test data points with predictions from the unshuffled and shuffled
            Y array
        inc_error_bars: bool, Default = False,
            Whether to include 95% confidence interval error bars on the scatter plot points

        Returns
        -------
        cv_results: Dict[str, Any]
            Contains the performance metrics from the fitted models using the original data set with emphasis on the
            test data results
        cv_results_y_scrambling: Dict[str, Any]
            Contains the performance metrics from the fitted models using the Y-scrambled array, with emphasis on
            the test data Results

        """

        dirname_y_scrambling = os.path.join(os.getcwd(), "ML Models", f"{self.name}", "Y-Scrambling")
        if not os.path.exists(dirname_y_scrambling):
            os.makedirs(dirname_y_scrambling)

        cv_results = self.cv(X, Y, model_params, test_ratio=test_ratio, sort_before_split=sort_before_split, **kwargs)

        np.random.seed(0)
        np.random.shuffle(Y)

        cv_results_y_scrambling = self.cv(
            X, Y, model_params, test_ratio=test_ratio, sort_before_split=sort_before_split, **kwargs
        )

        if plot_parity:
            # Produces a 2D scatter plot showing the parity plot data points, and the x = y line as a line plot
            original_paritydata = cv_results["Mean Y Test Parity Data"]
            y_scrambling_paritydata = cv_results_y_scrambling["Mean Y Test Parity Data"]

            original_error = cv_results["Mean Y Test Error (CI 95%)"]
            y_scrambling_error = cv_results_y_scrambling["Mean Y Test Error (CI 95%)"]

            original_rmse = cv_results["Mean Test RMSE"]
            y_scrambling_rmse = cv_results_y_scrambling["Mean Test RMSE"]
            original_r2 = cv_results["Mean Test r2"]
            y_scrambling_r2 = cv_results_y_scrambling["Mean Test r2"]

            scatter_parity_data = [original_paritydata, y_scrambling_paritydata]
            error = [original_error, y_scrambling_error]
            max_parity = np.vstack([original_paritydata, y_scrambling_paritydata]).max()
            min_parity = np.vstack([original_paritydata, y_scrambling_paritydata]).min()
            # Array for the x = y line in the parity plot
            x_equals_y = [
                [min_parity, min_parity],
                [max_parity, max_parity],
            ]
            scatter_legend = (
                f"Original ({original_paritydata.shape[0]} Test Data Points)",
                f"Y-Scrambling ({y_scrambling_paritydata.shape[0]} Test Data Points)",
            )
            plot_title = f"Original and Y-Scrambling Test Data Parity Plot\nOriginal Test RMSE = {round(original_rmse.astype('float'), 2)}, Original Test r2 = {round(original_r2, 2)}\nY-Scrambling Test RMSE = {round(y_scrambling_rmse.astype('float'), 2)}, Y-Scrambling Test r2 = {round(y_scrambling_r2, 2)}"
            output_file = os.path.join(
                dirname_y_scrambling,
                f"Y-Scrambling Test Data Parity Plot, {datetime.now().strftime('%d-%m-%Y, %H-%M-%S')}",
            )
            if inc_error_bars:
                plotter.plot(
                    plot_dim="2D",
                    scatter_data=scatter_parity_data,
                    error=error,
                    line_data=x_equals_y,
                    scatter_legend=scatter_legend,
                    line_legend="x = y",
                    xlabel=f"Actual",
                    ylabel=f"Predicted",
                    plottitle=plot_title,
                    output_file=output_file,
                )
            else:
                plotter.plot(
                    plot_dim="2D",
                    scatter_data=scatter_parity_data,
                    # error=error,
                    line_data=x_equals_y,
                    scatter_legend=scatter_legend,
                    line_legend="x = y",
                    xlabel=f"Actual",
                    ylabel=f"Predicted",
                    plottitle=plot_title,
                    output_file=output_file,
                )
            plt.close()

        logger.info(
            f"Completed Y-scrambling CV tests | Mean Test Loss: {cv_results['Mean Test RMSE']} | Y-scrambling Mean Test Loss: {cv_results_y_scrambling['Mean Test RMSE']}"
        )

        return cv_results, cv_results_y_scrambling

    def permutation_feature_importance(
        self, X: np.ndarray, Y: np.ndarray, repeats: int = 50
    ) -> Tuple[pd.Series, pd.Series]:
        """

        Provides a measure of the feature importance by shuffling (permuting) each feature individually to observe its
        effect on the mean-square-error (MSE) of the prediction against the MSE calculated from an unaltered X array.
        The permutation feature importance of categorical variables are returned per categorical variable instead of by
        their respective descriptors

        Parameters
        ----------
        X: np.ndarray,
            X array that contains the unprocessed variables data to be fitted to the model, i.e. The data has not yet
            undergone any transformations related to converted categorical variables to their respective descriptors
            or transformations related to standardisation/normalisation
        Y: np.ndarray,
            Y array that contains the unprocessed objective data, i.e. The data has not yet undergone any
            transformations related to standardisation/normalisation
        repeats: int, Default = 50
            The number of times to shuffle (permute) each feature. The average MSE over all repeats is calculated

        Returns
        -------
        feature_importance_mean: pd.Series
            The normalised permutation feature importance over all repeats
        feature_importance_stddev: pd.Series
            The standard deviation of the MSE after shuffling each feature over all repeats

        """
        logger.info(f"Performing permutation feature importance calculation for {self.name} model")

        Y_pred_base, _ = self.predict(X)
        mse_score_base = mean_squared_error(Y, Y_pred_base)

        results = []
        for i in range(X.shape[1]):
            temp_i_store = copy.copy(X[:, i])

            mse_score_i_shuffled_list = []
            for repeat in range(repeats):
                np.random.shuffle(X[:, i])
                Y_pred_i_shuffled, _ = self.predict(X)
                mse_score_i_shuffled = mean_squared_error(Y, Y_pred_i_shuffled)
                mse_score_i_shuffled_list.append(mse_score_i_shuffled)
                if repeat % 10 == 0:
                    print(
                        f"Variable {i + 1}, Repeat {repeat + 1}, Permutation MSE: {mse_score_i_shuffled}, Difference to Base MSE: {mse_score_i_shuffled - mse_score_base}"
                    )
            X[:, i] = copy.copy(temp_i_store)
            results.append(np.array(mse_score_i_shuffled_list))

        results = np.array(results).T
        results_diff = results - mse_score_base
        feature_importance_mean = np.mean(results_diff, axis=0)
        feature_importance_mean = feature_importance_mean / np.sum(feature_importance_mean)
        feature_importance_stddev = np.std(results_diff, axis=0)

        feature_importance_mean = pd.Series(feature_importance_mean, index=self.variables.names)
        feature_importance_stddev = pd.Series(feature_importance_stddev, index=self.variables.names)

        print(f"Permutation feature importance: {np.around(feature_importance_mean, decimals=3)}")

        logger.info(f"Completed permutation feature importance calculation")

        return feature_importance_mean, feature_importance_stddev

    def permutation_feature_importance_continuous(
        self, X: np.ndarray, Y: np.ndarray, repeats: int = 50
    ) -> Tuple[pd.Series, pd.Series]:
        """

        Provides a measure of the feature importance by shuffling (permuting) each feature individually to observe its
        effect on the mean-square-error (MSE) of the prediction against the MSE calculated from an unaltered X array.
        The permutation feature importance of categorical variables are returned as their respective descriptors

        Parameters
        ----------
        X: np.ndarray,
            X array that contains the unprocessed variables data to be fitted to the model, i.e. The data has not yet
            undergone any transformations related to converted categorical variables to their respective descriptors
            or transformations related to standardisation/normalisation
        Y: np.ndarray,
            Y array that contains the unprocessed objective data, i.e. The data has not yet undergone any
            transformations related to standardisation/normalisation
        repeats: int, Default = 50
            The number of times to shuffle (permute) each feature. The average MSE over all repeats is calculated

        Returns
        -------
        feature_importance_mean: pd.Series
            The normalised permutation feature importance over all repeats
        feature_importance_stddev: pd.Series
            The standard deviation of the MSE after shuffling each feature over all repeats

        """
        logger.info(f"Performing permutation feature importance calculation for {self.name} model")

        Y_pred_base, _ = self.predict(X)
        mse_score_base = mean_squared_error(Y, Y_pred_base)

        # Convert categorical variables names to descriptors
        if self.variables.num_cat_var > 0:
            X = self.variables.categorical_transform(X)

        # Transform the continuous variables and descriptors
        X = self.transform_only_by_predictor_type(X)

        results = []
        for i in range(X.shape[1]):
            temp_i_store = copy.copy(X[:, i])

            mse_score_i_shuffled_list = []
            for repeat in range(repeats):
                np.random.shuffle(X[:, i])

                Y_pred_i_shuffled, _ = self.predict(X, X_transform=False)

                mse_score_i_shuffled = mean_squared_error(Y, Y_pred_i_shuffled.flatten())
                mse_score_i_shuffled_list.append(mse_score_i_shuffled)
                if repeat % 10 == 0:
                    print(
                        f"Variable {i + 1}, Repeat {repeat + 1}, Permutation MSE: {mse_score_i_shuffled}, Difference to Base MSE: {mse_score_i_shuffled - mse_score_base}"
                    )
            X[:, i] = copy.copy(temp_i_store)
            results.append(np.array(mse_score_i_shuffled_list))

        results = np.array(results).T
        results_diff = results - mse_score_base
        feature_importance_mean = np.mean(results_diff, axis=0)
        feature_importance_mean = feature_importance_mean / np.sum(feature_importance_mean)
        feature_importance_stddev = np.std(results_diff, axis=0)

        feature_importance_mean = pd.Series(feature_importance_mean, index=self.variables.continuous_var_names)
        feature_importance_stddev = pd.Series(feature_importance_stddev, index=self.variables.continuous_var_names)

        print(f"Permutation feature importance:\n{np.around(feature_importance_mean, decimals=3)}")

        logger.info(f"Completed permutation feature importance calculation")

        return feature_importance_mean, feature_importance_stddev

    def partial_dependence_plot(self, X: np.ndarray) -> Dict[str, pd.DataFrame]:
        """

        Creates partial dependence plots of the fitted model using the provided X array

        Parameters
        ----------
        X: np.ndarray,
            X array that contains the unprocessed variables data to be fitted to the model, i.e. The data has not yet
            undergone any transformations related to converted categorical variables to their respective descriptors
            or transformations related to standardisation/normalisation

        Returns
        -------
        pdp_dict: Dict[str, pd.DataFrame]
            Dictionary that contains a DataFrame of the partial dependence plot data for every feature

        """
        logger.info(f"Creating partial dependence plots for {self.name} model")
        path = os.path.join(os.getcwd(), "ML Models", f"{self.name}", "Partial Dependence Plots")
        if not os.path.exists(path):
            os.makedirs(path)

        if self.variables.num_cat_var > 0:
            X = self.variables.categorical_transform(X)

        X = self.transform_only_by_predictor_type(X)

        X_copy = copy.copy(X)

        pdp_dict = {}
        for index, col in enumerate(X.T):
            Y_pred_pdp = []
            for value in col:
                X_copy[:, index] = value

                Y_pred, _ = self.predict(X_copy, X_transform=False)
                Y_pred_pdp.append([value, Y_pred.mean()])

            Y_pred_pdp_np = np.array(Y_pred_pdp)
            pdp_dict[self.variables.continuous_var_names[index]] = pd.DataFrame(
                Y_pred_pdp_np, columns=[f"{self.variables.continuous_var_names[index]}", f"{self.objective.name}",],
            )
            X_copy[:, index] = col

            plotter.plot(
                plot_dim="2D",
                scatter_data=Y_pred_pdp_np,
                scatter_legend=f"Number of Grid Points = {Y_pred_pdp_np.shape[0]}",
                xlabel=f"{self.variables.continuous_var_names[index]}",
                ylabel=f"{self.objective.name} ({self.objective.units})",
                plottitle=f"Partial Dependence Plot for {self.objective.name} against {self.variables.continuous_var_names[index]}",
                output_file=os.path.join(
                    path,
                    rf"Partial Dependence Plot for {self.objective.name} against {self.variables.continuous_var_names[index]}, {datetime.now().strftime('%d-%m-%Y, %H-%M-%S')}",
                ),
            )
            plt.close("all")

        logger.info(f"Completed partial dependence plot calculations")

        return pdp_dict

    def transform_by_predictor_type(
        self, X: np.ndarray, Y: Optional[np.ndarray] = None
    ) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
        """

        Function called to transform the X array and optional Y array. Parameters for the transformations are both
        generated and used here

        Parameters
        ----------
        X: np.ndarray,
            X array of only continuous data ready for transformations related to standardisation/normalisation
        Y: np.ndarray, Default = None
            Y array that contains the unprocessed objective dataready for transformations related to
            standardisation/normalisation

        """
        X = self.variables.transform(X, self.default_X_transform_type)

        if Y is not None:
            if self.objective.transformation_type is None:
                self.objective.transformation_type = self.default_Y_transform_type
            Y = self.objective.transform(Y)
            return X.astype("float"), Y.astype("float")
        else:
            return X.astype("float")

    def transform_only_by_predictor_type(
        self, X: np.ndarray, Y: Optional[np.ndarray] = None
    ) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
        """

        Function called to transform the X array and optional Y array. The transformations use the parameters previous
        generated when the self.transform_by_predictor_type function was previously called

        Parameters
        ----------
        X: np.ndarray,
            X array of only continuous data ready for transformations related to standardisation/normalisation
        Y: np.ndarray, Default = None
            Y array that contains the unprocessed objective dataready for transformations related to
            standardisation/normalisation

        """
        X = self.variables.transform_only(X)

        if Y is not None:
            Y = self.objective.transform_only(Y)
            return X.astype("float"), Y.astype("float")
        else:
            return X.astype("float")
