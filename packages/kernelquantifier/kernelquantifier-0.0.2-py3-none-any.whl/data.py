"""
@author: Dussap Bastien
This .py contains the LabelledCollection class used for the source distributions.

Code inspired by QuaPy : https://github.com/HLT-ISTI/QuaPy
"""

import numpy as np
import torch
from typing import List, Callable
from .utils import choose_device


class LabelledCollection:
    """
    LabelledCollection : The source is a list. This class, wrapped around list and add few methods of subsamplings.
    Attributes : 
        n_classes (int) : Number of classes.
        prop (np.array) : Proportion of the source.
        n_points (int) : number of points
        dim (int) : dimension of the data
        device (torch.device) : Device of the data (cpu/gpu)
    """

    def __init__(self, func:Callable = lambda x:x, *args) -> None:
        """
        Transform the data with the function func.
        For instance if the data is already a list use func = lambda x:x

        Args:
            func (function): The function that transform the data into a list.
        """

        self.data_ = func(*args)
        pi = np.empty(len(self.data_))
        for k, data in enumerate(self.data_):
            pi[k] = len(data)

        self.pos_classes = [0].append(np.cumsum(pi))
        self.prop = np.array([p/sum(pi) for p in pi])
        self.n_points = int(sum(pi))

    def sample(self, i, size):
        "get a sample of size size from class i"
        size = int(min(self.data_[i].shape[0], size))
        gen = np.random.default_rng()
        return self.data_[i][gen.choice(self.data_[i].shape[0], size, replace=False)]

    def subsample(self, size):
        """
        Return a LabelledCollection of sample of size size

        size [int]

        ---------------------
        return LabelledCollection
        """
        sample_data = []
        for i in range(self.n_classes):
            size = int(min(self.data_[i].shape[0], size))
            gen = np.random.default_rng()
            sample_data.append(self.data_[i][gen.choice(
                self.data_[i].shape[0], size, replace=False)])

        return LabelledCollection(lambda x: x, sample_data)

    def __getitem__(self, classe):
        return self.data_[classe]

    def __len__(self):
        return len(self.data_)

    @property
    def dim(self):
        """
        Returns the dimension of the data
        :return: integer
        """
        return self.data_[0].shape[1]

    @property
    def n_classes(self):
        """
        Returns the number of classes
        :return: integer
        """
        return len(self.prop)

    @property
    def device(self):
        device = self.data_[0].device
        for i in range(1, self.n_classes):
            if self.data_[i].device != device:
                raise TypeError("All classes are not on same device")
        return device

#
# Function to preprocess the data :

def to_device(X: List[torch.tensor], device: torch.device = choose_device()):
    """
    Send all element of the list on the device.

    Args:
        X (List[torch.tensor]): data
        device (torch.device, optional): device. Defaults to choose_device().

    Returns:
        List: data.to(device)
    """
    return [x.to(device) for x in X]
    
