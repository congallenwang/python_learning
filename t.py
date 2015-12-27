import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.gridspec as grid
#import talib as ta
#import matplotlib.finance as fn
#import dateutil.parser as ps

import sys
sys.path.append("/home/alan/Work/stock/python_learning")

from indicator import Indicator
from strategy import Strategy
from plotter import Plotter
from dataconstructor import DataConstructor

#print pd.__version__

#print data.head()

"""
Main Entry point
"""
if __name__ == '__main__':
    
    dt = DataConstructor()
    dt.BuildData('002215')
    
    data = dt.GetData()
    
    CloseOrder = []

    st = Strategy(data,CloseOrder)

    plotter = Plotter(data)
    st.run1()

    plotter.plot1(st.getoo())
    #data = pd.read_csv('000001.csv')
    """   
    #init the margin column  
    #data['margin']=np.zeros(len(data))
 
    #create indicator
    ind = Indicator(data)
    ind.genIndicator()

    #create the strategy
    CloseOrder = []
    st = Strategy(data,CloseOrder)

    #create the plot
    plotter = Plotter(data)

    #run back test instance
    st.run()
    
    print "finished"
    plotter.plot(CloseOrder)
    """

