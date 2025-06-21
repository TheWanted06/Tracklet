import os

version_ns = {}
with open(os.path.join("tracklet", "_version.py")) as f:
    exec(f.read(), version_ns)

from setuptools import setup, find_packages

setup(
    name="tracklet",
    version=version_ns["__version__"],
    packages=find_packages(),
    install_requires=[
        "InquirerPy",
        "pyyaml>=6.0",
        "PyYAML",
        "rich"
    ],
    entry_points={
        "console_scripts": [
            "tracklet=tracklet.cli:main",
        ],
    },
    author="Daniel",
    description="Local project tracking and metadata management system",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
