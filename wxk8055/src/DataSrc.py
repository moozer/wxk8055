'''
Created on 18 Feb 2013

@author: moz
'''
import csv
import random
import threading
import time
import copy

class DataSrc( object ):
    """ Base class for data sources
    
    """

    def __init__(self, ReadInterval ):
        self._ReadInterval = ReadInterval
        self._Inputs = 1 # just hardcode something that corresponds to _ReadData()
        self._WorkerThread = None 
        self._RunThread = threading.Event() # if isSet(), then the thread is running
        self._PendingData = [] # retrieved data, that has not been next()'ed.
        self._PendingDataLock = threading.Lock()
        self._InitDataArray()
        pass
        
    def _InitDataArray(self):
        self._data = []  # array to hold data to show
        for channel in range( 0, self._Inputs ):  #@UnusedVariable
            self._data.append( [] )

    @property
    def ReadInterval(self):
        ''' @return: the update interval specified at construction time '''
        return self._ReadInterval


    def _AppendData(self, data):
        ''' saves the entries to the internal data storage 
        @param data: a list of lists of data - might look odd for single values :-) ie. [[3]]
        '''
        for entry in data:
            for i in range(0, self._Inputs):
                self._data[i].append(entry[i])

    def _ReadData(self):
        ''' @return: a list of lists of acquired data '''
        return [[random.uniform(0, 100)]] # dummy value

    def next(self):
        ''' @return: the values read since last call to this function '''
        with self._PendingDataLock:
            val = copy.copy( self._PendingData )
            self._PendingData = [] # and reset to zero.
            
        if len(val) == 0:
            val = self._ReadData() # force reading one line if nothing is pending
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

    @property
    def Count(self):
        ''' @return: the number of data entries in the data list '''
        return len( self._data[0] )

    
    def GetSeries(self, InputNumber):
        ''' @return:The data corresponding to the specified "column" '''
        return self._data[InputNumber]

    #------- timer stuff ------
    @property   
    def IsTimerRunning(self):
        if not self._WorkerThread:
            return False
        return self._WorkerThread.isAlive()

    def _ThreadMain(self, EventFunction):
        while( self._RunThread.isSet( )):
            data = self._ReadData()
            with self._PendingDataLock:
                self._PendingData.append( data )
            
            EventFunction()
        
            # TODO: do a timer thing to do real ms interval, not runtime+interval
            time.sleep( (1.0*self._ReadInterval)/1000 )

    def StartTimer(self, EventFunction):
        self._WorkerThread = threading.Thread( name="DataSrc timer thread", 
                                               target=self._ThreadMain, 
                                               args=(EventFunction, ) )
        self._WorkerThread.daemon = True
        self._RunThread.set()
        self._WorkerThread.start()

    def StopTimer(self):
        self._RunThread.clear()
        while self._WorkerThread.isAlive():
            time.sleep( 0.010 )

    @property 
    def PendingCount(self):
        return len( self._PendingData )
    
    
class CsvDataSrc( DataSrc ):
    def __init__(self, filename, ReadInterval = 0 ):
        super(CsvDataSrc,self).__init__( ReadInterval =  ReadInterval )

        self._csvfile = open( filename, 'r')
        self._CsvReader = csv.DictReader( self._csvfile, delimiter='\t' )
        self._Inputs = len( self._CsvReader.fieldnames )
        self._InitDataArray()
        pass
    
    def _ReadData(self):
        ''' @return: a list of entries converted to float '''
        if self._ReadInterval > 0:
            entry = map(float, self._CsvReader.next().values() )
            return [entry]
    
        # else, we dump all data.
        retarray = []
        for entry in self._CsvReader:
            fentry = map(float, entry.values() )
            retarray.append(fentry)
            
        return retarray
    
#    def next(self):
#        return self.next()