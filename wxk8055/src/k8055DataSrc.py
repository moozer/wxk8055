'''
Created on 17 Feb 2013

@author: moz
'''
from k8055 import Board
from DataSrc import DataSrc
import csv

# TODO: comments and unittesting...

class k8055DataSrc(DataSrc):
    def __init__(self, ReadInterval = 500, address = 0):
        super(k8055DataSrc,self).__init__( ReadInterval =  ReadInterval )        
        self._board = Board( address = address )
        self._counter = 0
        self._InitDataArray( 3 )  # counter, a1, a2

        # TODO: automatic next file
        self._filename = "Run.csv"        
        self._CsvWriter = csv.writer(open(self._filename, "w+"), delimiter='\t',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)

        self._CsvWriter.writerow( ["Count", "a1 [inc]", "a2 [inc]"] )
        
    def _ReadData(self):
        self._board.read()
        a1 = float(self._board.analog1)
        a2 = float(self._board.analog2)
        self._counter += 1
        
        data = [self._counter, a1, a2]
        self._CsvWriter.writerow( data )
        
        return [data]
    
    
    
#class CsvDataSrc( DataSrc ):
#    def __init__(self, filename, ReadInterval = 0 ):
#        super(CsvDataSrc,self).__init__( ReadInterval =  ReadInterval )
#
#        self._csvfile = open( filename, 'r')
#        self._CsvReader = csv.DictReader( self._csvfile, delimiter='\t' )
#        self._Inputs = len( self._CsvReader.fieldnames )
#        self._InitDataArray()
#        pass
#    
#    def _ReadData(self):
#        ''' @return: a list of entries converted to float '''
#        if self._ReadInterval > 0:
#            entry = map(float, self._CsvReader.next().values() )
#            return [entry]
#    
#        # else, we dump all data.
#        retarray = []
#        for entry in self._CsvReader:
#            fentry = map(float, entry.values() )
#            retarray.append(fentry)
#            
#        return retarray
#    
