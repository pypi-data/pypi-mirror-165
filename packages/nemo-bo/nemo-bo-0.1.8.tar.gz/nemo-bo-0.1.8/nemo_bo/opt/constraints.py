import os
from attrs import define, field
from typing import Callable, List, Tuple, Union

import numpy as np
import torch
from torch import Tensor

import nemo_bo.utils.logger as logging_nemo
from nemo_bo.opt.variables import VariablesList

try:
    logging_nemo.logging_path
    logger = logging_nemo.logging_nemo_child(os.path.basename(__file__))
except AttributeError:
    logger = logging_nemo.logging_nemo_master(os.path.basename(__file__))


@define
class LinearConstraint:
    """

    Implements a linear constraint on the input variables for the optimisation. For example, linear constraints could be:

        a(F1) + b(F2) = 0
        a(F1) + b(F2) >= 0

    where a and b are coefficients for the features F1 and F2 respectively, and the right-hand side of the equation is
    0. Using an equals sign, =, would form a linear equality constraint whereas defining as 'greater than or equal to'
    forms an inequality constraint.

    By default in NEMO, all inequality constraints must be defined as 'greater than or equal to'. Note: This aligns
    with how constraints are defined in the scipy package, but is the opposite when compared to the pymoo package

    Parameters
    ----------
    constraint_type: str
        Defines whether the linear constraint should be an equality or inequality linear constraint by assigning as
        either 'eq' or 'ineq' respectively
    variables: VariablesList
        VariablesList object that contains information about all variables
    features: List[str]
        The name of the features to constrain, e.g. ['F1', 'F2'] for the example equation shown above
    coefficients: List[Union[int, float]]
        The coefficient for every features in the constraint. The values in the provided list must be given in
        the same order as the provided features to constrain, e.g. [a, b] for the example equation shown above
    rhs: Union[int, float]
        The value to set for the right-hand side of the equation, e.g. 0 for the example equation shown above

    """

    constraint_type: str
    variables: VariablesList
    features: List[str]
    coefficients: List[Union[int, float]]
    rhs: Union[int, float]
    index: List[int] = field(init=False)

    def __attrs_post_init__(self):
        self.index = [self.variables.continuous_var_names.index(f) for f in self.features]

    def build_polytope_sampler_constraint(self) -> [Tuple[Tensor, Tensor, float]]:
        """

        Function that creates the constraint tuple that is used in the polytope sampler

        """
        return (torch.tensor(self.index), torch.tensor(self.coefficients), self.rhs)

    def build_scipy_constraint(self, add_to_index: int, num_candidates: int) -> Callable:
        """

        Creates the constraint function that is supplied into the scipy minimize function

        Parameters
        ----------
        add_to_index: int
            Offsets the position of the feature to account for its position when more than one candidate is desired per
            iteration from the optimisation. This is offset is required because multiple candidates are supplied to the
            scipy minimize function in a flattened array
        num_candidates: int
            The number of candidates desired per iteration from the optimisation

        Returns
        -------
        constraint_fun: Callable
            Function that can take an X array and is supplied to the scipy minimize function as a constraint

        """
        new_index = [i + add_to_index for i in self.index]

        def constraint_fun(x: np.ndarray) -> np.ndarray:
            # Saves the original shape of the X array
            x_shape = x.shape

            # Reshapes the X array
            x = x.reshape(num_candidates, -1)

            # Un-normalise the variables
            x = (x * (np.array(self.variables.upper_bounds) - np.array(self.variables.lower_bounds))) + np.array(
                self.variables.lower_bounds
            )

            # Re-shape the X array back to the original shape
            x = x.reshape(x_shape)

            # Evaluate the X array for the constraint
            return np.sum(x[new_index] * self.coefficients) - self.rhs

        return constraint_fun

    def evaluate_pymoo_constraint(self, x: np.ndarray) -> np.ndarray:
        """

        Evaluate the X array for the constraint in pymoo

        Parameters
        ----------
        x: np.ndarray
            The X array to be evaluated. Can be more than one row of X-values

        Returns
        -------
        np.ndarray:
            The output value in the array for a given row in the supplied X array will be used by the pymoo package to
            evaluate whether the constraint was met


        """
        # Un-normalise the variables
        x = (x * (np.array(self.variables.upper_bounds) - np.array(self.variables.lower_bounds))) + np.array(
            self.variables.lower_bounds
        )

        # Multiply coefficients and rhs by -1 because pymoo uses the less than or equal to inequality operator for its constraints
        if self.constraint_type == "ineq":
            return np.sum(x[:, self.index] * [-coeff for coeff in self.coefficients], axis=1) - (self.rhs * -1)
        else:
            # an equality constraint can be expressed in this manner by squaring the inequality expression
            # See https://pymoo.org/misc/constraints.html for more details
            return (np.sum(x[:, self.index] * [-coeff for coeff in self.coefficients], axis=1) - (self.rhs * -1)) ** 2

    def bool_evaluate_constraint(self, X: np.ndarray) -> np.ndarray:
        """

        Evaluate whether the constraint is met and returns a boolean array

        Parameters
        ----------
        X: np.ndarray
            The X array to be evaluated that contains the categorical variables in their categorical form (e.g. as
            categorical level names and not as descriptors for CategoricalVariableWithDescriptors)

        Returns
        -------
        np.ndarray:
            A boolean is returned for all rows in the supplied X array that indicates whether the constraint was met

        """
        if self.constraint_type == "ineq":
            return np.around(np.sum(X[:, self.index] * self.coefficients, axis=1), 4) >= round(float(self.rhs), 4)
        else:
            return np.around(np.sum(X[:, self.index] * self.coefficients, axis=1), 4) == round(float(self.rhs), 4)


