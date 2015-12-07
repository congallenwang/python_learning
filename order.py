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

