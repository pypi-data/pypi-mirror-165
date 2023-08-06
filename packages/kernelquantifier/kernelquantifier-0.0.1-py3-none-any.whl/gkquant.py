# -*- coding: utf-8 -*-

"""
@author: Dussap Bastien
This .py contains the Generative Kernel Quantifier (GKQuant)
"""

import torch
import numpy as np

from torch.optim import Adam
from tqdm import tqdm
from typing import Union
from cvxopt import matrix, solvers

from .base import BaseQuantifier
from .utils import KL_divergence
from .rff import GaussianRFF, bandwidthRFF
from .data import LabelledCollection


class GenerativeKernelQuantifier(BaseQuantifier):
    """
    GenerativeKernelQuantifier.
    """

    def __init__(self,
                 kernel: str,
                 generator: torch.nn.Module):
        """
        Kernel [str] : For the moment oly gaussian kernel is supported
        generator [torch.nn.Module] : the nn to use.
        """

        assert kernel == 'gaussian', "Only Gaussian is implemented yet"

        self._kernel = kernel
        self.generator = generator

    def fit(self, data: LabelledCollection,
            sigma: Union[float, list],
            verbose: bool = False,
            number_rff: int = 1000) -> None:
        """
        data [.data.LabelledCollection] : the Source data
        sigma : Give a list of two elements to use the criteron to find the best sigma inside the interval.
        verbose [bool] : Plot the function eigmin(P) w.r.t bandwidth
        number_rff [int] : The number of RFF

        --------

        The fit function stock the KernelQuantifier.
        """

        self.n_points_ = data.n_points
        self.n_classes_ = data.n_classes
        self.device_ = data.device
        self.number_rff = number_rff
        self.generator = self.generator.to(self.device_)

        # First we choose the kernel
        if isinstance(sigma, list):
            sigma = bandwidthRFF(P=data,
                                 sigma_min=sigma[0],
                                 sigma_max=sigma[1],
                                 kernel=GaussianRFF,
                                 verbose=verbose,
                                 device=self.device_,
                                 number_rff=number_rff)

        self.kernel = GaussianRFF(D=number_rff,
                                  d=data.dim,
                                  sigma=float(sigma),
                                  device=self.device_)

    def quantify(self,
                 source: LabelledCollection,
                 target: torch.tensor,
                 initial_prop: Union[np.array, None] = None,
                 n_epoch: int = 20,
                 n_epochGM: int = 200,
                 lr: float = 0.1,
                 verbose: bool = False) -> np.array:
        """
        Quantify.
        Args:
            data (LabelledCollection): Source
            target (torch.tensor): target
            initial_prop (np.array | None, optional): If None, one step of KernelQuantifier will be used. Defaults to None.
            n_epoch (int, optional): number of epoch. Defaults to 20.
            n_epochGM (int, optional): number of epoch for the gen. Defaults to 200.
            lr (float, optional): learning rate of Adam. Defaults to 0.1.
            verbose (bool, optional) : Defaults to False

        Returns:
            np.array: Estimate Prop
            The class will also stock the prop and MMD during training in self.props and self.mmd
            See self.plot() to plot the kl and mmd.
        """

        def torch_to_matrix(tensor):
            "Transform a torch.tensor into a matrix (cvxopt)"
            tensor = tensor.cpu()
            return matrix(np.array(tensor).astype(np.double))

        self.mmd = []

        mu_target = self.kernel.fit(target)
        optimizer = Adam(self.generator.parameters(), lr=lr)

        if verbose:
            iteration = tqdm(range(n_epoch))
        else:
            iteration = range(n_epoch)

        # Initial props
        if initial_prop is None:
            # Do one step of KernelQuantifyRFF
            mu = [self.kernel.fit(source[i]) for i in range(self.n_classes_)]
            mu = torch.stack(mu, axis=1).float()

            n = self.n_points_

            P = torch_to_matrix(2*n/(n-1)*mu.T @ mu)
            q = torch_to_matrix(-2 * mu.T @ mu_target)
            # constraint
            G = matrix(-np.eye(self.n_classes_))
            h = matrix(np.zeros(self.n_classes_))
            A = matrix(np.ones(self.n_classes_)).T
            b = matrix([1.0])

            solvers.options['show_progress'] = False
            sol = solvers.qp(P, q, G, h, A, b)

            self.props_ = [np.array(sol["x"]).reshape(self.n_classes_)]

        else:
            self.props_ = [initial_prop]

        # Algorithm
        for _ in iteration:
            pi = self.props_[-1]

            # Optimisation w.r.t \theta (the generator)
            for _ in range(int(n_epochGM)):
                optimizer.zero_grad()
                f_Q = [self.generator(source[c], c)
                       for c in range(self.n_classes_)]

                mu = [self.kernel.fit(f_Q[i]) for i in range(self.n_classes_)]
                mu_pi = [mu[i] * pi[i] for i in range(self.n_classes_)]

                loss = torch.linalg.norm(sum(mu_pi) - mu_target)*1e5
                loss.backward()
                self.mmd.append(loss.item())
                optimizer.step()

            # Optimisation w.r.t a_i (the proportions)
            with torch.no_grad():
                f_Q = [self.generator(source[c], c)
                       for c in range(self.n_classes_)]
                mu = [self.kernel.fit(f_Q[i]) for i in range(self.n_classes_)]
                mu = torch.stack(mu, axis=1).float()

                n = self.n_points_

                P = torch_to_matrix(2*n/(n-1)*mu.T @ mu)
                q = torch_to_matrix(-2 * mu.T @ mu_target)
                # constraint
                G = matrix(-np.eye(self.n_classes_))
                h = matrix(np.zeros(self.n_classes_))
                A = matrix(np.ones(self.n_classes_)).T
                b = matrix([1.0])

                solvers.options['show_progress'] = False
                sol = solvers.qp(P, q, G, h, A, b)

                self.props_.append(np.array(sol["x"]).reshape(self.n_classes_))

        return self.props_[-1]

    def get_kl(self, target_prop: np.array):
        return [KL_divergence(pi, target_prop) for pi in self.props_]

    @property
    def sigma(self):
        return self.kernel.sigma
