#!/usr/bin/python
from distutils.core import setup
from setuptools import find_packages

setup(
    name='realtime_congress',
    description='Real Time Congress API Python Wrapper',
    long_description='Python wrapper for the Sunlight Foundation\'s Real Time Congress API.',
    author='Charlotte Python Group',
    author_email='flaviu@govkick.com',
    url='http://govkick.com/',
    packages=find_packages(),
)
