from setuptools import setup
import os
from redis_sessions import __version__

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

packages = ['aerospike_sessions']


setup(
    name='django-aerospike-sessions',
    version=__version__,
    description= "Aerospike Session Backend For Django",
    long_description=read("README.md"),
    keywords='django, sessions,',
    license='BSD',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
)
