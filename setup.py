"""Setup."""

from pathlib import Path

from setuptools import find_packages, setup

with Path("README.md").open(encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name="dgii_rnc",
    version="0.6",
    author="Luis C Garcia",
    packages=find_packages(where="src"),
    install_requires=["polars", "selenium", "webdriver-manager"],
    license="MIT",
    python_requires=">=3.11",
)
