# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     GAN
   Description :   
   Author :       lth
   date：          2022/8/29
-------------------------------------------------
   Change Activity:
                   2022/8/29 11:21: create this script
-------------------------------------------------
"""
__author__ = 'lth'

import torch.distributed.rpc
from torch import nn

from .BCE import BCE


class OriginalGan(nn.Module):
    def __init__(self):
        super(OriginalGan, self).__init__()
        self.discriminator_loss = BCE()
        self.generator_loss = BCE()

    def discriminator_calculate(self, real_logit, fake_logit):
        loss_p = self.discriminator_loss.calculate(input_tensor=real_logit, target=torch.ones_like(real_logit))
        loss_n = self.discriminator_loss.calculate(input_tensor=fake_logit, target=torch.zeros_like(fake_logit))

        return loss_n + loss_p

    def generator_calculate_v1(self, fake_logit):
        loss = -self.generator_loss.calculate(input_tensor=fake_logit, target=torch.zeros_like(fake_logit))
        return loss

    def generator_calculate_v2(self, fake_logit):
        loss = self.generator_loss.calculate(input_tensor=1 - fake_logit, target=torch.zeros_like(fake_logit))
        return loss


class WGan(nn.Module):
    def __init__(self, use_gradient_penalty=False):
        super(WGan, self).__init__()
        self.use_gradient_penalty = use_gradient_penalty

    def discriminator_calculate(self, real, fake, penalty_image):
        loss = torch.mean(real) - torch.mean(fake)
        if self.use_gradient_penalty:
            loss += torch.mean(torch.pow(penalty_image - 1, 2))
        return loss

    @staticmethod
    def generator_calculate(fake):
        loss = -torch.sum(fake)
        return loss


class LSGan(nn.Module):
    def __init__(self):
        super(LSGan, self).__init__()

    @staticmethod
    def discriminator_calculate(real, fake):
        loss = torch.mean(real - 1) + torch.mean(fake)
        return loss

    @staticmethod
    def generator_calculate(fake):
        loss = torch.mean(fake - 1)
        return loss
