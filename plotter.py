import matplotlib.pyplot as plt
import matplotlib.gridspec as grid

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
        ax1.plot(self.data.close,'k')
        #draw top line
        ax1.plot(self.data.m20,'r.')
        #draw bottom line
        ax1.plot(self.data.l20,'b.')
        #draw MA 
        ax1.plot(self.data.ma30,'y')
        ax1.plot(self.data.ma60,'g')
       
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

    def plot1(self,Orderlist):
        fig,ax=plt.subplots()
        ax.plot(self.data.close,'r')
        for o in Orderlist:
            t=o.getOrder()
            ax.plot(t[0],t[2],'g^')
        
        plt.show()

        pass
