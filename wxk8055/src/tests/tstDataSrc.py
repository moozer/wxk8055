'''
Created on 18 Feb 2013

@author: moz
'''
import unittest
from DataSrc import DataSrc, CsvDataSrc

interval = 100 
CsvFile = 'data/TwoInputs.csv'
Inputs = 3
CsvData = [[0,0,0], [1,0,0], [2,0,0]]
CsvEntriesCount = 469

class TestDataSrc(unittest.TestCase):

    def testConstruction(self):
        d = DataSrc( interval )
        self.assertEqual( d.ReadInterval, interval )

    def testNext(self):
        d = DataSrc( interval )
        self.assertEqual( len(d.next()), d.Inputs )
    
class TestCsvDataSrc(unittest.TestCase):

    def testConstruction(self):
        d = CsvDataSrc( CsvFile )
        self.assertEqual( d.ReadInterval, 0 ) # 0 is default value

    def testBadFilename(self):
        self.assertRaises( IOError, CsvDataSrc, 'NonExistingFilename')

    def testInputCount(self):
        d = CsvDataSrc( CsvFile )
        self.assertEqual( Inputs, d.Inputs )
        
    def testNext(self):
        d = CsvDataSrc( CsvFile, interval )
        self.assertEqual( d.next(), [CsvData[0]] )
        self.assertEqual( d.next(), [CsvData[1]] )
        self.assertEqual( d.next(), [CsvData[2]] )
        
#    def testGetAll(self):
#        d = CsvDataSrc( CsvFile )
#        self.assertEqual( len(d.next()), CsvEntriesCount )
#    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testDataSrc']
    unittest.main()