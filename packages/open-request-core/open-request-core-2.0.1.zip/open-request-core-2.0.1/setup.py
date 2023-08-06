#!/usr/bin/env python
# -*- coding: utf-8 -*-


import io
import os

from setuptools import setup, find_packages

import open_request_core


cwd = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(cwd, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()


setup(
    name="open-request-core",
    version=open_request_core.__version__,
    packages=find_packages(exclude=["test*"]),
    extras_require={
        "requests": ["requests"],
    },
    description="This is the core module of standard use for requests.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Rocky Peng",
    author_email="rockypengchina@outlook.com",
    url="https://github.com/meanstrong/open-request-core",
    maintainer="Rocky Peng",
    maintainer_email="rockypengchina@outlook.com",
    platforms=["any"],
    include_package_data=True,
    license="GPLv3",
    classifiers=["Programming Language :: Python", "Programming Language :: Python :: 3"],
)
