#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 14:37:52 2015

@author: adreyer
"""
print "Content-Type: text/plain\n"

import cgi,cgitb
import time
import logParser

LOG_DIRECTORY="../logs/"

cgitb.enable()
params=cgi.FieldStorage()
logfile=None
filters=[]

if "log" in params:
    #print params["log"].value
    #print "Pfad:",LOG_DIRECTORY+params["log"].value+".log"
    logfile=LOG_DIRECTORY+params["log"].value+".log"
    
date1=None
date2=None
if "cdate1" in params:
    #print "cdate1"
    #print params["cdate1"].value
    try:
        time.strptime(params["cdate1"].value.lstrip().rstrip(),"%d/%b/%Y")
        date1=params["cdate1"].value.lstrip().rstrip()
    except ValueError:
        print "First date does not have the right format. Will not use a filter here."
if "cdate2" in params:
    #print "cdate2"
    try:
        time.strptime(params["cdate2"].value.lstrip().rstrip(),"%d/%b/%Y")
        date2=params["cdate2"].value.lstrip().rstrip()
    except ValueError:
        print "Second date does not have the right format. Will not use a filter here."
if date1 or date2:
    filters.append((logParser.DATE,date1,date2))
    
if "cname" in params:
    #print "cname"
    filters.append((logParser.NAME,params["cname"].value))
if "cprotocol" in params:
    #print "cprotocol"
    filters.append((logParser.PROTOCOL,params["cprotocol"].value))
if "ctld" in params:
    #print "ctld"
    filters.append((logParser.TLD,params["ctld"].value))
if "cref" in params:
    #print "cref"
    filters.append((logParser.REF,params["cref"].value))
    
print "filters",filters
parser=logParser.LogParser(logfile,filters)

categories=[]
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

#stat1=[cgi.MiniFieldStorage('stat', 'sname'), cgi.MiniFieldStorage('stat', 'sdate'), cgi.MiniFieldStorage('stat', 'stime'), cgi.MiniFieldStorage('stat', 'sprotocol')]
#stat2=cgi.MiniFieldStorage('stat', 'sstatus')
#stat=stat1
#print "stat",stat
#print mapping[stat2.value]

if "stat" in params:
    print params["stat"]
    if isinstance(params["stat"],list):
        for cat in params["stat"]:
            categories.append(mapping[cat.value])
    else:
        categories.append(mapping[params["stat"].value])
    print "categories",categories
#    if "sname" in params["stat"]:
#        print "GEFUNDEN"
#    else:
#        print "nicht gefunden"
    
    
else:
    print "no stat"
    
parser.addCategory(categories)

#for name in params.keys():
#    print "%s : %s" % (name,params[name].value)
#    print params[name]," ",type(params[name])