# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     setup
   Description :   
   Author :       lth
   date：          2022/8/26
   information:   account  :luotianhang_amazing
                  password :Woaini139*
-------------------------------------------------
   Change Activity:
                   2022/8/26 3:11: create this script
-------------------------------------------------
https://blog.csdn.net/weixin_38346042/article/details/123422231

how to use:

python setup.py sdist
twine upload dist/*




"""
__author__ = 'lth'

import setuptools

with open("README.md","r",encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LTHTools",
    version="1.0.1", # first 0 means test
    author="lth",
    author_email="673567903@qq.com",
    description="this package is used for author only",
    long_description=long_description,
    long_description_content_type = "text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    packages=setuptools.find_packages(),

)

