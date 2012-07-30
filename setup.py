#!/usr/bin/env python

from setuptools import setup, find_packages

required_modules = [
	"simplejson",
	"web.py",
	]

readme = """
Web.py Helpers
"""

setup(
	name="webpy_helpers",
	version="0.0.2",
	description="",

	author="Christopher H. Casebeer",
	author_email="",
	url="https://github.com/casebeer/webpy_helpers",

	py_modules=["webpy_helpers"],
	install_requires=required_modules,

	tests_require=["nose"],
	test_suite="nose.collector",

	long_description=readme,
	classifiers=[
		"License :: OSI Approved :: BSD License",
		"Intended Audience :: Developers",
	]
)

