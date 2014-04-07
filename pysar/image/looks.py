"""
Look routine
"""
from __future__ import print_function, division

import sys,os
import getopt
import numpy as np
import _looks_mod
from pysar.utils.gen_tools import typecomplex

__all__ = ['look','look2D']

def look(data,win,null=None,verbose=0):
   """ 
   Incoherent averaging (looking) routine

   Parameters
   ----------
   data : 2D array
      Input data
   win : int or list
      Filter window size in pixels
      scalar values use a square window
      list should be in order [across, down]
   null : float or complex
      Null value to exclude from filter window
   verbose : int
      1 = print line counter to screen; 0 = don't

   Output
   ------
   D : 2D array
      Filtered data
   """
   out = look2D(data=data,win=win,null=null,verbose=verbose)
   return out

def look2D(data,win,null=None,verbose=0):
   """
   Incoherent averaging (looking) routine

   Parameters
   ----------
   data : 2D array
      Input data
   win : int or list
      Filter window size in pixels
      scalar values use a square window
      list should be in order [across, down]
   null : float or complex
      Null value to exclude from filter window
   verbose : int
      1 = print line counter to screen; 0 = don't

   Output
   ------
   D : 2D array
      Filtered data
   """
   try:
      a = len(win)
      if a == 1:
         d0, d1 = np.int32(win[0]), np.int32(win[0])
      elif a == 2:
         d0, d1 = np.int32(win[0]), np.int32(win[1])
      else:
         print('Incorrect window:  must be list length 1 or 2')
         return None
   except:
      d0, d1 = np.int32(win), np.int32(win)      

   if null:
      donul = 1
   else:
      donul, null = 0, -9.87654321e200

   shp = np.shape(data)
   data = data.flatten()
   dtyp = data.dtype

   outlen, inlen = (shp[0]//d1)*(shp[1]//d0), shp[0]*shp[1]

   if data.dtype == np.float32:
      out = _looks_mod.look2d_real(data,shp[1],d1,d0,outlen,donul,null,verbose)
   elif data.dtype == np.float64:
      out = _looks_mod.look2d_double(data,shp[1],d1,d0,outlen,donul,null,verbose)
   elif data.dtype == np.complex64:
      out = _looks_mod.look2d_cmplx(data,shp[1],d1,d0,outlen,donul,null,verbose)    
   elif data.dtype == np.complex128:
      out = _looks_mod.look2d_dcmplx(data,shp[1],d1,d0,outlen,donul,null,verbose)    
   else:
      print('Unsupported data type...defaulting to float or complex')
      dtyp = data.dtype
      if typecomplex(data):
         data = data.astype(np.complex64)
         out = _looks_mod.look2d_cmplx(data,shp[1],d1,d0,outlen,donul,null,verbose)
      else:
         data = data.astype(np.float32)
         out = _looks_mod.look2d_real(data,shp[1],d1,d0,outlen,donul,null,verbose)
      out = out.astype(dtyp)

   return out.reshape(-1,shp[1]//d0)



      
         
  





