from setuptools import setup

setup(
    name="text-toolkit-api",
    version="1.0.0",
    description="x402-gated text processing API for AI agents",
    packages=["text_toolkit"],
    install_requires=["requests>=2.28.0"],
    entry_points={
        "console_scripts": [
            "text-toolkit=text_toolkit.cli:cli",
        ],
    },
)