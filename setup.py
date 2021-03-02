# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in nothing/__init__.py
from nothing import __version__ as version

setup(
	name='nothing',
	version=version,
	description='Nothing ERPNext Application',
	author='libracore AG',
	author_email='ben.helmy@libracore.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
