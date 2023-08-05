from io import open
from setuptools import setup

"""
:author: Dmitry Ostroushko
:copyright: (c) 2021 Dmitry Ostroushko
"""

version = '0.1.3.0'
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cliannelibrary',
    version=version,

    author='Dmitry Ostroushko',
    author_email='dmitrlylianne@gmail.com',

    description=(
        u'Python module includes useful utilities for XML processing and woring with files.'
        u'Clianne Libraries'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/DmitryOstroushko/cliannelibrary',

    license='Apache License, Version 2.0, see LICENSE file',

    packages=['cliannelibrary'],
    install_requires=[],

    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython'
    ]
)
