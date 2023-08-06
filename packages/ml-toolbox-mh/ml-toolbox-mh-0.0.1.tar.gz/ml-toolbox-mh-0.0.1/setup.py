# _*_ coding: utf-8 _*_
# @Time        :  2022/8/31 13:23
# @Author      :  Wenfeng Min
# @File        :  setup.py

import setuptools


setuptools.setup(
    name="ml-toolbox-mh",   # 库的名字
    version="0.0.1",   # 库的版本号
    author="soft",
    author_email="18415507@qq.com",
    description="月亮小屋算法技术团队ML工具箱",
    long_description_content_type="text/markdown",
    url="https://github.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
