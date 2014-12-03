#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import njode
version = njode.__version__

setup(
    name='njode',
    version=version,
    author='',
    author_email='agc11d@gmail.com',
    packages=[
        'njode',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.7.1',
    ],
    zip_safe=False,
    scripts=['njode/manage.py'],
)