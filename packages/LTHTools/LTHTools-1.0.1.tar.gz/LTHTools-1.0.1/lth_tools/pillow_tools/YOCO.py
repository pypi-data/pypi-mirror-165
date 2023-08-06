# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     YOCO
   Description :   
   Author :       lth
   date：          2022/8/26
-------------------------------------------------
   Change Activity:
                   2022/8/26 6:04: create this script
-------------------------------------------------
"""
__author__ = 'lth'

import random

from PIL import Image, ImageEnhance


class YoCo:
    def __init__(self):
        self.image_aug_list = [ImageEnhance.Brightness, ImageEnhance.Color, ImageEnhance.Contrast, ImageEnhance.Color]
        self.image_aug_factor = [[1, 8], [-3, 3], [-10, 10], [1, 5]]

    def __call__(self, image_path):
        image = Image.open(image_path)
        width, height = image.width, image.height

        choose_width = random.random() > 0.5
        scale_factor = random.uniform(-1.5, 1.5)
        shift_x = int(width // 10 * scale_factor)
        shift_y = int(height // 10 * scale_factor)
        if choose_width:
            """
            width
            """
            image1 = image.crop((0, 0, width // 2 + shift_x, height))
            image2 = image.crop((width // 2 + shift_x, 0, width, height))
        else:
            """
            height
            """
            image1 = image.crop((0, 0, width, height // 2 + shift_y))
            image2 = image.crop((0, height // 2 + shift_y, width, height))

        image1 = self.image_aug(image1)
        image2 = self.image_aug(image2)

        new_image = Image.new("RGB", (width, height))

        if choose_width:
            new_image.paste(image1, (0, 0))
            new_image.paste(image2, (width // 2 + shift_x, 0))
        else:
            new_image.paste(image1, (0, 0))
            new_image.paste(image2, (0, height // 2 + shift_y))

        return new_image

    def image_aug(self, image):
        choose = random.randint(0, len(self.image_aug_list) - 1)
        factor = self.image_aug_factor[choose]
        return self.image_aug_list[choose](image).enhance(random.uniform(factor[0], factor[1]))
