from dataclasses import dataclass
from typing import Dict, List, Union

import numpy as np
from pymoo.core.problem import Problem

from nemo_bo.opt.constraints import ConstraintsList
from nemo_bo.opt.objectives import ObjectivesList
from nemo_bo.opt.variables import VariablesList


@dataclass
class NSGAProblemWrapper(Problem):
    """

    Class for defining a problem for the minimise function in NSGA-based methods

    Parameters
    ----------
    xl: int | float | List[int | float]
        Lower bounds for the variables for the NSGA algorithm. If integer, all lower bounds are equal to the integer value
    xu: int | float | List[int | float]
        Upper bounds for the variables for the NSGA algorithm. If integer, all upper bounds are equal to the integer value
    variables: VariablesList
        VariablesList object that contains information about all variables
    objectives: ObjectivesList
        ObjectivesList object that contains information about all objectives
    constraints: ConstraintsList
        ConstraintsList object that contains information about all constraints

    """

    def __init__(
        self,
        xl: Union[int, float, List[Union[int, float]]],
        xu: Union[int, float, List[Union[int, float]]],
        variables: VariablesList,
        objectives: ObjectivesList,
        constraints: ConstraintsList,
    ):
        self.variables = variables
        self.objectives = objectives
        self.constraints = constraints

        n_constr = self.constraints.n_constr if constraints is not None else 0

        super().__init__(
            n_var=self.variables.n_var, n_obj=self.objectives.n_obj, n_constr=n_constr, xl=xl, xu=xu,
        )

    def _evaluate(self, X: np.ndarray, out: Dict[str, np.ndarray], **kwargs) -> None:
        """

        Function to calculate the objective(s) and constraint(s) (if any) values

        Parameters
        ----------
        X: np.ndarray
            NSGA generated candidates' X-values
        out: Dict[str, np.ndarray]
            Contains the objective(s) and constraint(s) (if any) values for the generated candidates

        """
        X = (X * (np.array(self.variables.upper_bounds) - np.array(self.variables.lower_bounds))) + np.array(
            self.variables.lower_bounds
        )

        if self.variables.num_cat_descriptor_var > 0:
            F, _ = self.objectives.evaluate(self.variables.descriptor_to_name(X))
        else:
            F, _ = self.objectives.evaluate(X)

        for obj_index, obj in enumerate(self.objectives.max_bool_dict):
            if self.objectives.max_bool_dict[obj]:
                F[:, obj_index] *= -1
        out["F"] = F

        if self.n_constr > 0:
            # Min-max normalises the X array
            X = (X - np.array(self.variables.lower_bounds)) / (
                np.array(self.variables.upper_bounds) - np.array(self.variables.lower_bounds)
            )
            G = np.zeros((X.shape[0], self.n_constr))
            for index, constr in enumerate(self.constraints.constraints):
                G[:, index] = constr.evaluate_pymoo_constraint(X)
            out["G"] = G
