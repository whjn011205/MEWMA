from mspc import mspc
import numpy as np
from scipy.linalg import *
import scipy.linalg.lapack


class const_limit(mspc):
    def __init__(self,_dim=1,_mlen=100):
        super(const_limit, self).__init__(_dim,_mlen)
        self.ucl=0
        self.lcl=0
    
    def set_limit(self,_ucl,_lcl):
        self.ucl=_ucl
        self.lcl=_lcl