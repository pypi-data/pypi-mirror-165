# -*- coding: utf-8 -*-
#from setuptools import setup, find_packages

from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
#print("packages=find_packages()", find_packages())
setup(
    name="verilog_crypt", # package name
    version="0.0.2",
    author="author",
    author_email="author@innochip.com",
    description="verilog crypt package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/pypa/verilog_crypt_project",
    packages=find_packages(),
    package_data={
        'verilog_crypt': ['crypt_algo.cpython-38-x86_64-linux-gnu.so',
                        'crypt_interface.cpython-38-x86_64-linux-gnu.so',
                        'crypt_local.cpython-38-x86_64-linux-gnu.so',
                        'module.cpython-38-x86_64-linux-gnu.so',
                        'crypt_local_def_rules.txt',
                        'crypt_module_def_rules.txt']
    },
    platforms="Linux",
    #py_modules=['mytest.testc']
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
