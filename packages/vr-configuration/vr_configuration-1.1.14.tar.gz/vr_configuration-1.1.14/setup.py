# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',

        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    description='A Configuration management system for Python projects.',
    entry_points={
    },
    url='https://gitlab.com/dfki/ra/ni/ol/iml/vr/vr.configuration/',
    author='Bengt Lüers',
    author_email='bengt.lueers@gmail.com',
    install_requires=[
    ],
    long_description=(
        open('README.md').read()
    ),
    long_description_content_type='text/markdown',
    maintainer='Bengt Lüers',
    maintainer_email='bengt.lueers@gmail.com',
    name='vr_configuration',
    packages=find_packages(exclude=['test', 'tests']),
    package_data={
        '': ['py.typed'],
    },
    setup_requires=[
    ],
    version='1.1.14',
)
