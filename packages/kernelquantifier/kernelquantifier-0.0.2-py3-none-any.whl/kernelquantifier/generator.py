# -*- coding: utf-8 -*-

"""
@author: Dussap Bastien

This modules contains the nn.Modules used by the `Generative Kernel Quantifier` algorithm.
"""

import torch
from torch.nn import Module, init
from torch.nn.parameter import Parameter
from torch.nn import functional as F
from torch import Tensor
from typing import List

def available_generator()->list[str]:
    return list(__generator__.keys())

def select_generator(generator:str)->Module:
    return __generator__[generator]

############################## Ax + b_i ##############################

class ShareLinear(Module):
    """ f_i(x) = A * x + b_i """
    __constants__ = ['number_features', 'number_classe']
    number_features: int
    number_classe: int

    def __init__(self, number_features: int, number_classe: int, device=None, dtype=None) -> None:
        self.factory_kwargs = {'device': device, 'dtype': dtype}
        super(ShareLinear, self).__init__()
        self.number_features = number_features
        self.number_classe = number_classe
        self.weight = Parameter(torch.empty(
            (number_features), **self.factory_kwargs))
        self.bias = Parameter(torch.empty(
            (number_classe, number_features), **self.factory_kwargs))

        self.reset_parameters()

    def reset_parameters(self) -> None:
        init.constant_(self.weight, 1)
        init.constant_(self.bias, 0)

    def forward(self, input: Tensor, nb_distrib: int) -> Tensor:
        if input.device != self.factory_kwargs["device"]:
            input = input.to(self.factory_kwargs["device"])

        return F.linear(input, torch.diag(self.weight), self.bias[nb_distrib])

    def extra_repr(self) -> str:
        return 'number_features={}, number_classe={}'.format(
            self.number_features, self.number_classe
        )

############################## x + b_i ##############################


class Translation(Module):
    """ f_i(x) = x + b_i """
    __constants__ = ['number_features', 'number_classe']
    number_features: int
    number_classe: int

    def __init__(self, number_features: int, number_classe: int, device=None, dtype=None) -> None:
        self.factory_kwargs = {'device': device, 'dtype': dtype}
        super(Translation, self).__init__()
        self.number_features = number_features
        self.number_classe = number_classe
        self.bias = Parameter(torch.empty(
            (number_classe, number_features), **self.factory_kwargs))
        self.weight = torch.empty(
            (number_features, number_features), **self.factory_kwargs)

        self.reset_parameters()

    def reset_parameters(self) -> None:
        init.eye_(self.weight)
        init.constant_(self.bias, 0)

    def forward(self, input: Tensor, nb_distrib: int) -> Tensor:
        if input.device != self.factory_kwargs["device"]:
            input = input.to(self.factory_kwargs["device"])

        return F.linear(input, self.weight, self.bias[nb_distrib])

    def extra_repr(self) -> str:
        return 'number_features={}, number_classe={}'.format(
            self.number_features, self.number_classe
        )

############################## A_i x + b_i ##############################


class IndependantLinear(Module):
    """ f_i(x) = A_i * x + b_i """
    __constants__ = ['number_features', 'number_classe']
    number_features: int
    number_classe: int

    def __init__(self, number_features: int, number_classe: int, device=None, dtype=None) -> None:
        self.factory_kwargs = {'device': device, 'dtype': dtype}
        super(IndependantLinear, self).__init__()
        self.number_features = number_features
        self.number_classe = number_classe
        self.weight = Parameter(torch.empty(
            (number_classe, number_features), **self.factory_kwargs))
        self.bias = Parameter(torch.empty(
            (number_classe, number_features), **self.factory_kwargs))

        self.reset_parameters()

    def reset_parameters(self) -> None:
        init.constant_(self.weight, 1)
        init.constant_(self.bias, 0)

    def forward(self, input: Tensor, nb_distrib: int) -> Tensor:
        if input.device != self.factory_kwargs["device"]:
            input = input.to(self.factory_kwargs["device"])

        return F.linear(input, torch.diag(self.weight[nb_distrib]), self.bias[nb_distrib])

    def extra_repr(self) -> str:
        return 'number_features={}, number_classe={}'.format(
            self.number_features, self.number_classe
        )

__generator__ = {
    "sharelinear" : ShareLinear,
    "translation" : Translation,
    "independantlinear" : IndependantLinear,
    }
