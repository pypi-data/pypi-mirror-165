#!/usr/bin/env python3

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="nornir-maze",
    version="0.0.14",
    author="Willi Kubny",
    author_email="willi.kubny@gmail.com",
    description="A collection of Nornir tasks and functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/willikubny/nornir-maze",
    project_urls={
        "Repository": "https://github.com/willikubny/nornir-maze",
        "Bug Tracker": "https://github.com/willikubny/nornir-maze/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.9",
)
