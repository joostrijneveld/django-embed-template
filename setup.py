#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-embed-template',
    version='0.2.0',
    description='Override blocks in included templates',
    long_description="\n".join([open('README.rst').read(),
                                open('CHANGES.rst').read()]),
    url='https://github.com/joostrijneveld/django-embed-template',
    author='Joost Rijneveld',
    author_email='joost@joostrijneveld.nl',
    license='CC0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: User Interfaces',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='django templates embedding',
    packages=find_packages(),
    install_requires=['django>=1.8'],
)
