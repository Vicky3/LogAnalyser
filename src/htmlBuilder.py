# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 13:26:10 2015

@author: adreyer
"""

import StringIO

class HtmlBuilder:
    def __init__(self,t=None):
        self._title=t
        self._notifications=[]
        self._content=[]

    def setTitle(self,t):
        if isinstance(t, basestring):
            self._title=t
        else:
            raise TypeError

    def addNotification(self,n):
        if isinstance(n, basestring):
            self._notifications.append(n)
        else:
            raise TypeError

    def addHeadline(self,h):
        if isinstance(h, basestring):
            self._content.append((h,[]))
        else:
            raise TypeError

    def addContent(self,c):
        if isinstance(c, basestring) or isinstance(c, StringIO.StringIO):
            if len(self._content)==0:
                self._content.append((None,[c]))
            else:
                self._content[-1][1].append(c)
        else:
            raise TypeError

    def buildHtml(self):
        return None