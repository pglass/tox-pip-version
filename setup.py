#!/usr/bin/env python

import setuptools

setuptools.setup(
    name='tox-pip-version',
    author='Paul Glass',
    author_email='pnglass@gmail.com',
    description='Select PIP version to use with tox',
    url='https://github.com/pglass/tox-pip-version',
    license='MIT',
    version='0.0.1',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['tox>=2.0'],
    entry_points={'tox': 'pip_version = tox_pip_version.hooks'},
    package_dir={'baremetal_qe_common': 'baremetal_qe_common'},
)