@define
class NonLinearConstraint:
    """

    Implements a linear constraint on the input variables for the optimisation. For example, linear constraints could be:

        a(F1)^x + b(F2)^y = 0
        a(F1)^x + b(F2)^y >= 0

    where a and b are coefficients, and x and y are powers (exponents) for the features F1 and F2 respectively, and the
    right-hand side of the equation is 0. Using an equals sign, =, would form a linear equality constraint whereas
    defining as 'greater than or equal to' forms an inequality constraint.

    By default in NEMO, all inequality constraints must be defined as 'greater than or equal to'. Note: This aligns
    with how constraints are defined in the scipy package, but is the opposite when compared to the pymoo package

    Parameters
    ----------
    constraint_type: str
        Defines whether the linear constraint should be an equality or inequality linear constraint by assigning as
        either 'eq' or 'ineq' respectively
    variables: VariablesList
        VariablesList object that contains information about all variables
    features: List[str]
        The name of the features to constrain, e.g. ['F1', 'F2'] for the example equation shown above
    coefficients: List[Union[int, float]]
        The coefficient for every features in the constraint. The values in the provided list must be given in
        the same order as the provided features to constrain, e.g. [a, b] for the example equation shown above
    powers: List[int]
        The power (exponent) for every features in the constraint. The values in the provided list must be given in
        the same order as the provided features to constrain, e.g. [x, y] for the example equation shown above
    rhs: Union[int, float]
        The value to set for the right-hand side of the equation, e.g. 0 for the example equation shown above

    """

    constraint_type: str
    variables: VariablesList
    features: List[str]
    coefficients: List[Union[int, float]]
    powers: List[int]
    rhs: Union[int, float]
    index: List[int] = field(init=False)

    def __attrs_post_init__(self):
        self.index = [self.variables.continuous_var_names.index(f) for f in self.features]

    def build_polytope_sampler_constraint(self):
        raise RuntimeError("The polytope sampler cannot be used with non-linear constraints")

    def build_scipy_constraint(self, add_to_index: int, num_candidates: int) -> Callable:
        """

        Creates the constraint function that is supplied into the scipy minimize function

        Parameters
        ----------
        add_to_index: int
            Offsets the position of the feature to account for its position when more than one candidate is desired per
            iteration from the optimisation. This is offset is required because multiple candidates are supplied to the
            scipy minimize function in a flattened array
        num_candidates: int
            The number of candidates desired per iteration from the optimisation

        Returns
        -------
        constraint_fun: Callable
            Function that can take an X array and is supplied to the scipy minimize function as a constraint

        """
        new_index = [i + add_to_index for i in self.index]

        def constraint_fun(x: np.ndarray) -> np.ndarray:
            # Saves the original shape of the X array
            x_shape = x.shape

            # Reshapes the X array
            x = x.reshape(num_candidates, -1)

            # Un-normalise the variables
            x = (x * (np.array(self.variables.upper_bounds) - np.array(self.variables.lower_bounds))) + np.array(
                self.variables.lower_bounds
            )

            # Re-shape the X array back to the original shape
            x = x.reshape(x_shape)

            # Evaluate the X array for the constraint
            lhs_eval_list = []
            for i, c, p in zip(new_index, self.coefficients, self.powers):
                lhs_eval_list.append((((x[i]) ** p) * c))

            return sum(lhs_eval_list) - self.rhs

        return constraint_fun

    def evaluate_pymoo_constraint(self, x: np.ndarray) -> np.ndarray:
        """

        Evaluate the X array for the constraint in pymoo

        Parameters
        ----------
        x: np.ndarray
            The X array to be evaluated. Can be more than one row of X-values

        Returns
        -------
        np.ndarray:
            The output value in the array for a given row in the supplied X array will be used by the pymoo package to
            evaluate whether the constraint was met


        """
        # Un-normalise the variables
        x = (x * (np.array(self.variables.upper_bounds) - np.array(self.variables.lower_bounds))) + np.array(
            self.variables.lower_bounds
        )

        # Multiply coefficients and rhs by -1 because pymoo uses the less than or equal to inequality operator for its constraints
        lhs_eval_list = []
        if self.constraint_type == "ineq":
            for i, c, p in zip(self.index, self.coefficients, self.powers):
                lhs_eval_list.append((((x[:, i]) ** p) * -c))

            return np.sum(lhs_eval_list, axis=0) - (self.rhs * -1)

        else:
            # an equality constraint can be expressed in this manner by squaring the inequality expression
            # See https://pymoo.org/misc/constraints.html for more details
            for i, c, p in zip(self.index, self.coefficients, self.powers):
                lhs_eval_list.append((((x[:, i]) ** p) * -c))

            return (np.sum(lhs_eval_list, axis=0) - (self.rhs * -1)) ** 2

    def bool_evaluate_constraint(self, X: np.ndarray) -> np.ndarray:
        """

        Evaluate whether the constraint is met and returns a boolean array

        Parameters
        ----------
        X: np.ndarray
            The X array to be evaluated that contains the categorical variables in their categorical form (e.g. as
            categorical level names and not as descriptors for CategoricalVariableWithDescriptors)

        Returns
        -------
        np.ndarray:
            A boolean is returned for all rows in the supplied X array that indicates whether the constraint was met

        """
        if self.constraint_type == "ineq":
            return np.around(np.sum(X[:, self.index] * self.coefficients, axis=1), 4) >= round(float(self.rhs), 4)
        else:
            return np.around(np.sum(X[:, self.index] * self.coefficients, axis=1), 4) == round(float(self.rhs), 4)


