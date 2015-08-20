"""
Cone filter

Functions
---------

conefilter2d(data,window,null=None)
"""
from __future__ import print_function, division
import numpy as np
from pysar.signal import _conefilt_modc

__all__ = ['conefilter2d']

def conefilter2d(data,window,dx=1.,dy=1.,null=None,numthrd=8):
   '''
   conefilter2d(data,window,dx=1.,dy=1.,null=None)

   2d cone filter  

   Parameters
   ----------
   data        :        2d array
                        array to be filtered 
   window      :        float or 2d array 
                        window size for filter in same units as dx. 2d array must be same size as data. 

   Options
   -------
   dx          :        float
                        spacing along x-axis
   dy          :        float
                        same as dx but for y-axis 
   null        :        float
                        null value to exclude from filter [None]
   numthrd     :        int
                        number of pthreads [8]

   Return
   ------
   data        :        2d array 
                        filtered data; same size and shape as input
   '''
   if len(np.shape(data)) != 2:
      raise ValueError('input data must be 2d array')
   try:
      if len(np.shape(window)) == 2 and np.shape(window) != np.shape(data):
         raise ValueError('2d array window must be same size as data array')
      else:
         winarr = window
   except:
      winarr = np.empty_like(data)
      winarr.fill(window)

   nanmask = np.isnan(data)
   anynan = np.any(nanmask)
   if not anynan:
      del nanmask

   infmask = np.isinf(data)
   anyinf = np.any(infmask)
   if not anyinf:
      del infmask   
   
   if null is not None:
      if anynan:
         data[nanmask] = null
      if anyinf:
         data[infmask] = null
      nullmask = np.abs(data - null) < 1.e-7
      anynull = np.any(nullmask)
      if not anynull:
         del nullmask
   else:
      anynull = False
      null = -1.e9
      if anynan:
         data[nanmask] = null
      if anyinf:
         data[infmask] = null 

   drows, dcols = np.shape(data) 
   winarr = winarr.flatten()
   data = data.flatten()
   dtyp = data.dtype

   if data.dtype == np.float32:
      dx,dy,null = np.float32(dx), np.float32(dy), np.float32(null)
      if winarr.dtype != dtyp:
         winarr = winarr.astype(dtyp)
      data = _conefilt_modc.fconefilt2d(data.copy(),winarr,dcols,dx,dy,null,numthrd)
   else:
      raise NotImplementedError('only single precision is currently implemented')

   data = data.reshape(drows,dcols)
   if anynull:
      data[nullmask] = null
   if anynan:
      data[nanmask] = np.nan
   if anyinf:
      data[infmask] = np.inf

   return data

 
