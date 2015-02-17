#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 14:37:52 2015

Main script started by the website.
Will give arguments to parser and start parsing.

TODO finish doc when script grows!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

@author: adreyer
"""
#Needed to show plain text on website. Maybe has to be deleted when html is
#built.
print "Content-Type: text/plain\n"

import cgi,cgitb
import time
import logParser
import svgCreator

#Path where the log files are found.
LOG_DIRECTORY="../logs/"

def giveArgumentsToParser(params):
    """

    Reads in the arguments from the website. Checks if the dates have valid
    format. Builds a logParser that knows which arguments are given.

    Parameters
    ----------
    params : FieldStorage
             the arguments given by the website

    Returns
    -------
    logParser
        the parser that knows which arguments are given
    """
    #build name of requested log file
    logfile=None
    if "log" in params:
        logfile=LOG_DIRECTORY+params["log"].value+".log"

    #checks what filters are given
    filters=[]
    ##first look for valid dates
    date1=None
    date2=None
    if "cdate1" in params:
        try:
            date1=time.strptime(params["cdate1"].value.lstrip().rstrip(),
                          "%d/%b/%Y")
        except ValueError:
            print "First date does not have the right format. Will not " + \
                "use a filter here."
    if "cdate2" in params:
        try:
            date2=time.strptime(params["cdate2"].value.lstrip().rstrip(),
                          "%d/%b/%Y")
        except ValueError:
            print "Second date does not have the right format. Will not " + \
                "use a filter here."
    if date1 or date2:
        filters.append((logParser.DATE,date1,date2))

    ##look for other possible filters
    if "cname" in params:
        filters.append((logParser.NAME,params["cname"].value))
    if "cprotocol" in params:
        filters.append((logParser.PROTOCOL,params["cprotocol"].value))
    if "ctld" in params:
        filters.append((logParser.TLD,params["ctld"].value))
    if "cref" in params:
        filters.append((logParser.REF,params["cref"].value))

    #create parser
    parser=logParser.LogParser(logfile,filters)

    #check for requested categories / statistics to show
    categories=[]
    #mapping of strings to kind of statistic
    mapping={"sname":logParser.NAME,
             "sdate":logParser.DATE,
             "stime":logParser.TIME,
             "sprotocol":logParser.PROTOCOL,
             "sfile":logParser.FILE,
             "sget":logParser.RECTYPE,
             "sstatus":logParser.STATUS,
             "ssize":logParser.SIZE,
             "sreferer":logParser.REF,
             "sprogram":logParser.PROGRAM,
             "sos":logParser.OS,
             "slanguage":logParser.LANG,
             "stld":logParser.TLD}
    if "stat" in params:
        if isinstance(params["stat"],list):
            for cat in params["stat"]:
                categories.append(mapping[cat.value])
        else:
            categories.append(mapping[params["stat"].value])

    #add categories and return parser
    parser.addCategories(categories)
    return parser

#============================================================================
# MAIN
#============================================================================
#enables nice debugging information in browser when something goes wrong
#cgitb.enable()
#parse arguments
parsingRes=giveArgumentsToParser(cgi.FieldStorage()).parse()

res={logParser.PROTOCOL:{"banane":3,"gurke":2,"hasen":5,"moehre":2},
     logParser.PROGRAM:{"kaesekuchen":25,"schokokuchen":15}}

chart={logParser.NAME:svgCreator.createPieChart,
       logParser.PROTOCOL:svgCreator.createPieChart,
       logParser.FILE:svgCreator.createPieChart,
       logParser.RECTYPE:svgCreator.createPieChart,
       logParser.STATUS:svgCreator.createPieChart,
       logParser.REF:svgCreator.createPieChart,
       logParser.PROGRAM:svgCreator.createPieChart,
       logParser.OS:svgCreator.createPieChart,
       logParser.LANG:svgCreator.createPieChart,
       logParser.TLD:svgCreator.createPieChart,
       logParser.DATE:svgCreator.createBarChart,
       logParser.TIME:svgCreator.createBarChart,
       logParser.SIZE:svgCreator.createBarChart}

#TODO hier vernünftige Überschriften hinschreiben
mapping={logParser.NAME:"name",
         logParser.DATE:"date",
         logParser.TIME:"time",
         logParser.PROTOCOL:"protocol",
         logParser.FILE:"file",
         logParser.RECTYPE:"rectype",
         logParser.STATUS:"status",
         logParser.SIZE:"size",
         logParser.REF:"ref",
         logParser.PROGRAM:"program",
         logParser.OS:"os",
         logParser.LANG:"lang",
         logParser.TLD:"tld"}

top={logParser.NAME:None,
     logParser.DATE:None,
     logParser.TIME:None,
     logParser.PROTOCOL:2,
     logParser.FILE:None,
     logParser.RECTYPE:None,
     logParser.STATUS:None,
     logParser.SIZE:None,
     logParser.REF:None,
     logParser.PROGRAM:None,
     logParser.OS:None,
     logParser.LANG:None,
     logParser.TLD:None}

dic={}
for item in res.items():
    dic[mapping[item[0]]]=chart[item[0]](item[1],top[item[0]])