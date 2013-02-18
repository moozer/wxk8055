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
        self._data = [[]]
        pass
        
    @property
    def ReadInterval(self):
        ''' @return: the update interval specified at construction time '''
        return self._ReadInterval


    def _AppendData(self, data):
        ''' saves the entries to the internal data storage '''
        for i in range(0, self._Inputs):
            self._data[i].append(data[i])

    def next(self):
        ''' @return: the values read since last call to this function '''
        val = [0] # dummy value in array
        self._AppendData(val)
        return val 

    @property
    def Inputs(self):
        ''' @return: the number of inputs "lines" in the system '''
        return self._Inputs

    def GetMax(self):
        ''' @returns the highest value of currently read data '''
        maxlist = [max( datalist ) for datalist in self._data]
        return max(maxlist)

    def GetMin(self):
        ''' @returns the highest value of currently read data '''
        minlist = [min( datalist ) for datalist in self._data]
        return min(minlist)
    
    
class CsvDataSrc( DataSrc ):
    def __init__(self, filename, ReadInterval = 0 ):
        super(CsvDataSrc,self).__init__( ReadInterval =  ReadInterval )
        self._csvfile = open( filename, 'r')
        
        self._CsvReader = csv.DictReader( self._csvfile, delimiter='\t' )
        self._Inputs = len( self._CsvReader.fieldnames )
        pass
    
    def next(self):
        ''' @return: the entry converted to float '''
        if self._ReadInterval > 0:
            return [map(float, self._CsvReader.next().values() )]
    
        # else, we dump all data.
        retarray = []
        for entry in self._CsvReader:
            retarray.append(entry)
            
        return retarray