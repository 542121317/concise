#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "numpy",
    "pandas",
    "scipy",
    "scikit-learn",
    "matplotlib",
    "tensorflow",
]

test_requirements = [
    "pytest",
]

setup(
    name='concise',
    version='0.1.0',
    description="CONCISE (COnvolutional Neural for CIS-regulatory Elements) is a model for predicting PTR features like mRNA half-life from cis-regulatory elements using deep learning. ",
    long_description=readme + '\n\n' + history,
    author="Žiga Avsec",
    author_email='avsec@in.tum.de',
    url='https://github.com/avsecz/concise',
    packages=find_packages(),
    package_dir={'concise':
                 'concise'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='concise',
    classifiers=[
        # classifiers
        'Bioinformatics',
        'Genomics',
        # default
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        # "Programming Language :: Python :: 2",
        # 'Programming Language :: Python :: 2.6',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
