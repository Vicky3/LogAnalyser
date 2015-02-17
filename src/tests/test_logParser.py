# -*- coding: utf-8 -*-
"""
Created on Mon Feb  16 15:7:52 2015
Testcase for the logParser.
@author: jpoeppel
"""

import unittest
import logParser
import time


class TestParserObject(unittest.TestCase):
    
    def setUp(self):
        self.filters = [(logParser.NAME, "123.123.123.2"), (logParser.DATE, time.time)]
    
    def test_createParser(self):
        parser = logParser.LogParser()
        self.assertIsNotNone(parser)
        
    
    def test_createParserWithFilters(self):
        parser = logParser.LogParser(self.filters)
        self.assertIsNotNone(parser)
        self.assertTrue(len(parser.filters), len(self.filters))
        
    def test_createParserWithInvalidFilterType(self):
        filters = [(logParser.FILE, "123.123.123.2"), (logParser.TIME, time.time)]
        with self.assertRaises(TypeError):
            parser = logParser.LogParser(filters)
        
    def test_addFilter(self):
        parser = logParser.LogParser()
        parser.addFilter(self.filters[0])
        self.assertEqual(len(parser.filters),1)
        
    def test_addFilterWithInvalidType(self):
        parser = logParser.LogParser()
        with self.assertRaises(TypeError):
            parser.addFilter(("hans", "123.123.123.2"))
    
    def test_addFilters(self):
        parser = logParser.LogParser()
        parser.addFilters(self.filters)
        self.assertEqual(len(parser.filters), len(self.filters))
        
    
    def test_addCategory(self):
        parser = logParser.LogParser()
        parser.addCategory(logParser.NAME)
        self.assertTrue(len(parser.categories), 1)
        self.assertTrue(parser.categories[0], logParser.Name)
    
    def test_addCategories(self):
        parser = logParser.LogParser()
        parser.addCategories([logParser.NAME, logParser.FILE])
        self.assertTrue(len(parser.categories),2)
        self.assertTrue(parser.categories[1], logParser.FILE)
        
    def test_addCategoryWithInvalidType(self):
        parser = logParser.LogParser()
        with self.assertRaises(TypeError):
            parser.addCategory("hans")
        
    
    def test_parse(self):
        pass
    
    
if __name__ == '__main__':
    unittest.main()