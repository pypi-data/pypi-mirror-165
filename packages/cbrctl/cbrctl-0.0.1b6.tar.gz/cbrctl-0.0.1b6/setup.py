#!/usr/bin/env python
import codecs
import os.path
import re
import sys

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


install_requires = [
    'PyYAML',
    'kubernetes',
    'click'
]


setup_options = dict(
    name='cbrctl',
    version=find_version("cbrctl", "__init__.py"),
    description='Universal Command Line Environment for Carbonara.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Carbonara Inc.',
    url='http://trycarbonara.com',
    scripts=['bin/cbrctl'],
    packages=find_packages(),
    install_requires=install_requires,
    license="Apache License 2.0",
    python_requires=">= 3.7"
)

setup(**setup_options)
