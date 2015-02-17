# -*- coding: utf-8 -*-
"""
Created on Mon Feb  16 15:7:52 2015

Module containing the parser object handling the parsing of the logfiles.
@author: jpoeppel
"""

NAME = 0
DATE = 1
TIME = 2
PROTOCOL = 3
FILE = 4
RECTYPE = 5
STATUS = 6
SIZE = 7
REF =  8
PROGRAM = 9
OS = 10
LANG = 11
TLD = 12

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
            which can be any of (logParser.NAME, logParser.DATE, logParser.PROTOCOL, logParser.REF, 
            logParser.TLD)
            
        
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
        """
        Function to parse the specified text for the specified categories with the specified filters.
        
        Returns
        -------
        list of dicts
            A dictionary for each category where the keys correspond to the found category bins and the values
            contain the number of occurence. The dictionary furthmore contain pair ("__TITLE__", categoryName).
        """
        pass