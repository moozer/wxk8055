'''
Created on 18 Feb 2013

@author: moz
'''
import unittest
from DataSrc import DataSrc, CsvDataSrc
import time

interval = 100.0 
TestCount = 10

CsvFile = 'data/TwoInputs.csv'
Inputs = 3
CsvData = [[0,0,0], [1,0,0], [2,0,0]]
CsvEntriesCount = 469
CsvEntriesMaxVal = 468
CsvEntriesMinVal = 0
testvar = 0

def IncFunction():
    global testvar
    testvar = testvar +1


class TestDataSrc(unittest.TestCase):

    def testConstruction(self):
        d = DataSrc( interval )
        self.assertEqual( d.ReadInterval, interval )

    def testNext(self):
        d = DataSrc( interval )
        self.assertEqual( len(d.next()), d.Inputs )
    
    def testGetMaxMin(self):
        d = DataSrc( interval )
        for i in range( 0, TestCount ):
            d.next()

        self.assertLessEqual( d.GetMax(), 100 )
        self.assertGreaterEqual(d.GetMin(), 0)
        
        self.assertEqual(d.Count, TestCount)
        
    def testGetSeries(self):
        d = DataSrc( interval )
        for i in range( 0, TestCount ):
            d.next()
        
        self.assertEqual(len(d.GetSeries(0)), TestCount)
        for entry in d.GetSeries(0):
            self.assertLessEqual( entry, 100 )
            self.assertGreaterEqual(entry, 0)
    
    def testTimerThread(self):
        d = DataSrc( interval )
        self.assertEqual(d.IsTimerRunning, False)

        global testvar
        testvar = 0
        d.StartTimer( IncFunction )
        self.assertEqual(d.IsTimerRunning, True)

        time.sleep( .2*interval/1000 ) # .2 to make sure that we have at least started
        self.assertEqual( testvar, 1 )
        self.assertEqual( d.PendingCount, 1)
        time.sleep( 1.2*interval/1000 ) # 1.2 to make sure that we have two periods
        self.assertEqual( testvar, 2 )
        self.assertEqual( d.PendingCount, 2)
 
        d.StopTimer()
        
        d.next()
        self.assertEqual( d.PendingCount, 0)
        
    def testGetMaxMinDefault(self):
        d = DataSrc( CsvFile )
        self.assertEqual(d.GetMax( 10 ), 10)
        self.assertEqual(d.GetMin( 0), 0 )

 
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
        
    def testGetAll(self):
        d = CsvDataSrc( CsvFile )
        self.assertEqual( len(d.next()), CsvEntriesCount )
        
    def testGetMaxMin(self):
        d = CsvDataSrc( CsvFile )
        d.next()
        self.assertEqual(d.GetMax(), CsvEntriesMaxVal)
        self.assertEqual(d.GetMin(), CsvEntriesMinVal)
        
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testDataSrc']
    unittest.main()