# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 13:26:10 2015

A small class to build a basic HTML file.

@author: adreyer
"""

import StringIO

class HtmlBuilder:
    def __init__(self,title=None):
        """
        Constructor for the HtmlBuilder

        Parameters
        ----------
        title : String, optional
            the title a builded html should have

        Raises
        ------
        TypeError
            If the title is not a String.
        """
        if title!=None:
            self.setTitle(title)
        self._notifications=[]
        self._content=[]

    def setTitle(self,title):
        """
        Sets the title of the html to build.

        Parameters
        ----------
        title : String
            the title a builded html should have

        Raises
        ------
        TypeError
            If the title is not a String.
        """
        if isinstance(title, basestring):
            self._title=title
        else:
            raise TypeError

    def addNotification(self,notification):
        """
        Adds a notification to the html to build.

        Parameters
        ----------
        notification : String
            a notification a builded html should contain

        Raises
        ------
        TypeError
            If the notification is not a String.
        """
        if isinstance(notification, basestring):
            self._notifications.append(notification)
        else:
            raise TypeError

    def addHeadline(self,headline):
        """
        Adds a headline to the html to build.

        Parameters
        ----------
        headline : String
            a headline a builded html should contain

        Raises
        ------
        TypeError
            If the headline is not a String.
        """
        if isinstance(headline, basestring):
            self._content.append((headline,[]))
        else:
            raise TypeError

    def addContent(self,content):
        """
        Adds content to the latest headline of the html to build.

        Parameters
        ----------
        content : String or StringIO
            a content a builded html should contain

        Raises
        ------
        TypeError
            If the content is not a String or StringIO.
        """
        if isinstance(content, basestring) \
        or isinstance(content, StringIO.StringIO):
            if len(self._content)==0:
                self._content.append((None,[content]))
            else:
                self._content[-1][1].append(content)
        else:
            raise TypeError

    def buildHtml(self):
        """
        Builds a html with the saved title, headlines and content.
        """
        return None