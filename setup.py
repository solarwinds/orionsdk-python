#!/usr/bin/python
#
import os
import sys
from setuptools import setup, find_packages

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist')
    os.system('twine upload dist/*')
    sys.exit()

setup(
    name="orionsdk",
    version="0.4.0",  # Update also in __init__ ;
    description="Python API for the SolarWinds Orion SDK",
    long_description="Python client for interacting with the SolarWinds Orion API",
    author="SolarWinds",
    author_email="dan.jagnow@solarwinds.com",
    url='http://github.com/solarwinds/orionsdk-python',
    license='https://github.com/solarwinds/orionsdk-python/blob/master/LICENSE',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    package_data={'': ['LICENSE', 'README.md']},
    include_package_data=True,
    keywords='solarwinds swis orion orionsdk',
    platforms='Posix; MacOS X; Windows',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Internet',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    dependency_links=[],
    install_requires=['six', 'requests'],
)
