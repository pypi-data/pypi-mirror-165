# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     relu_2_leakyrelu
   Description :   
   Author :       lth
   date：          2022/8/29
-------------------------------------------------
   Change Activity:
                   2022/8/29 12:34: create this script
-------------------------------------------------
"""
__author__ = 'lth'

from torch import nn


def convert_relu_to_leakrelu(model):
    for child_name,child in model.named_children():
        if isinstance(child,nn.ReLU):
            setattr(model,child_name,nn.LeakyReLU(inplace= True))
        else:
            convert_relu_to_leakrelu(child)