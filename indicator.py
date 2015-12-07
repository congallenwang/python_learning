import pandas as pd
import talib as ta
import numpy as np

#Indicator for the TA 
class Indicator(object):
    def __init__(self,data):
        self.__dt=data

    def genIndicator(self):
        #top line
        self.__dt['m20'] = pd.rolling_max(self.__dt.close,20)
        self.__dt.m20=self.__dt.m20.shift(1)
        #bottom line
        self.__dt['l20'] = pd.rolling_min(self.__dt.close,20)
        self.__dt.l20=self.__dt.l20.shift(1)
        #MA30
        self.__dt['ma30'] = ta.MA(np.array(self.__dt.close),30)
        #MA60
        self.__dt['ma60'] = ta.MA(np.array(self.__dt.close),60)


