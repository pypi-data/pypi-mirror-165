#!/usr/bin/env python3
#
# Copyright DSDL Team of OpenDatalab. All rights reserved.
#

"""Setup file."""

from setuptools import setup, find_packages


def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content


version = {}
with open("tunas2dsdl/__version__.py") as version_file:
    exec(version_file.read(), version)

setup(
    name="tunas2dsdl",
    version=version["__version__"],
    description="Python SDK for Converting Tunas Format Dataset to DSDL YAML",
    long_description=readme(),
    long_description_content_type='text/markdown',
    author="DSDL team",
    author_email="hanxiao@pjlab.org.cn",
    packages=find_packages(),
    package_data={},
    include_package_data=True,
    install_requires=[
        "click>=8.1.3",
        "ruamel.yaml>=0.17.21",
        "tqdm>=4.64.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "tunas2dsdl = tunas2dsdl.cli:cli",
        ],
    },
)
