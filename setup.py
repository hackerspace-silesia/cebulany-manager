import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'Flask-RESTful==0.3.8',
    'Flask-SQLAlchemy==2.4.4',
    'flask-cors==3.0.8',
    'uwsgi==2.0.19.1',
    'alembic==1.4.2',
    'onetimepass==1.0.1',
]

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
