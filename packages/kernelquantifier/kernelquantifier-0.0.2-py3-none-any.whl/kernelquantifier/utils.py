# -*- coding: utf-8 -*-

"""
@author: Dussap Bastien
"""

import torch
import numpy as np
from torch.cuda import is_available, memory_allocated, memory_reserved, get_device_name


def cuda_info(dev):
    """Gives information about CUDA"""

    # setting device on GPU if available, else CPU
    print('Using device:', dev)
    print()

    # Additional Info when using cuda
    if dev.type == 'cuda':
        print(get_device_name(0))
        print('Memory Usage:')
        print('Allocated:', round(memory_allocated(0)/1024**3, 1), 'GB')
        print('Cached:   ', round(memory_reserved(0)/1024**3, 1), 'GB')

    print(torch.version.cuda)


def choose_device(verbose=False):
    """ If cuda is avalaible returns pytorch device("cuda:0"). device("cpu") otherwise """
    if is_available():
        dev = torch.device("cuda:0")
        if verbose:
            print("Running on the GPU")
    else:
        dev = torch.device("cpu")
        if verbose:
            print("Running on the CPU")

    return(dev)


def measure_performance(pi_hat, pi):
    """
    Measure the KL div, the absolute error and the relarive absolute error
    """

    return({'KL': KL_divergence(pi_hat, pi),
            'absolute_error': absolute_error(pi_hat, pi),
            'Relative Absolute Error': relative_absolute_error(pi_hat, pi),
            })


def KL_divergence(pi_hat, pi):
    """
    KL divergence between two distributions.
    """
    pi = np.array(pi)
    pi_hat = np.array(pi_hat)
    return 100*np.sum(pi_hat * np.log(pi_hat / pi))


def absolute_error(pi_hat, pi):
    """
    Absolute error between two distributions. (L1 norm)
    """

    pi = np.array(pi)
    return np.mean(np.abs(pi_hat - pi))


def relative_absolute_error(pi_hat, pi):
    """
    Relative Absolute Error between two distributions.
    """

    pi = np.array(pi)
    return np.mean(np.abs(pi_hat - pi)/pi)


def subsampling(P, size_sampling):
    """
    Parameters
    ----------
    P : torch.tensor
    size_sampling : int
    Returns
    -------
    torch.tensor
    """

    size = int(min(P.shape[0], size_sampling))
    gen = np.random.default_rng()
    return P[gen.choice(P.shape[0], size, replace=False)]


def subsampling_list(P, size_sampling):
    """
    Same as subsampling but for a list.
    Parameters
    ----------
    P : list of torch.tensor
    size_sampling : int
    Returns
    -------
    list of torch.tensor
    """
    return [subsampling(p, size_sampling) for p in P]
