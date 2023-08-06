#!/usr/bin/env python3

# BoBoBo

from setuptools import setup, find_packages

setup(
    name='boon-common',
    version='1.0.0-beta.1',
    keywords=("common", "utils", "protocol"),
    url='https://github.com/bobobozzz/boon.git',
    author='bobobocode',
    author_email='bobobomail@yeah.net',
    description="Common Modules",
    packages=find_packages(),
    install_requires=['DBUtils==2.0',
                      'pyyaml==5.3.1'],
    include_package_data=True,
    platforms="any",
    license="GPL v3.0"
)
