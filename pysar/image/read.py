'''
Read routines for a few standard file formats
'''
from __future__ import print_function
import sys,os
import numpy as np

__all__ = ['readHDF5','readNetCDF'] 

###-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def readHDF5(filename,dataid='z',rtrnxy=False):
   '''
   Return binary data from a single band HDF5 file

   Parameters
   ----------

   filename :  str
               Name of file
   dataid   :  str
               Data tag ['z']
   rtrnxy   :  bool
               Return x,y,data tuple (must be tagged 'x' and 'y') [False]

   Returns
   -------

   rtrn     :  ndarray or tuple of ndarrays if rtrnxy=True
               Data tagged dataid, 'x', and 'y'
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
   
   if rtrnxy:
      return x,y,z
   else:
      return z

###-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def readNetCDF(filename,dataid='z',rtrnxy=False):
   '''
   Return binary data from a single band NetCDF file

   Parameters
   ----------
   
   filename :  str
               Name of file
   dataid   :  str
               Data tag ['z']
   rtrnxy   :  bool
               Return x,y,data tuple (must be tagged 'x' and 'y') [False]

   Returns
   -------

   rtrn     :  ndarray or tuple of ndarrays if rtrnxy=True
               Data tagged dataid, 'x', and 'y'
   '''
   try:
      from netCDF4 import Dataset
   except:
      raise ImportError('netCDF4 for Python is required for readNetCDF')
  
   try:
      fn = Dataset(filename,'r')
      z = fn.variables[dataid][...]
      try:
         x = fn.variables['x'][...]
         y = fn.variables['y'][...]
      except:
         try:  ### for backward compatability 
             rows, cols = fn.variables['dimension'][1], fn.variables['dimension'][0]
             xmin, xmax = fn.variables['x_range'][0], fn.variables['x_range'][1]
             ymin, ymax = fn.variables['y_range'][0], fn.variables['y_range'][1]
             x = np.linspace(xmin,xmax,cols)
             y = np.linspace(ymin,ymax,rows)
             z = z.reshape(rows, cols)
         except:
             x, y = None, None
   except:
      raise
   finally:
      fn.close()

   if rtrnxy:
      return x,y,z
   else:
      return z
 
    
