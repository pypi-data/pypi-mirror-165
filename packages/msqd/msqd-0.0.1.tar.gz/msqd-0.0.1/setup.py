#! /usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='msqd',
    version='0.0.1',
    description='Trading strategy development and deployment.',
    long_description='This is a general-purpose library for designing, tesing and deploying algorithmic trading strategies.',
    author='Samuel Naughton Baldwin',
    author_email='sam.naughton2000@gmail.com',
    packages=find_packages(exclude=['tests*']),
    package_dir={'msqd': 'src/msqd'},
)