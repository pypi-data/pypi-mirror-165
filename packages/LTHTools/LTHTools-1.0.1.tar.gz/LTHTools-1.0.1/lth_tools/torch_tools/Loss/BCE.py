# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     BCE
   Description :   
   Author :       lth
   date：          2022/8/29
-------------------------------------------------
   Change Activity:
                   2022/8/29 11:22: create this script
-------------------------------------------------
"""
__author__ = 'lth'

from torch import nn
import torch
class BCE(nn.Module):
    def __init__(self,eps = 1e-5,reduction = "sum"):
        super(BCE, self).__init__()

        assert reduction in ["sum","mean","none"]
        self.reduction = reduction
        self.eps = eps

    def calculate(self,input_tensor,target):
        input_tensor = self.clamp(input_tensor)

        output = -target*torch.log(input_tensor)-(1.-target)*torch.log(1.-input_tensor)

        if self.reduction is "sum":
            output = torch.sum(output)
        elif self.reduction is "mean":
            output = torch.mean(output)
        elif self.reduction is "none":
            pass
        else:
            raise ValueError("reduction must be sum , mean , none")

        return output


        return output


    def clamp(self,input_tensor):
        input_tensor = torch.clamp(input_tensor,self.eps,1-self.eps)
        return input_tensor