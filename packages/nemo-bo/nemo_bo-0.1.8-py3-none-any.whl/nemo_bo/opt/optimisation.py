import ast
import os
import pickle
from attrs import define, field
from datetime import datetime
from typing import Any, Dict, Optional, Tuple, List, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from botorch.utils.multi_objective.hypervolume import Hypervolume
from botorch.utils.multi_objective.pareto import is_non_dominated
from gpytorch.kernels import AdditiveStructureKernel

import nemo_bo.utils.logger as logging_nemo
import nemo_bo.utils.plotter as plotter
from nemo_bo.acquisition_functions.base_acq_function import AcquisitionFunction
from nemo_bo.acquisition_functions.expected_improvement.expected_improvement import ExpectedImprovement
from nemo_bo.opt.benchmark import Benchmark, ModelBenchmark, SyntheticBenchmark
from nemo_bo.opt.constraints import ConstraintsList
from nemo_bo.opt.objectives import ObjectivesList, RegressionObjective
from nemo_bo.opt.samplers import LatinHyperCubeSampling, PoolBased, SampleGenerator
from nemo_bo.opt.variables import VariablesList
from nemo_bo.utils.data_proc import remove_nan, remove_all_nan_rows

try:
    logging_nemo.logging_path
    logger = logging_nemo.logging_nemo_child(os.path.basename(__file__))
except AttributeError:
    logger = logging_nemo.logging_nemo_master(os.path.basename(__file__))


