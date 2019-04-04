#!/usr/bin/env python

long_description = open('README.md').read()

import setuptools

setuptools.setup(
    name='tox-pip-version',
    author='Paul Glass',
    author_email='pnglass@gmail.com',
    description='Select PIP version to use with tox',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/pglass/tox-pip-version',
    license='MIT',
    version='0.0.4',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['tox>=2.0'],
    entry_points={
        'tox': 'pip_version = tox_pip_version.hooks'
    },
    package_dir={
        'tox_pip_version': 'tox_pip_version'
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Framework :: tox',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
