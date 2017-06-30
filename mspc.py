import numpy as np


class mspc(object):

    def __init__(self,_dim=1,_maxlen=1500,_current=0):
        self.dim=_dim
        self.maxlen=_maxlen
        self.stat=np.zeros(_maxlen,dtype=float)
        self.current=_current
        #print("mspc init")
        #print("dim",self.dim)
        #print("current",self.current)
        #print("aaa",id(self.dim))
        
    def initialize(self):
        #to edit        
        pass
    
    def monitor_obs(self):
        pass

    def monitor(self,data=[],dis1=False,dis2=False,tau=10):
        #not monitoring a distributuion, monitoring a data from a matrix
        if dis1==False:  
            num=len(data) 
            if num>self.maxlen:
                num=self.maxlen
            self.initialize()#
                
            i=0
            for row in data[0:num]: 
                i+=1
                if self.monitor_obs(row):
                    break
            return i
        
        else:
            #monitoring a single distribution                
            if dis2==False: 
                obs=np.zeros(self.dim)
                self.initialize()
                for i in range(self.maxlen):
                    obs=dis1.sample()
                    if self.monitor_obs(obs):
                        break
                return i+1
            
            else:
                #print("monitor two dist")
                #monitoring two distributions
                obs=np.zeros(self.dim)
                self.initialize()
                for i in range(tau):
                    obs=dis1.sample()
                    #print("obs1\n",obs)
                    if self.monitor_obs(obs):
                        return i+1
                for i in range (tau,self.maxlen):
                    obs=dis2.sample()
                    #print("obs1\n",obs)
                    if self.monitor_obs(obs):
                        return i+1
            
