'''
Read routines for a few standard file formats
'''
from __future__ import print_function
import sys,os
import numpy as np

__all__ = ['readHDF5','readNetCDF','readRaster'] 

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

###-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def readRaster(filename,bandnum=1,rtrnmeta=True,rtrndtyp=np.float32):
   '''
   Return data from a GDAL-readable raster file 

   Parameters
   ----------

   filename :  str
               Name of file
   bandnum  :  int
               Band number to retrieve [1]
   rtrnmeta :  bool
               Return metadata [True]
   rtrndtyp :  dtype
               Return data type [numpy.float32]

   Returns
   -------

   rtrn     :  array[,meta]
   '''
   try:
      from osgeo import gdal, osr
   except ImportError:
      try:
         import gdal, osr
      except ImportError:
         raise ImportError('gdal for Python is required for readRaster')

   gdal.UseExceptions()
   if not os.path.exists(filename):
       raise ValueError('%s does not exist' % filename)

   try:   
       meta = {}
       ds = gdal.Open(filename)
       meta['driver'] = ds.GetDriver().ShortName

       gt = ds.GetGeoTransform()
       sr = osr.SpatialReference(wkt=ds.GetProjection()) 
       
       meta['width'] = ds.RasterXSize
       meta['length'] = ds.RasterYSize

       meta['minx'] = gt[0]
       meta['miny'] = gt[3] + meta['width']*gt[4] + meta['length']*gt[5]
       meta['maxx'] = gt[0] + meta['width']*gt[1] + meta['length']*gt[2]
       meta['maxy'] = gt[3]
       meta['dx'] = gt[1]
       meta['dy'] = gt[5]

       meta['reference'] = ds.GetProjectionRef()
       meta['projection'] = sr.GetAttrValue('projection').strip().replace('_',' ')
       meta['datum'] = sr.GetAttrValue('datum').strip()
       meta['unit'] = sr.GetAttrValue('unit').strip().lower()

       band = ds.GetRasterBand(bandnum)
       meta['bandnum'] = bandnum
       meta['dtype'] = gdal.GetDataTypeName(band.DataType)

       data = band.ReadAsArray(0,0,meta['width'],meta['length'])
       if rtrndtyp is not None:
          data = data.astype(rtrndtyp)
   except:
       raise 
   finally:
       band = None
       ds = None

   if rtrnmeta:
      return data,meta
   else:
      return data
 
