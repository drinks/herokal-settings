from herokal import __version__
from setuptools import setup, find_packages

long_description = open('README.rst').read()

setup(
    name="herokal_settings",
    version=__version__,
    author="Dan Drinkard",
    author_email="dan.drinkard@gmail.com",
    url="https://github.com/drinks/herokal-settings",
    description="Make your django local_settings play nice with Heroku",
    long_description=long_description,
    license='BSD',
    packages=find_packages(),
    install_requires=['dj-database-url'],
    platforms=['any']
)
