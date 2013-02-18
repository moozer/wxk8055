'''
Created on 18 Feb 2013

@author: moz
'''

class DataSrc( object ):
    """ Base class for data sources
    
    """
    def __init__(self, ReadInterval ):
        self._ReadInterval = ReadInterval
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
        return len( self.next() )
        pass
    
    

#class CsvDataSrc(object):
#    '''
#    classdocs
#    '''
#
#
#    def __init__(selfparams):
#        '''
#        Constructor
#        '''
        