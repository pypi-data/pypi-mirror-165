import copy
import os

from attrs import define, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler

import nemo_bo.utils.logger as logging_nemo
import nemo_bo.utils.perf_metrics as pm
import nemo_bo.utils.plotter as plotter
from nemo_bo.models.base.available_models import create_predictor_list
from nemo_bo.models.base.base_model import Base_Model
from nemo_bo.opt.variables import VariablesList
from nemo_bo.utils.data_proc import sort_train_test_split_shuffle, remove_nan
from nemo_bo.utils.transformations import Transformations

try:
    logging_nemo.logging_path
    logger = logging_nemo.logging_nemo_child(os.path.basename(__file__))
except AttributeError:
    logger = logging_nemo.logging_nemo_master(os.path.basename(__file__))


@define(kw_only=True)
class Objective:
    """

    Base class for an objective

    Parameters
    ----------
    name: str
        Name of the objective
    obj_max_bool: bool
        Whether the objective is to be maximised (True) or minimised (False)
    lower_bound: int | float
        The lower bound of the objective
    upper_bound: int | float
        The upper bound of the objective
    transformation_type: str. Default = None
        The type of transformation that should be applied to the objective for modelling. When left as the default
        None, the modelling uses the default transformations specified by the model type. When specified, can be
        "normalisation", "standardisation", or "none" for min-max normalisation, standardisation to a mean of 0 and a
        standard deviation of 1, or no transformation respectively
    units: str, Default = ""
        The units for the objective

    """

    name: str
    obj_max_bool: bool
    lower_bound: Union[int, float]
    upper_bound: Union[int, float]
    transformation_type: Optional[str] = None
    units: str = ""

    def transform(self, Y: np.ndarray) -> np.ndarray:
        """

        Fit the transformation scalar to the inputted Y array when self.transformation_type is "normalisation" or
        "standardisation". The Y array is subsequently transformed according to the fit scalar. When
        self.transformation_type = "none", no transformation occurs

        Parameters
        ----------
        Y: np.ndarray
            Y array containing untransformed values for one objective

        """
        if self.transformation_type is None:
            raise AttributeError(
                "Please either: 1. Fit the model first, or 2. Set transformation_type = 'none', 'normalisation', or 'standarisation' when creating the objective instance"
            )

        if self.transformation_type == "none":
            return Y
        self.transformations = Transformations()
        if self.transformation_type == "normalisation":
            return self.transformations.minmaxscaler(Y)
        elif self.transformation_type == "standardisation":
            return self.transformations.standardscaler(Y)

    def transform_only(self, Y: np.ndarray) -> np.ndarray:
        """

        The Y array is transformed according to the fit scalar in the self.transformations object. When
        self.transformation_type = "none", no transformation occurs

        Parameters
        ----------
        Y: np.ndarray
            Y array containing untransformed values for one objective

        """
        if self.transformation_type is None:
            raise AttributeError(
                "Please either: 1. Fit the model first, or 2. Set transformation_type = 'none', 'normalisation', or 'standarisation' when creating the objective instance"
            )

        if self.transformation_type == "none":
            return Y
        if self.transformation_type == "normalisation":
            return self.transformations.minmaxscaler_transform_only(Y)
        elif self.transformation_type == "standardisation":
            return self.transformations.standardscaler_transform_only(Y)

    def inverse_transform(self, Y_transform: np.ndarray) -> np.ndarray:
        """

        The Y_transform array undergoes an inverse transform according to the fit scalar in the self.transformations
        object. When self.transformation_type = "none", no transformation occurs

        Parameters
        ----------
        Y_transform: np.ndarray
            Y array containing transformed values for one objective

        """
        if self.transformation_type == "none":
            return Y_transform
        if isinstance(self.transformations.scaler, MinMaxScaler):
            return self.transformations.inverse_minmaxscaler(Y_transform)
        elif isinstance(self.transformations.scaler, StandardScaler):
            return self.transformations.inverse_standardscaler(Y_transform)


