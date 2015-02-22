#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 14:37:52 2015

Main script started by the website.
Will give arguments to parser and start parsing. The results are given to the
svgCreator to create pie/bar charts.

TODO finish doc when script grows!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

@author: adreyer
"""
#Needed to interpret the printed output as html (following blanc line is)
#print "Content-Type: text/html"
print "Content_Type: text/plain"
print
print "<TITLE>Log Analyser - Result</TITLE>"
#print "<H1>Your results:</H1>"

import cgi,cgitb
import time
import htmlBuilder
import logParser
import svgCreator

#Path where the log files are found.
LOG_DIRECTORY="../logs/"

def createParserWithArguments(params):
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
            hBuilder.addNotification("First date does not have the " + \
                "valid format. Will not use a filter here.")
    if "cdate2" in params:
        try:
            date2=time.strptime(params["cdate2"].value.lstrip().rstrip(),
                          "%d/%b/%Y")
        except ValueError:
            hBuilder.addNotification("Second date does not have the " + \
                "valid format. Will not use a filter here.")
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
    mapping={"sname":logParser.NAME, "sdate":logParser.DATE,
             "stime":logParser.TIME, "sprotocol":logParser.PROTOCOL,
             "sfile":logParser.FILE, "sget":logParser.RECTYPE,
             "sstatus":logParser.STATUS, "ssize":logParser.SIZE,
             "sreferer":logParser.REF, "sprogram":logParser.PROGRAM,
             "sos":logParser.OS, "slanguage":logParser.LANG,
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

def makeSVGs(dataToPlot):
    """
    Builds SVG images. Depending on the category either a pie chart or a bar
    chart is created. Also depending on the category a maximum ofwedges/bars
    is defined.

    Parameters
    ----------
    dataToPlot : dict of dicts
        the parsing results

    Returns
    -------
    dict
        a dictionary containing titles for the plots in keys and the svg
        image as StringIO in values
    """
    #mapping which type of plot is for which category
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

    #mapping of titles for the plots depending on categories
    #TODO create nice titles
    titles={logParser.NAME:"IP Adress/Name",
            logParser.DATE:"Date of request",
            logParser.TIME:"Time of request",
            logParser.PROTOCOL:"Used Protocol",
            logParser.FILE:"Requested File",
            logParser.RECTYPE:"Request Type",
            logParser.STATUS:"Request Status",
            logParser.SIZE:"Size of requested object",
            logParser.REF:"Referenz path",
            logParser.PROGRAM:"Requesting program",
            logParser.OS:"Used operating system",
            logParser.LANG:"Used language",
            logParser.TLD:"Top-Level-Domain"}

    #how many wedges/bars should be created depending on category
    #(None for as much as in data)
    top={logParser.NAME:14, logParser.DATE:None, logParser.TIME:None,
         logParser.PROTOCOL:7, logParser.FILE:7, logParser.RECTYPE:7,
         logParser.STATUS:7, logParser.SIZE:7, logParser.REF:7,
         logParser.PROGRAM:7, logParser.OS:14, logParser.LANG:7,
         logParser.TLD:14}

    #creation of the svgs (key: title - value: svg)
    dic={}
    for k,v in dataToPlot.items():
        dic[titles[k]]=chart[k](v,top[k])
    return dic

#============================================================================
# MAIN
#============================================================================
#enables nice debugging information in browser when something goes wrong
cgitb.enable()

hBuilder=htmlBuilder.HtmlBuilder("Log Analyser - Result")

#parse arguments
parsingRes,notifications=createParserWithArguments(cgi.FieldStorage()).parse()
#notifications concerning invalid lines
hBuilder.addNotification("Number of invalid lines: " + str(len(notifications)))
for note in notifications:
    hBuilder.addNotification("Invalid line: "+note)

#build svgs from the parsed data
res=makeSVGs(parsingRes)

#give results to htmlBuilder
for k,v in res.items():
    hBuilder.addHeadline(k)
    hBuilder.addContent(v)

print hBuilder.buildHtml()