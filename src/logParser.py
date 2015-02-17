# -*- coding: utf-8 -*-
"""
Created on Mon Feb  16 15:7:52 2015

Module containing the parser object handling the parsing of the logfiles.
@author: jpoeppel
"""

import time
import re

NAME = 0
DATE = 3
TIME = 4
PROTOCOL = 7
FILE = 6
RECTYPE = 5
STATUS = 8
SIZE = 9
REF =  10
PROGRAM = 11
OS = 12
LANG = 13
TLD = 1

ALLOWEDFILTERTYPES = [NAME, DATE, PROTOCOL, REF, TLD]
ALLOWEDCATEGORYTYPES = [NAME, DATE, TIME, PROTOCOL, FILE, RECTYPE, STATUS, SIZE, REF, PROGRAM, OS, LANG, TLD]

class LogParser(object):
    
    def __init__(self, fileName = None, filters = []):
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
        TypeError
            If at least one of the given filters uses an invalid type. 
            This is passed through from addFilters.
            Is also thrown if fileName is not a string.
        """
        self.filters = []
        self.categories = []
        self.addFilters(filters)
        self.setFile(fileName)
    
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
        TypeError
            If the filename is not a string.
        """
        
        if fileName != None and not isinstance(fileName, str):
            raise TypeError("Filename must be a string.")
        else:
            self.fileName = fileName
    
    def parse(self):
        """
        Function to parse the specified text for the specified categories with the specified filters.
        
        Returns
        -------
        dic of dicts
            A dictionary for each category where the keys correspond to the found category bins and the values
            contain the number of occurence. Each dictionary is stored with the corresponding categoryType
            as key in the outer dictionary.
            
        Raises
        ------
        IOError
            If no filename was specified but categories were specified. Or the file could not be opened.
        """
        if len(self.categories) == 0:
            return {}
        if self.fileName == None:
            raise IOError("No file was specified.")
            
        res = {{} for cat in self.categories}

        
        with open(self.fileName) as parsedFile:
            for line in parsedFile:
                lineValid = True
                lineAr = line.split(' ')
                for f in self.filters:
                    if f[0] == DATE:
                        #Date needs to check for potentially 2 conditions
                        dString = lineAr[DATE][1:11]
                        dTime = time.strptime(dString, "%d/%b/%Y")
                        if (f[1] != None and dTime < f[1]) or (f[2] != None and dTime > f[2]):
                            lineValid = False
                            break
                    elif f[0] == TLD:
                        #TLDs are part of the name
                        if lineAr[NAME][lineAr[NAME].rfind('.')+1:] != f[1]:
                            lineValid = False
                            break
                    else:
                        # Name, Protocol and Ref just search for their arguments in the respective fields.
                        if lineAr[f[0]].find(f[1]) < 0:
                            lineValid = False
                            break
                if lineValid:
                    for cat in self.categories:
                        if cat in [NAME, PROTOCOL, RECTYPE, PROGRAM]:
                            if res[cat].has_key(lineAr[cat]):
                                res[cat][lineAr[cat]] += 1
                            else:
                                res[cat][lineAr[cat]] = 1
                        elif cat == DATE:
                            dString = lineAr[DATE][:10]
                            if res[cat].has_key(dString):
                                res[cat][dString] += 1
                            else:
                                res[cat][dString] = 1
                        elif cat == TIME:
                            hString = lineAr[DATE][12:14]
                            if res[cat].has_key(hString):
                                res[cat][hString] += 1
                            else:
                                res[cat][hString] = 1
                        elif cat == FILE:
                            regex = re.compile(r"/*.[a-z,A-Z]+$")
                            files = regex.search(lineAr[FILE])
                            
                        pass
                                            
                        
                
            
        return res

                
        