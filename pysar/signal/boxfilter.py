"""
Boxcar filter 

Functions
---------
boxcar1d(data,window,null=None,nullset=None)
boxcar2d(data,window,null=None,nullset=None,thread='auto',numthrd=8,tdthrsh=1e5)

"""
from __future__ import print_function, division
import numpy as np
import _filter_modc

__all__ = ['boxcar1d','boxcar2d']


def boxcar1d(data,window,null=None,nullset=None):
   """ 
   boxcar1d(data,window,null=None,nullset=None)

   1d boxcar filter

   Parameters
   ----------
   data     :  array
               1D array of data to be filtered 
   window   :  int 
               Filter window size in discrete points
   null     :  float or complex
               Null value in image.  This creates an internal boolean array and 
                  replaces null values after filtering.
   nullset  :  float or complex
               Set given null value to zero before filtering and restore to original
                  when filtering is complete.  Only valid if null is provided.  

   Output:
   -------
   D :         array
               1D array of filtered data

   """ 
 
   try:
      b = np.shape(data)[1]
   except:
      if len(data) < 2:
         ValueError('data is a scalar')

   if null != None:
      nuls = np.abs(data - null) < 3.e-7
      if nullset != None:
         data[nuls] = nullset

   if data.dtype == np.float32:
      data = _filter_modc.boxfilter1d(data.copy(),window)
   elif data.dtype == np.float64:
      data = _filter_modc.d_boxfilter1d(data.copy(),window)
   elif data.dtype == np.complex64:
      data.real = _filter_modc.boxfilter1d(data.real.copy(),window)
      data.imag = _filter_modc.boxfilter1d(data.imag.copy(),window)
   elif data.dtype == np.complex128:
      data.real = _filter_modc.d_boxfilter1d(data.real.copy(),window)
      data.imag = _filter_modc.d_boxfilter1d(data.imag.copy(),window)
   else:
      print('Unsupported data type, defaulting to float32')
      print('Consider swithing to float32/float64 or complex64/complex128 before calling the filter\n')
      dtyp = data.dtype
      data = data.astype(np.float32)
      data = _filter_modc.boxfilter1d(data.copy(),window)
      data = data.astype(dtyp)

   if null != None:
      data[nuls] = null

   return data


###=============================================================================



def boxcar2d(data,window,null=None,nullset=None,thread='auto',numthrd=8,tdthrsh=1e5):
   """
   boxcar2d(data,window,null=None,nullset=None,thread='auto',numthrd=8,tdthrsh=1e5)

   2d boxcar filter 

   Parameters
   ----------
   data :      array
               2D array of data to be filtered 
   window :    int or list
               Filter window size in discrete points
                  scalar values use a square window
                  lists should be in order [across, down] 
   null :      float or complex
               Null value in image.  This creates an internal boolean array and 
                  replaces null values after filtering.
   nullset :   float or complex 
               Set given null value to nullset before filtering and restore to original
                  when filtering is complete.  Only valid if null is provided.
   thread  :   string
               Multi-threading options:  ['yes','no','auto'].  'auto' decides based on 
                  the size of data array   
   numthrd :   int
               Number of threads.  Only valid if thread != 'no'
   tdthrsh :   int
               Threshold for 'auto' threading.  Filter is threaded if 
                  number of elements in data > tdthrsh

   Output:
   -------
   D :         array
               2D array of filtered data

   """

   try:
      b = len(window)
      if b == 1:
         d0, d1 = np.int32(window[0]), np.int32(window[0])
      elif b == 2:
         d0, d1 = np.int32(window[0]), np.int32(window[1])
      else:
         raise ValueError('Window must be a list [across,down], [across], or a scalar')
   except:
      d0, d1 = np.int32(window), np.int32(window)

   if null != None:
      nuls = np.abs(data - null) < 3.e-7
      if nullset != None:
         data[nuls] = nullset 

   shp = np.shape(data)
   data = data.flatten()
   dtyp = data.dtype

   threadit = False
   if thread == 'yes':
      threadit = True
   elif thread == 'auto' and len(data) > tdthrsh:
      threadit = True

   if data.dtype == np.float32 and threadit:
      data = _filter_modc.tr_boxfilter2d(data.copy(),shp[1],d0,d1,numthrd)
   elif data.dtype == np.float32:
      data = _filter_modc.boxfilter2d(data.copy(),shp[1],d0,d1)
   elif data.dtype == np.float64 and threadit:
      data = _filter_modc.dtr_boxfilter2d(data.copy(),shp[1],d0,d1,numthrd)
   elif data.dtype == np.float64:
      data = _filter_modc.d_boxfilter2d(data.copy(),shp[1],d0,d1)
   elif data.dtype == np.complex64 and threadit:
      data.real = _filter_modc.tr_boxfilter2d(data.real.copy(),shp[1],d0,d1,numthrd)
      data.imag = _filter_modc.tr_boxfilter2d(data.imag.copy(),shp[1],d0,d1,numthrd)
   elif data.dtype == np.complex64:
      data.real = _filter_modc.boxfilter2d(data.real.copy(),shp[1],d0,d1)
      data.imag = _filter_modc.boxfilter2d(data.imag.copy(),shp[1],d0,d1)
   elif data.dtype == np.complex128 and threadit:
      data.real = _filter_modc.dtr_boxfilter2d(data.real.copy(),shp[1],d0,d1,numthrd)
      data.imag = _filter_modc.dtr_boxfilter2d(data.imag.copy(),shp[1],d0,d1,numthrd)
   elif data.dtype == np.complex128:
      data.real = _filter_modc.d_boxfilter2d(data.real.copy(),shp[1],d0,d1)
      data.imag = _filter_modc.d_boxfilter2d(data.imag.copy(),shp[1],d0,d1)
   else:
      print('Unsupported data type, defaulting to float32')
      print('Consider swithing to float32/float64 or complex64/complex128 before calling the filter\n')
      dtyp = data.dtype
      data = data.astype(np.float32)
      if threadit:
         data = _filter_modc.tr_boxfilter2d(data.copy(),shp[1],d0,d1,numthrd)
      else:
         data = _filter_modc.boxfilter2d(data.copy(),shp[1],d0,d1)
      data = data.astype(dtyp)

   data = data.reshape(shp)
   if null != None:
      data[nuls] = null

   return data
               
