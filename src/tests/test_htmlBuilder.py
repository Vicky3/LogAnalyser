# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 13:27:48 2015

@author: adreyer
"""

import unittest
import htmlBuilder

class TestHtmlBuilder(unittest.TestCase):

    def setUp(self):
        pass

    def test_createHtmlBuilder(self):
        builder = htmlBuilder.HtmlBuilder()
        self.assertIsNotNone(builder)

    def test_createHtmlBuilderWithTitle(self):
        self.fail("test incomplete")

    def test_setTitle(self):
        self.fail("test incomplete")

    def test_addNotification(self):
        self.fail("test incomplete")

    def test_addHeadline(self):
        self.fail("test incomplete")

    def test_addContent(self):
        self.fail("test incomplete")

    def test_isString(self):
        self.fail("test incomplete")

    def test_buildHtml(self):
        self.fail("test incomplete")

if __name__ == '__main__':
    unittest.main()