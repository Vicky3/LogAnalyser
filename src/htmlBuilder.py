# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 13:26:10 2015

A small class to build a basic HTML file.

@author: adreyer
"""

import StringIO
#import xml.etree.cElementTree as ET
#import lxml.html.builder as HB
import xml.dom.minidom as dom

class HtmlBuilder:

#    __START_HTML="<!DOCTYPE html>\n<html>\n<head>\n<title>"
#    __END_HEADER_START_BODY="</title>\n</head>\n<body>\n<h1>"
#    __START_TABLE='</h1>\n<table style="width:100%">'
#    __END_TABLE_AND_HTML="</table>\n</body>\n</html>"

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
#        site=ET.Element("html")
#        head=ET.SubElement(site,"head")
#        body=ET.SubElement(site,"body")
#        if self._title:
#            title=ET.SubElement(head,"title")
#            title.text=self._title
#            h1=ET.SubElement(body,"h1")
#            h1.text=self._title
#        body.text="test"
#        table=ET.SubElement(body,"table",{"style":"width:100%"})
#        newline=True

        doc=dom.Document()
        site=doc.createElement("html")
        if self._title:
            head=doc.createElement("head")
            title=doc.createElement("title")
            ttext=doc.createTextNode(self._title)
            title.appendChild(ttext)
            head.appendChild(title)
            site.appendChild(head)
        body=doc.createElement("body")
        if self._title:
            h1=doc.createElement("h1")
            th1=doc.createTextNode(self._title)
            h1.appendChild(th1)
            body.appendChild(h1)
        for n in self._notifications:
            n1=doc.createTextNode("NOTE: "+n)
            br=doc.createElement("br")
            body.appendChild(n1)
            body.appendChild(br)
        newline=True
        tr
        for c in self._content:
            if newline:
                tr=doc.createElement("tr")
            td=doc.createElement("td")
            if c[0]:
                h2=doc.createElement("h2")
                th2=doc.createTextNode(c[0])
                h2.appendChild(th2)


        site.appendChild(body)
        print site.toprettyxml()


        return None