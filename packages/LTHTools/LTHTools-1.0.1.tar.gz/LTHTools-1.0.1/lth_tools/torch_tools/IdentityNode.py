# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     IdentityNode
   Description :   
   Author :       lth
   date：          2022/8/29
-------------------------------------------------
   Change Activity:
                   2022/8/29 10:08: create this script
-------------------------------------------------
"""
__author__ = 'lth'
from torch import  nn
from torch.autograd import Function
import torch

class IdentityNode_(Function):
    @staticmethod
    def forward(ctx, input):
        ctx.save_for_backward(input)
        return input

    @staticmethod
    def backward(ctx, grad_outputs):
        result, = ctx.saved_tensors
        weight=torch.ones_like(grad_outputs)
        weight[...,-4:]*=1.5  # here is the key
        return result * grad_outputs *weight


class IdentityNode(nn.Module):
    def __init__(self):
        super(IdentityNode, self).__init__()

    def forward(self, input_tensor):
        return IdentityNode_.apply(input_tensor)