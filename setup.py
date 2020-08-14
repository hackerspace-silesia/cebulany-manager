import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'requirements.txt')) as fp:
    requires = fp.readlines()

setup(
    name='cebulany manager',
    version='0.0.4',
    classifiers=[],
    author='Firemark',
    author_email='marpiechula@gmail.com',
    url='https://github.com/hackerspace-silesia/cebulany-manager',
    packages=find_packages(),
    install_requires=requires,
    tests_require=requires,
)
