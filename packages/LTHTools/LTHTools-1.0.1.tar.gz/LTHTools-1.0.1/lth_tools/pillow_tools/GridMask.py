# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     GridMask
   Description :   
   Author :       lth
   date：          2022/8/26
-------------------------------------------------
   Change Activity:
                   2022/8/26 6:03: create this script
-------------------------------------------------
"""
__author__ = 'lth'

import random

from PIL import Image


class GridMask():
    def __init__(self):
        pass

    def __call__(self, image: Image.Image, nums: int):
        """

        :param image: PIL格式的图片
        :param nums: grid的数量（以行为主）
        :return: image PIL格式的图片
        """
        width, height = image.width, image.height

        min_length = min(width, height)

        min_grids_cols = min_length // (2 * nums)

        mask = Image.new("RGB", (min_grids_cols, min_grids_cols), (0, 0, 0))

        start_point_x, start_point_y = random.randint(0, width // 2), random.randint(0, height // 2)

        for col in range(nums):
            for row in range(nums):
                image.paste(mask, (start_point_x + 2 * min_grids_cols * col, start_point_y + 2 * min_grids_cols * row))
        return image
