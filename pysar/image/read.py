'''
Read routines for a few standard file formats
'''
from __future__ import print_function
import sys,os
import numpy as np

__all__ = ['readHDF5'] #,'readNetCDF','readRaster','readGeoTiff']

###-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def readHDF5(filename,dataid='z',retxy=False):
   '''
   Return binary data from a single band HDF5 file

   Parameters
   ----------

   filename :  str
               Name of file
   dataid   :  str
               Data tag ['z']
   retxy    :  bool
               Return x,y,data tuple (must be tagged 'x' and 'y') [False]

   Returns
   -------

   ret      :  ndarray or tuple of ndarrays if retxy=True
               Data tagged dataid
   '''
   try:
      import h5py
   except ImportError:
      raise ImportError('h5py is required for readhdf5')

   try:
      fn = h5py.File(filename,'r')
      z = fn[dataid][...]
      try:
         x = fn['x'][...]
         y = fn['y'][...]
      except:
         x, y = None, None
   except:
      raise
   finally:
      fn.close()
   
   if retxy:
      return x,y,z
   else:
      return z

###-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

      
    
