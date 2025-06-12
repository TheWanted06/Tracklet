from setuptools import setup, find_packages

setup(
    name="tracklet",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyyaml>=6.0",
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
