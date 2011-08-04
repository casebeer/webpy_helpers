#!/usr/bin/env python

from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

required_modules = [
	"simplejson",
	"web.py",
	]

setup(
	name="webpy_helpers",
	version="0.0.1",
	description="",
	author="Christopher H. Casebeer",
	author_email="",
	url="",
	py_modules=["webpy_helpers", "distribute_setup"],
	#packages=find_packages(exclude='tests'),
	install_requires=required_modules
	)

