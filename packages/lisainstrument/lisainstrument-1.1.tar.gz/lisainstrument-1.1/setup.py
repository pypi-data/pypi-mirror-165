#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-module-docstring,exec-used

from typing import Dict
import setuptools


with open("README.md", 'r', encoding='utf-8') as fh:
    long_description = fh.read()

META: Dict[str, str] = {}
with open("lisainstrument/meta.py", 'r', encoding='utf-8') as file:
    exec(file.read(), META)

setuptools.setup(
    name='lisainstrument',
    version=META['__version__'],
    author=META['__author__'],
    author_email=META['__email__'],
    description='LISA Instrument simulates instrumental noises, propagates laser beams, generates measurements and the on-board processing to deliver simulated telemetry data.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.in2p3.fr/lisa-simulation/instrument",
    packages=setuptools.find_packages(),
    install_requires=[
        'h5py',
        'numpy',
        'scipy',
        'matplotlib',
        'lisaconstants',
        'packaging',
    ],
    tests_require=['pytest'],
    python_requires='>=3.7',
)
