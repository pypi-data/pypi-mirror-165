#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# System modules
import os
import sys
import runpy
from setuptools import setup, find_packages


def read_file(filename):
    with open(filename, errors="ignore") as f:
        return f.read()


packages = find_packages(exclude=["tests"])

rpm_package = "python3-" + packages[0]
try:
    rpm = "rpm" in sys.argv[1]
except IndexError:
    rpm = False

# run setup
setup(
    name=rpm_package if rpm else packages[0],
    description="Pythonic access to the OpenSenseMap API",
    author="Yann Büchau",
    author_email="nobodyinperson@gmx.de",
    keywords="opensensemap,sensemap,api",
    license="GPLv3",
    version=runpy.run_path(os.path.join(packages[0], "version.py")).get(
        "__version__", "0.0.0"
    ),
    url="https://gitlab.com/tue-umphy/co2mofetten/software/python3-sensemapi",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    install_requires=["requests", "click>=7"],
    tests_require=["numpy", "pandas", "click>=7"],
    extras_require={
        "pandas": ["pandas>=0.23.4"],
        "cache": ["CacheControl[filecache]>=0.12.5"],
        "mqtt": ["paho-mqtt>=1.4", "pandas>=0.23.4"],
    },
    entry_points={
        "console_scripts": ["sensemapi = sensemapi.cli.commands.main:cli"],
        "sensemapi.commands": [
            "route-mqtt = sensemapi.cli.commands.route_mqtt:route_mqtt [mqtt]"
        ],
    },
    test_suite="tests",
    packages=packages,
)
