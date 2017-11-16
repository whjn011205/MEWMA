from mspc import mspc
from const_limit import const_limit
import numpy as np
import scipy.linalg as la
import scipy.linalg.lapack
#import update

from ctypes import *
import ctypes
#print("sgsgdsgdsgdgdgggggggggggggg")
import update
#c_double_p =  ctypes.POINTER(ctypes.c_double)
#lib=ctypes.cdll.LoadLibrary("update.so")
#updateA=lib.update
#update2=lib.update2

class mewma(const_limit):
    def __init__(self,_dim=1,_mlen=100,_lam=1,_dyn=False,_mu=np.array([0.0]),_cov=np.array([1.0])):
        #super(mewma,self).__init__(_dim,_mlen)
        super(mewma,self).__init__(_dim,_mlen)
        self.lam   = _lam  
        self.dynamic = _dyn 
        self.mu      = _mu
        self.cov   = _cov
        self.z  = np.zeros(_dim,dtype=float)
        self.adjust = 1
        self.covInv = la.inv(self.cov)
        print(self.cov)
                
    def monitor_obs(self,obs):
        
        val=update.update(self.mu, self.cov, self.covInv,self.z, 
            obs,self.lam, self.adjust,self.dim)
        ## This is to verify whether the C code has the same result as using python version code
#         adjust2=self.adjust
#         val=sample.update(self.mu.copy(), self.cov.copy(), self.covInv.copy(),self.z.copy(), 
#             obs.copy(),self.lam, adjust2,self.dim)
#         val2=self._updateA(obs)
#         print(val, val2)
#         val = 0.01
#         val = self._updateA(obs)

        self.stat[self.current] = val
        self.current += 1
        
        if val > self.ucl:
            return True
     
        return False
        
    def initialize(self):
        self.z = np.zeros(self.z.shape,dtype=float)
        self.adjust = 1
        self.current = 0
            
    def T2(self, mat, vec):
        return la.cho_solve(la.cho_factor(mat),self.vec)
        #tmp = np.zeros(len(vec),dtype=float)
        #tmp=la.cho_solve(la.cho_factor(self.sigma),vec)
        #self.sigma.solve(vec,tmp)
    
    # This method is the pure python version of update function 
    def _updateA(self, obs):
        cons = self.lam/(2-self.lam)

        obs = obs-self.mu
        self.z *= (1-self.lam)
        self.z += obs * self.lam
                
        val = np.dot(self.z,np.dot(self.covInv,self.z))
       
        self.adjust *= (1-self.lam)**2
        val /= (1-self.adjust)
        val /= cons
        
        return val
        
