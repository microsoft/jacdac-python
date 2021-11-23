from setuptools import setup, find_packages
from jacdac.constants import JD_VERSION

setup(
    version=JD_VERSION,
    packages=find_packages(
        include=['jacdac', 'jacdac.*'], exclude=['*test.py', 'jacdac.examples.*'])

)
