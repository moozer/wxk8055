'''
Created on 18 Feb 2013

@author: moz
'''
import unittest
from DataSrc import DataSrc


class Test(unittest.TestCase):


    def testDataSrc(self):
        interval = 100
        d = DataSrc( 100 )
        self.assertEqual( d.ReadInterval, interval )

    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testDataSrc']
    unittest.main()