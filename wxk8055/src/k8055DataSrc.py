'''
Created on 17 Feb 2013

@author: moz
'''
from k8055 import Board
from DataSrc import DataSrc

# TODO: comments and unittesting...

class k8055DataSrc(DataSrc):
    def __init__(self, ReadInterval = 500, address = 0):
        super(k8055DataSrc,self).__init__( ReadInterval =  ReadInterval )        
        self.b = Board( address = address )
        
    def _ReadData(self):
        self.b.read()
        a1 = float(self.b.analog1)
        a2 = float(self.b.analog2)
        
        return [[a1, a2]]
    
    
    
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
