# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     Affine
   Description :   
   Author :       lth
   date：          2022/8/26
-------------------------------------------------
   Change Activity:
                   2022/8/26 6:08: create this script
-------------------------------------------------
"""
__author__ = 'lth'

import cv2
import numpy as np


class Affine:
    """
    opencv tools , used for data augment

    """

    @staticmethod
    def translate(img):
        """
        this function is used to translate the image in the filed

        img should be np.ndarray

        mat=[[1,0,x],
             [0,1,y]]

         ______________________> x
        |
        |
        v
        y
        """

        assert type(img) is np.ndarray, "the type of the img should be np.ndarray ,or it will not be supported"

        mat = np.array([[1, 0, 0], [0, 1, 200]], dtype=float)
        img = cv2.warpAffine(img, mat, (img.shape[:2][::-1]))
        return img

    @staticmethod
    def resize(img):
        """
        used to resize the data

        img:np.ndarray
        """
        assert type(img) is np.ndarray, "the type of the img should be np.ndarray ,or it will not be supported"

        return cv2.resize(img, dsize=None, fx=0.5, fy=0.5)

    @staticmethod
    def resize2(img):
        """
        used to resize the data

        img:np.ndarray
        """
        assert type(img) is np.ndarray, "the type of the img should be np.ndarray ,or it will not be supported"

        return image[::2, ::2]

    @staticmethod
    def rotate(img):
        """
        used to rotate the data

        img:np.ndarray
        """
        assert type(img) is np.ndarray, "the type of the img should be np.ndarray ,or it will not be supported"

        center = img.shape[:2][::-1]
        angle = -45

        M = cv2.getRotationMatrix2D(center, angle, 1)
        img = cv2.warpAffine(img, M, img.shape[:2][::-1])
        return img

    @staticmethod
    def mirror_v(img):
        """
        used to mirror in vertical direction to aug the data

        img:np.ndarray
        """
        assert type(img) is np.ndarray, "the type of the img should be np.ndarray ,or it will not be supported"

        return img[::-1]

    @staticmethod
    def mirror_h(img):
        """
        used to mirror in horizontal direction to aug the data

        img:np.ndarray
        """
        assert type(img) is np.ndarray, "the type of the img should be np.ndarray ,or it will not be supported"
        img = img.transpose(1, 0, 2)
        img = img[::-1]
        img = img.transpose(1, 0, 2)
        return img

    @staticmethod
    def mirror_hw(img):
        """
        used to mirror both in horizontal and vertical direction to aug the data

        img:np.ndarray
        """
        assert type(img) is np.ndarray, "the type of the img should be np.ndarray ,or it will not be supported"
        img = Affine.mirror_h(img)
        img = Affine.mirror_v(img)
        return img

    @staticmethod
    def show(img):
        """
        used to show the image

        img:np.ndarray
        """
        assert type(img) is np.ndarray, "the type of the img should be np.ndarray, or it will not be supported"

        cv2.imshow("test", img)
        cv2.waitKey()

    @staticmethod
    def make_img_black_ground(shape):
        """
        used to create a black ground

        shape:(w,h) w and h is int  respectively
        """
        return np.zeros(shape, dtype=np.uint8)

    @staticmethod
    def make_img_random_background(img):
        shape = img.shape[:2]

        # [low,high)
        img = np.random.randint(0, 2, size=shape) * 255
        return img.astype(np.uint8)

    @staticmethod
    def make_img_with_lines(img):
        """
        used to creat lines in the image

        img:np.ndarray
        """
        shape = img.shape[:2]
        img = Affine.make_img_black_ground(shape)
        img[:, 10:20] = 255
        img[10:20, :] = 255
        return img

    """
    均值滤波︰算法简单，计算速度快，在去噪的同时去除了很多细节部分，将图像变得模糊
    高斯滤波:去除高斯噪声
    中值滤波:去除椒盐噪声
    """

    @staticmethod
    def gaussian_blur(img):
        """
        used to make the image blur in the method of gaussian

        img:np.ndarray
        """
        return cv2.GaussianBlur(img, (11, 11), 0)

    @staticmethod
    def mean_blur(img):
        """
        used to make the image blur in the method of mean_blur

        img:np.ndarray
        """
        kernel = np.array([[1, 1, 1],
                           [1, 1, 1],
                           [1, 1, 1]], np.float)

        return cv2.filter2D(img, -1, kernel / 9)

    @staticmethod
    def median_blur(img):
        """
        used to make the image blur in the method of median_blur

        img:np.ndarray
        """
        return cv2.medianBlur(img, 5)

    @staticmethod
    def sharpen_laplace(img):
        """
        used to sharpen the image in the method of laplace

        img:np.ndarray
        """
        kernel = np.array([[-1, -1, -1],
                           [-1, 9, -1],
                           [-1, -1, -1]], np.float)

        # kernel = np.array([[0, -1, 0],
        #                    [-1, 5, -1],
        #                    [0, -1, 0]], np.float)

        return cv2.filter2D(img, -1, kernel)

    @staticmethod
    def color2gray(img):
        """
        this is used to convert the image to the gray from BGR, since the function imread output the image in BGR format

        img:np.ndarray
        """
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def threshold(img):
        """
        this is used to make the image binarize

        img:np.ndarray and len(img.shape) should be 2
        """
        img = Affine.color2gray(img)
        _, ret = cv2.threshold(img, 200, 255, cv2.THRESH_OTSU)
        return ret

    @staticmethod
    def merge2one(img1, img2):
        assert img1.shape == img2.shape, "the shape should be same"

        return cv2.addWeighted(img1, 0.5, img2, 0.5, 1)

    @staticmethod
    def vstack(img1, img2):
        assert img1.shape == img2.shape, "the shape should be same"

        return np.vstack([img1, img2])

    @staticmethod
    def hstack(img1, img2):
        assert img1.shape == img2.shape, "the shape should be same"

        return np.hstack([img1, img2])

    @staticmethod
    def yoco(img1, img2):
        """
        a way to make data aug
        """
        assert img1.shape == img2.shape, "the shape should be same"
        height, width = img1.shape[:2]
        middle = width // 2

        img = np.zeros_like(img1)

        img[:middle, ...] = img2[:middle, ...]
        img[middle:, ...] = img2[middle:, ...]
        return img1

    @staticmethod
    def warpaffine(img):
        height, width = img.shape[:2]
        mat_src = np.float32([[0, 0], [0, height - 1], [width - 1, 0]])
        mat_dst = np.float32([[50, 50], [100, height - 100], [width - 100, 100]])

        mat_trans = cv2.getAffineTransform(mat_src, mat_dst)  # matrix shape (2,3)
        dst = cv2.warpAffine(img, mat_trans, (width, height))
        return dst
