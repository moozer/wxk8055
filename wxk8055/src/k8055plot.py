'''
Created on 19 Feb 2013

@author: moz
'''

# TODO: handle warning
import matplotlib
from k8055DataSrc import k8055DataSrc
matplotlib.use('WXAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas
import pylab
from wxk8055gui import MyFrame
import wx
from DataSrc import DataSrc, CsvDataSrc
import numpy as np

def IssueUpdatePlotEvent( wxObject ):
    #print "IssueUpdatePlotEvent"
    wx.CallAfter( wxObject.draw_plot )
    
class MainFrame( MyFrame ):
    def __init__(self, datagen ):
        MyFrame.__init__(self, None, -1, "Velleman plot program")
                
        self._paused = False # TODO: add button to handle pausing
        self._datagen = datagen
        self._SkipCount = 1 # the this number of inputs in the graph
        self.init_plot()
        
        # start acquisition loop
        self._datagen.StartTimer( IssueUpdatePlotEvent, self )
        

    def init_plot(self):
         
        self.dpi = 100
        self.fig = Figure((3.0, 3.0), dpi=self.dpi)

        self.axes = self.fig.add_subplot(111)
        self.axes.set_axis_bgcolor('black')
        self.axes.set_title('Very important random data', size=12)
        
        pylab.setp(self.axes.get_xticklabels(), fontsize=8)
        pylab.setp(self.axes.get_yticklabels(), fontsize=8)

        self._plot_data = [i for i in range( 0, self._datagen.Inputs) ]

        # plot the data as a line series, and save the reference 
        # to the plotted line series
        #
        for i in range( 0, self._datagen.Inputs ):
            self._plot_data[i] = self.axes.plot(self._datagen.GetSeries(i),
                                                linewidth=1,
                                                color=(1, 1, 0),
                                                )[0]
                   
        # add the actual canvas
        self.canvas = FigCanvas(self.plotpanel, -1, self.fig)
        
        self.plotpanelvbox = wx.BoxSizer(wx.VERTICAL)
        self.plotpanelvbox.Add(self.canvas, 1, flag=wx.LEFT | wx.TOP | wx.GROW)
        
        self.plotpanel.SetSizer(self.plotpanelvbox)
        self.plotpanelvbox.Fit(self)
        
    def draw_plot(self):
        """ Redraws the plot
        """
        #print "plotting... "
        #print "pending: %d"%self._datagen.PendingCount 

        if not self._paused and self._datagen.PendingCount > 0:
            self._datagen.next() # update of data
        #print "pending: %d"%self._datagen.PendingCount 
        
        
        xmin, xmax = self.GetXMinMax()
        ymin, ymax = self.GetYMaxMin()

        self.axes.set_xbound(lower=xmin, upper=xmax)
        self.axes.set_ybound(lower=ymin, upper=ymax)
        
        # TODO: check box to handle grid on/off
#        # anecdote: axes.grid assumes b=True if any other flag is
#        # given even if b is set to False.
#        # so just passing the flag into the first statement won't
#        # work.
#        #
#        if self.cb_grid.IsChecked():
#            self.axes.grid(True, color='gray')
#        else:
#            self.axes.grid(False)

        # TODO: check box to handle x labels on/off
#        # Using setp here is convenient, because get_xticklabels
#        # returns a list over which one needs to explicitly 
#        # iterate, and setp already handles this.
#        #  
#        pylab.setp(self.axes.get_xticklabels(), 
#            visible=self.cb_xlab.IsChecked())
        
        for i in range( self._SkipCount, self._datagen.Inputs ):
            self._plot_data[i].set_xdata(np.arange( self._datagen.Count ))
            self._plot_data[i].set_ydata(np.array(self._datagen.GetSeries(i)))
        
        self.canvas.draw()
        
    def GetXMinMax(self, XWindow = 50):
        # when xmin is on auto, it "follows" xmax to produce a
        # sliding window effect. therefore, xmin is assigned after
        # xmax.
        #
        if self.ControlBoxXMax.is_auto():
            xmax = self._datagen.Count if self._datagen.Count > XWindow else XWindow
        else:
            xmax = int(self.ControlBoxXMax.manual_value())
        
        if self.ControlBoxXMin.is_auto():
            xmin = xmax - XWindow
        else:
            xmin = int(self.ControlBoxXMin.manual_value())

        return xmin, xmax

    def GetYMaxMin(self):
        # for ymin and ymax, find the minimal and maximal values
        # in the data set and add a mininal margin.
        #
        # note that it's easy to change this scheme to the
        # minimal/maximal value in the current display, and not
        # the whole data set.
        #
        
        if self.ControlBoxYMin.is_auto():
            ymin = round( self._datagen.GetMin()) - 1
        else:
            ymin = int(self.ControlBoxYMin.manual_value())
            
        if self.ControlBoxYMax.is_auto():
            ymax = round( self._datagen.GetMax()) - 1
        else:
            ymax = int(self.ControlBoxYMax.manual_value())
            
        return ymin-1, ymax+1
    
    # -- overloading event handlers
    
    def OnQuitButtonClick(self, event):
        self.Destroy()
        
    def OnFileExit(self, event):
        self.Destroy()
        
    def OnFileSave(self, event):
        MyFrame.OnFileSave(self, event)

if __name__ == '__main__':
    #datasource = DataSrc( 500 )
    #datasource = CsvDataSrc( 'Run.csv')    
    datasource = k8055DataSrc( ReadInterval = 200)
    
    wxk8055 = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = MainFrame( datasource )
    wxk8055.SetTopWindow(frame_1)
    frame_1.Show()
    wxk8055.MainLoop()
