#!/usr/bin/env python3

from setuptools import setup

setup(
    name="blueos_bootstrap",
    version="0.0.1",
    description="Blue Robotics BlueOS Docker System Bootstrap",
    license="MIT",
    install_requires=["docker == 5.0.0", "six == 1.15.0", "requests == 2.26.0"],
)
