#!/usr/bin/env python

print "Content-Type: text/plain\n"

import os
import cgi,cgitb
cgitb.enable()
params=cgi.FieldStorage()
for name in params.keys():
#    print "%s : %s" % (name,params[name].value)
    print type(params[name])
    if isinstance(params[name], list):
        for f in params[name]:
            print f

print os.environ
#print "User: %s" % os.environ['USER']
print "Search path: %s" % os.environ['PATH']

try:
    var=os.environ['QUERY_STRING']
    vars=var.split('&')

    v={}
    for var in vars:
        s=var.split('=')
        v[s[0]]=s[1]

    print v
except KeyError:
    print "No query string found."