from setuptools import find_packages, setup

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name='dgii_rnc',
    version='0.5',
    author='Luis C Garcia',
    packages=find_packages(where="src"),
    install_requires=[
        'polars', 'selenium'
    ],
    license="MIT",
    python_requires = ">=3.10"
)
