import os
from dataclasses import dataclass
from itertools import combinations
from joblib import Parallel, delayed
from typing import Optional, Tuple, Union

import numpy as np
import random
import torch
from scipy import spatial
from scipy.optimize import Bounds
from scipy.optimize import minimize as scipy_minimize
from scipy.stats import norm

import nemo_bo.utils.logger as logging_nemo
from nemo_bo.acquisition_functions.base_acq_function import AcquisitionFunction
from nemo_bo.acquisition_functions.expected_improvement.ehvi import ExpectedHypervolumeImprovement
from nemo_bo.opt.constraints import ConstraintsList
from nemo_bo.opt.objectives import ObjectivesList
from nemo_bo.opt.samplers import PoolBased, SampleGenerator, PolytopeSampling
from nemo_bo.opt.variables import VariablesList
from nemo_bo.utils.data_proc import remove_all_nan_rows

try:
    logging_nemo.logging_path
    logger = logging_nemo.logging_nemo_child(os.path.basename(__file__))
except AttributeError:
    logger = logging_nemo.logging_nemo_master(os.path.basename(__file__))


@dataclass
class ExpectedImprovement(AcquisitionFunction):
    """

    Class to instantiate to use the acquisition functions expected improvement for single-objective problems or
    expected hypervolume improvement for multi-objective problems

    Parameters
    ----------
    num_candidates: int
        The number of sets of X arrays to be suggested by the acquisition function

    """

    num_candidates: int
    num_restarts: Optional[int] = 8

    def generate_candidates(
        self,
        Y: np.ndarray,
        variables: VariablesList,
        objectives: ObjectivesList,
        sampler: Union[SampleGenerator, PoolBased],
        constraints: Optional[ConstraintsList] = None,
        **kwargs,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """

        Function that is called when generate the best candidates using the expected improvement or expected
        hypervolume acquisition functions. This selection is made automatically based on the number of objectives

        Parameters
        ----------
        Y: np.ndarray
            An array containing Y-values for all objectives
        variables: VariablesList
            VariablesList object that contains information about all variables
        objectives: ObjectivesList
            ObjectivesList object that contains information about all objectives
        sampler: SampleGenerator | PoolBased
            Used during the ei or ehvi functions to generate samples (SampleGenerator) or provide the samples defined
            by the user (PoolBased)
        constraints: ConstraintsList, Default = None
            ConstraintsList object that contains information about all constraints

        Returns
        -------
        selected_X: np.ndarray
            Array of X-values of the identified candidates' that have the highest expected improvement or expected
            hypervolume improvement
        selected_Y: np.ndarray
            Array of Y-values of the identified candidates' that have the highest expected improvement or expected
            hypervolume improvement

        """
        self.sampler = sampler

        Y = remove_all_nan_rows(Y)

        if isinstance(self.sampler, PoolBased):
            if self.num_candidates > 4:
                logger.warning(
                    f"The number of suggested candidates is 5 or greater, which is not recommended for pool-based samples with more than 60 samples due to long run times"
                )

        if objectives.n_obj > 1:
            if isinstance(self.sampler, SampleGenerator):
                if self.sampler.num_new_points is None:
                    # num_new_points = 5000
                    if self.num_candidates == 1:
                        self.sampler.num_new_points = 131072
                        # self.sampler.num_new_points = 500
                    elif self.num_candidates == 2:
                        self.sampler.num_new_points = 256
                        # self.sampler.num_new_points = 50
                    elif self.num_candidates == 3:
                        self.sampler.num_new_points = 64
                    elif self.num_candidates == 4:
                        # self.sampler.num_new_points = 100 # approx 4 million combinations
                        self.sampler.num_new_points = 32  # approx 1.2 million combinations
                    elif self.num_candidates == 5:
                        # self.sampler.num_new_points = 60 # approx 5.5 million combinations
                        self.sampler.num_new_points = 16
            selected_X, selected_Y = self.ehvi(Y, variables, objectives, constraints)

        elif objectives.n_obj == 1:
            if isinstance(self.sampler, SampleGenerator):
                if self.sampler.num_new_points is None:
                    if isinstance(self.sampler, PolytopeSampling):
                        self.sampler.num_new_points = 1024
                    else:
                        self.sampler.num_new_points = 1048576

            self.xi = kwargs.get("xi", 0.01)
            selected_X, selected_Y = self.ei(Y, variables, objectives, constraints)

        self.reset = False

        return selected_X, selected_Y

    def ei(
        self,
        Y: np.ndarray,
        variables: VariablesList,
        objectives: ObjectivesList,
        constraints: Optional[ConstraintsList] = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """

        Function that determines the candidates with the best expected improvement

        Parameters
        ----------
        Y: np.ndarray
            An array containing Y-values for all objectives
        variables: VariablesList
            VariablesList object that contains information about all variables
        objectives: ObjectivesList
            ObjectivesList object that contains information about all objectives
        constraints: ConstraintsList, Default = None
            ConstraintsList object that contains information about all constraints

        Returns
        -------
        selected_X: np.ndarray
            Array of X-values of the identified candidates' that have the highest expected improvement
        selected_Y: np.ndarray
            Array of Y-values of the identified candidates' that have the highest expected improvement

        """
        logger.info(f"Identifying conditions with the highest expected hypervolume improvement")

        success_bool_list = []
        res_fun_list = []
        selected_X_list = []
        selected_Y_list = []
        for iteration in range(self.num_restarts):
            if isinstance(self.sampler, PoolBased):
                logger.info(f"Returning X values from the provided sample pool")
                X_new_points = self.sampler.X_pool
            elif isinstance(self.sampler, SampleGenerator):
                X_new_points = self.sampler.generate_samples(variables, constraints)

            Y_new_points, Y_new_points_stddev = objectives.evaluate(X_new_points)

            logger.info(f"Identifying approximate conditions with the highest expected hypervolume improvement")
            with np.errstate(divide="warn"):
                imp = Y_new_points - np.amax(Y) - self.xi
                Z = imp / Y_new_points_stddev
                ei = imp * norm.cdf(Z) + Y_new_points_stddev * norm.pdf(Z)
                ei[Y_new_points_stddev == 0.0] = 0.0

            sorting_indices = ei[:, -1].argsort()
            index_array = np.arange(X_new_points.shape[0]).reshape(-1, 1)
            concat = np.hstack((X_new_points, Y_new_points, ei))
            concat_sorted = concat[sorting_indices][::-1]
            index_array_sorted = index_array[sorting_indices][::-1]

            X_ei = concat_sorted[:, :-2]
            Y_ei = concat_sorted[:, -2].flatten()

            # 0 index for the highest uncertainty one at the top of the array
            chosen_indices = [0]
            # cosine similarity index of 1.0 for the highest uncertainty one at the top of the array
            cosine_simularity_list = [1.0]
            # Comparing the X_values for the highest uncertainty with every other entry down the sorted X_array
            for index, x in enumerate(X_ei):
                cosine_simularity_index = 1 - spatial.distance.cosine(X_ei[0], x)
                # Only passes if the cosine similarity index of a given x row is greater than 0.1 different from all of the x's in the list
                if all((((x - cosine_simularity_index) ** 2) ** 0.5) > 0.1 for x in cosine_simularity_list):
                    cosine_simularity_list.append(cosine_simularity_index)
                    chosen_indices.append(index)

                if len(chosen_indices) == self.num_candidates:
                    break

            X_ei = X_ei[chosen_indices]
            Y_ei = Y_ei[chosen_indices].astype(np.float64)

            # Writes the indexes of the selected candidates in the sample pool
            if isinstance(self.sampler, PoolBased):
                self.sampler.index = index_array_sorted[: self.num_candidates].flatten().tolist()

                logger.info("Conditions were successfully selected using expected improvement")
                return X_ei, Y_ei

            elif isinstance(self.sampler, SampleGenerator):

                def fun(X):
                    X = X.astype(np.float64).reshape(X_ei.shape)
                    if variables.num_cat_descriptor_var > 0:
                        X = variables.descriptor_to_name(X)

                    Y, Y_stddev = objectives.evaluate(X)

                    with np.errstate(divide="warn"):
                        imp = Y - np.amax(Y) - self.xi
                        Z = imp / Y_stddev
                        ei = imp * norm.cdf(Z) + Y_stddev * norm.pdf(Z)
                        ei[Y_stddev == 0.0] = 0.0

                    # ei_mean = np.mean(ei)
                    ei_sum = np.sum(ei)

                    # return ei_mean
                    return ei_sum

                # Convert the names of categorical variables to their descriptor values
                if variables.num_cat_descriptor_var > 0:
                    X_ei = variables.categorical_transform(X_ei)

                logger.info(f"Optimising the variable location that provides the highest expected improvement")
                if constraints is None:
                    method = "L-BFGS-B"
                    consts = ()
                    options = {"iprint": 99, "maxiter": 1000, "maxfun": 1000000}
                else:
                    method = "SLSQP"
                    consts = constraints.create_scipy_constraints(self.num_candidates)
                    options = {"disp": True, "maxiter": 1000}

                np.random.seed(random.randint(0, 9999999))
                res = scipy_minimize(
                    fun,
                    X_ei.flatten(),
                    method=method,
                    jac="3-point",
                    bounds=Bounds(
                        lb=np.repeat(np.array(variables.lower_bounds), self.num_candidates),
                        ub=np.repeat(np.array(variables.upper_bounds), self.num_candidates),
                        keep_feasible=True,
                    ),
                    constraints=consts,
                    options=options,
                )

                if res.success == True:
                    selected_X = res.x.astype(np.float64).reshape(X_ei.shape)

                    if variables.num_cat_var > 0:
                        selected_X = variables.categorical_values_euc(selected_X)
                    if variables.num_cat_descriptor_var > 0:
                        selected_X = variables.descriptor_to_name(selected_X)

                    selected_Y, Y_new_stddev = objectives.evaluate(selected_X)

                else:
                    selected_X = X_ei
                    selected_Y = Y_ei.reshape(-1, 1) if Y_ei.ndim == 1 else Y_ei

                success_bool_list.append(res.success)
                res_fun_list.append(res.fun)
                selected_X_list.append(selected_X)
                selected_Y_list.append(selected_Y)

        best_fun_index = res_fun_list.index(min(res_fun_list))
        if not any(success_bool_list):
            logger.warning(
                "Optimisation of the variable location that provides the highest expected improvement failed. Will use the best estimated position"
            )

        else:
            logger.info("Successfully optimised the variable location that provides the highest expected improvement")

        return selected_X_list[best_fun_index], selected_Y_list[best_fun_index]

    def ehvi(
        self,
        Y: np.ndarray,
        variables: VariablesList,
        objectives: ObjectivesList,
        constraints: Optional[ConstraintsList] = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """

        Function that determines the candidates with the best expected hypervolume improvement

        Parameters
        ----------
        Y: np.ndarray
            An array containing Y-values for all objectives
        variables: VariablesList
            VariablesList object that contains information about all variables
        objectives: ObjectivesList
            ObjectivesList object that contains information about all objectives
        constraints: ConstraintsList, Default = None
            ConstraintsList object that contains information about all constraints

        Returns
        -------
        selected_X: np.ndarray
            Array of X-values of the identified candidates' that have the highest expected hypervolume improvement
        selected_Y: np.ndarray
            Array of Y-values of the identified candidates' that have the highest expected hypervolume improvement

        """
        logger.info(f"Identifying conditions with the highest expected hypervolume improvement")

        # Construct hypervolume reference point
        ref_point = self.build_ref_point(objectives.max_bool_dict)

        success_bool_list = []
        res_fun_list = []
        selected_X_list = []
        selected_Y_list = []
        for iteration in range(self.num_restarts):
            # logger.info(f"Generating {num_new_points} mixed integer Latin hypercube sampling points in the variable space")
            if isinstance(self.sampler, PoolBased):
                logger.info(f"Returning X values from the provided sample pool")
                X_new_points = self.sampler.X_pool
                index_combos = list(combinations(np.arange(X_new_points.shape[0]), self.num_candidates))
            elif isinstance(self.sampler, SampleGenerator):
                X_new_points = self.sampler.generate_samples(variables, constraints)

            Y_new_points, Y_new_points_stddev = objectives.evaluate(X_new_points)

            sign_adjusted_Y = self.Y_norm_minmax_transform(Y, objectives.bounds, objectives.max_bool_dict)
            sign_adjusted_Y_new_points = self.Y_norm_minmax_transform(
                Y_new_points, objectives.bounds, objectives.max_bool_dict
            )

            # Min_max normalisation of Y standard deviation
            # I think this should be fine to minmax normalise like this
            for obj_index, _ in enumerate(objectives.bounds):
                Y_new_points_stddev[:, obj_index] = Y_new_points_stddev[:, obj_index] / (
                    objectives.bounds[obj_index, 1] - objectives.bounds[obj_index, 0]
                )

            # Creates a list of expected hypervolume improvements for all combinations of the new Y points
            logger.info(f"Identifying approximate conditions with the highest expected hypervolume improvement")
            ehvi = ExpectedHypervolumeImprovement(
                ref_point=torch.tensor(ref_point, dtype=torch.double),
                Y=torch.tensor(sign_adjusted_Y, dtype=torch.double),
            )
            # ehvi_list = []
            X_new_points_combos = list(combinations(X_new_points, self.num_candidates))
            Y_new_points_combos = list(combinations(Y_new_points, self.num_candidates))
            Y_new_points_stddev_combos = list(combinations(Y_new_points_stddev, self.num_candidates))
            sign_adjusted_Y_new_points_combos = list(combinations(sign_adjusted_Y_new_points, self.num_candidates))

            def ehvi_process(candidates_Y, candidates_Y_stddev):
                try:
                    val = ehvi.ehvi_calc(Y_new=candidates_Y, Y_new_stddev=candidates_Y_stddev,)
                    return val
                except ValueError:
                    return torch.tensor(1e-8, dtype=torch.double)

            ehvi_list = Parallel(n_jobs=4)(
                delayed(ehvi_process)(
                    torch.tensor(np.array(candidates_Y), dtype=torch.double),
                    torch.tensor(np.array(candidates_Y_stddev), dtype=torch.double),
                )
                for candidates_Y, candidates_Y_stddev in zip(
                    sign_adjusted_Y_new_points_combos, Y_new_points_stddev_combos
                )
            )

            # Selects the variables and objective values of the candidate(s) that produced the highest expected hypervolume improvement
            max_idx = ehvi_list.index(max(ehvi_list))
            X_ehvi = np.array(X_new_points_combos[max_idx])
            Y_ehvi = np.array(Y_new_points_combos[max_idx])

            # Writes the indexes of the selected candidates in the sample pool
            if isinstance(self.sampler, PoolBased):
                self.sampler.index = list(index_combos[max_idx])

                logger.info("Conditions were successfully selected using expected hypervolume improvement")
                return X_ehvi, Y_ehvi

            elif isinstance(self.sampler, SampleGenerator):
                # The objective function to be minimized for the scipy optimize minimize method
                def fun(X_norm):
                    X_norm_reshape = X_norm.astype(np.float64).reshape(X_ehvi.shape)
                    X = (
                        X_norm_reshape * (np.array(variables.upper_bounds) - np.array(variables.lower_bounds))
                    ) + np.array(variables.lower_bounds)

                    if variables.num_cat_descriptor_var > 0:
                        X = variables.descriptor_to_name(X)

                    Y, Y_stddev = objectives.evaluate(X)

                    sign_adjusted_Y = self.Y_norm_minmax_transform(Y, objectives.bounds, objectives.max_bool_dict)
                    # Min_max normalisation of Y standard deviation
                    # I think this should be fine to minmax normalise like this
                    for obj_index, _ in enumerate(objectives.bounds):
                        Y_stddev[:, obj_index] = Y_stddev[:, obj_index] / (
                            objectives.bounds[obj_index, 1] - objectives.bounds[obj_index, 0]
                        )

                    try:
                        fun_val = -1 * ehvi.ehvi_calc(
                            Y_new=torch.tensor(sign_adjusted_Y, dtype=torch.double),
                            Y_new_stddev=torch.tensor(Y_stddev, dtype=torch.double),
                        )
                    except ValueError:
                        fun_val = -1 * torch.tensor(1e-8, dtype=torch.double)

                    return fun_val.item()

                # Convert the names of categorical variables with their descriptor values
                if variables.num_cat_descriptor_var > 0:
                    X_ehvi = variables.categorical_transform(X_ehvi)

                # Normalise all variable values against the bounds. This will need to change if one-hot is implemented fully
                X_ehvi_norm = (X_ehvi - np.array(variables.lower_bounds)) / (
                    np.array(variables.upper_bounds) - np.array(variables.lower_bounds)
                )

                # Performs the scipy optimize minimize method
                logger.info(
                    f"Optimising the variable location that provides the highest expected hypervolume improvement"
                )
                if constraints is None:
                    method = "L-BFGS-B"
                    consts = ()
                    options = {"iprint": 99, "maxiter": 1000, "maxfun": 1000000}
                else:
                    method = "SLSQP"
                    consts = constraints.create_scipy_constraints(self.num_candidates)
                    options = {"disp": True, "maxiter": 1000}

                np.random.seed(random.randint(0, 9999999))
                res = scipy_minimize(
                    fun,
                    X_ehvi_norm.flatten(),
                    method=method,
                    jac="3-point",
                    bounds=Bounds(
                        lb=np.zeros_like(X_ehvi_norm).flatten(),
                        ub=np.ones_like(X_ehvi_norm).flatten(),
                        keep_feasible=True,
                    ),
                    constraints=consts,
                    options=options,
                )

                if res.fun * -1 > max(ehvi_list).item():
                    if not res.success == True:
                        logger.warning(
                            f"Attempts to optimise the variable location that provides the highest expected hypervolume improvement failed to converge but still improved and so will use the new X values"
                        )

                    # Transform the optimised X value and calculate the corresponding objective Y values
                    selected_X = res.x.astype(np.float64).reshape(X_ehvi.shape)
                    selected_X = (
                        selected_X * (np.array(variables.upper_bounds) - np.array(variables.lower_bounds))
                    ) + np.array(variables.lower_bounds)

                    if variables.num_cat_var > 0:
                        selected_X = variables.categorical_values_euc(selected_X)
                    if variables.num_cat_descriptor_var > 0:
                        selected_X = variables.descriptor_to_name(selected_X)

                    selected_Y, selected_Y_stddev = objectives.evaluate(selected_X)

                else:
                    selected_X = X_ehvi
                    selected_Y = Y_ehvi

                success_bool_list.append(res.fun * -1 > max(ehvi_list).item())
                res_fun_list.append(res.fun)
                selected_X_list.append(selected_X)
                selected_Y_list.append(selected_Y)

        best_fun_index = res_fun_list.index(min(res_fun_list))
        if not any(success_bool_list):
            logger.warning(
                "Optimisation of the variable location that provides the highest expected hypervolume improvement failed. Will use the best estimated position"
            )

        else:
            logger.info(
                "Successfully optimised the variable location that provides the highest expected hypervolume improvement"
            )

        return selected_X_list[best_fun_index], selected_Y_list[best_fun_index]
