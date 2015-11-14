import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import talib as ta

#print pd.__version__

#print data.head()

class Order(object):
    def __init__(self):
        self.__price = 0
        self.__index = 0
        self.__stock = 0
        self.__closePrice = 0
        self.__closeIndex = 0
        self.__finished = False
        self.__margin = 0;

    def setOrder(self,index,data):
        self.__index = index
        self.__price = data.Close
        self.__stock = 1
        self.__finished = False

    def closeOrder(self,index,data):
        self.__closePrice = data.Close
        self.__closeIndex = index
        self.__finished = True
        self.__margin = sself.__closePrice - self.__price

    def getOrder(self):
        return self.__index,self.__closeIndex,self.__margin

    def isFinished(self):
        return self.__finished

if __name__ == '__main__':
    data = pd.read_csv('orcl-2000.csv')
    OpenOrder = []
    CloseOrder = []
    
    data['m20'] = pd.rolling_max(data.Close,20)

    for i in range(20,len(data)):
        if data.loc[i].Close >= data.loc[i].m20 and len(OpenOrder)==0:
            od = Order()
            od.setOrder(i,data.loc[i])
            OpenOrder.append(od)

        if data.loc[i].Close < (data.loc[i].m20 * 0.9) and len(OpenOrder)>0:
            od = OpenOrder.pop(0)
            od.closeOrder(i,data.loc[i])
            CloseOrder.append(od)

    print "finished"
    #print data.head()
    #od = Order()
    #od.setOrder(0,data.loc[0])

