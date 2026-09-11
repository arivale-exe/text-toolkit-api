#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="text-toolkit",
    version="1.0.0",
    description="x402-gated text processing API for autonomous agents",
    author="Automaton",
    py_modules=["server", "texttoolkit", "api"],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "text-toolkit=server:run_server",
        ],
    },
    python_requires=">=3.8",
    license="MIT",
)