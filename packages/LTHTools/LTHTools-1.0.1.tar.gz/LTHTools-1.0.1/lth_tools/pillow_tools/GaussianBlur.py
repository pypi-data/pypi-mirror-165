# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     GaussianBlur
   Description :   
   Author :       lth
   date：          2022/8/26
-------------------------------------------------
   Change Activity:
                   2022/8/26 6:02: create this script
-------------------------------------------------
"""
__author__ = 'lth'

from PIL import ImageFilter


class GaussianBlur(ImageFilter.Filter):
    name = "GaussianBlur"

    def __init__(self, radius=2, bounds=None):
        self.radius = radius
        self.bounds = bounds

    def filter(self, image):
        if self.bounds:
            clips = image.crop(self.bounds).gaussian_blur(self.radius)
            image.paste(clips, self.bounds)
            return image
        else:
            return image.gaussian_blur(self.radius)