@define(kw_only=True)
class RegressionObjective(Objective):
    """

    Class for an objective to be modelled using a regression machine learning model

    Parameters
    ----------
    name: str
        Name of the objective
    obj_max_bool: bool
        Whether the objective is to be maximised (True) or minimised (False)
    lower_bound: int | float
        The lower bound of the objective
    upper_bound: int | float
        The upper bound of the objective
    transformation_type: str. Default = None
        The type of transformation that should be applied to the objective for modelling. When left as the default
        None, the modelling uses the default transformations specified by the model type. When specified, can be
        "normalisation", "standardisation", or "none" for min-max normalisation, standardisation to a mean of 0 and a
        standard deviation of 1, or no transformation respectively
    units: str, Default = ""
        The units for the objective
    predictor_type: str | Base_Model | List[str | Base_Model], Default = None
        Specifies the type of predictor/model to use for the objective. If unspecified, it will use all of the default
        predictors/models built-in NEMO
    predictor_params_dict: Dict[str, Dict[str, Callable]], Default = None
        Specifies the predictor/model hyperparameters to optimise during model fitting using the HyperOpt package.
        Dictionary with keys corresponding to the model names, and corresponding values that are dictionaries that
        specify the hyperameters to optimise in the HyperOpt format. Any predictor/model types that are unspecified in
        this dictionary will use the default hyperparameters defined by each the model
    gp_kernel_choices: list, Default = None
        Specifies the Gaussian Process (GP) kernels to use. Will only use this argument if GP's are used for model
        fitting. If unspecified, will use the default kernels defined for GP models in NEMO (can find these in
        nemo_bo.models.gp)
    model_params: Dict[str, Any], Default = None
        Specifies the model hyperparameters to use for model fitting
    hyperopt_evals: Dict[str, int], Default = None
        Overrides the default number of HyperOpt iterations for each specified model's hyperparameter optimisation.
        The dictionary keys correspond to the model name, and the values correspond to the number of iterations to use.
        Any predictor/model types that are unspecified in this dictionary will use the default number of iterations
        defined by each the model

    """

    predictor_type: Optional[Union[str, Base_Model, List[Union[str, Base_Model]]]] = None
    predictor_params_dict: Optional[Dict[str, Dict[str, Callable]]] = None
    gp_kernel_choices: Optional[list] = None
    model_params: Optional[Dict[str, Any]] = None
    hyperopt_evals: Optional[Dict[str, int]] = None
    input_predictor_type: str = field(init=False)
    # input_predictor_params_dict: Dict[str, Dict[str, Callable]] = field(init=False)
    obj_function: Base_Model = field(init=False)
    permutation_feature_importance: pd.Series = field(init=False)
    transformations: Transformations = field(init=False)

    def __attrs_post_init__(self):
        self.input_predictor_type = self.predictor_type = create_predictor_list(self.predictor_type)
        # self.input_predictor_params_dict = self.predictor_params_dict
        self.obj_function = None
        self.permutation_feature_importance = None
        self.transformations = None

    def fit_regressor(
        self, X: np.ndarray, Y: np.ndarray, variables: VariablesList, test_ratio: Optional[float] = 0.2, **kwargs
    ) -> None:
        """

        Fits regression objectives to a specific predictor/model type (self.predictor_type) and defined model
        hyperparameters (self.model_params)

        Parameters
        ----------
        X: np.ndarray
            X array that contains the unprocessed variables data to be fitted to the model, i.e. The data has not yet
            undergone any transformations related to converted categorical variables to their respective descriptors
            or transformations related to standardisation/normalisation
        Y: np.ndarray
            Y array that contains the unprocessed objective data for all calculable and regression objectives, i.e.
            The data has not yet undergone any transformations related to standardisation/normalisation
        variables: VariablesList
            VariablesList object that contains information about all variables
        test_ratio: float, Default = 0.2,
            The proportion of inputted X and Y arrays to be split for the validation and test sets where applicable

        """
        X, Y = remove_nan(X, Y)

        self.obj_function = self.predictor_type(variables, self)
        self.obj_function.fit(X, Y, test_ratio=test_ratio, **self.model_params, **kwargs)

        # Calculate permutation feature importance
        (self.permutation_feature_importance, _,) = self.obj_function.permutation_feature_importance_continuous(X, Y)

    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """

        Returns the untransformed predicted mean and standard deviation using the fitted machine learning models at
        the X values

        Parameters
        ----------
        X: np.ndarray
            X array that contains the unprocessed variables data to be fitted to the model, i.e. The data has not yet
            undergone any transformations related to converted categorical variables to their respective descriptors
            or transformations related to standardisation/normalisation

        Returns
        -------
        Y_pred: np.ndarray
            The untransformed predicted mean values using the fitted machine learning models at the X values
        Y_pred_stddev: np.ndarray
            The untransformed predicted standard deviations using the fitted machine learning models at the X values

        """
        Y_pred, Y_pred_stddev = self.obj_function.predict(X)

        return Y_pred.astype("float"), Y_pred_stddev.astype("float")

    def model_and_hyperparameter_opt(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        variables: VariablesList,
        model_search_bool: bool,
        test_ratio: Optional[float] = None,
        test_data: Optional[List[np.ndarray]] = None,
        **kwargs,
    ) -> None:
        """

        Parameters
        ----------
        X: np.ndarray
            X array that contains the unprocessed variables data to be fitted to the model, i.e. The data has not yet
            undergone any transformations related to converted categorical variables to their respective descriptors
            or transformations related to standardisation/normalisation
        Y: np.ndarray
            Y array that contains the unprocessed objective data for all calculable and regression objectives, i.e.
            The data has not yet undergone any transformations related to standardisation/normalisation
        variables: VariablesList
            VariablesList object that contains information about all variables
        model_search_bool: bool
            Whether automated model and hyperparameter optimisation is to be performed during fitting the regression
            models
        test_ratio: float, Default = 0.2,
            The proportion of inputted X and Y arrays to be split for the validation and test sets where applicable
        test_data: List[np.ndarray], Default = None,
            Test data to use for the initial model and hyperparameter optimisation, instead of creating it
            automatically. The X array is at index 0 and the Y array is at index 1

        """
        X, Y = remove_nan(X, Y)

        if model_search_bool:
            test_loss_list = []
            model_list = []
            model_params_list = []

            if test_data is None:
                # Splits the dataset to create training and test datasets
                if test_ratio is None:
                    test_ratio = 0.2
                if kwargs.get("sort_before_split", True):
                    (X_train, X_test, Y_train, Y_test,) = sort_train_test_split_shuffle(
                        X, Y, test_ratio=test_ratio, seed=1
                    )
                else:
                    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_ratio, random_state=1)
            else:
                # Uses the supplied test dataset
                X_train = X
                X_test = test_data[0]
                Y_train = Y
                Y_test = test_data[1]

            # Performs hyperopt for each predictor type passed into this function and appends each respective best model and hyperparameters
            for predictor_class in self.input_predictor_type:
                predictor_instance = predictor_class(variables, self)
                model, model_params = predictor_instance.hyperparam_opt(
                    X_train, Y_train, test_ratio, predictor_params_dict=self.predictor_params_dict, **kwargs
                )
                model_list.append(model)
                model_params_list.append(model_params)

            # Determines the test set prediction accuracy using each optimised predictor type
            for m in model_list:
                Y_test_pred, _ = m.predict(X_test)
                dict = pm.all_performance_metrics(Y_test, Y_test_pred)
                test_loss_list.append(dict["RMSE"])

            # Identifies which predictor type had the most accurate test set prediction
            best_index = test_loss_list.index(min(test_loss_list))
            self.predictor_type = self.input_predictor_type[best_index]
            self.model_params = model_params_list[best_index]

        # The always_hyperparam_opt attribute is from the predictor/model. When True, the identified previously best
        # predictor type undergoes hyperparameter optimisation every Bayesian optimisation iteration
        elif self.obj_function.always_hyperparam_opt:
            # No model search; only hyperopt for the current best predictor type (identified previously)
            predictor_instance = self.predictor_type(variables, self)
            _, self.model_params = predictor_instance.hyperparam_opt(
                X, Y, test_ratio, predictor_params_dict=self.predictor_params_dict, **kwargs
            )

        # Re-fits the model but with the complete dataset
        self.fit_regressor(X, Y, variables, test_ratio=test_ratio, **kwargs)

    def parity_plot(self) -> None:
        """

        Creates a parity plot for evaluating the fit quality of the regression model for the objective

        """
        # The include_validation attribute is from the predictor/model. When True, the X and Y data are split into
        # training and validation sets
        if self.obj_function.include_validation:
            # Produces a 2D scatter plot showing the parity plot data points, and the x = y line as a line plot
            train_paritydata = self.obj_function.performance_metrics["Train Parity Data"]
            train_rmse = self.obj_function.performance_metrics["Train RMSE"]
            train_r2 = self.obj_function.performance_metrics["Train r2"]
            val_paritydata = self.obj_function.performance_metrics["Validation Parity Data"]
            val_rmse = self.obj_function.performance_metrics["Validation RMSE"]
            val_r2 = self.obj_function.performance_metrics["Validation r2"]

            scatter_parity_data = [train_paritydata, val_paritydata]
            error = [
                self.obj_function.Y_train_error,
                self.obj_function.Y_val_error,
            ]
            max_parity = np.amax(np.vstack([train_paritydata, val_paritydata]))
            min_parity = np.amin(np.vstack([train_paritydata, val_paritydata]))
            # Array for the x = y line in the parity plot
            x_equals_y = [
                [min_parity, min_parity],
                [max_parity, max_parity],
            ]
            scatter_legend = (
                f"Train ({train_paritydata.shape[0]} experiments) (95% CI)",
                f"Validation ({val_paritydata.shape[0]} experiments) (95% CI)",
            )
            plot_title = f"{self.name} Parity Plot ({self.obj_function.name} Model)\nTrain RMSE = {round(train_rmse.astype('float'), 2)} {self.units}, Train r2 = {round(train_r2, 2)}, \nValidation RMSE = {round(val_rmse.astype('float'), 2)} {self.units}, Validation r2 = {round(val_r2, 2)}"
            path = os.path.join(os.getcwd(), "ML Models", f"{self.obj_function.name}", "Parity Plots")
            if not os.path.exists(path):
                os.makedirs(path)
            output_file = os.path.join(
                path,
                rf"{self.name} Parity Plot ({self.obj_function.name} Model), {datetime.now().strftime('%d-%m-%Y, %H-%M-%S')}",
            )

        else:
            train_paritydata = self.obj_function.performance_metrics["Parity Data"]
            train_rmse = self.obj_function.performance_metrics["RMSE"]
            train_r2 = self.obj_function.performance_metrics["r2"]
            scatter_parity_data = train_paritydata
            error = self.obj_function.Y_pred_error
            max_parity = np.amax(np.vstack([train_paritydata]))
            min_parity = np.amin(np.vstack([train_paritydata]))
            # Array for the x = y line in the parity plot
            x_equals_y = [
                [min_parity, min_parity],
                [max_parity, max_parity],
            ]
            scatter_legend = f"Train ({train_paritydata.shape[0]} experiments) (95% CI)"
            plot_title = f"{self.name} Parity Plot ({self.obj_function.name} Model)\nRMSE = {round(train_rmse.astype('float'), 2)} {self.units}, r2 = {round(train_r2, 2)}"
            path = os.path.join(os.getcwd(), "ML Models", f"{self.obj_function.name}", "Parity Plots")
            if not os.path.exists(path):
                os.makedirs(path)
            output_file = os.path.join(
                path,
                rf"{self.name} Parity Plot ({self.obj_function.name} Model), {datetime.now().strftime('%d-%m-%Y, %H-%M-%S')}",
            )

        plotter.plot(
            plot_dim="2D",
            scatter_data=scatter_parity_data,
            error=error,
            line_data=x_equals_y,
            scatter_legend=scatter_legend,
            line_legend="x = y",
            xlabel=f"Actual {self.name} ({self.units})",
            ylabel=f"Predicted {self.name} ({self.units})",
            plottitle=plot_title,
            output_file=output_file,
        )
        plt.close()

    def partial_dependence_plot(self, X: np.ndarray) -> Dict[str, pd.DataFrame]:
        """

        Creates a partial dependence plot of the fitted model using the provided X array

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
        partial_dependence_plot_dict = self.obj_function.partial_dependence_plot(X)

        return partial_dependence_plot_dict

    def cv(self, X: np.ndarray, Y: np.ndarray, test_ratio: float = 0.2, **kwargs) -> Dict[str, Any]:
        """

        Function that is called to start the cross validation procedure using the fitted model hyperparameters and
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
        test_ratio: float, Default = 0.2,
            The proportion of inputted X and Y arrays to be split into the validation and test sets where applicable

        Returns
        -------
        Dict[str, Any]
        Dictionary containing the models, their respective prediction quality for all k-folds and average cv statistics
        across all k-folds

        """
        X, Y = remove_nan(X, Y)

        cv_results = self.obj_function.cv(X, Y, self.model_params, test_ratio=test_ratio, **kwargs,)

        return cv_results

    def y_scrambling_cv(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        test_ratio: float = 0.2,
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
        test_ratio: float, Default = 0.2,
            The proportion of inputted X and Y arrays to be split into the validation and test sets where applicable
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
        X, Y = remove_nan(X, Y)

        cv_results, cv_results_y_scrambling = self.obj_function.y_scrambling_cv(
            X,
            Y,
            self.model_params,
            test_ratio=test_ratio,
            plot_parity=plot_parity,
            inc_error_bars=inc_error_bars,
            **kwargs,
        )

        return cv_results, cv_results_y_scrambling


class DeterministicFunction:
    """

    Inherit this DeterministicFunction class to write the calculable function

    Parameters
    ----------
    obj_function_data: Any
        Information that is required for the evaluate function

    """

    def __init__(self, obj_function_data: Optional[Any] = None):
        self.obj_function_data = obj_function_data

    def evaluate(self, X: np.ndarray, *args, **kwargs) -> Tuple[np.ndarray, np.ndarray]:
        """

        The script to calculate and return the corresponding output values and standard deviations using the inputted
        X array

        Parameters
        ----------
        X: np.ndarray
            X array that contains the unprocessed variables data to be fitted to the model, i.e. The data has not
            undergone any transformations related to converted categorical variables to their respective descriptors
            or transformations related to standardisation/normalisation

        """
        pass


@define(kw_only=True)
class CalculableObjective(Objective):
    """

    Class for a calculable objective

    Parameters
    ----------
    name: str
        Name of the objective
    obj_max_bool: bool
        Whether the objective is to be maximised (True) or minimised (False)
    lower_bound: int | float
        The lower bound of the objective
    upper_bound: int | float
        The upper bound of the objective
    transformation_type: str. Default = None
        The type of transformation that should be applied to the objective for modelling. When left as the default
        None, the modelling uses the default transformations specified by the model type. When specified, can be
        "normalisation", "standardisation", or "none" for min-max normalisation, standardisation to a mean of 0 and a
        standard deviation of 1, or no transformation respectively
    units: str, Default = ""
        The units for the objective
    obj_function: DeterministicFunction, Default = None
        Contains the information and script to calculate the output values and standard deviations of the calculable
        objective.

    """

    obj_function: Optional[DeterministicFunction] = None

    def calculate(self, X: np.ndarray, *args, **kwargs) -> Tuple[np.ndarray, np.ndarray]:
        """

        Function to calculate the output values and standard deviations of the calculable objective

        Parameters
        ----------
        X: np.ndarray,
            X array that contains the unprocessed variables data to be fitted to the model, i.e. The data has not
            undergone any transformations related to converted categorical variables to their respective descriptors
            or transformations related to standardisation/normalisation

        Returns
        -------
        Y: np.ndarray
            The calculated output values
        Y_stddev: np.ndarray
            The calculated standard deviations of the output values. Note: this is often equal to 0 for calculable
            objectives

        """
        Y, Y_stddev = self.obj_function.evaluate(X, *args, **kwargs)

        return Y.astype("float"), Y_stddev

    def add_obj_function(self, obj_function: DeterministicFunction) -> None:
        """

        If the extract_excel functionality was used to import a calculable objective, this function can be used to add
        the calculable objective information and script

        Parameters
        ----------
        obj_function: DeterministicFunction
            Contains the information and script to calculate the output values and standard deviations of the calculable
            objective

        """
        self.obj_function = obj_function


@define
class ObjectivesList:
    """

    Class that stores all objectives and their respective properties

    Parameters
    ----------
    objectives: List[Objective]
        A list of RegressionObjective and/or CalculableObjective objects

    """

    objectives: List[Objective]
    n_obj: int = field(init=False)
    names: List[str] = field(init=False)
    units: List[str] = field(init=False)
    max_bool_dict: Dict[str, bool] = field(init=False)
    bounds: np.ndarray = field(init=False)
    predictor_types: Dict[str, str] = field(init=False)

    def __attrs_post_init__(self):
        self.n_obj = len(self.objectives)
        self.names = [obj.name for obj in self.objectives]
        self.units = [obj.units for obj in self.objectives]
        self.max_bool_dict = {obj.name: obj.obj_max_bool for obj in self.objectives}
        self.bounds = np.array(
            [[obj.lower_bound for obj in self.objectives], [obj.upper_bound for obj in self.objectives],]
        ).T
        self.predictor_types = {}

    def fit(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        variables: VariablesList,
        model_search_bool: Optional[bool] = None,
        test_ratio: Optional[float] = None,
        test_data: Optional[List[np.ndarray]] = None,
        **kwargs,
    ) -> None:
        """

        Function that fits all regression objectives, including identifying suitable models and hyperparameters when
        applicable

        Parameters
        ----------
        X: np.ndarray
            X array that contains the unprocessed variables data to be fitted to the model, i.e. The data has not yet
            undergone any transformations related to converted categorical variables to their respective descriptors
            or transformations related to standardisation/normalisation
        Y: np.ndarray
            Y array that contains the unprocessed objective data for all calculable and regression objectives, i.e.
            The data has not yet undergone any transformations related to standardisation/normalisation
        variables: VariablesList
            VariablesList object that contains information about all variables
        model_search_bool: bool
            Whether automated model and hyperparameter optimisation is to be performed during fitting the regression
            models
        test_ratio: float, Default = 0.2,
            The proportion of inputted X and Y arrays to be split for the validation and test sets where applicable
        test_data: List[np.ndarray], Default = None,
            Test data to use for the initial model and hyperparameter optimisation, instead of creating it
            automatically. The X array is at index 0 and the Y array is at index 1

        """
        if model_search_bool is None:
            model_search_bool = kwargs.get("model_search_bool", False)

        # Fit the ML regression models
        for obj_index, obj in enumerate(self.objectives):
            if isinstance(obj, RegressionObjective):
                obj.model_and_hyperparameter_opt(
                    X,
                    Y[:, obj_index],
                    variables,
                    model_search_bool=model_search_bool,
                    test_ratio=test_ratio,
                    test_data=test_data,
                    **kwargs,
                )
                self.predictor_types[self.names[obj_index]] = self.objectives[obj_index].obj_function.name
            else:
                self.predictor_types[self.names[obj_index]] = "calculable objective"

    def evaluate(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """

        Function that uses the inputted X array to predict the RegressionObjective and/or calculate the
        CalculableObjective outputs

        Parameters
        ----------
        X: np.ndarray
            X array that contains the unprocessed variables data to be fitted to the model, i.e. The data has not yet
            undergone any transformations related to converted categorical variables to their respective descriptors
            or transformations related to standardisation/normalisation

        Returns
        -------
        Y: np.ndarray
            The output values obtained from the regression and/or calculable objectives
        Y_stddev: np.ndarray
            The standard deviations obtained from the regression and/or calculable objectives

        """
        Y = np.zeros((X.shape[0], len(self.objectives)), dtype=np.float64)
        Y_stddev = np.zeros_like(Y)
        for obj_index, obj in enumerate(self.objectives):
            if isinstance(obj, RegressionObjective):
                Y[:, obj_index], Y_stddev[:, obj_index] = obj.predict(X)
            elif isinstance(obj, CalculableObjective):
                Y[:, obj_index], Y_stddev[:, obj_index] = obj.calculate(X)

        return Y.astype("float"), Y_stddev.astype("float")

    def parity_plot(self) -> None:
        """

        Creates a parity plot for evaluating the fit quality of all regression models

        """
        for obj in self.objectives:
            if isinstance(obj, RegressionObjective):
                obj.parity_plot()

    def partial_dependence_plot(self, X: np.ndarray) -> Dict[str, Dict[str, pd.DataFrame]]:
        """

        Creates a partial dependence plots for all fitted regression models using the provided X array

        Parameters
        ----------
        X: np.ndarray,
            X array that contains the unprocessed variables data to be fitted to the model, i.e. The data has not yet
            undergone any transformations related to converted categorical variables to their respective descriptors
            or transformations related to standardisation/normalisation

        Returns
        -------
        partial_dependence_plots_dict: Dict[str, Dict[str, pd.DataFrame]]
            Dictionary where the keys are the names of the objectives and the values are dictionaries that each contain
            a DataFrame of the partial dependence plot data for every feature

        """
        partial_dependence_plots_dict = {}
        for obj in self.objectives:
            if isinstance(obj, RegressionObjective):
                partial_dependence_plots_dict[obj.name] = obj.partial_dependence_plot(X)

        return partial_dependence_plots_dict

    def cv(self, X: np.ndarray, Y: np.ndarray, test_ratio: float = 0.2, **kwargs) -> Dict[str, Dict[str, Any]]:
        """

        Function that is called to start the cross validation procedure for every regression objective using their
        respective fitted model hyperparameters and returns a dictionary containing the fitting results with emphasis
        on the test results for each. The number of k-folds is determined by the reciprocal of the test_ratio

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
            The proportion of inputted X and Y arrays to be split into the validation and test sets where applicable

        Returns
        -------
        cv_dict: Dict[str, Dict[str, Any]]
            Dictionary where the keys are the names of the objectives and the values are dictionaries containing the
            models, their respective prediction quality for all k-folds and average cv statistics across all k-folds

        """
        cv_dict = {}
        for obj_index, obj in enumerate(self.objectives):
            if isinstance(obj, RegressionObjective):
                cv_dict[obj.name] = obj.cv(X, Y[:, obj_index], test_ratio=test_ratio, **kwargs)

        return cv_dict

    def y_scrambling_cv(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        test_ratio: float = 0.2,
        plot_parity: bool = True,
        inc_error_bars: bool = False,
        **kwargs,
    ) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, Dict[str, Any]]]:
        """

        Compares the model fitting and accuracy of test data using cross validation for the supplied X and Y data set
        and a Y-scrambled array of all regression objectives

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
            The proportion of inputted X and Y arrays to be split into the validation and test sets where applicable
        plot_parity: bool, Default = True,
            Whether to plot a scatter plot of the Y test data points with predictions from the unshuffled and shuffled
            Y array
        inc_error_bars: bool, Default = False,
            Whether to include 95% confidence interval error bars on the scatter plot points

        Returns
        -------
        cv_dict: Dict[str, Any]
            Dictionary where the keys are the names of the objectives and the values contain the performance metrics
            from the fitted models using the original data set with emphasis on the test data results
        cv_y_scrambling_dict: Dict[str, Any]
            Dictionary where the keys are the names of the objectives and the values contain the performance metrics
            from the fitted models using the Y-scrambled array, with emphasis on the test data Results

        """
        cv_dict, cv_y_scrambling_dict = {}, {}
        for obj_index, obj in enumerate(self.objectives):
            if isinstance(obj, RegressionObjective):
                cv_dict[obj.name], cv_y_scrambling_dict[obj.name] = obj.y_scrambling_cv(
                    X,
                    Y[:, obj_index],
                    test_ratio=test_ratio,
                    plot_parity=plot_parity,
                    inc_error_bars=inc_error_bars,
                    **kwargs,
                )

        return cv_dict, cv_y_scrambling_dict

    def append(self, obj: Objective):
        """

        Function for appending an additional regression or calculable objective to the current ObjectiveList object

        Parameters
        ----------
        obj: Objective
            Regression or calculable objective

        """
        obj_list = copy.copy(self.objectives)
        obj_list.append(obj)

        return ObjectivesList(obj_list)

    def add_calculable_obj_function(self, name: str, obj_function: DeterministicFunction) -> None:
        """

        If the extract_excel functionality was used to import a calculable objective, this function can be used to add
        the calculable objective information and script to the named calculable objective

        Parameters
        ----------
        name: str
            Name of the calculable objective to add the obj_function data to
        obj_function: DeterministicFunction
            Contains the information and script to calculate the output values and standard deviations of the calculable
            objective

        """
        for obj in self.objectives:
            if isinstance(obj, CalculableObjective):
                if name == obj.name:
                    obj.obj_function = obj_function
                    break
