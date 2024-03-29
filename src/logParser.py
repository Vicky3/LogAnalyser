# -*- coding: utf-8 -*-
"""
Created on Mon Feb  16 15:7:52 2015

Module containing the parser object handling the parsing of the logfiles.
@author: jpoeppel
"""

import time
import re
from collections import defaultdict

#Category values. These values correspond to the index of the split line array in most cases.
NAME = 0
USER = 2
DATE = 3
TIME = 4
TIMEZONE = 5
RECTYPE = 6
FILE = 7
PROTOCOL = 8
SIZE = 10
STATUS = 9
REF =  11
PROGRAM = 12
#These three categories to not correspond to indices since they are not always present/extractable.
OS = 14
LANG = 13
TLD = 15


binSize = 100

fileRegex = re.compile(r"/*\.[a-z,A-Z]+$")
refRegex = re.compile(r"([a-z,A-Z]+://[^/]+/[^/]+/)")
tldRegex = re.compile(r"\.([a-z,A-Z]+)$")
osRegex = re.compile(r"\(.*(Macintosh|Win[^;\)]+|Sun[^;\)]+|IO[^;\)]+)[;\s\)]")
lanRegex = re.compile(r" \[([a-z,A-Z]{2})\] ")

completeReg = re.compile(r"(\S+) (\S+) (\S+) \[([^:]+):(\d+:\d+:\d+) ([^\]]+)\] \"(?:(?:(\S+) "+ \
                            "(.*?)(?:(?: (\S+)\")|(?:\")))|(?:.\")) (\S+) (\S+) \"(.*)\" \"(.*)\"$")
