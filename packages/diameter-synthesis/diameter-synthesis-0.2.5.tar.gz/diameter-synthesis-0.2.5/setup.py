#!/usr/bin/env python

import imp
import sys
from pathlib import Path

from setuptools import setup, find_packages

if sys.version_info < (2, 7):
    sys.exit("Sorry, Python < 2.7 is not supported")

VERSION = imp.load_source("", "diameter_synthesis/version.py").__version__

setup(
    name="diameter-synthesis",
    author="BlueBrain Cells",
    version=VERSION,
    description="Diametrize cells",
    long_description=Path("README.rst").read_text(encoding="utf-8"),
    long_description_content_type="text/x-rst",
    license="GNU General Public License v3.0",
    url="https://diameter-synthesis.readthedocs.io",
    project_urls={
        "Tracker": "https://github.com/BlueBrain/diameter-synthesis/issues",
        "Source": "https://github.com/BlueBrain/diameter-synthesis",
    },
    install_requires=[
        "click>=7.0",
        "jsonschema>=3",
        "matplotlib>=2.2.0",
        "morphio>=2.3.4",
        "neurom>=3.0,<4.0",
        "numpy>=1.15.0",
        "pandas>=0.24.0",
        "scipy>=0.13.3",
    ],
    extras_require={'plot': 'seaborn>=0.11.1'},
    entry_points={
        "console_scripts": ["diameter-synthesis=diameter_synthesis.cli:cli"],
    },
    python_requires=">=3.6",
    packages=find_packages(include=["diameter_synthesis*"], exclude=["tests"]),
    include_package_data=True,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
