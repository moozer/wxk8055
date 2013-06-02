'''
Created on May 21, 2013

@author: moz
'''
import time
import k8055
import datetime

DACvalfile = "dacval.txt"
sleeptime = 0.5
outfilename = "measurements_130521.csv"

if __name__ == '__main__':
    b = k8055.Board()
    starttime = datetime.datetime.now()
    datafile = open( outfilename,"w")
    
    print "start time: %s"%starttime
    print "looping every %f seconds"%sleeptime
    print "datafile: %s"%outfilename
    
    print "dtime\toutput\tana1\tana2"
    
    while True:
        
        # read dac value from file.
        f = open( DACvalfile )
        dacval = int(f.readline())
        f.close()

        # set the output        
        b.set_analog1( dacval)

        # read and output something
        b.read()       
        dtime = datetime.datetime.now()-starttime
        
        # output to screen and file 
        print "%s\t%d\t%d\t%d"%(dtime, b.analog_output1, b.analog1, b.analog2)
        print >> datafile, "%s\t%d\t%d\t%d"%(dtime, b.analog_output1, b.analog1, b.analog2)

        time.sleep( sleeptime )
        