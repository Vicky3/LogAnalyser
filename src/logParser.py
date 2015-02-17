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

ALLOWEDFILTERTYPES = [NAME, DATE, PROTOCOL, REF, TLD]
ALLOWEDCATEGORYTYPES = [NAME, DATE, TIME, PROTOCOL, FILE, RECTYPE, STATUS, SIZE, REF, PROGRAM, OS, LANG, TLD]

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
            This is passed through from setFile
        TypeError
            If at least one of the given filters uses an invalid type. 
            This is passed through from addFilters.
        """
        self.filters = []
        self.categories = []
        self.addFilters(filters)
        self.setFile(f)
    
    def addFilter(self, fil):
        """
        Function that allows to add a filter the parser should follow.
        
        Parameters
        ----------
        fil : Tuple(FilterType, Arg1 [,Arg2])
            Tuple specifying the filter. FilterTypes my be any of (logParser.NAME, logParser.DATE, 
            logParser.PROTOCOL, logParser.REF, logParser.TLD). Arguments are of type String. 
            DATE filter will need 2 arguments, all other only use 1 argument.
            
        Raises
        ------
        TypeError
            If the given filter uses an invalid type.
        """
        if fil[0] not in ALLOWEDFILTERTYPES:
            raise TypeError("Invalid filterType", fil[0])
        else:
            self.filters.append(fil)
    
    def addFilters(self, filterList):
        """
        Function that allows to add a list of filters the parser should follow.
        
        Parameters
        ----------
        filterList : list of Tuple(FilterType, Arg1 [,Arg2])
            Tuple specifying the filter. FilterTypes my be any of (logParser.NAME, logParser.DATE, 
            logParser.PROTOCOL, logParser.REF, logParser.TLD). Arguments are of type String. 
            DATE filter will need 2 arguments, all other only use 1 argument.
            
        Raises
        ------
        TypeError
            If the given filter uses an invalid type.
            This is passed from addFilter()
        """
        for f in filterList:
            self.addFilter(f)
    
    def addCategory(self, cat):
        """
        Function that allows to add a category the parser should look for.
        
        Parameters
        ----------
        cat : CategoryType
            CategoryType my be any of (logParser.NAME, logParser.DATE, logParser.TIME, 
            logParser.PROTOCOL, logParser..FILE, logParser.RECTYPE, logParser.STATUS, logParser.SIZE,
            logParser.REF, logParser.PROGRAM, logParser.OS, logParser.LANG logParser.TLD).
        
        Raises
        ------
        TypeError
            If an invalid CategoryType is given.
        """
        if cat not in ALLOWEDCATEGORYTYPES:
            raise TypeError("Invalid CategoryType", cat)
        else:
            self.categories.append(cat)
            
    
    def addCategories(self, catList):
        """
        Function that allows to add a list of categories the parser should look for.
        
        Parameters
        ----------
        catList : list of CategoryType
            CategoryType my be any of (logParser.NAME, logParser.DATE, logParser.TIME, 
            logParser.PROTOCOL, logParser..FILE, logParser.RECTYPE, logParser.STATUS, logParser.SIZE,
            logParser.REF, logParser.PROGRAM, logParser.OS, logParser.LANG logParser.TLD).
        
        Raises
        ------
        TypeError
            If an invalid CategoryType is given.
            This is passed from addCategory
        """
        for cat in catList:
            self.addCategory(cat)
    
    def setFile(self, fileName):
        """
        Function that allows to set the file the parser should parse.
        
        Parameters
        ----------
        fileName : String
            String containing the complete filename, including the path to the file that should be parsed.
            
        Raises
        ------
        IOError
            If the file with the specified name cannot be opened.
        """
        
        if fileName != None and fileName != '':
            try:
                self.file = file(fileName, 'r')
            except IOError:
                raise IOError("File {} was not found.".format(fileName))
        
    
    def parse(self):
        """
        Function to parse the specified text for the specified categories with the specified filters.
        
        Returns
        -------
        list of dicts
            A dictionary for each category where the keys correspond to the found category bins and the values
            contain the number of occurence. The dictionary furthmore contain pair ("__TITLE__", categoryName).
        """
        pass