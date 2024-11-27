# setup.py
from setuptools import setup, find_packages

setup(
    name="chord",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
)