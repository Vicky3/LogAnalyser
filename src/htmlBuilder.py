# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 13:26:10 2015

@author: adreyer
"""

class HtmlBuilder:
    def __init__(self,t=None):
        self._title=t
        self._notifications=[]
        self._content=[]

    def setTitle(self,t):
        pass

    def addNotification(self,n):
        pass

    def addHeadline(self,h):
        pass

    def addContent(self,c):
        pass

    def _isString(self,s):
        pass

    def buildHtml(self):
        return None