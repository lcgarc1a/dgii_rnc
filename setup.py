from setuptools import setup, find_packages

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name='dgii_rnc',
    version='0.4',
    author='Luis C Garcia',
    packages=find_packages(where="src"),
    install_requires=[
        'polars'
    ],
    license="MIT",
    python_requires = ">=3.6"
)
