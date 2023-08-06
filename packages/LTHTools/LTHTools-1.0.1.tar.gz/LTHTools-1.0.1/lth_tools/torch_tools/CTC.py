# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     CTC
   Description :   
   Author :       lth
   date：          2022/8/26
-------------------------------------------------
   Change Activity:
                   2022/8/26 6:09: create this script
-------------------------------------------------
"""
__author__ = 'lth'


import copy

import numpy as np
import torch
import torch.nn.functional as F
from torch import nn
from torch.autograd import Function


class CTCLTH_log(nn.Module):
    def __init__(self, num_list, reduction="sum"):
        super(CTCLTH_log, self).__init__()
        self.reduction = reduction
        self.blank_label = "^"
        self.loss = None
        self.gradient = None
        # blank in the first place as default
        self.dict_num_to_index = {l: index for index, l in enumerate(["^"] + num_list)}
        self.dict_index_to_num = {index: l for index, l in enumerate(["^"] + num_list)}

    def forward(self, pred, target, input_length, target_length):
        """
        ctc 的本质是对选中的index 做 nllloss softmax--> ln -->nlloss 本质是 挑选出对应的标签  去掉负号 然后求平均
        :param pred: T N C
        :param target: N (N1_length+N2_length)
        :param input_length: used to construct the T  is a tuple  (INPUT_LENGTH,INPUT_LENGTH,....)
        :param target_length: used to construct the 2c+1    (Target_length1,Target_lenght2,....)
        :return: loss
        """

        loss_res = []
        T, N, C = pred.shape
        for i in range(N):

            loss = torch.zeros_like(pred[:, i, :])
            start_index = target_length[i - 1] if i > 0 else 0
            label = target[start_index:start_index + target_length[i]]

            pad_target = torch.tensor([0] * (2 * len(label) + 1))
            for index, gl in enumerate(label):
                pad_target[2 * index + 1] = gl

            assert input_length[i] >= 2 * target_length[
                i] + 1, f"the input_length or target_length is illegal in Batch index {i}"

            alpha, beta = self.create_alpha_beta_table(
                gt_labels=pad_target, outputs=pred[:, i, :],
                input_length=input_length[i],
                target_length=target_length[i])

            for t in range(T):
                for k in range(C):
                    dp_dy_tk = torch.tensor(0, dtype=torch.float32)
                    lab_lk = [index for index, pt in enumerate(pad_target) if pt == k]
                    for s in lab_lk:
                        dp_dy_tk += (alpha[t, s] * beta[t, s])
                    loss[t, k] = dp_dy_tk / (pred[t, i, k])

            loss_res.append(-CTCLTH_log.logsumexp(alpha[-1, -2], alpha[-1, -1]))
        loss_res = torch.tensor(loss_res)
        if self.reduction == "none" or self.reduction == "None" or self.reduction == "NONE":
            return loss_res
        elif self.reduction == "sum" or self.reduction == "SUM" or self.reduction == "Sum":
            return torch.sum(loss_res)
        elif self.reduction == "mean" or self.reduction == "Mean" or self.reduction == "MEAN":
            return torch.mean(loss_res)

    def create_alpha_beta_table(self, gt_labels, outputs, input_length, target_length):
        alpha_table = torch.ones([input_length, target_length * 2 + 1]) * np.float("-inf")
        beta_table = torch.ones([input_length, target_length * 2 + 1]) * np.float("-inf")

        for alpha_i in range(input_length):
            for alpha_j in range(target_length * 2 + 1):
                alpha_table[alpha_i, alpha_j] = self.config_alpha(alpha_i, alpha_j, outputs,
                                                                  gt_labels, alpha_table)

        for beta_i in range(input_length - 1, -1, -1):
            for beta_j in range(target_length * 2, -1, -1):
                beta_table[beta_i, beta_j] = self.config_beta(beta_i, beta_j, outputs, gt_labels,
                                                              beta_table)

        return alpha_table, beta_table

    def config_alpha(self, t, s, output, pad_gt_label, alpha_table):
        if s < 0 or s >= len(pad_gt_label):
            return np.float("-inf")
        current_character = self.dict_index_to_num[pad_gt_label[s].item()]
        assert current_character in self.dict_num_to_index.keys(), "the char not in dicts ,please check the input label"
        current_character_score = output[t, self.dict_num_to_index[current_character]]

        if t == 0:
            if s == 0:
                return output[t, 0]
            elif s == 1:
                return current_character_score
            else:
                return np.float("-inf")
        alpha_tag_t_s = CTCLTH_log.logsumexp(alpha_table[t - 1, s],
                                             alpha_table[t - 1, s - 1] if s - 1 >= 0 else torch.tensor(float("-inf")))
        if current_character == self.blank_label or (
                s >= 2 and self.dict_index_to_num[pad_gt_label[s - 2].item()] == current_character):
            return alpha_tag_t_s + current_character_score
        else:
            return CTCLTH_log.logsumexp(alpha_tag_t_s, alpha_table[t - 1, s - 2] if s - 2 >= 0 else torch.tensor(
                float("-inf"))) + current_character_score

    def config_beta(self, t, s, output, pad_gt_label, beta_table):
        if s < 0 or s >= len(pad_gt_label):
            return np.float("-inf")
        current_character = self.dict_index_to_num[pad_gt_label[s].item()]
        current_character_label_score = output[t, self.dict_num_to_index[current_character]]
        last_time_step = output.shape[0] - 1
        last_channel_step = len(pad_gt_label) - 1

        if t == last_time_step:
            if s == last_channel_step:
                return output[t, 0]
            elif s == last_channel_step - 1:
                return current_character_label_score
            else:
                return np.float("-inf")
        beta_tag_t_s = CTCLTH_log.logsumexp(beta_table[t + 1, s],
                                            beta_table[t + 1, s + 1] if s + 1 <= last_channel_step else torch.tensor(
                                                float("-inf")))
        if current_character == self.blank_label or (
                s + 2 <= last_channel_step and self.dict_index_to_num[pad_gt_label[s + 2].item()] == current_character):
            return beta_tag_t_s + current_character_label_score
        else:
            return CTCLTH_log.logsumexp(beta_tag_t_s,
                                        beta_table[t + 1, s + 2] if s + 2 <= last_channel_step else torch.tensor(
                                            float("-inf"))) + current_character_label_score

    @staticmethod
    def logsumexp(a, b):
        if a < b:
            a, b = b, a
        if b == np.float("-inf"):
            return a
        else:
            return a + torch.log(1 + torch.exp(b - a))


class CTCFormal_(Function):
    @staticmethod
    def forward(ctx, input, target, input_length, target_length, num_list):

        ctx.blank_label = "^"
        ctx.dict_num_to_index = {l: index for index, l in enumerate(["^"] + num_list)}
        ctx.dict_index_to_num = {index: l for index, l in enumerate(["^"] + num_list)}
        input = torch.exp(input)

        T, N, C = input.shape
        loss_res = torch.tensor(0.)
        for i in range(N):

            start_index = target_length[i - 1] if i > 0 else 0
            label = target[start_index:start_index + target_length[i]]

            pad_target = torch.tensor([0] * (2 * len(label) + 1))
            for index, gl in enumerate(label):
                pad_target[2 * index + 1] = gl

            assert input_length[i] >= 2 * target_length[
                i] + 1, f"the input_length or target_length is illegal in Batch index {i}"

            alpha, beta = CTCFormal_.create_alpha_beta_table(
                gt_labels=pad_target, outputs=input[:, i, :],
                input_length=input_length[i],
                target_length=target_length[i])
            for t in range(T):
                for k in range(C):
                    dp_dy_tk = 0
                    lab_lk = [index for index, pt in enumerate(pad_target) if pt == k]
                    for s in lab_lk:
                        dp_dy_tk += (alpha[t, s] * beta[t, s])
                    # 计算  gradient
                    input[t, i, k] = -dp_dy_tk / ((input[t, i, k])* (alpha[-1, -1] + alpha[-1, -2]))+input[t,i,k]

            loss_res.add_(-torch.log((alpha[-1, -1] + alpha[-1, -2])))
        ctx.save_for_backward(input)
        return loss_res

    @staticmethod
    def backward(ctx, grad_output):
        result, = ctx.saved_tensors
        return result * grad_output, None, None, None, None

    @staticmethod
    def create_alpha_beta_table(gt_labels, outputs, input_length, target_length):
        alpha_table = torch.zeros([input_length, target_length * 2 + 1], requires_grad=True)
        beta_table = torch.zeros([input_length, target_length * 2 + 1], requires_grad=True)

        for alpha_i in range(input_length):
            for alpha_j in range(target_length * 2 + 1):
                alpha_table[alpha_i, alpha_j] = CTCFormal_.config_alpha(t=alpha_i, s=alpha_j, output=outputs,
                                                                        pad_gt_label=gt_labels, alpha_table=alpha_table)

        for beta_i in range(input_length - 1, -1, -1):
            for beta_j in range(target_length * 2, -1, -1):
                beta_table[beta_i, beta_j] = CTCFormal_.config_beta(beta_i, beta_j, outputs, gt_labels,
                                                                    beta_table)

        return alpha_table, beta_table

    @staticmethod
    def config_alpha(t, s, output, pad_gt_label, alpha_table):
        current_character = pad_gt_label[s]
        current_character_score = output[t, current_character]

        if t == 0:
            if s == 0:
                return output[0, 0]
            elif s == 1:
                return current_character_score
            else:
                return 0

        alpha_tag_t_s = alpha_table[t - 1, s] + (alpha_table[t - 1, s - 1] if s - 1 >= 0 else 0)

        if current_character == "^" or (s >= 2 and pad_gt_label[s - 2] == pad_gt_label[s]):
            return alpha_tag_t_s * current_character_score
        else:
            return (alpha_tag_t_s + (alpha_table[t - 1, s - 2] if s - 2 >= 0 else 0)) * current_character_score

    @staticmethod
    def config_beta(t, s, output, pad_gt_label, beta_table):
        current_character = pad_gt_label[s]
        current_character_score = output[t, current_character]

        last_time_step = output.shape[0] - 1
        last_channel_step = len(pad_gt_label) - 1

        if t == last_time_step:
            if s == last_channel_step:
                return output[-1, 0]
            elif s == last_channel_step - 1:
                return current_character_score
            else:
                return 0

        beta_tag_t_s = beta_table[t + 1, s] + (beta_table[t + 1, s + 1] if s + 1 <= last_channel_step else 0)
        if current_character == "^" or (
                s + 2 <= last_channel_step and pad_gt_label[s + 2] == pad_gt_label[s]):
            return beta_tag_t_s * current_character_score
        else:
            return (beta_tag_t_s + (
                beta_table[t + 1, s + 2] if s + 2 <= last_channel_step else 0)) * current_character_score


class CTCFormal(nn.Module):
    def __init__(self, num_list):
        super(CTCFormal, self).__init__()
        self.num_list = num_list

    def forward(self, input_variable):
        input, target, input_length, target_length = input_variable
        return CTCFormal_.apply(input, target, input_length, target_length, self.num_list)


if __name__ == "__main__":
    num_list = ["a", "b", "c", "d"]
    dict_num_to_index = {l: index for index, l in enumerate(["^"] + num_list)}

    basic_length = 51
    basic_channel = len(num_list) + 1
    dummy_input = torch.rand([2, 1, basic_length, basic_channel], requires_grad=False, dtype=torch.float32)

    conv1 = nn.Conv2d(in_channels=1, out_channels=1, kernel_size=3, stride=1, padding=(1, 1))
    conv2 = copy.deepcopy(conv1)

    dummy_input1 = conv1(dummy_input)
    dummy_input2 = conv2(dummy_input)
    dummy_input1 = dummy_input1.view(2, -1, basic_channel)
    dummy_input2 = dummy_input2.view(2, -1, basic_channel)
    dummy_input1 = torch.transpose(dummy_input1, 1, 0)
    dummy_input2 = torch.transpose(dummy_input2, 1, 0)
    dummy_input1 = torch.log_softmax(dummy_input1, dim=2)
    dummy_input2 = torch.log_softmax(dummy_input2, dim=2)
    target1 = "abd"
    target2 = "abcc"
    t = [target1, target2]
    target = target1 + target2
    target = torch.tensor([dict_num_to_index[t] for t in target], dtype=torch.long)
    input_length = torch.full((2,), basic_length, dtype=torch.long)
    target_length = tuple([len(tt) for tt in t])
    target_length = torch.tensor(target_length, dtype=torch.long)



    # model= CTCLTH_log(num_list=num_list)
    # model.forward(dummy_input1, target, input_length, target_length)



    import time

    Loss = CTCFormal(num_list=num_list)
    start_time = time.time()
    loss = Loss((dummy_input1, target, input_length, target_length))
    loss.backward()
    end_time = time.time()
    print("time:", end_time - start_time)
    print("lth loss:", loss)
    print("conv grad:", conv1.weight.grad)
    print("=================================================================================")
    start_time = time.time()
    ctcloss = F.ctc_loss(log_probs=dummy_input2, targets=target, input_lengths=input_length,
                         target_lengths=target_length, reduction="sum")
    ctcloss.backward()
    end_time = time.time()
    print("time:", end_time - start_time)
    print("pytorch loss:", ctcloss)
    print("conv grad:", conv2.weight.grad)
