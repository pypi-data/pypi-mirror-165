"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path
from util import read_version
import shutil

here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

version=read_version.get_version_from_file('VERSION')
public_version=read_version.get_version_from_file('PUBLIC_VERSION')
setup(
    install_requires=[
        "spark-nlp==4.0.0" #+ public_version
    ],
    name="internal-with-fin",  # Required
    version='0.1.7',##version,
    description="NLP Text processing library built on top of Apache Spark",
    long_description=long_description,
    url="http://nlp.johnsnowlabs.com",
    author="John Snow Labs",
    author_email="john@johnsnowlabs.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="NLP spark development",  # Optional
    packages=find_packages(exclude=["test_jsl"]),
    include_package_data=True,  # Needed to install jar file
)
