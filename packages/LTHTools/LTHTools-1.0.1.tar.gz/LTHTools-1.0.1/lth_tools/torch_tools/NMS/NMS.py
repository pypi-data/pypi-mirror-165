# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     NMS
   Description :   
   Author :       lth
   date：          2022/8/29
-------------------------------------------------
   Change Activity:
                   2022/8/29 10:38: create this script
-------------------------------------------------
"""
__author__ = 'lth'

import torch

from . import bbox_iou


def nms(prediction, conf_threshold=0.1, nms_threshold=0.9):
    """

    :param prediction: N,7,output_nums_from_model  --> 7 [x,y,w,h,cls_pred,cls_conf,obj_conf]
    :return:
    """
    prediction = prediction.permute(0, 2, 1)

    output = [None for _ in range(len(prediction))]
    for image_i, image_pred in enumerate(prediction):
        class_conf, class_pred = prediction[:, :, 5].permute(1, 0), prediction[:, :, 4].permute(1, 0)
        conf = prediction[:, :, 6].permute(1, 0)

        conf_mask = ((conf * class_conf) >= conf_threshold).squeeze()

        image_pred = image_pred[conf_mask]
        class_conf = class_conf[conf_mask]
        class_pred = class_pred[conf_mask]
        conf = conf[conf_mask]

        if not image_pred.size(0):
            continue
        #  x,y,w,h,cls_conf,cls_pred,obj_conf
        detections = torch.cat((image_pred[:, :4], class_conf.float(), class_pred.conf(), conf.float()), 1)

        unique_labels = detections[:, 5].cpu().unique()

        if prediction.is_cuda():
            unique_labels = unique_labels.cuda()
            detections = detections.cuda()

        for c in unique_labels:
            detections_class = detections[detections[:, 5] == c]
            _, conf_sort_index = torch.sort(detections_class[:, 6] * detections_class[:, 4], descending=True)
            detections_class = detections_class[conf_sort_index]

            max_detections = []

            while detections_class.size(0):
                max_detections.append(detections_class[0].unsqueeze(0))
                if len(detections_class) == 1:
                    break
                ious = bbox_iou(max_detections[-1], detections_class[1:])
                detections_class = detections_class[1:][ious < nms_threshold]
            max_detections = torch.cat(max_detections).data

            output[image_i] = max_detections if output[image_i] is None else torch.cat(
                (output[image_i, max_detections]))

    return output
