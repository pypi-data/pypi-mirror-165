#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import find_packages, setup

EXCLUDE_FROM_PACKAGES = ["contrib", "docs", "test*"]
CURDIR = os.path.abspath(os.path.dirname(__file__))


def load_requirements(fname):
    try:
        from pip._internal.req import parse_requirements
    except ImportError:
        from pip.req import parse_requirements
    reqs = parse_requirements(fname, session="test")
    try:
        return [str(ir.req) for ir in reqs]
    except:
        return [str(ir.requirement) for ir in reqs]


with open("README.md") as f:
    readme = f.read()

setup(
    name="i2b2rls",
    version="0.0.5",
    description="i2b2 user management with PostgreSQL Row Level Security",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Fabian Thomczyk",
    author_email="fabian.thomczyk@uniklinik-freiburg.de",
    url="https://gitlab.com/mds-imbi-freiburg/i2b2/i2b2rls",
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "i2b2rls=i2b2rls.i2b2fire:main",
        ]
    },
    zip_safe=False,
    install_requires=load_requirements("requirements.txt"),
    python_requires=">=3.6",
    license="License :: MIT License",
)