@define
class Optimisation:
    """

    Class used to optimise a problem defined by the variables, objectives, acquisition function used to suggest new
    experiments, and optional constraints, sampler, and/or benchmark functions

    Parameters
    ----------
    variables: VariablesList
        VariablesList object that contains information about all variables
    objectives: ObjectivesList
        ObjectivesList object that contains information about all objectives
    acquisition_func: AcquisitionFunction
        Specifies the method used to suggest new candidates
    sampler: SampleGenerator, PoolBased, Default = None
        Specifies the method to obtain samples, either using a generator or from a sample pool
    constraints: ConstraintsList, Default = None
        ConstraintsList object that contains information about all constraints
    benchmark_func: Benchmark, Default = None
        Provides a method to predict the outcome of the suggested candidates made by the acquisition function when a
        simulated optimisation is being performed

    """

    variables: VariablesList
    objectives: ObjectivesList
    acquisition_func: AcquisitionFunction
    sampler: Optional[Union[SampleGenerator, PoolBased]] = None
    constraints: Optional[ConstraintsList] = None
    benchmark_func: Optional[Benchmark] = None
    optimisation_dict: Dict[str, Any] = field(init=False)
    X_columns: List[str] = field(init=False)
    Y_columns: List[str] = field(init=False)
    X: np.ndarray = field(init=False)
    Y: np.ndarray = field(init=False)
    optimisation_only: pd.DataFrame = field(init=False)
    selected_X: np.ndarray = field(init=False)
    selected_Y: np.ndarray = field(init=False)

    def __attrs_post_init__(self):
        if isinstance(self.acquisition_func, ExpectedImprovement) and self.sampler is None:
            self.sampler = LatinHyperCubeSampling(num_new_points=1024)

        # Dictionary that stores the optimisation information for every iteration
        self.optimisation_dict = {}

        # Constructs lists of variables and objectives with their respective units where provided
        self.X_columns = []
        for name, units in zip(self.variables.names, self.variables.units):
            if units == "":
                self.X_columns.append(name)
            else:
                self.X_columns.append(f"{name} ({units})")

        self.Y_columns = []
        for name, units in zip(self.objectives.names, self.objectives.units):
            if units == "":
                self.Y_columns.append(name)
            else:
                self.Y_columns.append(f"{name} ({units})")

    def run(
        self,
        X: Optional[np.ndarray] = None,
        Y: Optional[np.ndarray] = None,
        number_of_iterations: int = 200,
        test_ratio: float = 0.2,
        number_opt_iterations_completed: int = 0,
        model_run_counter: int = 0,
        model_run_counter_threshold: int = 5,
        plot_pareto_hypervolume: bool = False,
        test_data: Optional[List[np.ndarray]] = None,
        **kwargs,
    ) -> Dict[str, Dict[str, Any]]:
        """

        A convenient function to start a Bayesian optimisation, including model fitting. It will also request the results
        at the end of each iteration and save all optimisation data, and then automatically start the next iteration.

        Parameters
        ----------
        X: np.ndarray
            X array that contains the unprocessed variables data to be fitted to the model, i.e. The data has not yet
            undergone any transformations related to converted categorical variables to their respective descriptors
            or transformations related to standardisation/normalisation
        Y: np.ndarray
            Y array that contains the unprocessed objective data for all calculable and regression objectives, i.e.
            The data has not yet undergone any transformations related to standardisation/normalisation
        number_of_iterations: int, Default = 200,
            Number of optimisation iterations to perform
        test_ratio: float, Default = 0.2,
            The proportion of inputted X and Y arrays to be split for the validation and test sets where applicable
        number_opt_iterations_completed: int, Default = 0,
            The number of optimisation iterations completed so far. This is used to identify the training data in the
            provided X and Y arrays
        model_run_counter: int, Default = 0,
            Assigns the run counter for the first iteration when this function is called. When the model_run_counter is
            equal to model_run_counter_threshold, an automated model and hyperparameter optimisation will occur at the
            next opportunity
        model_run_counter_threshold: int, Default = 5,
            Sets the threshold value for when an automated model and hyperparameter optimisation should occur
        plot_pareto_hypervolume: bool, Default = False,
            Sets whether to generate the 2D pareto plot (2 objectives) and hypervolume over iterations plot every
            iteration
        test_data: List[np.ndarray], Default = None,
            Test data to use for the initial model and hyperparameter optimisation, instead of creating it
            automatically. The X array is at index 0 and the Y array is at index 1

        Returns
        -------
        self.optimisation_dict: Dict[str, Dict[str, Any]]
            Dictionary that stores the optimisation information for every iteration

        """
        if isinstance(self.benchmark_func, SyntheticBenchmark):
            # X = self.sampler.__class__((2 * self.variables.n_var) + 2 if self.variables.n_var >= 4 else 10).generate_samples(self.variables, self.constraints)
            X = self.sampler.__class__(
                (5 * self.variables.n_var) if self.variables.n_var >= 2 else 10
            ).generate_samples(self.variables, self.constraints)
            Y, _ = self.benchmark_func.evaluate(X)
            Y = Y.reshape(-1, 1)

        self.X = X
        self.Y = Y

        for iteration in range(number_of_iterations):
            if model_run_counter % model_run_counter_threshold == 0:
                model_search_bool = True
                print("Will perform automated model and hyperparameter selection")
            else:
                model_search_bool = False
                print("Depending on predictor type, will perform model fitting with stored hyperparameters")

            if plot_pareto_hypervolume:
                # Scatter plot of the Y data
                self.plot_scatter_opt(
                    Y=self.Y, number_opt_iterations=number_opt_iterations_completed,
                )

                # Plot hypervolume over iterations plot
                self.plot_hypervolume(
                    Y=self.Y, number_opt_iterations=number_opt_iterations_completed,
                )

            # Obtain suggested candidates
            self.selected_X, self.selected_Y = self.find_candidates(
                self.X,
                self.Y,
                model_search_bool=model_search_bool,
                test_ratio=test_ratio,
                test_data=test_data,
                **kwargs,
            )
            if self.selected_Y.ndim == 1:
                self.selected_Y = self.selected_Y.reshape(-1, 1)

            # Creates a DataFrame of the suggested candidates
            suggested_XY = pd.DataFrame(
                np.hstack((self.selected_X, self.selected_Y)), columns=self.X_columns + self.Y_columns,
            )
            with pd.option_context("display.max_rows", None, "display.max_columns", None):
                print(suggested_XY)

            # If the optimisation is not a simulated one that used a sample pool or a benchmark function
            if not isinstance(self.sampler, PoolBased) and self.benchmark_func is None:
                if not os.path.exists(os.path.join(os.getcwd(), "Results")):
                    os.makedirs(os.path.join(os.getcwd(), "Results"))
                # Creates an Excel file containing the suggested candidates
                suggested_XY.to_excel(
                    os.path.join(
                        os.getcwd(),
                        "Results",
                        f"Iteration {iteration + 1} suggested candidates {datetime.now().strftime('%d-%m-%Y, %H-%M-%S')}.xlsx",
                    )
                )
                while True:
                    try:
                        # Requests a new array containing the actual Y-values. The array has to be the correct shape
                        # and a list type to be accepted
                        actual_result = ast.literal_eval(
                            input(
                                f"Variables for the current opt iteration have been suggested (see print or 'Iteration {iteration + 1} suggested candidates.xlsx')\nPlease input the actual results in a python list:\n"
                            )
                        )
                        assert isinstance(actual_result, list)

                        self.selected_Y = (
                            np.array(actual_result)
                            if self.acquisition_func.num_candidates > 1
                            else np.array(actual_result).reshape(1, -1)
                        )

                        assert (
                            self.selected_Y.shape[0] == self.acquisition_func.num_candidates
                            and self.selected_Y.shape[1] == self.objectives.n_obj
                            and np.issubdtype(self.selected_Y.dtype, np.number)
                        )

                        break
                    except AssertionError or IndexError or ValueError or SyntaxError:
                        print(
                            "\nAssertionError: Please ensure that you have inputted the actual numerical results in a python list with the correct dimensions for the number of candidates (x) and number of objectives (y)\n"
                        )

            # Updates the X and Y arrays with the new candidates
            self.X = np.vstack((self.X, self.selected_X))
            self.Y = np.vstack((self.Y, self.selected_Y))

            # Saves the optimisation and model information for the current iteration
            self.save(iteration, model_search_bool, model_run_counter)

            # After every iteration, adds 1 to the model_run_counter number
            if self.acquisition_func.reset or model_search_bool:
                model_run_counter = 1
            else:
                model_run_counter += 1

            number_opt_iterations_completed += 1

        return self.optimisation_dict

    def find_candidates(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        model_search_bool,
        test_ratio: float = 0.2,
        test_data: Optional[List[np.ndarray]] = None,
        **kwargs,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """

        Function that returns the suggested candidates by:
        1. Fitting any required regression models
        2. Uses an acquisition function to suggest the next best candidates
        3. Updates the Y-values with

        Parameters
        ----------
        X: np.ndarray,
            X array that contains the unprocessed variables data to be fitted to the model, i.e. The data has not yet
            undergone any transformations related to converted categorical variables to their respective descriptors
            or transformations related to standardisation/normalisation
        Y: np.ndarray,
            Y array that contains the unprocessed objective data for all calculable and regression objectives, i.e.
            The data has not yet undergone any transformations related to standardisation/normalisation
        model_search_bool: bool
            Whether automated model and hyperparameter optimisation is to be performed when fitting the regression
            models
        test_ratio: float, Default = 0.2,
            The proportion of inputted X and Y arrays to be split for the validation and test sets where applicable
        test_data: List[np.ndarray], Default = None,
            Test data to use for the initial model and hyperparameter optimisation, instead of creating it
            automatically. The X array is at index 0 and the Y array is at index 1

        Returns
        -------
        selected_X: np.ndarray
            The X array of the suggested candidates
        selected_Y: np.ndarray
            The Y array of the suggested candidates

        """
        if any(isinstance(obj, RegressionObjective) for obj in self.objectives.objectives):

            # Fit the ML regression models
            self.objectives.fit(
                X, Y, self.variables, model_search_bool, test_ratio=test_ratio, test_data=test_data, **kwargs
            )

        # Use the fitted regression models, calculable objectives, and acquisition function to suggest new candidates
        selected_X, selected_Y = self.acquisition_func.generate_candidates(
            Y, self.variables, self.objectives, self.sampler, self.constraints, **kwargs
        )

        # If a sample pool was used, obtain the actual Y-values and removing the chosen samples from the sample pool
        if isinstance(self.sampler, PoolBased):
            selected_Y = self.sampler.Y_and_update_pool(self.sampler.index)

        else:
            # If a benchmark function is provided, use it to predict the outcome of the suggested X array
            if self.benchmark_func is not None:
                if self.benchmark_func.fitted:
                    selected_Y, _ = self.benchmark_func.evaluate(selected_X)
                else:
                    raise AttributeError("Please firstly fit the benchmark function(s) and check its quality")

        return selected_X, selected_Y

    def save(self, iteration: int, model_search_bool: bool, model_run_counter: int) -> None:
        """

        Saves the optimisation and model information for the current iteration

        Parameters
        ----------
        iteration: int
            Iteration number for the current optimisation
        model_search_bool: bool
            Whether automated model and hyperparameter optimisation was performed when the regression models were fitted
        model_run_counter: int
            The run counter for this optimisation iteration

        """
        # Save excel for current iteration data
        if not os.path.exists(os.path.join(os.getcwd(), "Results")):
            os.makedirs(os.path.join(os.getcwd(), "Results"))

        # Temporarily stored the information in these lists
        model_info_list = [model_search_bool, model_run_counter]
        model_info_columns = [
            "Model and Hyperparameter Optimisation",
            "Model Run Counter",
        ]
        for obj in self.objectives.objectives:
            if isinstance(obj, RegressionObjective):
                if obj.obj_function.include_validation:
                    model_info_list.append(obj.obj_function.performance_metrics["Train RMSE"])
                    model_info_list.append(obj.obj_function.performance_metrics["Train r2"])
                    model_info_list.append(obj.obj_function.performance_metrics["Validation RMSE"])
                    model_info_list.append(obj.obj_function.performance_metrics["Validation r2"])
                    model_info_columns.append(f"{obj.name} Model Train RMSE")
                    model_info_columns.append(f"{obj.name} Model Train r2")
                    model_info_columns.append(f"{obj.name} Model Validation RMSE")
                    model_info_columns.append(f"{obj.name} Model Validation r2")
                else:
                    model_info_list.append(obj.obj_function.performance_metrics["RMSE"])
                    model_info_list.append(obj.obj_function.performance_metrics["r2"])
                    model_info_columns.append(f"{obj.name} Model Train RMSE")
                    model_info_columns.append(f"{obj.name} Model Train r2")
                model_info_list.append(obj.obj_function.name)

                if obj.obj_function.name == "gp":
                    if isinstance(obj.model_params["kernel"], AdditiveStructureKernel):
                        model_info_list.append(
                            f"AdditiveStructureKernel(ScaleKernel(MaternKernel(ard_num_dims=n_var, nu={obj.model_params['kernel'].base_kernel.base_kernel.nu}, lengthscale_prior=GammaPrior(3.0, 6.0)), outputscale_prior=GammaPrior(2.0, 0.15)), num_dims=n_var)"
                        )
                    else:
                        model_info_list.append(
                            f"ScaleKernel(MaternKernel(nu={obj.model_params['kernel'].base_kernel.nu}, ard_num_dims=n_var, lengthscale_prior=GammaPrior(3.0, 6.0)), outputscale_prior=GammaPrior(2.0, 0.15))"
                        )
                else:
                    model_info_list.append(obj.model_params)

                model_info_columns.append(f"{obj.name} Model Type")
                model_info_columns.append(f"{obj.name} Model Hyperparameters")

        model_info_list.append(datetime.now().strftime("%d-%m-%Y, %H-%M-%S"))
        model_info_columns.append("Date and Time")
        # Duplicates this information for every candidate
        model_info = np.array([model_info_list] * self.acquisition_func.num_candidates)

        # Creates the DataFrames of optimisation information
        optimisation_results = pd.DataFrame(np.hstack((self.X, self.Y)), columns=self.X_columns + self.Y_columns)
        if iteration == 0:
            self.optimisation_only = pd.DataFrame(
                np.hstack((self.selected_X, self.selected_Y, model_info)),
                columns=self.X_columns + self.Y_columns + model_info_columns,
            )
        else:
            self.optimisation_only = pd.concat(
                (
                    self.optimisation_only,
                    pd.DataFrame(
                        np.hstack((self.selected_X, self.selected_Y, model_info)),
                        columns=self.X_columns + self.Y_columns + model_info_columns,
                    ),
                ),
                axis=0,
                ignore_index=True,
            )

        # Writes the optimisation information DataFrames into Excel files
        with pd.ExcelWriter(
            os.path.join(
                os.getcwd(),
                "Results",
                f'Optimisation Results (after {iteration + 1} iteration(s)) {datetime.now().strftime("%d-%m-%Y, %H-%M-%S")}.xlsx',
            )
        ) as writer:
            optimisation_results.to_excel(writer, sheet_name="Training + Opt")
            self.optimisation_only.to_excel(writer, sheet_name="Only Opt")
            for obj in self.objectives.objectives:
                if isinstance(obj, RegressionObjective):
                    if obj.obj_function.include_validation:
                        obj.obj_function.performance_metrics["Train Parity Data"].to_excel(
                            writer, sheet_name=f"{obj.name} Train Parity Data"
                        )
                        obj.obj_function.performance_metrics["Validation Parity Data"].to_excel(
                            writer, sheet_name=f"{obj.name} Validation Parity Data"
                        )
                    else:
                        obj.obj_function.performance_metrics["Parity Data"].to_excel(
                            writer, sheet_name=f"{obj.name} Train Parity Data"
                        )

        # Writes pickle files containing every iteration's optimisation information
        self.optimisation_dict[f"Iteration {iteration + 1}"] = {}
        self.optimisation_dict[f"Iteration {iteration + 1}"]["Date and Time"] = datetime.now().strftime(
            "%d-%m-%Y, %H-%M-%S"
        )
        self.optimisation_dict[f"Iteration {iteration + 1}"]["Training + Optimisation Table"] = optimisation_results
        self.optimisation_dict[f"Iteration {iteration + 1}"]["Optimisation Table"] = self.optimisation_only
        self.optimisation_dict[f"Iteration {iteration + 1}"]["Optimisation Selected X"] = self.selected_X
        self.optimisation_dict[f"Iteration {iteration + 1}"]["Optimisation Selected Y"] = self.selected_Y
        self.optimisation_dict[f"Iteration {iteration + 1}"][
            "Model and Hyperparameter Optimisation"
        ] = model_search_bool
        self.optimisation_dict[f"Iteration {iteration + 1}"]["Model Run Counter"] = model_run_counter
        for obj in self.objectives.objectives:
            if isinstance(obj, RegressionObjective):
                self.optimisation_dict[f"Iteration {iteration + 1}"][f"{obj.name} Model Type"] = obj.obj_function.name
                if obj.obj_function.name == "gp":
                    if isinstance(obj.model_params["kernel"], AdditiveStructureKernel):
                        self.optimisation_dict[f"Iteration {iteration + 1}"][
                            f"{obj.name} Model Hyperparameters"
                        ] = f"AdditiveStructureKernel(ScaleKernel(MaternKernel(ard_num_dims=n_var, nu={obj.model_params['kernel'].base_kernel.base_kernel.nu}, lengthscale_prior=GammaPrior(3.0, 6.0)), outputscale_prior=GammaPrior(2.0, 0.15)), num_dims=n_var)"
                    else:
                        self.optimisation_dict[f"Iteration {iteration + 1}"][
                            f"{obj.name} Model Hyperparameters"
                        ] = f"ScaleKernel(MaternKernel(nu={obj.model_params['kernel'].base_kernel.nu}, ard_num_dims=n_var, lengthscale_prior=GammaPrior(3.0, 6.0)), outputscale_prior=GammaPrior(2.0, 0.15))"
                else:
                    self.optimisation_dict[f"Iteration {iteration + 1}"][
                        f"{obj.name} Model Hyperparameters"
                    ] = obj.model_params
                self.optimisation_dict[f"Iteration {iteration + 1}"][
                    f"{obj.name} Model Performance Metrics"
                ] = obj.obj_function.performance_metrics

        with open(
            os.path.join(
                os.getcwd(),
                "Results",
                f"Optimisation Results (after {iteration + 1} iteration(s)) {datetime.now().strftime('%d-%m-%Y, %H-%M-%S')}.pickle",
            ),
            "wb",
        ) as handle:
            pickle.dump(self.optimisation_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def calc_hypervolume(self, Y: np.ndarray) -> float:
        """

        Calculates the hypervolume of a Y-array that has been min-max normalised by the pre-defined objective bounds

        Parameters
        ----------
        Y: np.ndarray
            Y-array with objective data. Any data points with NaN values will be removed

        Returns
        -------
        The normalised hypervolume of a Y-array

        """
        Y_no_nan = remove_all_nan_rows(Y)
        ref_point = self.acquisition_func.build_ref_point(self.objectives.max_bool_dict)
        sign_adjusted_Y = self.acquisition_func.Y_norm_minmax_transform(
            Y_no_nan, self.objectives.bounds, self.objectives.max_bool_dict
        )

        # Calculates pareto front
        pareto_mask = is_non_dominated(torch.tensor(sign_adjusted_Y, dtype=torch.double))
        pareto_front = sign_adjusted_Y[pareto_mask]

        # Calculates the hypervolume
        hv = Hypervolume(ref_point=torch.tensor(ref_point, dtype=torch.double))
        return hv.compute(torch.tensor(pareto_front, dtype=torch.double))

    def plot_scatter_opt(self, Y: np.ndarray, number_opt_iterations: int) -> None:
        """

        Plots the Y-array for 1, 2, or 3 objective optimisation problems, with multi-objective pareto fronts when
        applicable

        Parameters
        ----------
        Y: np.ndarray
            Y-array with objective data. Any data points with NaN values will be removed
        number_opt_iterations: int
            Number of Bayesian optimisation iterations performed so far

        """
        train_num = Y.shape[0] - (number_opt_iterations * self.acquisition_func.num_candidates)
        opt_num = number_opt_iterations * self.acquisition_func.num_candidates

        if self.objectives.n_obj == 1:
            iterations = np.array((range(Y.shape[0]))) + 1
            Y = np.hstack((iterations.reshape(-1, 1), Y))

        else:
            Y_no_nan = remove_all_nan_rows(Y)

            sign_adjusted_Y = self.acquisition_func.Y_norm_minmax_transform(
                Y_no_nan, self.objectives.bounds, self.objectives.max_bool_dict
            )

            # Calculates pareto front
            Y_to_expnum = torch.tensor(np.array(sign_adjusted_Y), dtype=torch.double)
            pareto_mask_to_expnum = is_non_dominated(Y_to_expnum)
            pareto_front = Y_no_nan[pareto_mask_to_expnum]

            non_zero_objs = np.where(np.all(~np.isclose(Y_no_nan, 0.0), axis=0))[0]
            if len(non_zero_objs) > 0:
                # Uses the first objective in the array that has all non-zero values
                pareto_front_sorted = pareto_front[pareto_front[:, non_zero_objs[0]].argsort()]
            else:
                # Else just use the first objective
                pareto_front_sorted = pareto_front[pareto_front[:, 0].argsort()]

        train_experiments = Y[
            :train_num, :,
        ]
        opt_experiments = Y[
            train_num:, :,
        ]

        train_experiments = remove_all_nan_rows(train_experiments)
        opt_experiments = remove_all_nan_rows(opt_experiments)

        scatter_data = [train_experiments, opt_experiments]
        scatter_legend = [
            f"Training ({train_num} experiments)"
            if train_num == train_experiments.shape[0]
            else f"Training ({train_num} expt, showing {train_experiments.shape[0]} expt)",
            f"Optimisation ({opt_num} experiments)"
            if train_num == opt_experiments.shape[0]
            else f"Optimisation ({opt_num} expt, showing {opt_experiments.shape[0]} expt)",
        ]

        title = "Pareto Plot"
        output = os.path.join(os.getcwd(), f'Pareto Plot {datetime.now().strftime("%d-%m-%Y, %H-%M-%S")}.png',)

        if self.objectives.n_obj == 1:
            plotter.plot(
                plot_dim="2D",
                scatter_data=scatter_data,
                # Create array to use for drawing the start of the optimisation line
                line_data=[[train_num + 0.5, min(Y[:, 1])], [train_num + 0.5, max(Y[:, 1])]],
                scatter_legend=scatter_legend,
                line_legend="Start of Optimisation",
                xlabel=f"Number of Iterations",
                ylabel=f"{self.objectives.names[0]} {self.objectives.units[0]}",
                plottitle=f"{title}\n{self.objectives.names[0]} vs. Number of Iterations",
                output_file=rf"{output}",
            )
        elif self.objectives.n_obj == 2:
            plotter.plot(
                plot_dim="2D",
                scatter_data=scatter_data,
                line_data=pareto_front_sorted,
                scatter_legend=scatter_legend,
                line_legend="Pareto front",
                xlabel=f"{self.objectives.names[0]} {self.objectives.units[0]}",
                ylabel=f"{self.objectives.names[1]} {self.objectives.units[1]}",
                plottitle=f"{title}\n{self.objectives.names[0]} vs. {self.objectives.names[1]}",
                output_file=rf"{output}",
            )
        elif self.objectives.n_obj == 3:
            plotter.plot(
                plot_dim="3D",
                scatter_data=scatter_data,
                surface_data=pareto_front_sorted,
                scatter_legend=scatter_legend,
                surface_legend="Pareto front",
                xlabel=f"{self.objectives.names[0]} {self.objectives.units[0]}",
                ylabel=f"{self.objectives.names[1]} {self.objectives.units[1]}",
                zlabel=f"{self.objectives.names[2]} {self.objectives.units[2]}",
                plottitle=f"{title}\n{self.objectives.names[0]} vs. {self.objectives.names[1]} vs. {self.objectives.names[2]}",
                output_file=rf"{output}",
            )

        plt.close()

    def plot_hypervolume(self, Y: np.ndarray, number_opt_iterations: int) -> None:
        """

        Plots the hypervolume over all iterations

        Parameters
        ----------
        Y: np.ndarray
            Y-array with objective data. Any data points with NaN values will be removed
        number_opt_iterations: int
            Number of Bayesian optimisation iterations performed so far

        """
        train_num = Y.shape[0] - (number_opt_iterations * self.acquisition_func.num_candidates)
        opt_num = number_opt_iterations * self.acquisition_func.num_candidates

        iterations = np.array((range(Y.shape[0]))) + 1
        del_index = [index for index in range(Y.shape[0]) if np.any(np.isnan(Y[index]), axis=0)]
        iterations = np.delete(iterations, del_index, axis=0)

        no_nan_train_num = sum(expt_number <= train_num for expt_number in iterations)
        no_nan_opt_num = sum(expt_number > train_num for expt_number in iterations)

        Y_no_nan = remove_all_nan_rows(Y)
        ref_point = self.acquisition_func.build_ref_point(self.objectives.max_bool_dict)
        sign_adjusted_Y = self.acquisition_func.Y_norm_minmax_transform(
            Y_no_nan, self.objectives.bounds, self.objectives.max_bool_dict
        )
        # Recalculates the hypervolume for every additional row in the data
        hv_list = [0]
        for y_index in range(2, Y_no_nan.shape[0] + 1):
            # Calculates pareto front
            obj_data_to_expnum = sign_adjusted_Y[:y_index, :]
            obj_data_to_expnum_np = np.array(obj_data_to_expnum)
            Y_to_expnum = torch.tensor(obj_data_to_expnum_np, dtype=torch.double)
            pareto_mask_to_expnum = is_non_dominated(Y_to_expnum)
            pareto_front_to_expnum = obj_data_to_expnum_np[pareto_mask_to_expnum]

            # Calculates the hypervolume
            hv = Hypervolume(ref_point=torch.tensor(ref_point, dtype=torch.double))
            hv_list.append(hv.compute(torch.tensor(pareto_front_to_expnum, dtype=torch.double)))

        if Y.shape[0] == len(iterations):
            title = f"Hypervolume\nTraining: {train_num} expt\nOptimisation: {opt_num} expt"
        else:
            title = f"Hypervolume\nTraining: {train_num} expt, showing {no_nan_train_num} expt\nOptimisation: {opt_num} expt, showing {no_nan_opt_num} expt"

        output_file = os.path.join(
            os.getcwd(), rf"Hypervolume vs. Iteration {datetime.now().strftime('%d-%m-%Y, %H-%M-%S')}.png",
        )

        hv_array = np.array([[expt_number, hv_list[index]] for index, expt_number in enumerate(iterations)])
        plotter.plot(
            plot_dim="2D",
            scatter_data=hv_array,
            line_data=[[train_num + 0.5, 0.0], [train_num + 0.5, 1.0]],
            scatter_legend="Hypervolume",
            line_legend="Start of Optimisation",
            xlabel=f"Iteration",
            ylabel=f"Normalised Hypervolume",
            plottitle=title,
            output_file=output_file,
        )
        plt.close()
