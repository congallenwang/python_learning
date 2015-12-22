import pandas as pd
import numpy as np

class DataConstructor(object):
    def __init__(self):
        self.__data=[]


    #read data from csv file and constructor needed column 
    def BuildData(self,code):
        self.__data = pd.read_csv('002215.csv',index_col='date')
        del self.__data['open']
        del self.__data['low'] 
        del self.__data['volume']
        del self.__data['amount'] 
        del self.__data['high'] 

        #self.__data = pd.read_csv('000001.csv')
        d0 = pd.read_csv('000001.csv',index_col='date')

        #read sh index into data
        self.__data['refc']=d0.close[self.__data.index[0]:self.__data.index[-1]]

        #init the margin column  
        self.__data['margin']=np.zeros(len(self.__data))

        #In=close/ref(c,1)-refc/ref(refc,1)*100
        self.__data['IN']=(self.__data.close.shift(-1)/self.__data.close-self.__data.refc.shift(-1)/self.__data.refc)*100

        #in_apex
        self.__data['IN_apex']=np.zeros(len(self.__data))
        self.__data.IN_apex[self.__data[self.__data.IN.shift(1)>self.__data.IN][self.__data.IN.shift(2)<self.__data.IN.shift(1)].index]=1

    #get dat
    def GetData(self):
        return self.__data
