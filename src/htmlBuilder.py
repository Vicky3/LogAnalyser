# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 13:26:10 2015

A small class to build a basic HTML file.

@author: adreyer
"""

import StringIO
import xml.dom.minidom as dom
import xml.sax.saxutils

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
        doc=dom.Document()
        site=doc.createElement("html")
        #when title set - make a head for the html document
        if self._title:
            head=doc.createElement("head")
            title=doc.createElement("title")
            ttext=doc.createTextNode(self._title)
            title.appendChild(ttext)
            head.appendChild(title)
            site.appendChild(head)
        #====================================================================
        body=doc.createElement("body")
        #if title - write it!
        if self._title:
            h1=doc.createElement("h1")
            th1=doc.createTextNode(self._title)
            h1.appendChild(th1)
            body.appendChild(h1)
        #print notifications
        for n in self._notifications:
            n1=doc.createTextNode("NOTE: "+n)
            br=doc.createElement("br")
            body.appendChild(n1)
            body.appendChild(br)
        #--------------------------------------------------------------------
        #print content (in a table with two columns)
        newline=True
        table=doc.createElement("table")
        table.setAttribute("style","width:100%")
        for c in self._content:
            #two columns
            if newline:
                tr=doc.createElement("tr")
                newline=False
            else:
                table.appendChild(tr)
                newline=True
            td=doc.createElement("td")
            #if headline is set - write it
            if c[0]:
                h2=doc.createElement("h2")
                th2=doc.createTextNode(c[0])
                h2.appendChild(th2)
                td.appendChild(h2)
            #content
            for co in c[1]:
                if isinstance(co, basestring):
                    #can be a simple string...
                    content=doc.createTextNode(co)
                else:
                    #...or a StringIO with an svg in it
                    content=doc.createTextNode(co.getvalue())
                td.appendChild(content)
                br=doc.createElement("br")
                td.appendChild(br)
            tr.appendChild(td)
        if not newline:
            table.appendChild(tr)
        body.appendChild(table)
        site.appendChild(body)

        return xml.sax.saxutils.unescape(site.toprettyxml(encoding="utf-8"),
                                         {"&quot;":'"'})