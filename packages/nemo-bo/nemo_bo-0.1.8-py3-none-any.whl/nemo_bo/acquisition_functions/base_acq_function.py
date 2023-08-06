import os
from dataclasses import dataclass
from typing import Dict, List

import numpy as np

import nemo_bo.utils.logger as logging_nemo

try:
    logging_nemo.logging_path
    logger = logging_nemo.logging_nemo_child(os.path.basename(__file__))
except AttributeError:
    logger = logging_nemo.logging_nemo_master(os.path.basename(__file__))


@dataclass
class AcquisitionFunction:
    """

    Base class for acquisition functions that should be inherited from

    """

    def build_ref_point(self, max_bool_dict: Dict[str, bool]) -> List[float]:
        """

        Function that creates the normalised reference point for hypervolumne calculations

        Parameters
        ----------
        max_bool_dict: Dict[str, bool]
            A dictionary where the keys are the objective names and the values are whether the objective is to be
            maximised (True) or minimised (False)

        """
        ref_point = []
        hv_obj_minmax = np.array([[-0.01, 1.01] for _ in enumerate(max_bool_dict)])
        for obj_index, obj in enumerate(max_bool_dict):
            if max_bool_dict[obj]:
                ref_point.append(hv_obj_minmax[obj_index][0])
            else:
                ref_point.append(hv_obj_minmax[obj_index][1] * -1)

        return ref_point

    def Y_norm_minmax_transform(self, Y: np.ndarray, bounds: np.ndarray, max_bool_dict: Dict[str, bool]) -> np.ndarray:
        """

        Function that min-max normalisation transforms the objective values and multiplies by -1 for minimising
        objectives

        Parameters
        ----------
        Y: np.ndarray
            Y array to be transformed
        bounds: np.ndarray

        max_bool_dict: Dict[str, bool]
            A dictionary where the keys are the objective names and the values are whether the objective is to be
            maximised (True) or minimised (False)

        Returns
        -------
        sign_adjusted_Y: np.ndarray
            Transformed Y array

        """
        # Transforms Y using min_max normalisation
        sign_adjusted_Y = np.zeros_like(Y)
        for obj_index, obj in enumerate(max_bool_dict):
            if Y.ndim > 1:
                sign_adjusted_Y[:, obj_index] = (Y[:, obj_index] - bounds[obj_index, 0]) / (
                    bounds[obj_index, 1] - bounds[obj_index, 0]
                )

                # To determine the pareto front, maximising objective values are left unchanged and minimising
                # objective values are multiplied by -1
                if not max_bool_dict[obj]:
                    sign_adjusted_Y[:, obj_index] *= -1
            else:
                sign_adjusted_Y[obj_index] = (Y[obj_index] - bounds[obj_index, 0]) / (
                    bounds[obj_index, 1] - bounds[obj_index, 0]
                )

                # To determine the pareto front, maximising objective values are left unchanged and minimising
                # objective values are multiplied by -1
                if not max_bool_dict[obj]:
                    sign_adjusted_Y[obj_index] *= -1

        return sign_adjusted_Y
