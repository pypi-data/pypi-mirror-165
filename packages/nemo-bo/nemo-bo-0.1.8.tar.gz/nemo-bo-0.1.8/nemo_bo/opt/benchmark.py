import os
from attrs import define, field
from typing import Optional, Tuple

import numpy as np
import torch

from botorch.test_functions.synthetic import (
    Ackley,
    DixonPrice,
    Griewank,
    Levy,
    Michalewicz,
    Rastrigin,
    Rosenbrock,
    StyblinskiTang,
)

import nemo_bo.utils.logger as logging_nemo
from nemo_bo.opt.objectives import CalculableObjective, ObjectivesList, RegressionObjective
from nemo_bo.opt.variables import VariablesList

try:
    logging_nemo.logging_path
    logger = logging_nemo.logging_nemo_child(os.path.basename(__file__))
except AttributeError:
    logger = logging_nemo.logging_nemo_master(os.path.basename(__file__))


@define
class Benchmark:
    """

    Benchmark functions are typically used to simulate the outcomes of experiments in a closed-loop manner and therefore
    can be helpful to evaluate the quality of an optimisation (inferred from the effectiveness of the utilised ML
    model(s) and/or acquisition function to identify the optimum)

    Parameters
    ----------
    variables: VariablesList
        VariablesList object that contains information about all variables
    objectives: ObjectivesList
        ObjectivesList object that contains information about all objectives

    """

    def evaluate(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """

        Returns the corresponding output values and standard deviations using the inputted X array and benchmark method

        Parameters
        ----------
        X: np.ndarray,
            X array that contains the unprocessed variables data to be used in the prediction, i.e. The data has not
            yet undergone any transformations related to converted categorical variables to their respective
            descriptors or transformations related to standardisation/normalisation

        """
        pass


class SyntheticBenchmark:
    """

    Adopts the following synthetic functions from the BoTorch package to use as functions in a benchmark. The
    recommended bounds for each dimension is shown in parentheses:

    1. Ackley (-32.768, 32.768)
    2. DixonPrice (-10.0, 10.0)
    3. Griewank (-600.0, 600.0)
    4. Levy (-10.0, 10.0)
    5. Michalewicz (0.0, math.pi)
    6. Rastrigin (-5.12, 5.12)
    7. Rosenbrock (-5.0, 10.0)
    8. StyblinskiTang (-5.0, 5.0)

    Parameters
    ----------
    function_name: str
        The name of the synthetic function to use ('ackley', 'dixon-price', 'griewank', 'levy', 'michalewicz',
        'rastrigin', 'rosenbrock', or 'styblinski-tang')
    dim: int
        The number of input dimensions
    noise_std: float = None
        Standard deviation of the observation noise

    """

    def __init__(self, function_name: str, dim: int, noise_std: Optional[float] = None):
        if function_name == "ackley":
            self.synthetic_function = Ackley(dim=dim, noise_std=noise_std)
        if function_name == "dixon-price":
            self.synthetic_function = DixonPrice(dim=dim, noise_std=noise_std)
        if function_name == "griewank":
            self.synthetic_function = Griewank(dim=dim, noise_std=noise_std)
        if function_name == "levy":
            self.synthetic_function = Levy(dim=dim, noise_std=noise_std)
        if function_name == "michalewicz":
            self.synthetic_function = Michalewicz(dim=dim, noise_std=noise_std)
        if function_name == "rastrigin":
            self.synthetic_function = Rastrigin(dim=dim, noise_std=noise_std)
        if function_name == "rosenbrock":
            self.synthetic_function = Rosenbrock(dim=dim, noise_std=noise_std)
        if function_name == "styblinski-tang":
            self.synthetic_function = StyblinskiTang(dim=dim, noise_std=noise_std)

        self.fitted = True

    def evaluate(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """

        Calculate the corresponding output values using the desired synthetic function and the inputted X array

        Parameters
        ----------
        X: np.ndarray
            X array that contains only numerical data

        """
        Y = self.synthetic_function.evaluate_true(torch.tensor(X)).cpu().detach().numpy()

        return Y, np.zeros_like(Y)


@define
class ModelBenchmark(Benchmark):
    """

    This type of benchmark object is used to accurately predict the outcome of optimisation suggestions as they typically
    utilise all available data for regression objectives. This method will also work for the calculable objectives in
    the optimisation problem.

    Parameters
    ----------
    variables: VariablesList
        VariablesList object that contains information about all variables
    objectives: ObjectivesList
        ObjectivesList object that contains information about all objectives

    """

    variables: VariablesList
    objectives: ObjectivesList
    fitted: bool = field(init=False)

    def __attrs_post_init__(self):
        self.fitted = False

    def fit(self, X: np.ndarray, Y: np.ndarray, test_ratio: float = 0.2, **kwargs) -> None:
        """

        Fits ML models for all specified regression objectives to be used a benchmark functions

        Parameters
        ----------
        X: np.ndarray,
            X array that contains the unprocessed variables data to be fitted to the model, i.e. The data has not yet
            undergone any transformations related to converted categorical variables to their respective descriptors
            or transformations related to standardisation/normalisation
        Y: np.ndarray,
            Y array that contains the unprocessed objective data for all calculable and regression objectives, i.e.
            The data has not yet undergone any transformations related to standardisation/normalisation
        test_ratio: float
            The proportion of inputted X and Y arrays to be split for the validation set where applicable

        """
        logger.info(
            "Performing hyperparameter and model search for the best predictor models for use as benchmarkers for the regression objectives"
        )

        # Fit the ML regression models
        self.objectives.fit(
            X, Y, self.variables, model_search_bool=True, test_ratio=test_ratio, **kwargs,
        )
        self.fitted = True

        logger.info(
            f"Identified the best predictor models and hyperparameters for the benchmarkers for the regression objectives"
        )

    def evaluate(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """

        Returns the corresponding output values and standard deviations using the inputted X array and benchmark models
        and calculable objectives

        Parameters
        ----------
        X: np.ndarray,
            X array that contains the unprocessed variables data to be used in the prediction, i.e. The data has not
            yet undergone any transformations related to converted categorical variables to their respective
            descriptors or transformations related to standardisation/normalisation

        Returns
        ----------
        Y: np.ndarray
            Complete Y array of output values from all calculable and regression objectives using the provided
            X array
        Y_pred_stddev: np.ndarray
            Complete array of corresponding standard deviations for the predicted Y-values of all calculable and
            regression objectives using the provided X array

        """
        Y = np.zeros((X.shape[0], self.objectives.n_obj), dtype=np.float64)
        Y_stddev = np.zeros_like(Y)
        for obj_index, obj in enumerate(self.objectives.objectives):
            if isinstance(obj, RegressionObjective):
                Y[:, obj_index], Y_stddev[:, obj_index] = obj.predict(X)
            elif isinstance(obj, CalculableObjective):
                Y[:, obj_index], Y_stddev[:, obj_index] = obj.calculate(X)

        return Y.astype("float"), Y_stddev.astype("float")
