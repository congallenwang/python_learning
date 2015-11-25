import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import talib as ta
import matplotlib.finance as fn
import dateutil.parser as ps
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
        self.__margin = 0
        #highest number reached
        self.hh = 0

    def setOrder(self,index,data):
        self.__index = index
        #set hh=close
        self.hh=self.__price = data.close
        self.__stock = 1
        self.__finished = False

    def closeOrder(self,index,data):
        self.__closePrice = data.close
        self.__closeIndex = index
        self.__finished = True
        self.__margin = self.__closePrice - self.__price

    def getMargin(self):
        return self.__margin

    def getPrice(self):
        return self.__price

    def getOrder(self):
        return self.__index,self.__closeIndex,self.__price,self.__closePrice,self.__margin

    def isFinished(self):
        return self.__finished

class Plotter(object):
    def __init__(self,data):
        self.data = data;
        pass

    def plot(self,Oderlist):
        plt.plot(np.array(self.data.loc[:,['close']]))
        plt.plot(np.array(self.data.loc[:,'m20']),'r+')
        #draw bottom line
        plt.plot(np.array(self.data.loc[:,'l20']),'b*')
        for o in Oderlist:
	    t = o.getOrder()
            plt.plot(t[0],t[2]+1,'g^')
            plt.plot(t[1],t[3]+1,'rv')
            x=[t[0],t[1]]
            y=[t[2],t[3]]
	    if t[3]>=t[2]:
                plt.plot(x,y,'g')
            else:
                plt.plot(x,y,'r')
        plt.show()

def checkSell(o,d):
    #update hh if needed
    if d.m20>o.hh:
        o.hh=d.m20
    
    #check if need to sell position
    if (d.close < o.hh * 0.9) or (d.close<o.getPrice()*0.95):
        return True

    return False


class Strategy(object):
    def __init__(self,data,OO,CO):
        self.__dt=data
        self.__oo=OO
        self.__co=CO        

    def run(self):
        for i in range(30,len(self.__dt)):        
            #check for buy postion
            if self.__dt.loc[i].close >= self.__dt.loc[i-1].m20 and len(self.__oo)==0:
                od = Order()
                od.setOrder(i,self.__dt.loc[i])
                self.__oo.append(od)

            #check for short position
            if len(self.__oo)>0:            
                if checkSell(self.__oo[0],self.__dt.loc[i]) == True:
                    od = self.__oo.pop(0)
                    od.closeOrder(i,self.__dt.loc[i])
                    self.__co.append(od)
        
            #calculate daily margin
            margin = 0.0
            for o in self.__oo:
                margin += self.__dt.loc[i].close-o.getPrice()
        
            for o in self.__co:
                margin += o.getMargin()
        
            self.__dt.loc[i,['margin']]=1000.0+margin

        #end for
     
        #handle last order if any
        if len(self.__oo)>0:
            od = self.__oo.pop(0)
            od.closeOrder(i,self.__dt.loc[len(self.__dt)-1])
            self.__co.append(od)

if __name__ == '__main__':
    data = pd.read_csv('000001.csv')
    OpenOrder = []
    CloseOrder = []
    
    #top line
    data['m20'] = pd.rolling_max(data.close,20)
   
    #bottom line
    data['l20'] = pd.rolling_min(data.close,20)

    data['margin']=np.zeros(len(data))
    """
    for i in range(0,len(data)):
        data.loc[i,'ndate']=fn.date2num(ps.parse(data.loc[i,'date']))
    """    
    #create the strategy
    st = Strategy(data,OpenOrder,CloseOrder)


    #create the plot
    plotter = Plotter(data)
    
    st.run()
    """
    for i in range(30,len(data)):        
        #check for buy postion
        if data.loc[i].close >= data.loc[i-1].m20 and len(OpenOrder)==0:
            od = Order()
            od.setOrder(i,data.loc[i])
            OpenOrder.append(od)

        #check for short position
        if len(OpenOrder)>0:            
            if checkSell(OpenOrder[0],data.loc[i]) == True:
                od = OpenOrder.pop(0)
                od.closeOrder(i,data.loc[i])
                CloseOrder.append(od)
        
        #calculate daily margin
        margin = 0.0
        for o in OpenOrder:
            margin += data.loc[i].close-o.getPrice()
        
        for o in CloseOrder:
            margin += o.getMargin()
        
        data.loc[i,['margin']]=1000.0+margin

        #end for

    #handle last order if any
    if len(OpenOrder)>0:
        od = OpenOrder.pop(0)
        od.closeOrder(i,data.loc[len(data)-1])
        CloseOrder.append(od)
    """

    print "finished"
    plotter.plot(CloseOrder)


