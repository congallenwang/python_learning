import pandas as pd
import numpy as np

class DataConstructor(object):
    def __init__(self):
        self.data=[]


    #read data from csv file and constructor needed column 
    def BuildData(self,code):
        self.data = pd.read_csv('600218.csv',index_col='date')
        del self.data['open']
        del self.data['low'] 
        del self.data['volume']
        del self.data['amount'] 
        del self.data['high'] 

        #self.__data = pd.read_csv('000001.csv')
        d0 = pd.read_csv('000001.csv',index_col='date')

        #read sh index into data
        self.data['refc']=d0.close[self.data.index[0]:self.data.index[-1]]

        #init the margin column  
        #self.__data['margin']=np.zeros(len(self.__data))

        #In=close/ref(c,1)-refc/ref(refc,1)*100
        self.data['IN']=(self.data.close/self.data.close.shift(7)-self.data.refc/self.data.refc.shift(7))*100

        #in_apex=(IN<REF(IN,1) AND REF(IN,1)>REF(IN,2)) ? 1,0;
        self.data['IN_apex']=np.zeros(len(self.data))
        index = self.data.IN[self.data.IN.shift(1)>self.data.IN][self.data.IN.shift(2)<self.data.IN.shift(1)].index
        self.data.IN_apex[index]=1

        #IN_T1 = (MAX(IN,15)<0.10 AND MIN(IN,15)>0 AND SUM(IN_apex,15)>4)) ? 1, 0
        self.data['IN_T1']=np.zeros(len(self.data))
        index = self.data.IN[pd.rolling_max(self.data.IN,15)<10][pd.rolling_min(self.data.IN,15)>0][pd.rolling_sum(self.data.IN_apex,15)>4].index
        self.data.IN_T1[index]=1

        #IN_T = (IN<0 AND REF(IN,1)>0 AND SUM(IN_T1,3)>0) ? 1, 0
        self.data['IN_T']=np.zeros(len(self.data))
        index = self.data.IN[self.data.IN<self.data.IN.shift(1)][self.data.IN.shift(1)>0][pd.rolling_sum(self.data.IN_T1,3)>0].index
        self.data.IN_T[index]=1

    #get dat
    def GetData(self):
        return self.data
