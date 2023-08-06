# -*- coding: utf-8 -*-
# pylint: disable=E1101
# pylint: disable=E1102

"""
@author: Dussap Bastien

"""

import torch
import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm
from pykeops.torch import LazyTensor

from .utils import choose_device
from .data import LabelledCollection

def available_kernel()->list[str]:
    "Return the available kernel_type with RFF"
    return list(__kernel_type__.keys())

def select_kernel(kernel_type:str):
    return __kernel_type__[kernel_type]

class GaussianKernel:

    def __init__(self, sigma=1):
        """
        Gaussian kernel.

        sigma [float] : Bandwidth of the kernel.
        device [torch.device] : Device used to do the computation. The default is torch.device("cpu").

        Returns
        -------
        None.

        """
        self.sigma = sigma

    def fit_X(self, X: LabelledCollection):
        """
        Transform the data into a c by c matrix of <mu(P_i), pi(P_j)>.

        Parameters
        ----------
        X [LabelledCollection] : the data.
        """

        c = X.n_classes
        P = torch.empty((c, c))

        for i in range(c):
            for j in range(i, c):
                P[i, j] = LazyProductGaussian(X[i], X[j], self.sigma)

                if i != j:
                    P[j, i] = P[i, j]

        return P

    def fit_Xy(self, X: LabelledCollection, y: torch.tensor):
        """
        Transform the data into a c vector : <mu(P_i), mu(q)>.

        Parameters
        ----------
        X [LabelledCollection] : the source data.
        y [LabelledCollection] : The target data
        """

        if y.device != X.device:
            y = y.to(X.device)

        c = X.n_classes
        q = torch.empty((c))

        for i in range(c):
            q[i] = LazyProductGaussian(X[i], y, sigma=self.sigma)

        return q

def LazyProductGaussian(X:torch.tensor, Y:torch.tensor, sigma:float):
    """
    Do the scalar product <mu(X), mu(Y)> on CPU/GPU with a linear memory footprint,
    using pykeops routine.

    Args:
        X (torch.tensor): 1er class
        Y (torch.tensor): 2nd class
        sigma (float): bandwidth

    Returns:
        torch.tensor (size 1x1)
    """
    n_i = X.shape[0]
    n_j = Y.shape[0]

    x_l = LazyTensor(X.view(X.shape[0], 1, X.shape[1]))
    y_k = LazyTensor(Y.view(1, Y.shape[0], Y.shape[1]))

    D_lk = ((x_l - y_k)**2).sum(dim=-1)
    K_ij = (-D_lk/(2*sigma**2)).exp().sum(dim=0).sum(dim=0)/(n_i*n_j)

    return K_ij

# ---------------------------------------------------------------------------------

__kernel_type__ = {
    "gaussian" : GaussianKernel,
    }

def bandwidth_kernel(P: LabelledCollection, sigma_min: float, sigma_max: float, verbose: bool = True, kernel = GaussianKernel):
    """
    Choose the bandwidth using the criterion.

    Parameters
    ----------
    P [LabelledCollection] : source data
    sigma_min [float] : min sigma to test.
    sigma_max [float] : max sigma to test.
    device [torch.device] : device on which do the computation
    verbose [Boolean] : plot
    kernel [class] : GaussianKernel

    Returns
    -------
    sigma [float]
    """

    sigma = np.linspace(sigma_min, sigma_max, 50)
    iteration = tqdm(sigma) if verbose else sigma
    distance = []

    with torch.no_grad():
        for s in iteration:
            k = kernel(sigma=float(s))
            A = k.fit_X(P.subsample(10000))
            distance.append(torch.linalg.eigh(A)[0][0])
        
        mean_distance = torch.tensor(distance)
        best_sigma = sigma[np.argmax(mean_distance)]
        if verbose:
            plt.figure(figsize=(15, 8))
            plt.scatter(sigma, distance)
            plt.plot(sigma, mean_distance, color="red")
            plt.vlines(best_sigma, ymin=0, ymax=np.max(distance),
                       colors="red", linestyles='dashed')
            plt.show()
            print("Sigma = ", best_sigma)

    return float(best_sigma)
