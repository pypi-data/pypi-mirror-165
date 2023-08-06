"""
@author: Dussap Bastien
This .py contains BaseClass : BaseQuantifier and BaseFeatureMap.
"""

import torch
import numpy as np
from pykeops.torch import LazyTensor
from abc import ABCMeta, abstractmethod

from .utils import KL_divergence
from .data import LabelledCollection

# Base Quantifier abstract class
# ------------------------------------


class BaseQuantifier(metaclass=ABCMeta):
    """
    Abstract Quantifier. A quantifier is defined as an object of a class that implements the method :meth:`fit`, 
    the method :meth:`quantify`.
    """

    @abstractmethod
    def fit(self, source: LabelledCollection)->None:
        """Fit the quantifier on the Source.

        Args:
            source (LabelledCollection): Source
        """
        ...

    @abstractmethod
    def quantify(self, source: LabelledCollection, target: torch.tensor)->np.array:
        """Quantify the target.

        Args:
            source (LabelledCollection): Source
            target (torch.tensor): Target

        Returns:
            np.array: Estimate proportions.
        """
        ...

    @abstractmethod
    def get_kl(self, pi_target: np.array) -> np.array:
        """
        Return the KL divergence between pi_target and the estimate proportion.
        """
        return KL_divergence(self.props_, pi_target)

    @property
    def n_classes(self):
        """
        Returns the number of classes
        :return: integer
        """
        return len(self.classes_)


##############################################################################################################


class BaseFeatureMap():
    """
    Abstract Feature_map. A Feature_map is defined as an object of a class that implements the method `fit` (KME), 
    the method `fit` is always the same and use omega defined in init.
    The implementation with LazyTensor (pykeops) prevents memory overflow.
    """

    def __init__(self, D: int, d: int, device: torch.device, dtype:torch.dtype, seed:int=123) -> None:
        """super init

        Args:
            D (int): Number of RFF
            d (int): Dimension of the data
            device (torch.device) : CPU/GPU
        """
        self.D = D
        self.d = d
        self.device = device
        self.dtype = dtype
        self.seed = seed

    def fit(self, X: torch.tensor) -> torch.tensor:
        """super fit
        self.w must have been difined in init !!

        Args:
            X (torch.tensor): data

        Returns:
            torch.tensor: mu(X) dim=[X.shape[0], self.D]
        """
        if X.device != self.device:
            X = X.to(self.device)

        n = X.shape[0]

        # LazyTensor (n, 1, d)
        x_i = LazyTensor(X.view(X.shape[0], 1, X.shape[1]))
        # LazyTensor (1, d, D)
        w_j = LazyTensor(self.w.view(1, self.w.shape[0], self.w.shape[1]))

        u = (x_i | w_j)  # The matrix multiplication, LazyTensor (n, D), 
        C = u.cos().concat(u.sin())  # Apply a cos and a sin, LazyTensor (n, D, 2)
        return self.cons*(C.sum(dim=0)/n).flatten()  # Mean, the reduction is performed Tensor (2D)
