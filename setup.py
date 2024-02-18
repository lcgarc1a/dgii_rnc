from setuptools import setup, find_packages

setup(
    name='dgii_rnc',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'polars[all]'
    ],
)
