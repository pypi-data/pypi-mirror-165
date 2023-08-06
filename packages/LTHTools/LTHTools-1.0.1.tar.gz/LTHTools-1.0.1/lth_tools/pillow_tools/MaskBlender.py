# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     MaskBlende
   Description :   
   Author :       lth
   date：          2022/8/26
-------------------------------------------------
   Change Activity:
                   2022/8/26 4:19: create this script
-------------------------------------------------
"""
__author__ = 'lth'

import random

from PIL import ImageEnhance, Image, ImageDraw


class MaskBlender:
    def __init__(self):
        self.image_aug_list = [ImageEnhance.Brightness, ImageEnhance.Color, ImageEnhance.Contrast, ImageEnhance.Color]
        self.image_aug_factor = [[1, 8], [-3, 3], [-10, 10], [1, 5]]
        self.mode = ["chord", "ellipse", "line", "pieslice", "polygon", "rectangle"]

    def __call__(self, image_path):
        image = Image.open(image_path).convert("RGBA")
        width, height = image.width, image.height
        blank = Image.new("RGBA", (width, height), color=(0, 0, 0))
        blank.paste(image, (0, 0))
        for _ in range(random.randint(3, 6)):
            mask = self.get_mask(width, height)
            r, g, b, a = mask.split()
            temp = self.image_aug(image)
            blank.paste(temp, (0, 0), mask=r)
        blank.save("mask_blender.png")

    def get_mask(self, width, height):
        Mask = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        mask = ImageDraw.Draw(Mask)
        mask_height, mask_width = random.randint(0, height // 2), random.randint(0, width // 2)

        x1, y1 = random.randint(0, width), random.randint(0, height)
        MaskBlender.get_different_mask(x1, y1, x1 + mask_width, y1 + mask_height, mask,
                                              mode=random.choice(self.mode)
                                              )
        return Mask

    @staticmethod
    def get_different_mask(x1, y1, x2, y2, mask, mode):
        if mode == "rectangle":
            mask.rectangle((x1, y1, x2, y2), fill=(255, 255, 255))
        elif mode == "polygon":
            mask.polygon((x1, y1, x1 + random.randint(50, 100), x2 + random.randint(-100, 100), x2, y2),
                         fill=(255, 255, 255))
        elif mode == "pieslice":
            mask.pieslice((x1, y1, x2, y2), 0, -90, fill=(0, 255, 0))
        elif mode == "line":
            mask.line((x1, y1, x1 + random.randint(50, 100), x2 + random.randint(-100, 100), x2, y2),
                      fill=(255, 255, 255), width=random.randint(5, 10))
        elif mode == "ellipse":
            mask.ellipse((x1, y1, x2, y2), fill=(255, 255, 255))
        elif mode == "chord":
            mask.chord((x1, y1, x2, y2), 0, -90, fill=(255, 255, 255))
        else:
            pass


    def image_aug(self, image):
        choose = random.randint(0, len(self.image_aug_list) - 1)
        factor = self.image_aug_factor[choose]
        return self.image_aug_list[choose](image).enhance(random.uniform(factor[0], factor[1]))