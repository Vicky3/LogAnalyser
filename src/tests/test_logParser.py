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
        self.fileName = "testData/testLog.log"
        
    def test_createParser(self):
        parser = logParser.LogParser()
        self.assertIsNotNone(parser)        
    
    def test_createParserWithFilters(self):
        parser = logParser.LogParser(filters = self.filters)
        self.assertIsNotNone(parser)
        self.assertTrue(len(parser.filters), len(self.filters))
        
    def test_createParserWithFile(self):
        
        parser = logParser.LogParser(f = self.fileName)
        self.assertIsNotNone(parser)
        self.assertIsNotNone(parser.file)
        
    def test_createParserWithIncorrectFile(self):
        with self.assertRaises(IOError):
            parser = logParser.LogParser(f = "blub")
        
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
        
    def test_setFile(self):
        parser = logParser.LogParser()
        parser.setFile(self.fileName)
        self.assertIsNotNone(parser.file)
        
    def test_setFileInvalidFilename(self):
        parser = logParser.LogParser()
        with self.assertRaises(IOError):
            parser.setFile("blub")
    
    def test_parseProto(self):
        parser = logParser.LogParser(f = self.fileName)
        parser.addCategory(logParser.PROTOCOL)
        res = parser.parse()
        self.assertTrue(len(res)>0)
        self.assertEqual(res[0]["HTTP/1.1"], 18)
        
    def test_parseDate(self):
        parser = logParser.LogParser(f = self.fileName)
        parser.addCategory(logParser.DATE)
        res = parser.parse()
        self.assertTrue(len(res)>0)
        self.assertEqual(res[0]["01/Dec/2000"], 13)
        
    def test_parseIp(self):
        parser = logParser.LogParser(f = self.fileName)
        parser.addCategory(logParser.NAME)
        res = parser.parse()
        self.assertTrue(len(res)>0)
        self.assertEqual(res[0]["128.165.108.196"], 6)
        
    def test_parseTime(self):
        parser = logParser.LogParser(f = self.fileName)
        parser.addCategory(logParser.TIME)
        res = parser.parse()
        self.assertTrue(len(res)>0)
        self.assertEqual(res[0]["00"], 16)
        
    def test_parseFile(self):
        parser = logParser.LogParser(f = self.fileName)
        parser.addCategory(logParser.FILE)
        res = parser.parse()
        self.assertTrue(len(res)>0)
        self.assertEqual(res[0]["jpg"], 3)
        
    def test_parseRecType(self):
        parser = logParser.LogParser(f = self.fileName)
        parser.addCategory(logParser.RECTYPE)
        res = parser.parse()
        self.assertTrue(len(res)>0)
        self.assertEqual(res[0]["POST"], 3)
        
    def test_parseStatus(self):
        parser = logParser.LogParser(f = self.fileName)
        parser.addCategory(logParser.STATUS)
        res = parser.parse()
        self.assertTrue(len(res)>0)
        self.assertEqual(res[0]["3"], 5)
        
    def test_parseSize(self):
        parser = logParser.LogParser(f = self.fileName)
        parser.addCategory(logParser.SIZE)
        res = parser.parse()
        self.assertTrue(len(res)>0)
        self.assertEqual(res[0]["-"], 4)
        
    def test_parseRef(self):
        parser = logParser.LogParser(f = self.fileName)
        parser.addCategory(logParser.REF)
        res = parser.parse()
        self.assertTrue(len(res)>0)
        self.assertEqual(res[0]["http://bibiserv.techfak.uni-bielefeld.de/genefisher/"], 4)
        
    def test_parseProg(self):
        parser = logParser.LogParser(f = self.fileName)
        parser.addCategory(logParser.PROGRAM)
        res = parser.parse()
        self.assertTrue(len(res)>0)
        self.assertEqual(res[0]["Mozilla/4.51"], 4)
        
    def test_parseOs(self):
        parser = logParser.LogParser(f = self.fileName)
        parser.addCategory(logParser.OS)
        res = parser.parse()
        self.assertTrue(len(res)>0)
        self.assertEqual(res[0]["Macintosh"], 4)
            
    def test_parseLang(self):
        parser = logParser.LogParser(f = self.fileName)
        parser.addCategory(logParser.LANG)
        res = parser.parse()
        self.assertTrue(len(res)>0)
        self.assertEqual(res[0]["None"], 18)
        
    def test_parseTLD(self):
        parser = logParser.LogParser(f = self.fileName)
        parser.addCategory(logParser.TLD)
        res = parser.parse()
        self.assertTrue(len(res)>0)
        self.assertEqual(res[0]["edu"], 11)
        
    def test_parseMultiple(self):
        parser = logParser.LogParser(f = self.fileName)
        parser.addCategory(logParser.REF)
        parser.addCategory(logParser.PROGRAM)
        res = parser.parse()
        self.assertEqual(len(res),2)
        self.assertEqual(res[0]["http://bibiserv.techfak.uni-bielefeld.de/genefisher/"], 4)
        self.assertEqual(res[1]["Mozilla/4.51"], 4)
    
if __name__ == '__main__':
    unittest.main()