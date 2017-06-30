import cProfile,pstats,io
import numpy as np
import sys
import time
#sys.path.insert(0,'D:/WH/MSPC/MSPC_python/')
#sys.path.insert(0,'../')

from mewma import mewma

np.set_printoptions(formatter={'float': '{:0.2f} '.format})

dim=3
rep=10000
maxlen=500
tau=400
ucl=40
lcl=0
m0=20 #how many data needed before statrting to monitor

mu=np.zeros(dim,dtype=float)
sigma=np.identity(dim,dtype=float)
mu2=mu
sigma2=sigma*1.1



ew=mewma(_dim=dim,_mlen=maxlen,_lam=0.1,_dyn=False,_mu=mu,_cov=sigma)

ew.set_limit(ucl,lcl)
print("lcl:",ew.lcl)
print("ucl:",ew.ucl)
print("mean:\n",mu)
print("cov:\n",sigma,)

print("\ntau",tau)

print("mean2:\n",mu2)
print("cov2:\n",sigma2,)

print("\nrunID   t-tau  MonStat  obs")
print("----------------------------------------------")

result=np.zeros(rep)

pr=cProfile.Profile()
pr.enable()

start=time.time()
for i in range(rep):
    
    icdata=np.random.multivariate_normal(mu,sigma,tau)
    obsdata=np.random.multivariate_normal(mu2,sigma2,maxlen-tau)
    #data=np.concatenate((icdata,obsdata),axis=0)
    ic_idx=0
    obs_idx=0
    ew.initialize()
    
    for j in range(maxlen):
        if j < tau:
            obs=icdata[j]
        else:
            obs=obsdata[j-tau]
                
        alarm=ew.monitor_obs(obs)
        if alarm is True and j>=m0:
            print("%-6i  %-4i"%(i,j-tau),"%8.3f  " % (ew.stat[ew.current-1]),obs,)
            break
    
    # if cannot detect the change
    if alarm is False:
        print("undetected")
        result[i]=9999
        continue
    else:
        result[i]=j-tau

end=time.time()
print("%i loops, use: %fs" %(rep, end-start))

# false_alarm_rate=sum([1 for t in result if t<0])/rep
# mean_response_time=np.mean([t for t in result if t>=0])
# sd_response_time=( np.mean([(t-mean_response_time)**2 for t in result if t>=0]) )**0.5
# print("Average response time:",mean_response_time)
# print("Standard Deviation:",sd_response_time)
# print("False_alrm_rate:",false_alarm_rate)
    

pr.disable()
pr.create_stats()
print("\n------------------------------------\nProfiling")
print("--------------------------------------\n")
pr.print_stats(sort='tottime')


#s=io.StringIO()
#sortby='cumulative'
#ps=pstats.Stats(pr,stream=s).sort_stats(sortby)
#ps.print_stats()
#print(s.getvalue)