#!/usr/bin/env python

long_description = open("README.md").read()

import setuptools

setuptools.setup(
    name="tox-setuptools-version",
    author="LvffY",
    author_email="louberger@hotmail.fr",
    description="Select SETUPTOOLS version to use with tox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LvffY/tox-setuptools-version",
    license="MIT",
    version="0.0.0.1",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["tox>=2.0"],
    entry_points={"tox": ["setuptools_version = tox_setuptools_version.hooks"]},
    package_dir={"tox_setuptools_version": "tox_setuptools_version"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Framework :: tox",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    keywords=("tox", "setuptools", "2to3"),
)
