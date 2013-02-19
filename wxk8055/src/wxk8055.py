'''
Created on 17 Feb 2013

@author: moz

This program connects to a Velleman k8055 board and using
wxwidgets and matplotlib, shows the analog values for the 
two DA converters
'''
# TODO: add refs to where I found the stuff

import wx
from wx_mpl_dynamic_graph import GraphFrame
from k8055DataSrc import k8055DataSrc
from DataSrc import CsvDataSrc

if __name__ == '__main__':
    # TODO: add check on existence...
    # TODO: some GUI selection of board
    #DataSrc = k8055DataSrc()
    DataSrc = CsvDataSrc( 'tests/data/TwoInputs.csv')    
    # TODO: Some GUI to specify the interval
    ReadInterval = 500 # in ms
   
    app = wx.PySimpleApp()
    app.frame = GraphFrame( DataSrc )
    app.frame.Show()
    app.MainLoop()