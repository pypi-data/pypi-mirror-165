# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     GroupNorm
   Description :   
   Author :       lth
   date：          2022/8/26
-------------------------------------------------
   Change Activity:
                   2022/8/26 6:10: create this script
-------------------------------------------------
"""
__author__ = 'lth'
import torch
from torch import nn


class GroupNorm(nn.Module):
    def __init__(self, num_features, num_groups, eps=1e-5, weight=None, bias=None):
        super(GroupNorm, self).__init__()
        if weight is None:
            self.weight = nn.Parameter(torch.ones(num_features, dtype=torch.float))
        else:
            self.weight = weight
        if bias is None:
            self.bias = nn.Parameter(torch.zeros(num_features, dtype=torch.float))
        else:
            self.bias = bias

        self.num_groups = num_groups
        self.eps = eps

    def forward(self, x):
        N, C, H, W = x.size()
        G = self.num_groups
        assert C % G == 0

        x = x.reshape(N, G, -1, H, W)
        mean = torch.mean(x, [2, 3, 4], keepdim=True)

        std = torch.sqrt((torch.mean(torch.pow(x - mean, 2), [2, 3, 4], keepdim=True)) + self.eps)
        x = (x - mean) / std
        x = x.reshape(N, C, H, W)

        weight = self.weight.unsqueeze(0).unsqueeze(-1).unsqueeze(-1).expand_as(x)
        bias = self.bias.unsqueeze(0).unsqueeze(-1).unsqueeze(-1).expand_as(x)

        return x * weight + bias

if __name__ == "__main__":
    dummy_input = torch.randn([1, 2, 3, 3], dtype=torch.float)

    model = GroupNorm(num_features=2, num_groups=2)

    result1 = model(dummy_input)
    print(result1)
    g = nn.GroupNorm(num_groups=2, num_channels=2)
    result2 = g(dummy_input)
    print(result2)

    # torch.onnx.export(model,dummy_input,"test.onnx",opset_version=11)