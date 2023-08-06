#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = "tdviewer",
    version = "0.0.2",
    keywords = ["pip", "3d", "pcd", "pointcloud"],
    description = "点云数据可视化模块",
    long_description = "点云数据可视化模块",
    license = "MIT Licence",

    url = "https://github.com/hide-in-code",
    author = "hejinlong",
    author_email = "2969921454@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["opencv-python", "open3d-python", "vedo"]
)
