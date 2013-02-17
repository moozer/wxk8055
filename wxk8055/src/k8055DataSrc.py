'''
Created on 17 Feb 2013

@author: moz
'''
from k8055 import Board

# TODO: comments and unittesting...

class k8055DataSrc():
    def __init__(self, address = 0):
        self.b = Board( address = address )
        
    def next(self):
        self.b.read()
        a1 = self.b.analog1
        a2 = self.b.analog2
        
        return [a1, a2]