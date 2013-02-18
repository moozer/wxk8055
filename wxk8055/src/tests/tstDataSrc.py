'''
Created on 18 Feb 2013

@author: moz
'''
import unittest
from DataSrc import DataSrc

interval = 100 
class TestDataSrc(unittest.TestCase):

    def testConstruction(self):
        d = DataSrc( interval )
        self.assertEqual( d.ReadInterval, interval )

    def testNext(self):
        d = DataSrc( interval )
        self.assertEqual( len(d.next()), d.Inputs )
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testDataSrc']
    unittest.main()