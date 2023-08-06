#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
import versioneer

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()
with open("README.rst", "r") as fh:
    long_description = fh.read()
with open("requirements.txt", "r") as fh:
    requirements = [line.strip() for line in fh]

test_requirements = []

setup(
    author="Jillian Rowe",
    author_email="jillian@dabbleofdevops.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Helpers to generate different configurations for PCluster",
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="aws_pcluster_helpers",
    name="aws_pcluster_helpers",
    entry_points={
        "console_scripts": [
            "pcluster-helper=aws_pcluster_helpers.cli:cli",
        ],
    },
    packages=find_packages(include=["aws_pcluster_helpers", "aws_pcluster_helpers.*"]),
    data_files=[
        (
            "templates",
            [
                "aws_pcluster_helpers/models/_templates/slurm.config",
            ],
        ),
    ],
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/dabble-of-devops-bioanalyze/aws_pcluster_helpers",
    zip_safe=False,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
