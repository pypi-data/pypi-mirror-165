#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: bb(bobby.miao)
# Description: APP Launch Test

from setuptools import setup, find_packages

setup(
    name='bblt',
    version='1.0.5',
    keywords='launchtest',
    description='APP Launch Test',
    license='MIT License',
    url='https://github.com/xiaoyaoamiao/lt.git',
    author='bob',
    author_email='miao2005du@163.com',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[
            'matplotlib >= 3.5.0',
            'ImageHash >= 4.2.1',
            'facebook-wda  >= 1.0.11',
            'pandas >= 1.3.4',
            'Pillow >= 8.1.0',
            'uiautomator2>=2.16.13',
            'Pillow == 8.1.0'
        ],
)