from __future__ import annotations

import copy
import os
from functools import partial
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Tuple

import gpytorch
import numpy as np
import torch
from gpytorch.distributions import MultivariateNormal
from gpytorch.kernels import AdditiveStructureKernel, Kernel, MaternKernel, ScaleKernel
from gpytorch.likelihoods import GaussianLikelihood, Likelihood
from gpytorch.means import ConstantMean
from gpytorch.models import ExactGP
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe
from hyperopt.pyll.base import Literal
from torch import Tensor

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


class ExactGPModel(ExactGP):
    """

    Defines the GP model and forward function for regression. Details about the parameters can be found within the
    GPyTorch package documentation

    """

    def __init__(self, trainX: Tensor, trainY: Tensor, likelihood: Likelihood, kernel: Kernel):
        super(ExactGPModel, self).__init__(trainX, trainY, likelihood)
        self.mean_module = ConstantMean()
        self.covar_module = kernel

    def forward(self, x: Tensor) -> MultivariateNormal:
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        return MultivariateNormal(mean_x, covar_x)


class GPModel(Base_Model):
    """

    Used to create a GP model for the RegressionObjective

    See docstring for Base_Model __init__ function for information

    """

    def __init__(
        self, variables: VariablesList, objective: RegressionObjective, always_hyperparam_opt: bool = True, **kwargs
    ):
        super().__init__(variables, objective, always_hyperparam_opt)
        self.default_X_transform_type = "normalisation"
        self.default_Y_transform_type = "standardisation"
        self.include_validation = False
        self.name = "gp"

    def fit(self, X: np.ndarray, Y: np.ndarray, **params) -> None:
        """

        Function that is called to start the GP model fitting procedure

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

        Called by the fit and cv-related functions for fitting the GP model using pre-processed X and Y training data
        in the class instance

        """
        X_tensor = torch.tensor(self.X_train, device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu"),)
        Y_tensor = torch.tensor(
            self.Y_train, device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu"),
        ).flatten()

        self.n_iterations = int(params.get("n_iterations", 50))
        self.kernel = params.get("kernel", ScaleKernel(MaternKernel(nu=2.5)))

        self.likelihood = GaussianLikelihood()
        self.model = ExactGPModel(X_tensor, Y_tensor, self.likelihood, copy.deepcopy(self.kernel))
        if torch.cuda.is_available():
            self.likelihood = self.likelihood.to("cuda")
            self.model = self.model.to("cuda")

        self.model.train()
        self.likelihood.train()

        self.optimizer = torch.optim.Adam(self.model.parameters())

        mll = gpytorch.mlls.ExactMarginalLogLikelihood(self.likelihood, self.model)

        for i in range(self.n_iterations):
            self.optimizer.zero_grad()
            output = self.model(X_tensor)
            mll_loss = -mll(output, Y_tensor).sum()
            mll_loss.backward()
            self.optimizer.step()

        self.model.eval()
        self.likelihood.eval()

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

        # Split to reduce memory requirements. I think this is not ideal for the quality of the prediction but it helps
        # to prevent crashing caused by memory limitations when the X array is too large
        split_size = 50000
        X_split = np.split(X, np.array((range(1, int(X.shape[0] / split_size) + 1))) * split_size)
        observed_Y_pred_list = []
        for X_split_each in X_split:
            if X_split_each.shape[0] == 0:
                continue
            with torch.no_grad():
                observed_Y_pred = self.likelihood(
                    self.model(
                        torch.tensor(
                            X_split_each, device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu"),
                        )
                    )
                )
            observed_Y_pred_list.append(observed_Y_pred)

        Y_pred = np.hstack([observed_Y_pred.mean.cpu().detach().numpy() for observed_Y_pred in observed_Y_pred_list])
        Y_pred_upper = np.hstack(
            [observed_Y_pred.confidence_region()[1].cpu().detach().numpy() for observed_Y_pred in observed_Y_pred_list]
        )

        Y_pred = self.objective.inverse_transform(Y_pred)
        Y_pred_upper = self.objective.inverse_transform(Y_pred_upper)
        Y_pred_stddev = (np.subtract(Y_pred_upper, Y_pred)) / 1.96

        return Y_pred.flatten(), Y_pred_stddev.flatten()

    @staticmethod
    def default_params(n_var: int, gp_kernel_choices: Optional[List[Kernel]] = None) -> Dict[str, Any]:
        """

        Function that returns the default hyperparameters to use for the hyperparameter optimisation of GP models
        using the hyperopt package. Returns a dictionary that is used for the space argument in the hyperopt.fmin
        function

        Parameters
        ----------
        n_var: int
            Number of continuous variables
        gp_kernel_choices: List[Kernel], Default = None
            The types of kernels to use for the GP hyperparameter optimisation

        """
        if gp_kernel_choices is None:
            gp_kernel_choices = [
                AdditiveStructureKernel(
                    base_kernel=ScaleKernel(MaternKernel(ard_num_dims=n_var, nu=0.5)), num_dims=n_var,
                ),
                AdditiveStructureKernel(
                    base_kernel=ScaleKernel(MaternKernel(ard_num_dims=n_var, nu=1.5)), num_dims=n_var,
                ),
                AdditiveStructureKernel(
                    base_kernel=ScaleKernel(MaternKernel(ard_num_dims=n_var, nu=2.5)), num_dims=n_var,
                ),
                ScaleKernel(MaternKernel(nu=0.5, ard_num_dims=n_var)),
                ScaleKernel(MaternKernel(nu=1.5, ard_num_dims=n_var)),
                ScaleKernel(MaternKernel(nu=2.5, ard_num_dims=n_var)),
            ]
        return {
            "n_iterations": hp.quniform("n_iterations", 5, 500, 1),
            "kernel": hp.choice("kernel", gp_kernel_choices),
        }

    def hyperparam_opt(
        self,
        X: np.ndarray,
        Y: np.ndarray,
        test_ratio: float,
        predictor_params_dict: Optional[Dict[str, Dict[str, Callable]]] = None,
        gp_kernel_choices: Optional[list] = None,
        **kwargs,
    ) -> Tuple[GPModel, Dict[str, Any]]:
        """

        Function to be called for performing hyperparameter optimisation for GP models using the hyperopt package.
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
        predictor_params_dict: Dict[str, Dict[str, Callable]], Default = None
            Dictionary with a key 'gp' and a corresponding value that is a dictionary that is used for the space
            argument in the hyperopt.fmin function
        gp_kernel_choices: List[Kernel], Default = None
            The types of kernels to use for the GP hyperparameter optimisation

        Returns
        -------
        model: GPModel
            The model fitted with the best hyperparameters found using the hyperopt package

        model_params: Dict[str, Any]
            Dictionary containing the best hyperparameters found using the hyperopt package

        """
        if predictor_params_dict is None:
            predictor_params_dict = self.default_params(self.variables.n_var, gp_kernel_choices)
        else:
            predictor_params_dict = predictor_params_dict.get(
                self.name, self.default_params(self.variables.n_var, gp_kernel_choices)
            )

        if self.objective.hyperopt_evals is None:
            hyperopt_evals = 1
        else:
            hyperopt_evals = self.objective.hyperopt_evals.get(self.name, 1)
        # if self.objective.hyperopt_evals is None:
        #     hyperopt_evals = 40
        # else:
        #     hyperopt_evals = self.objective.hyperopt_evals.get(f"{self.name}", 40)

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

        # HyperOpt returns an integer for the best GP kernel. This sets it to the actual kernel.
        gp_kernel_choices = [i.obj for i in predictor_params_dict["kernel"].pos_args if isinstance(i, Literal)]
        model_params["kernel"] = gp_kernel_choices[model_params["kernel"]]

        model = self.new_instance(self.__class__, **kwargs)
        model.fit(X, Y, test_ratio=test_ratio, **model_params, **kwargs)

        logger.info(f"Completed hyperparameter opt")
        return model, model_params
