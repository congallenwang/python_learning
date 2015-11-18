plt.plot(np.array(data.loc[:,['Close']]))

plt.plot(np.array(data.loc[:,['m20']]),'r+')
for o in CloseOrder:
	t = o.getOrder()
        plt.plot(t[0],t[2]+1,'g^')
        plt.plot(t[1],t[3]+1,'rv')
        x=[t[0],t[1]]
        y=[t[2],t[3]]
        
	if t[3]>=t[2]:
        	plt.plot(x,y,'g')
        else:
                plt.plot(x,y,'r')
