!/usr/bin/env python

#print "Content-Type: text/plain\n"

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