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
        
        parser = logParser.LogParser(fileName = self.fileName)
        self.assertIsNotNone(parser)
        self.assertEqual(parser.fileName, self.fileName)
        
    def test_createParserWithIncorrectFile(self):
        with self.assertRaises(TypeError):
            parser = logParser.LogParser(fileName = 123)
        
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
        self.assertEqual(parser.categories[0], logParser.NAME)
    
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
        self.assertEqual(parser.fileName, self.fileName)
        
    def test_setFileInvalidFilename(self):
        parser = logParser.LogParser()
        with self.assertRaises(TypeError):
            parser.setFile(123)
    
    def test_parseProto(self):
        parser = logParser.LogParser(fileName = self.fileName)
        parser.addCategory(logParser.PROTOCOL)
        res, invalidLines = parser.parse()
        self.assertTrue(len(res)>0)
        self.assertEqual(res[logParser.PROTOCOL]["HTTP/1.1"], 14)
        
    def test_parseDate(self):
        parser = logParser.LogParser(fileName = self.fileName)
        parser.addCategory(logParser.DATE)
        res, invalidLines = parser.parse()
        self.assertTrue(len(res)>0)
        self.assertEqual(res[logParser.DATE]["01/Dec/2000"], 13)
        
    def test_parseIp(self):
        parser = logParser.LogParser(fileName = self.fileName)
        parser.addCategory(logParser.NAME)
        res, invalidLines = parser.parse()
        self.assertTrue(len(res)>0)
        self.assertEqual(res[logParser.NAME]["128.165.108.196"], 6)
        
    def test_parseTime(self):
        parser = logParser.LogParser(fileName = self.fileName)
        parser.addCategory(logParser.TIME)
        res, invalidLines = parser.parse()
        self.assertTrue(len(res)>0)
        self.assertEqual(res[logParser.TIME]["00"], 15)
        
    def test_parseFile(self):
        parser = logParser.LogParser(fileName = self.fileName)
        parser.addCategory(logParser.FILE)
        res, invalidLines = parser.parse()
        self.assertTrue(len(res)>0)
        self.assertEqual(res[logParser.FILE][".jpg"], 3)
        
    def test_parseRecType(self):
        parser = logParser.LogParser(fileName = self.fileName)
        parser.addCategory(logParser.RECTYPE)
        res, invalidLines = parser.parse()
        self.assertTrue(len(res)>0)
        self.assertEqual(res[logParser.RECTYPE]["POST"], 2)
        
    def test_parseStatus(self):
        parser = logParser.LogParser(fileName = self.fileName)
        parser.addCategory(logParser.STATUS)
        res, invalidLines = parser.parse()
        self.assertTrue(len(res)>0)
        self.assertEqual(res[logParser.STATUS]["300"], 5)
        
    def test_parseSize(self):
        parser = logParser.LogParser(fileName = self.fileName)
        parser.addCategory(logParser.SIZE)
        res, invalidLines = parser.parse()
        self.assertTrue(len(res)>0)
        self.assertEqual(res[logParser.SIZE]["Unknown"], 4)
        
    def test_parseRef(self):
        parser = logParser.LogParser(fileName = self.fileName)
        parser.addCategory(logParser.REF)
        res, invalidLines = parser.parse()
        self.assertTrue(len(res)>0)
        self.assertEqual(res[logParser.REF]["http://bibiserv.techfak.uni-bielefeld.de/genefisher/"], 4)
        
    def test_parseProg(self):
        parser = logParser.LogParser(fileName = self.fileName)
        parser.addCategory(logParser.PROGRAM)
        res, invalidLines = parser.parse()
        self.assertTrue(len(res)>0)
        self.assertEqual(res[logParser.PROGRAM]["Mozilla/4.51"], 3)
        
    def test_parseOs(self):
        parser = logParser.LogParser(fileName = self.fileName)
        parser.addCategory(logParser.OS)
        res, invalidLines = parser.parse()
        self.assertTrue(len(res)>0)
        self.assertEqual(res[logParser.OS]["Macintosh"], 3)
            
    def test_parseLang(self):
        parser = logParser.LogParser(fileName = self.fileName)
        parser.addCategory(logParser.LANG)
        res, invalidLines = parser.parse()
        self.assertTrue(len(res)>0)
        self.assertEqual(res[logParser.LANG]["Unknown"], 17)
        
    def test_parseTLD(self):
        parser = logParser.LogParser(fileName = self.fileName)
        parser.addCategory(logParser.TLD)
        res, invalidLines = parser.parse()
        self.assertTrue(len(res)>0)
        self.assertEqual(res[logParser.TLD]["edu"], 10)
        
    def test_parseMultiple(self):
        parser = logParser.LogParser(fileName = self.fileName)
        parser.addCategory(logParser.REF)
        parser.addCategory(logParser.PROGRAM)
        res, invalidLines = parser.parse()
        self.assertEqual(len(res),2)
        self.assertEqual(res[logParser.REF]["http://bibiserv.techfak.uni-bielefeld.de/genefisher/"], 4)
        self.assertEqual(res[logParser.PROGRAM]["Mozilla/4.51"], 3)
        
    def test_parseWithoutFile(self):
        parser = logParser.LogParser()
        parser.addCategory(logParser.REF)
        with self.assertRaises(IOError):
            parser.parse()
            
    def test_parseNoCategories(self):
        parser = logParser.LogParser(fileName = self.fileName)
        res, invalidLines = parser.parse()
        self.assertEqual(len(res),0)
    
if __name__ == '__main__':
    unittest.main()