@define
class MaxActiveFeaturesConstraint:
    """

    Implements a constraint that limits the number of variables/features that have values greater than 0. For example,
    if max_active = 2, the examples 1 and 2 below would pass the constraint whereas example 3 would fail the
    constraint:

        - Example with 4 variables in the X array
        - Only need to consider variables at index 0, 1, 2
        - Ensure that only 2 variables from indexes 0, 1, and 2 are above 0 (max_active = 2)

        1. X = [0.5, 0.7, 0.0, 1.0] -> 2 variables from indexes 0, 1, 2 are above 0 -> Pass
        2. X = [0.5, 0.0, 0.3, 1.0] -> 2 variables from indexes 0, 1, 2 are above 0 -> Pass
        3. X = [0.5, 0.7, 0.3, 1.0] -> 3 variables from indexes 0, 1, 2 are above 0 -> Fail

    Parameters
    ----------
    variables: VariablesList
        VariablesList object that contains information about all variables
    features: List[str]
        The name of the features to consider in the constraint, e.g. ['F1', 'F2']
    max_active: int
        The maximum number of features from the provided names that can be above 0

    """

    variables: VariablesList
    features: List[str]
    max_active: int
    index: List[int] = field(init=False)

    def __attrs_post_init__(self):
        self.index = [self.variables.continuous_var_names.index(f) for f in self.features]

    def build_polytope_sampler_constraint(self):
        raise RuntimeError("The polytope sampler cannot be used with max active number of features constraints")

    def build_scipy_constraint(self, add_to_index: int) -> Callable:
        """

        Creates the constraint function that is supplied into the scipy minimize function

        Parameters
        ----------
        add_to_index: int
            Offsets the position of the feature to account for its position when more than one candidate is desired per
            iteration from the optimisation. This is offset is required because multiple candidates are supplied to the
            scipy minimize function in a flattened array

        Returns
        -------
        constraint_fun: Callable
            Function that can take an X array and is supplied to the scipy minimize function as a constraint

        """
        new_index = [i + add_to_index for i in self.index]

        def constraint_fun(x: np.ndarray) -> np.ndarray:
            # The values in the x array that come from the scipy minimize function need to be normalised between 0 and 1
            # Returns a one where the values are above 0 and zero where they equal 0
            x = np.where(x > 0, 1, 0)

            # Evaluate the one-zero X array for the constraint
            return np.sum(x[new_index] * ([-1] * len(new_index))) - (self.max_active * -1)

        return constraint_fun

    def evaluate_pymoo_constraint(self, x: np.ndarray) -> np.ndarray:
        """

        Evaluate the X array for the constraint in pymoo

        Parameters
        ----------
        x: np.ndarray
            The X array to be evaluated. Can be more than one row of X-values

        Returns
        -------
        np.ndarray:
            The output value in the array for a given row in the supplied X array will be used by the pymoo package to
            evaluate whether the constraint was met


        """
        # The values in the x array that come from pymoo need to be normalised between 0 and 1
        # Multiply coefficients and rhs by -1 because pymoo uses the less than or equal to inequality operator for its constraints
        X = np.where(x > 0, 1, 0)
        return np.sum(X[:, self.index], axis=1) - self.max_active

    def bool_evaluate_constraint(self, X: np.ndarray) -> np.ndarray:
        """

        Evaluate whether the constraint is met and returns a boolean array

        Parameters
        ----------
        X: np.ndarray
            The X array to be evaluated that contains the categorical variables in their categorical form (e.g. as
            categorical level names and not as descriptors for CategoricalVariableWithDescriptors)

        Returns
        -------
        np.ndarray:
            A boolean is returned for all rows in the supplied X array that indicates whether the constraint was met

        """
        X = np.where(X > 0, 1, 0)
        return np.sum(X[:, self.index], axis=1) <= self.max_active


