# -*- coding: utf-8 -*-
# pylint: disable=E1101
# pylint: disable=E1102

"""
@author: Dussap Bastien
This module contains the possible RFF.
"""

import numpy as np
import torch
import matplotlib.pyplot as plt
from pykeops.torch import LazyTensor

from tqdm import tqdm
from .utils import *
from .data import LabelledCollection
from .base import BaseFeatureMap


def bandwidthRFF(P: LabelledCollection, sigma_min: float, sigma_max: float, device: torch.device, kernel, verbose: bool = True, number_rff: int = 1000):
    """
    Choose the bandwidth using the criterion.

    Parameters
    ----------
    P [LabelledCollection] : source data
    sigma_min [float] min sigma to test.
    sigma_max [float] max sigma to test.
    device [torch.device] : device on which do the computation.
    verbose [Boolean] : plot.
    kernel [class] : GaussianKernel.
    number_rff [int] : number of random fourier features.

    Returns
    -------
    sigma [float]
    """
    X_plot = np.linspace(sigma_min, sigma_max, 50)
    sigma = np.repeat(X_plot, 5)

    feature_maps = [kernel(D=number_rff, d=P[0].shape[1], sigma=s, device=device)
                 for s in sigma]
    iteration = tqdm(feature_maps) if verbose else feature_maps
    distance = []
    with torch.no_grad():
        for feature_map in iteration:
            Q = P.subsample(10000)
            A = torch.zeros((number_rff, len(P)))
            for i in range(len(P)):
                A[:, i] = feature_map.git(Q[i]).to(feature_map.device)
            distance.append(torch.linalg.eigh(A.T@A)[0][0])

        mean_distance = torch.tensor(distance).reshape(50, 5).mean(axis=1)
        best_sigma = X_plot[np.argmax(mean_distance)]
        if verbose:
            plt.figure(figsize=(15, 8))
            plt.scatter(sigma, distance)
            plt.plot(X_plot, mean_distance, color="red")
            plt.vlines(best_sigma, ymin=0, ymax=np.max(distance),
                       colors="red", linestyles='dashed')
            plt.show()
            print("Sigma = ", best_sigma)

    return best_sigma


def MMD(P: torch.tensor, Q: torch.tensor, feature_map: BaseFeatureMap):
    """
    MMD distance between two distributions.

    Parameters
    ----------
    P : torch.tensor
    Q : torch.tensor
    gauss : BaseFeatureMap
        Mapping between the data and the RKHS.

    Returns
    -------
    float
        MMD distance.
    """

    mu_p = feature_map.fit(P)
    mu_q = feature_map.fit(Q)
    res = torch.linalg.norm(mu_p - mu_q)
    return res.cpu()


################################################ RFF ###################################

class GaussianRFF(BaseFeatureMap):

    def __init__(self,
                 D: int,
                 d: int,
                 sigma:float=1,
                 device: torch.device = choose_device(verbose=False))->None:
        """
        Random fourier features of a gaussian.

        Parameters
        ----------
        D : int (even)
            Number of fourier features.
        d : int
            Dimension of the data.
        sigma : float, optional
            Bandwidth of the kernel.
        device : torch.device, optional
            Device used to do the computation. The default is torch.device("cpu").

        Returns
        -------
        None.

        """
        assert D % 2 == 0
        super().__init__(D, d, device)

        self.sigma = sigma
        self.w = torch.from_numpy(np.random.default_rng().normal(
            0, 1./self.sigma, (int(self.D/2), d))).float().to(self.device)
        self.cons = np.sqrt(2/self.D)

    def __repr__(self) -> str:
        return "Kernel = Gaussian, D = {}, d = {}, sigma = {} and device = {}".format(
            self.D, self.d, self.sigma, self.device)


class LaplaceRFF():

    def __init__(self, D, d, sigma=1, device=choose_device(verbose=False)):
        """
        Random fourier features of a gaussian.

        Parameters
        ----------
        D : int
            Number of fourier features.
        d : int
            Dimension of the data.
        sigma : float, optional
            Bandwidth of the kernel.
        device : torch.device, optional
            Device used to do the computation. The default is torch.device("cpu").

        Returns
        -------
        None.

        """
        self.D = D
        self.d = d
        self.sigma = sigma
        self.w = torch.from_numpy(np.random.default_rng().laplace(
            0, 1./sigma, (int(D/2), d))).float().to(device)
        self.cons = np.sqrt(2/D)
        self.device = device

    def fit_transform(self, X):
        """
        Mapping the data X to the RKHS.

        Parameters
        ----------
        X : torch.tensor
            Data.
        Returns
        -------
        torch.tensor
            Transformed data.

        """
        if X.device != self.device:
            X = X.to(self.device)
        u = (X@self.w.T)
        return self.cons * torch.cat((torch.cos(u), torch.sin(u)), dim=1)

    def __repr__(self) -> str:
        return "Kernel = Gaussian, D = {}, d = {}, sigma = {} and device = {}".format(
            self.D, self.d, self.sigma, self.device)


class StandardtRFF():

    def __init__(self, D, d, sigma=1, device=choose_device(verbose=False)):
        """
        Random fourier features of a gaussian.

        Parameters
        ----------
        D : int
            Number of fourier features.
        d : int
            Dimension of the data.
        sigma : float, optional
            Bandwidth of the kernel.
        device : torch.device, optional
            Device used to do the computation. The default is torch.device("cpu").

        ReturnsP_source
        -------
        None.

        """
        self.D = D
        self.d = d
        self.sigma = sigma
        self.w = torch.from_numpy(np.random.default_rng().standard_t(
            sigma, (int(D/2), d))).float().to(device)
        self.cons = np.sqrt(2/D)
        self.device = device

    def fit_transform(self, X):
        """
        Mapping the data X to the RKHS.

        Parameters
        ----------
        X : torch.tensor
            Data.
        Returns
        -------
        torch.tensor
            Transformed data.

        """
        if X.device != self.device:
            X = X.to(self.device)
        u = (X@self.w.T)
        return self.cons * torch.cat((torch.cos(u), torch.sin(u)), dim=1)

    def __repr__(self) -> str:
        return "Kernel = Gaussian, D = {}, d = {}, sigma = {} and device = {}".format(
            self.D, self.d, self.sigma, self.device)
