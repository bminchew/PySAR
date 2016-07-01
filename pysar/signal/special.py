"""
Specialty filtering routines

Contents
--------

taper(data,percent)                    :  Basic cosine taper
conefilter2d(data,window,null=None)    :  Cone-shaped filter

"""
from __future__ import print_function, division
import numpy as np
import conefilter
from conefilter import *

__all__ = ['taper','conefilter'] + conefilter.__all__

###===================================================================================
def taper(data,percent=3):
   """
   Cosine taper

   taper(data,percent)

   Parameters
   ----------
   data  :        array
                  Input data
   percent :      float
                  Percent of len(data) to taper (%)

   Outputs
   --------
   F   :          array
                  Tapered data

   """

   if not len(data) > 1: 
      raise ValueError('data is a scalar')
   if not percent >= 0:  
      raise ValueError('percent must be >= 0')

   n = np.int32(len(data)*percent/100.)
   if n == 0: return data

   theta = np.linspace(np.pi,2.*np.pi,n)
   taper = 0.5*(np.cos(theta)+1)
   data[:n]  *= taper
   data[-n:] *= taper[::-1]
   return data