@define
class CategoricalConstraint:
    """

    Implements a constraint that prevents chosen categorical levels (e.g. chemicals) from two variables/features from
    being simultaneously selected. For example, the examples 1 and 2 below would pass the constraint whereas examples
    3 and 4 would fail the constraint:

        - Exampler where variables at indexes 0 and 1 are 'Solvent' and 'Base' respectively
        - In the 'Solvent' variable, the categorical level called 'Water' cannot be selected at the same time as
        categorical levels called 'Sodium' or 'Potassium' in the 'Base' variable

        1. X = ['Water', 'Triethylamine'] -> Pass
        2. X = ['Toluene', 'Sodium'] -> Pass
        3. X = ['Water', 'Sodium'] -> Fail
        4. X = ['Water', 'Potassium'] -> Fail

    Parameters
    ----------
    variables: VariablesList
        VariablesList object that contains information about all variables
    feature1: str
        The name of one of the feature to consider in the constraint, e.g. 'Solvent'
    feature2: str
        The name of the other feature to consider in the constraint, e.g. 'Base'
    categorical_levels1: List[Union[str, int, float]]
        The categorical levels in feature1 that cannot be simultaneously selected with categorical levels in feature2,
        e.g. ['Water']
    categorical_levels2: List[Union[str, int, float]]
        The categorical levels in feature2 that cannot be simultaneously selected with categorical levels in feature1,
        e.g. ['Sodium', 'Potassium']

    """

    variables: VariablesList
    feature1: str
    feature2: str
    categorical_levels1: List[Union[str, int, float]]
    categorical_levels2: List[Union[str, int, float]]
    index: List[int] = field(init=False)

    def __attrs_post_init__(self):
        self.index1 = [self.variables.names.index(self.feature1)]
        self.index2 = [self.variables.names.index(self.feature2)]

    def build_polytope_sampler_constraint(self):
        raise RuntimeError("The polytope sampler cannot be used with categorical constraints")

    def build_scipy_constraint(self, add_to_index: int, num_candidates: int) -> Callable:
        """

        Creates the constraint function that is supplied into the scipy minimize function

        Parameters
        ----------
        add_to_index: int
            Offsets the position of the feature to account for its position when more than one candidate is desired per
            iteration from the optimisation. This is offset is required because multiple candidates are supplied to the
            scipy minimize function in a flattened array

        Returns
        -------
        constraint_fun: Callable
            Function that can take an X array and is supplied to the scipy minimize function as a constraint

        """

        def constraint_fun(x: np.ndarray) -> np.ndarray:
            # Saves the original shape of the X array
            x_shape = x.shape

            # Reshapes the X array
            x = x.reshape(num_candidates, -1)

            # Un-normalise the variables
            x = (x * (np.array(self.variables.upper_bounds) - np.array(self.variables.lower_bounds))) + np.array(
                self.variables.lower_bounds
            )

            # Converts the descriptor values generated by the scipy minimize function into the categorical level that
            # is the closest by Euclidean distance
            x = self.variables.descriptor_to_name(x)

            # Checks if the forbidden categorical levels are in the chosen features
            for row_index, (x1, x2) in enumerate(
                zip(x[:, self.index1 + add_to_index], x[:, self.index2 + add_to_index])
            ):
                if x1 in self.categorical_levels1:
                    x[row_index, self.index1 + add_to_index] = 1
                if x2 in self.categorical_levels2:
                    x[row_index, self.index2 + add_to_index] = 1

            # Re-shape the X array back to the original shape
            x = x.reshape(x_shape)

            # Evaluate the X array for the constraint
            return (x[{self.index1 + add_to_index}] * -1) + (x[{self.index2 + add_to_index}] * -1) - (-1)

        return constraint_fun

    def evaluate_pymoo_constraint(self, x: np.ndarray) -> np.ndarray:
        """

        Evaluate the X array for the constraint in pymoo

        Parameters
        ----------
        x: np.ndarray
            The X array to be evaluated. Can be more than one row of X-values

        Returns
        -------
        np.ndarray:
            The output value in the array for a given row in the supplied X array will be used by the pymoo package to
            evaluate whether the constraint was met


        """
        # Un-normalise the variables
        x = (x * (np.array(self.variables.upper_bounds) - np.array(self.variables.lower_bounds))) + np.array(
            self.variables.lower_bounds
        )

        # Converts the descriptor values generated by the scipy minimize function into the categorical level that
        # is the closest by Euclidean distance
        x = self.variables.descriptor_to_name(x)

        # Checks if the forbidden categorical levels are in the chosen features
        for row_index, (x1, x2) in enumerate(zip(x[:, self.index1], x[:, self.index2])):
            if x1 in self.categorical_levels1:
                x[row_index, self.index1] = 1
            if x2 in self.categorical_levels2:
                x[row_index, self.index2] = 1

        return np.sum(x[:, [self.index1, self.index2]], axis=1) - 1

    def bool_evaluate_constraint(self, X: np.ndarray) -> np.ndarray:
        """

        Evaluate whether the constraint is met and returns a boolean array

        Parameters
        ----------
        X: np.ndarray
            The X array to be evaluated that contains the categorical variables in their categorical form (e.g. as
            categorical level names and not as descriptors for CategoricalVariableWithDescriptors)

        Returns
        -------
        np.ndarray:
            A boolean is returned for all rows in the supplied X array that indicates whether the constraint was met

        """
        # Checks if the forbidden categorical levels are in the chosen features
        for row_index, (x1, x2) in enumerate(zip(X[:, self.index1], X[:, self.index2])):
            if x1 in self.categorical_levels1:
                X[row_index, self.index1] = 1
            if x2 in self.categorical_levels2:
                X[row_index, self.index2] = 1

        return np.sum((X[:, [self.index1, self.index2]]), axis=1) <= 1


