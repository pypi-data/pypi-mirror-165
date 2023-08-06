# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pyriandx",
    # version=__version__,
    author="UMCCR and Contributors",
    author_email="services@umccr.org",
    description="API client CLI/SDK for PierianDx web services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/umccr/pyriandx",
    license="MIT",
    packages=find_packages(exclude=("tests", "docs")),
    package_data={
        "pyriandx": ["json/*.json"]
    },
    entry_points={
        "console_scripts": ["pyriandx=pyriandx.cli:main"]
    },
    project_urls={
        "Bug Tracker": "https://github.com/umccr/pyriandx/issues",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    extras_require={
        "dev": [
            "pipdeptree",
            "sphinx",
            "twine",
            "setuptools",
            "wheel",
            "build",
            "pdoc3",
            "tox",
            "nose2",
            "pre-commit",
            "detect-secrets",
            "ggshield",
        ],
        "test": [
            "pytest",
            "pytest-cov",
            "flake8",
            "mockito",
        ],
    },
    install_requires=[
        "requests",
        "urllib3",
        "docopt",
        "coloredlogs",
        "verboselogs",
        "colorama",
    ],
    python_requires=">=3.6",
)
