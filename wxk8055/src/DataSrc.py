'''
Created on 18 Feb 2013

@author: moz
'''
import csv

class DataSrc( object ):
    """ Base class for data sources
    
    """
    def __init__(self, ReadInterval ):
        self._ReadInterval = ReadInterval
        self._Inputs = 1 # just hardcode something that corresponds to next()
        pass
        
    @property
    def ReadInterval(self):
        ''' @return: the update interval specified at construction time '''
        return self._ReadInterval

    def next(self):
        ''' @return: the values read since last call to this function '''
        return [[0]] # dummy value

    @property
    def Inputs(self):
        ''' @return: the number of inputs "lines" in the system '''
        return self._Inputs
    
class CsvDataSrc( DataSrc ):
    def __init__(self, filename, ReadInterval = 0 ):
        super(CsvDataSrc,self).__init__( ReadInterval =  ReadInterval )
        self._csvfile = open( filename, 'r')
        
        self._CsvReader = csv.DictReader( self._csvfile, delimiter='\t' )
        self._Inputs = len( self._CsvReader.fieldnames )
        pass
    
    def next(self):
        ''' @return: the entry converted to float '''
        return map(float, self._CsvReader.next().values() )
    