@define
class ConstraintsList:
    """

    Class that contains information and functions for all constraints

    Parameters
    ----------
    constraints: List[Union[LinearConstraint, NonLinearConstraint, MaxActiveFeaturesConstraint, CategoricalConstraint]]
        List of all constraints

    """

    constraints: List[Union[LinearConstraint, NonLinearConstraint, MaxActiveFeaturesConstraint, CategoricalConstraint]]
    n_constr: int = field(init=False)
    variables: VariablesList = field(init=False)

    def __attrs_post_init__(self):
        self.n_constr = len(self.constraints)
        self.variables = self.constraints[0].variables

    def create_scipy_constraints(self, num_candidates: int) -> List[Tuple[Tensor, Tensor, float]]:
        """

        Creates the constraint functions that are supplied into the scipy minimize function for all constraints

        Parameters
        ----------
        add_to_index: int
            Offsets the position of the feature to account for its position when more than one candidate is desired per
            iteration from the optimisation. This is offset is required because multiple candidates are supplied to the
            scipy minimize function in a flattened array

        Returns
        -------
        scipy_constraints: Callable
            Function that can take an X array and is supplied to the scipy minimize function as a constraint

        """
        scipy_constraints = []
        for constr in self.constraints:
            for candidate_number in range(num_candidates):
                if not isinstance(constr, CategoricalConstraint):
                    add_to_index = candidate_number * constr.variables.n_var
                else:
                    add_to_index = candidate_number * len(constr.variables.variables)
                scipy_constraints.append(
                    {
                        "type": constr.constraint_type,
                        "fun": constr.build_scipy_constraint(add_to_index, num_candidates)
                        if not isinstance(constr, MaxActiveFeaturesConstraint)
                        else constr.build_scipy_constraint(add_to_index),
                    }
                )

        return scipy_constraints

    def bool_evaluate_constraints(self, X: np.ndarray) -> np.ndarray:
        """

        Evaluate whether all constraints are met and returns a boolean array

        Parameters
        ----------
        X: np.ndarray
            The X array to be evaluated that contains the categorical variables as their categorical level names and
            not as descriptors for CategoricalVariableWithDescriptors and/or as their discrete values for
            CategoricalVariableDiscreteValues

        Returns
        -------
        np.ndarray:
            A boolean is returned for all rows in the supplied X array that indicates whether the constraint was met

        """
        # Ensures that the X array is in its numerical form with descriptors if any CategoricalVariableWithDescriptors
        # or CategoricalVariableDiscreteValues variables are present.
        if self.variables.num_cat_var > 0:
            X = self.variables.categorical_transform(X)

        pass_fail = np.zeros((X.shape[0], self.n_constr))
        for constr_index, constr in enumerate(self.constraints):
            if not isinstance(constr, CategoricalConstraint):
                pass_fail[:, constr_index] = constr.bool_evaluate_constraint(X)
            else:
                # CategoricalConstraint requires all descriptors that are part of CategoricalVariableWithDescriptors
                # variables to be converted to their categorical level name
                pass_fail[:, constr_index] = constr.bool_evaluate_constraint(self.variables.descriptor_to_name(X))

        return np.all(pass_fail, axis=1)
