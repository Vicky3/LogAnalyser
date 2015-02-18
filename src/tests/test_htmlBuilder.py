# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 13:27:48 2015

Testcase for HtmlBuilder.

@author: adreyer
"""

import unittest
import htmlBuilder
import StringIO

class TestHtmlBuilder(unittest.TestCase):

    def setUp(self):
        pass

    def test_createHtmlBuilder(self):
        builder=htmlBuilder.HtmlBuilder()
        self.assertIsNotNone(builder)

    def test_createHtmlBuilderWithTitle(self):
        title="A Title"
        builder=htmlBuilder.HtmlBuilder(title)
        self.assertIsNotNone(builder)
        self.assertEqual(builder._title,title)

    def test_setTitle(self):
        title="Another Title"
        builder=htmlBuilder.HtmlBuilder()
        builder.setTitle(title)
        self.assertEqual(builder._title,title)

    def test_setInvalidTitle(self):
        title={"title":"testtitle"}
        builder=htmlBuilder.HtmlBuilder()
        with self.assertRaises(TypeError):
            builder.setTitle(title)

    def test_isString(self):
        s="TestString"
        builder=htmlBuilder.HtmlBuilder()
        self.assertTrue(builder._isString(s))

    def test_isStringFalse(self):
        s={"string":"testString"}
        builder=htmlBuilder.HtmlBuilder()
        self.assertFalse(builder._isString(s))

    def test_addNotification(self):
        notification="A failure occured. Please check input!"
        builder=htmlBuilder.HtmlBuilder()
        builder.addNotification(notification)
        self.assertEqual(len(builder._notifications),1)
        self.assertEqual(builder._notifications[0],notification)
        notification2="Oh no! Another failure!"
        builder.addNotification(notification2)
        self.assertEqual(len(builder._notifications),2)
        self.assertEqual(builder._notifications[1],notification2)

    def test_addHeadline(self):
        headline="A nice headline"
        builder=htmlBuilder.HtmlBuilder()
        builder.addHeadline(headline)
        self.assertEqual(len(builder._content),1)
        self.assertEqual(builder._content[0][0],headline)
        headline2="Another headline"
        builder.addHeadline(headline2)
        self.assertEqual(len(builder._content),2)
        self.assertEqual(builder._content[1][0],headline2)

    def test_addContentText(self):
        content="Very important stuff"
        builder=htmlBuilder.HtmlBuilder()
        builder.addHeadline("Topic 1")
        builder.addContent(content)
        self.assertEqual(len(builder._content),1)
        self.assertEqual(builder._content[0][1][0],content)
        content2="Even more important stuff"
        builder.addContent(content2)
        self.assertEqual(len(builder._content),2)
        self.assertEqual(builder._content[0][1][1],content2)

    def test_addContentSVG(self):
        with open('testData/smiley.svg', 'r') as f:
            svg = f.read()
        s=StringIO.StringIO()
        s.write(svg)
        builder=htmlBuilder.HtmlBuilder()
        builder.addHeadline("Topic 1")
        builder.addContent(s)
        self.assertEqual(len(builder._content),1)
        self.assertEqual(builder._content[0][1][0],s)

    def test_addContentWithNoHeadline(self):
        content="Very important stuff"
        builder=htmlBuilder.HtmlBuilder()
        builder.addContent(content)
        self.assertEqual(len(builder._content),1)
        self.assertEqual(builder._content[0][1][0],content)
        headline="Topic 1"
        builder.addHeadline(headline)
        content2="Even more important stuff"
        builder.addContent(content2)
        self.assertEqual(len(builder._content),1)
        self.assertEqual(builder._content[1][0],headline)
        self.assertEqual(builder._content[1][1][0],content2)

    def test_buildHtmlBasic(self):
        title="A Title"
        headline="A nice headline"
        content="Very important stuff"
        content2="Even more important stuff"
        headline2="Another headline"
        content3="Some more stuff (not really important)"
        builder=htmlBuilder.HtmlBuilder()
        builder.setTitle(title)
        builder.addHeadline(headline)
        builder.addContent(content)
        builder.addContent(content2)
        builder.addHeadline(headline2)
        builder.addContent(content3)
        res=builder.buildHtml()
        with open('testData/site1.html', 'r') as f:
            true = f.read()
        self.assertEqual(res,true)

    def test_buildHtmlWithSVG(self):
        title="A Title"
        headline="A nice headline"
        with open('testData/smiley.svg', 'r') as f:
            content = f.read()
        content2="Even more important stuff"
        headline2="Another headline"
        content3="Some more stuff (not really important)"
        builder=htmlBuilder.HtmlBuilder()
        builder.setTitle(title)
        builder.addHeadline(headline)
        builder.addContent(content)
        builder.addContent(content2)
        builder.addHeadline(headline2)
        builder.addContent(content3)
        res=builder.buildHtml()
        with open('testData/site2.html', 'r') as f:
            true = f.read()
        self.assertEqual(res,true)

if __name__ == '__main__':
    unittest.main()