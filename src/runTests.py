# -*- coding: utf-8 -*-
"""
Created on Sun Feb 15, 14:58:31 2015

@author: adreyer & jpoeppel
"""

import unittest
import argparse

def parseArguments():
  """
    Function that takes program parameters and checks for required arguments.
  """
  parser = argparse.ArgumentParser(description='A script running all the tests present in the current directory.')
  parser.add_argument('-v', '--verbosity', type=int, default=3,
                      help='Verbosity the tests should run with.')
  parser.add_argument('-p', '--pattern', type=str, default='*',
                      help='Pattern test cases need to match in order to be run.')
  return parser.parse_args()

if __name__ == '__main__':
  args = parseArguments()
  testLoader = unittest.TestLoader()
  suite = testLoader.discover('tests',pattern = args.pattern)
  unittest.TextTestRunner(verbosity=args.verbosity).run(suite)
  


