from order import Order

#Stategy class
class Strategy(object):
    def __init__(self,data,CO):
        self.__dt=data
        self.__oo=[]
        self.__co=CO        

    def checkSell(self,o,d):
        #update hh if needed
        if d.m20>o.hh:
            o.hh=d.m20
    
        #check if need to sell position
        if (d.close < o.hh * 0.9) or (d.close<o.getPrice()*0.95):
            return True

        return False

    """
    simple toitose trategy
    """
    def run(self):
        for i in range(30,len(self.__dt)):        
            #check for buy postion
            if self.__dt.loc[i].close >= self.__dt.loc[i-1].m20 and len(self.__oo)==0:
                od = Order()
                od.setOrder(i,self.__dt.loc[i])
                self.__oo.append(od)

            #check for short position
            if len(self.__oo)>0:            
                if self.checkSell(self.__oo[0],self.__dt.loc[i]) == True:
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
    Zone strategy
    """
    def ZoneCheckBuy(self,i):
        d = self._dt.loc[i]
        pass

    def run1(self):
	    for i in range(30,len(self.__dt)): 
        


        pass

