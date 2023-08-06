# This Expected Hypervolume Improvement acquisition function code was copied and adapted from the BoTorch package
# M. Balandat, B. Karrer, D. R. Jiang, S. Daulton, B. Letham, A. G. Wilson, and E. Bakshy. BoTorch: A Framework for
# Efficient Monte-Carlo Bayesian Optimization. Advances in Neural Information Processing Systems 33, 2020.
# http://arxiv.org/abs/1910.06403
# https://github.com/pytorch/botorch
# https://botorch.org/

from itertools import product

import torch
from botorch.utils.multi_objective.box_decompositions.non_dominated import FastNondominatedPartitioning
from torch import Tensor
from torch.distributions import Normal


class ExpectedHypervolumeImprovement:
    """

    Class for the Expected Hypervolume Improvement acquisition function adapted from the BoTorch package

    """

    def __init__(self, ref_point: Tensor, Y: Tensor):
        self.ref_point = ref_point
        self.partitioning = FastNondominatedPartitioning(ref_point=self.ref_point, Y=Y,)

        cell_bounds = self.partitioning.get_hypercell_bounds()
        self.cell_lower_bounds = cell_bounds[0]
        self.cell_upper_bounds = cell_bounds[1]

        self._cross_product_indices = torch.tensor(
            list(product(*[[0, 1] for _ in range(ref_point.shape[0])])), dtype=torch.long, device=ref_point.device,
        )

    def psi(self, lower: Tensor, upper: Tensor, mu: Tensor, sigma: Tensor) -> Tensor:
        u = (upper - mu) / sigma
        return sigma * Normal(0, 1).log_prob(u).exp() + (mu - lower) * (1 - Normal(0, 1).cdf(u))

    def nu(self, lower: Tensor, upper: Tensor, mu: Tensor, sigma: Tensor) -> Tensor:
        return (upper - lower) * (1 - Normal(0, 1).cdf((upper - mu) / sigma))

    def ehvi_calc(self, Y_new: Tensor, Y_new_stddev: Tensor) -> Tensor:
        # Reshaped to batch_size number of rows in the tensors
        Y_new = Y_new.reshape(Y_new.shape[0], 1, Y_new.shape[1])
        Y_new_stddev = Y_new_stddev.reshape(Y_new_stddev.shape[0], 1, Y_new_stddev.shape[1])

        cell_upper_bounds = self.cell_upper_bounds.clamp_max(1e10 if Y_new.dtype == torch.double else 1e8)

        psi_lu = self.psi(lower=self.cell_lower_bounds, upper=cell_upper_bounds, mu=Y_new, sigma=Y_new_stddev,)
        psi_ll = self.psi(lower=self.cell_lower_bounds, upper=self.cell_lower_bounds, mu=Y_new, sigma=Y_new_stddev,)

        nu = self.nu(lower=self.cell_lower_bounds, upper=cell_upper_bounds, mu=Y_new, sigma=Y_new_stddev,)

        psi_diff = psi_ll - psi_lu

        stacked_factors = torch.stack([psi_diff, nu], dim=-2)

        all_factors_up_to_last = stacked_factors.gather(
            dim=-2,
            index=self._cross_product_indices.expand(stacked_factors.shape[:-2] + self._cross_product_indices.shape),
        )

        return all_factors_up_to_last.prod(dim=-1).sum()
