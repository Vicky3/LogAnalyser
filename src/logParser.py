# -*- coding: utf-8 -*-
"""
Created on Mon Feb  16 15:7:52 2015

Module containing the parser object handling the parsing of the logfiles.
@author: jpoeppel
"""

NAME = 0
DATE = 1
PROTOCOL = 2
FILE = 3
RECTYPE = 4
STATUS = 5
SIZE = 6
REF =  7
PROGRAM = 8
OS = 9
LANG = 10
TLD = 11

class LogParser(object):
    
    def __init__(self, f = None, filters = []):
        """
        Constructor for the LogParser.
        
        Parameters
        ----------
        f : String, optional
            Path to the file that is to be parsed (Default None)
        filters : list of tuple(TYPE, Arg1 [, Arg2])
            List of filters that should be applied. A filter is always a tuple consisting of the type
            which can be any of (NAME, DATE, PROTOCOL, REF, TLD)
            
        
        Raises
        ------
        IOError
            If the given file cannot be opened.
        TypeError
            If at least one of the given filters uses an invalid type.
        """
        pass
    
    def addFilter(fil):
        pass
    
    def addFilters(filterList):
        pass
    
    def addCategory(cat):
        pass
    
    def addCategories(catList):
        pass
    
    def setFile(fileName):
        pass
    
    def parse():
        pass