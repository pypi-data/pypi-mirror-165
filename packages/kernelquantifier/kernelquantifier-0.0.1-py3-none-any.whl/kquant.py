# -*- coding: utf-8 -*-

"""
@author: Dussap Bastien
This .py contains the KernelQuantifier with and without RFF
Code inspired by QuaPy : https://github.com/HLT-ISTI/QuaPy
"""

import numpy as np
import torch

from typing import Union
from cvxopt import matrix, solvers


from .rff import GaussianRFF, bandwidthRFF
from .data import LabelledCollection
from .base import BaseQuantifier
from .utils import choose_device
from .kernel import GaussianKernel, bandwidth_kernel


class KernelQuantifierRFF(BaseQuantifier):
    """
    KernelQuantifier without RFF.
    """

    def __init__(self, kernel: str = "gaussian"):
        """
        Kernel [str] : "gaussian"
        device [torch.device] : device
        """

        self.kernel_ = kernel

        assert self.kernel_ == "gaussian", "No other kernel implemented yet"

    def fit(self,
            data: LabelledCollection,
            sigma: Union[float, list],
            verbose: bool,
            number_rff: int) -> None:
        """
        data [.data.LabelledCollection] : the Source data
        sigma : Give a list of two elements to use the criteron to find the best sigma inside the interval.
        verbose [bool] : plot the function eigmin(P) w.r.t bandwidth
        number_rff [int] : The number of RFF

        --------

        The fit function stock the mu(P_i) and the kernel.
        """

        self.device_ = data.device
        self.n_points_ = data.n_points
        self.n_classes_ = data.n_classes

        # First we choose the kernel
        if isinstance(sigma, list):
            sigma = bandwidthRFF(P=data,
                                 sigma_min=sigma[0],
                                 sigma_max=sigma[1],
                                 kernel=GaussianRFF,
                                 verbose=verbose,
                                 device=self.device_,
                                 number_rff=number_rff)

        self.kernel = GaussianRFF(
            D=number_rff, d=data.dim, sigma=sigma, device=self.device_)

        # Then, compute mu(P_i) with this kernel
        self.mu_ = [self.kernel.fit(data[i]) for i in range(data.n_classes)]
        self.mu_ = torch.stack(self.mu_, axis=1).float()

    def refit(self, data: LabelledCollection):
        """
        Refit the mu on the data.

        Args:
            data (LabelledCollection): Data
        """
        self.mu_ = [self.kernel.fit(data[i])  for i in range(data.n_classes)]
        self.mu_ = torch.stack(self.mu_, axis=1).float()

    def quantify(self, data: LabelledCollection, target: torch.tensor) -> np.array:
        """

        Args:
            data [LabelledCollection] : Source
            target [torch.tensor] : the target distribution

        -----------------

        return : np.array (self.n_classes_) containing the estimate prop of the target.
        """
        def torch_to_matrix(tensor):
            tensor = tensor.cpu()
            return matrix(np.array(tensor).astype(np.double))

        b = self.kernel.fit(target)
        n = self.n_points_

        P = torch_to_matrix(2*n/(n-1)*self.mu_.T @ self.mu_)
        q = torch_to_matrix(-2 * self.mu_.T @ b)
        # constraint
        G = matrix(-np.eye(self.n_classes_))
        h = matrix(np.zeros(self.n_classes_))
        A = matrix(np.ones(self.n_classes_)).T
        b = matrix([1.0])

        solvers.options['show_progress'] = False
        sol = solvers.qp(P, q, G, h, A, b)

        self.props_ = np.array(sol["x"]).reshape(self.n_classes_)
        return self.props_

    def get_kl(self, pi_target: np.array) -> np.array:
        return super().get_kl(pi_target)

    @property
    def sigma(self):
        return self.kernel.sigma

############################################################################################


class KernelQuantifier(BaseQuantifier):
    """
    KernelQuantifier without RFF.
    """

    def __init__(self, kernel: str = "gaussian"):
        """
        Kernel [str] : "gaussian"
        """

        self.kernel_ = kernel

        assert self.kernel_ == "gaussian", "No other kernel implemented yet"

    def fit(self, data: LabelledCollection,
            sigma: Union[float, list], verbose: bool = False) -> None:
        """
        data [KMPE.data.LabelledCollection] : the Source data
        sigma :
        verbose [bool] : plot the function eigmin(P) w.r.t bandwidth

        --------

        The fit function stock the kernel and the matrix A.
        """

        self.device_ = data.device
        self.n_points_ = data.n_points
        self.n_classes_ = data.n_classes

        # First we choose the kernel
        if isinstance(sigma, list):
            sigma = bandwidth_kernel(P=data,
                                     sigma_min=sigma[0],
                                     sigma_max=sigma[1],
                                     kernel=GaussianKernel,
                                     verbose=verbose)

        self.kernel = GaussianKernel(sigma=float(sigma))
        self.A = self.kernel.fit_X(data)

    def quantify(self, data: LabelledCollection, target: torch.tensor) -> np.array:
        """
        Generate class prevalence estimates for the sample's target
        :param target: torch.tensor
        :return: `np.ndarray` of shape `(self.n_classes_)` with class prevalence estimates.
        """

        def torch_to_matrix(tensor):
            tensor = tensor.cpu()
            return matrix(np.array(tensor).astype(np.double))

        q = self.kernel.fit_Xy(data, target)

        P = torch_to_matrix(2*self.A)
        q = torch_to_matrix(-2 * q)
        G = matrix(-np.eye(self.n_classes_))
        h = matrix(np.zeros(self.n_classes_))
        A = matrix(np.ones(self.n_classes_)).T
        b = matrix([1.0])

        solvers.options['show_progress'] = False
        sol = solvers.qp(P, q, G, h, A, b)

        self.props_ = np.array(sol["x"]).reshape(self.n_classes_)
        return self.props_

    def get_kl(self, pi_target: np.array) -> np.array:
        return super().get_kl(pi_target)
