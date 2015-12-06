import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as grid
import talib as ta
import matplotlib.finance as fn
import dateutil.parser as ps
#print pd.__version__

#print data.head()


#Order class
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



#plot class response for graphic output
class Plotter(object):
    def __init__(self,data):
        self.data = data;
        pass

    def plot(self,Oderlist):
        #set height ration to 4:1
        gs=grid.GridSpec(2,1,height_ratios=[4,1])
       
        fig=plt.figure()

        #ax1 for main chart, ax2 for margin
        ax1=fig.add_subplot(gs[0])
        ax2=fig.add_subplot(gs[1],sharex=ax1)
        
        #draw on main chart
        ax1.plot(np.array(self.data.loc[:,['close']]),'k')
        #draw top line
        ax1.plot(np.array(self.data.loc[:,'m20']),'r.')
        #draw bottom line
        ax1.plot(np.array(self.data.loc[:,'l20']),'b.')
        #draw MA 
        ax1.plot(np.array(self.data.ma30),'y')
        ax1.plot(np.array(self.data.ma60),'g')
       
        #draw order b/s mark
        for o in Oderlist:
	    """
            t0=__index
            t1=__closeIndex
            t2=__price
            t3=__closePrice
            t4=__margin
            """
            t = o.getOrder()
            ax1.plot(t[0],t[2]+1,'g^')
            ax1.plot(t[1],t[3]+1,'rv')
            x=[t[0],t[1]]
            y=[t[2],t[3]]
	    if t[3]>=t[2]:
                ax1.plot(x,y,'g')
            else:
                ax1.plot(x,y,'r')
        
        #draw magin on ax2
        ax2.plot(self.data.margin,'g')

        plt.tight_layout()
        plt.subplots_adjust(hspace=0.1)
        plt.xlim(2000,3000)
        #show the plot
        plt.show()

def checkSell(o,d):
    #update hh if needed
    if d.m20>o.hh:
        o.hh=d.m20
    
    #check if need to sell position
    if (d.close < o.hh * 0.9) or (d.close<o.getPrice()*0.95):
        return True

    return False

#Stategy class
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

"""
Main Entry point
"""
if __name__ == '__main__':
    data = pd.read_csv('000001.csv')
    OpenOrder = []
    CloseOrder = []
   
    #init the margin column  
    data['margin']=np.zeros(len(data))
 
    #create indicator
    ind = Indicator(data)
    ind.genIndicator()

    #create the strategy
    st = Strategy(data,OpenOrder,CloseOrder)

    #create the plot
    plotter = Plotter(data)
    
    st.run()
    
    print "finished"
    plotter.plot(CloseOrder)