ALLOWEDFILTERTYPES = [NAME, DATE, PROTOCOL, REF, TLD]
ALLOWEDCATEGORYTYPES = [NAME, DATE, TIME, PROTOCOL, FILE, RECTYPE, 
                        STATUS, SIZE, REF, PROGRAM, OS, LANG, TLD]

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
        self.catMap = {NAME: self._defaultHelper, PROTOCOL: self._defaultHelper, 
                       RECTYPE: self._defaultHelper, DATE: self._defaultHelper,
                       PROGRAM: self._programHelper, TIME: self._timeHelper, 
                       FILE: self._fileHelper, STATUS: self._statusHelper,
                       SIZE: self._sizeHelper, REF: self._refHelper, 
                       OS: self._osHelper, LANG: self._langHelper, TLD: self._tldHelper}
        
    
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
            logParser.PROTOCOL, logParser..FILE, logParser.RECTYPE, logParser.STATUS, 
            logParser.SIZE, logParser.REF, logParser.PROGRAM, logParser.OS, 
            logParser.LANG, logParser.TLD).
        
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
            logParser.PROTOCOL, logParser..FILE, logParser.RECTYPE, logParser.STATUS, 
            logParser.SIZE, logParser.REF, logParser.PROGRAM, logParser.OS, 
            logParser.LANG logParser.TLD).
        
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
            String containing the complete filename, including the path to the file 
            that should be parsed.
            
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
            A dictionary for each category where the keys correspond to the found category 
            bins and the values contain the number of occurence. Each dictionary is stored 
            with the corresponding categoryType as key in the outer dictionary.
        list of Strings
            A list containing all lines that could not be matched at all (invalid format/characters)
            
        Raises
        ------
        IOError
            If no filename was specified but categories were specified. 
            Or the file could not be opened.
        """
        if len(self.categories) == 0:
            return {}, []
        if self.fileName == None:
            raise IOError("No file was specified.")
            
        res = {cat: defaultdict(int) for cat in self.categories}
        invalidLines = []
        start = time.time()
        cats = self.categories
        fils = self.filters
        with open(self.fileName) as parsedFile:
            for line in parsedFile:
                lineValid = True
                lineRes = completeReg.match(line)
                #If the line could not be matched, we deem it invalid (wrong format/invalid chars)
                if lineRes == None:
                    invalidLines.append(line)
                    continue
                lineAr = lineRes.groups()
                for f in fils:
                    if f[0] == DATE:
                        #Date needs to check for potentially 2 conditions
                        try:                            
                            dTime = time.strptime(lineAr[DATE], "%d/%b/%Y")
                        except:
                            print "Invalid date format."
                        else:
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
                    for cat in cats:
                        #Get key for the category with helper functions
                        key = self.catMap[cat](lineAr, cat)
                        res[cat][key] += 1
                                                
        #TODO remove later
        print "Parsing took {} seconds <br>".format(time.time()-start)    
        return res, invalidLines
        
         
    def _defaultHelper(self, lineAr, cat):
        """
        Helping function that returns the key for the default categories 
        (NAME, PROTOCOL and RECTYPE).
        
        Parameters
        ----------
        lineAr : list of Strings
            Split list containing all groups found by the regex previously.
        cat : int
            Category number that is to be analysed.
            
        Returns
        -------
        String
            Unknown, if the category string could not be found, or was not present.
            The category string from the line otherwise.
        
        """
        if lineAr[cat] == None or lineAr[cat] == "-":
            return "Unknown"
        else:
            return lineAr[cat]
        
    def _programHelper(self, lineAr, cat):
        """
        Helping function that returns the key for the program category.
        
        Parameters
        ----------
        lineAr : list of Strings
            Split list containing all groups found by the regex previously.
        cat : int
            Category number that is to be analysed.
            
        Returns
        -------
        String
            Unknown, if the category string could not be found, or was not present.
            The category string from the line otherwise.
        
        """
        if lineAr[cat] == None or lineAr[cat] == "-":
            return "Unknown"
        else:
            return lineAr[cat].split(' ')[0]
        
    def _timeHelper(self, lineAr, cat):
        """
        Helping function that returns the key for the time category.
        
        Parameters
        ----------
        lineAr : list of Strings
            Split list containing all groups found by the regex previously.
        cat : int
            Category number that is to be analysed.
            
        Returns
        -------
        String
            Unknown, if the category string could not be found, or was not present.
            The category string from the line otherwise.
        
        """
        if lineAr[cat] == None or lineAr[cat] == "-":
            return "Unknown"
        else:
            return lineAr[TIME][:2]
        
    def _fileHelper(self, lineAr, cat):
        """
        Helping function that returns the key for the file category.
        
        Parameters
        ----------
        lineAr : list of Strings
            Split list containing all groups found by the regex previously.
        cat : int
            Category number that is to be analysed.
            
        Returns
        -------
        String
            Unknown, if the category string could not be found, or was not present.
            The category string from the line otherwise.
        
        """
        files = fileRegex.search(lineAr[cat] if lineAr[cat] != None else "")
        if files == None:
            return "Unknown"
        else:
            return files.group()
        
    def _statusHelper(self, lineAr, cat):
        """
        Helping function that returns the key for the status category.
        
        Parameters
        ----------
        lineAr : list of Strings
            Split list containing all groups found by the regex previously.
        cat : int
            Category number that is to be analysed.
            
        Returns
        -------
        String
            Unknown, if the category string could not be found, or was not present.
            The category string from the line otherwise.
        
        """
        if lineAr[cat] == None or lineAr[cat] == "-":
            return "Unknown"
        else:
            return "%s00" % lineAr[STATUS][0]

    def _sizeHelper(self, lineAr, cat):
        """
        Helping function that returns the key for the size category.
        
        Parameters
        ----------
        lineAr : list of Strings
            Split list containing all groups found by the regex previously.
        cat : int
            Category number that is to be analysed.
            
        Returns
        -------
        String
            Unknown, if the category string could not be found, or was not present.
            The category string from the line otherwise.
        
        """
        #Might be improvable
        if lineAr[cat] == None or lineAr[cat] == "-":
            return "Unknown"
        else:
            binNr = int(lineAr[cat])/binSize
            return "%i-%i" % (binNr*binSize+1,(binNr+1)*binSize) 
        
    def _refHelper(self, lineAr, cat):
        """
        Helping function that returns the key for the reference category.
        
        Parameters
        ----------
        lineAr : list of Strings
            Split list containing all groups found by the regex previously.
        cat : int
            Category number that is to be analysed.
            
        Returns
        -------
        String
            Unknown, if the category string could not be found, or was not present.
            The category string from the line otherwise.
        
        """
        refRes = refRegex.search(lineAr[cat] if lineAr[cat] != None else "")
        if refRes == None:
            return "Unknown"
        else:
            return refRes.group()
        
    def _osHelper(self, lineAr, cat):
        """
        Helping function that returns the key for the operating system category.
        
        Parameters
        ----------
        lineAr : list of Strings
            Split list containing all groups found by the regex previously.
        cat : int
            Category number that is to be analysed.
            
        Returns
        -------
        String
            Unknown, if the category string could not be found, or was not present.
            The category string from the line otherwise.
        
        """
        isRes= osRegex.search(lineAr[PROGRAM] if lineAr[PROGRAM] != None else "")
        if isRes == None:
            return "Unknown"
        else:
            return isRes.groups()[0]
            
            
    def _langHelper(self, lineAr, cat):
        """
        Helping function that returns the key for the language category.
        
        Parameters
        ----------
        lineAr : list of Strings
            Split list containing all groups found by the regex previously.
        cat : int
            Category number that is to be analysed.
            
        Returns
        -------
        String
            Unknown, if the category string could not be found, or was not present.
            The category string from the line otherwise.
        
        """
        lanRes = lanRegex.search(lineAr[PROGRAM] if lineAr[PROGRAM] != None else "")
        if lanRes == None:
            return "Unknown"
        else:
            return lanRes.groups()[0]
        
    def _tldHelper(self, lineAr, cat):
        """
        Helping function that returns the key for the top-level-domain category.
        
        Parameters
        ----------
        lineAr : list of Strings
            Split list containing all groups found by the regex previously.
        cat : int
            Category number that is to be analysed.
            
        Returns
        -------
        String
            Unknown, if the category string could not be found, or was not present.
            The category string from the line otherwise.
        
        """
        tlds = tldRegex.search(lineAr[NAME] if lineAr[NAME] != None else "")
        
        if tlds == None:
            return "Unknown"
        else:
            return tlds.groups()[0]
            
if __name__=="__main__":
    import profile
    parser=LogParser("../logs/micro_1.log",[])
    parser.addCategories(ALLOWEDCATEGORYTYPES)
    profile.run('parser.parse()')

                
        