"""
:author: Dmitry Ostroushko
:copyright: (c) 2021 Dmitry Ostroushko


This is a package inintializator __init__.
In __init_ author defines resources which will be imported by package import. 
"""


from .file_library import *
from .xml_library import *
from .exceptions import *

# This is a simple way to import package modules
#import cliannelibrary.file_library
#import cliannelibrary.xml_library
#import cliannelibrary.parse_library


__author__ = 'Dmitry Ostroushko'
__version__ = '0.1.3.1'
__email__ = 'dmitrylianne@gmail.com'
