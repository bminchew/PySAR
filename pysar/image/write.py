'''
Write routines for a few standard file formats
'''
from __future__ import print_function
import sys,os
import numpy as np

__all__ = ['writeHDF5','writeNetCDF','writeRaster','writeGeoTiff']

###-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def writeHDF5(z,filename,x=None,y=None,dataname=None):
   '''
   Write binary data to an HDF5 file

   Parameters
   ----------

   z        :  ndarray
               Data array
   filename :  str
               Name of output file
   x        :  array-like
               2-element list: (top-left x value, x spacing) [(0,1)]
   y        :  array-like
               2-element list: (top-left y value, y spacing) [(z.shape[0]-1,-1)] 
   dataname :  str
               Optional name for dataset to be included in the header [None]
   '''
   import datetime as dt
   now = dt.datetime.now().isoformat()
   try:
      import h5py
   except ImportError:
      raise ImportError('h5py is required for writehdf5')
   try:
      rows,cols = z.shape
   except:
      raise ValueError('z must be a numpy array')
   xyerr = '%s must be None, a 2-element array-like variable, '
   xyerr += 'or a numpy array with length = width(z)' 
   if x is None:
      x = np.arange(cols,dtype=z.dtype)
   elif len(x) == 2:
      x = np.asarray(x,dtype=z.dtype)
      x = x[0] + np.arange(cols)*x[1]
   elif len(x) != cols:
      raise ValueError(xyerr % 'x')
   elif x.dtype != z.dtype:
      x = x.astype(z.dtype)
   if y is None:
      y = np.arange(rows,dtype=z.dtype)
   elif len(y) == 2:
      y = np.asarray(y,dtype=z.dtype)
      y = y[0] + np.arange(rows)*y[1]
   elif len(y) != rows:
      raise ValueError(xyerr % 'y')
   elif y.dtype != z.dtype:
      y = y.astype(z.dtype) 

   if sys.version_info[0] == 2 and isinstance(dataname,basestring):
      zname = dataname
   elif sys.version_info[0] == 3 and isinstance(dataname,str):
      zname = dataname
   else:
      zname = 'z'
 
   try:
      fn = h5py.File(filename,'w') 
      fn.create_dataset('x',data=x)
      fn.create_dataset('y',data=y)
      fn.create_dataset('z',data=z)
      fn['z'].dims.create_scale(fn['x'],'x')
      fn['z'].dims.create_scale(fn['y'],'y')
      fn['z'].dims[0].attach_scale(fn['y'])
      fn['z'].dims[1].attach_scale(fn['x'])
      fn.attrs['Remark'] = 'Created by PySAR writeHDF5 on %s' % now
      fn['z'].attrs['Name'] = zname
   except:
      raise
   finally:
      fn.close()

###-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def writeRaster(z,filename,filetype='GTiff',x=None,y=None,null=None,coords='EPSG:4326'):
   '''
   Write binary data to a GeoTiff file

   Parameters
   ----------

   z        :  ndarray
               Data array 
   filename :  str
               Name of output file
   filetype :  str
               Type of GDAL-supported raster file (`list`_)
   x        :  array-like 
               2-element list: (top-left x value, x spacing) 
               or array of x positions [(0,1)]
   y        :  array-like
               2-element list: (top-left y value, y spacing) 
               or array of y positions [(z.shape[0]-1,-1)]
   null     :  scalar type(z)
               Null or no-data value [None]
   coords   :  str
               Coordinate system (must be recognizable by GDAL) [EPSG:4326]

   Notes
   -----

   *  Requires gdal for python
   *  Only supports single-band outputs
   *  If x or y are default or None, coords is set to None

   .. _list: http://www.gdal.org/formats_list.html
   '''
   try:
      from osgeo import gdal, osr
   except ImportError:
      try:
         import gdal, osr
      except ImportError:
         raise ImportError('gdal for Python is required for writeGeoTiff')
   try:
      ztype = z.dtype.name
      gdtp = _npdtype2gdaldtype()
      if ztype in gdtp.numpy_dtypes:
         gdt = eval('gdal.%s' % gdtp.numpy2gdal[ztype])
      else:
         raise TypeError(ztype,' is not a supported type')
   except:
      raise ValueError('z must be a numpy array')
   err = '%s must be length 2 or %d'

   rows,cols = np.shape(z)
   if x is None:
      x = [0,1]
      coords = None
   elif len(x) == cols:
      xt = [x[0],(x[1]-x[0])]
      x = xt
   elif len(x) != 2:
      raise ValueError(err % ('x',cols))
   if y is None:
      y = [rows-1,-1]
      coords = None
   elif len(y) == rows:
      yt = [y[0],(y[1]-y[0])]
      y = yt
   elif len(y) != 2:
      raise ValueError(err % ('y',rows))
   gxfrm = [x[0],x[1],0,y[0],0,y[1]]

   try:
      rast = gdal.GetDriverByName(filetype).Create(filename,cols,rows,1,gdt)
      rast.SetGeoTransform(gxfrm)

      if coords is not None:  ### set reference coordinate system 
         srs = osr.SpatialReference()
         srs.SetWellKnownGeogCS(coords)
         rast.SetProjection(srs.ExportToWkt())

      band = rast.GetRasterBand(1)
      band.WriteArray(z)   ### write z data 
      if null is not None:
         band.SetNoDataValue(null)
      band.FlushCache()   
   except:
      raise
   finally:
      rast, band = None, None

###-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def writeGeoTiff(z,filename,x=None,y=None,null=None,coords='EPSG:4326'):
   '''
   Write binary data to a GeoTiff file

   Parameters
   ----------

   z        :  ndarray
               Data array
   filename :  str
               Name of output file
   x        :  array-like
               2-element list: (top-left x value, x spacing)
               or array of x positions [(0,1)]
   y        :  array-like
               2-element list: (top-left y value, y spacing)
               or array of y positions [(z.shape[0]-1,-1)]
   null     :  scalar type(z)
               Null or no-data value [None]
   coords   :  str
               Coordinate system (must be recognizable by GDAL) [EPSG:4326]

   Notes
   -----

   *  Requires gdal for python
   *  Only supports single-band outputs
   *  If x or y are default or None, coords is set to None
   '''
   writeRaster(z,filename=filename,filetype='GTiff',x=x,y=y,null=null,coords=coords)

###-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def writeNetCDF(z,filename,x=None,y=None,null=None,xunit=None,yunit=None,zunit=None,
         dataname=None,ncform=4,maxio=1.e8):
   '''
   Write binary data to a NetCDF file

   Parameters
   ----------
   z      :     2d array
                data to be written to netCDF file
   filename  :  str
                output file name
   x      :     array-like
                2-element list: (top-left x value, x spacing)
                or array of x positions [(0,1)]
   y      :     array-like
                2-element list: (top-left y value, y spacing)
                or array of y positions [(z.shape[0]-1,-1)]
   null   :     scalar type(z)
                Null or no-data value [None]
   xunit  :     string or None
                units in x direction [None]
   yunit  :     string or None
                units in y direction [None]
   zunit  :     string or None
                units in z direction [None]
   dataname :   str
                Optional name given to z in the header [None]
   ncform :     int (either 3 or 4) or str (netcdf4 type)
                NetCDF format [4]
   maxio  :     int or float
                maximum single block for output [1.e8]

   Output
   ------
   None

   Notes
   -----
   * if size(z) > maxio, file is written line by line to conserve memory.
   '''
   ncformoptions = ['NETCDF4', 'NETCDF4_CLASSIC','NETCDF3_CLASSIC','NETCDF3_64BIT']
   try:
      from netCDF4 import Dataset
   except:
      raise ImportError('netCDF4 for Python is required for writeNetCDF')
   try:
      rows,cols = z.shape
   except:
      raise ValueError('z must be a numpy array')
   xyerr = '%s must be None, a 2-element array-like variable, '
   xyerr += 'or a numpy array with length = width(z)'
   if x is None:
      x = np.arange(cols,dtype=z.dtype)
   elif len(x) == 2:
      x = np.asarray(x,dtype=z.dtype)
      x = x[0] + np.arange(cols)*x[1]
   elif len(x) != cols:
      raise ValueError(xyerr % 'x')
   elif x.dtype != z.dtype:
      x = x.astype(z.dtype)
   if y is None:
      y = np.arange(rows,dtype=z.dtype)
   elif len(y) == 2:
      y = np.asarray(y,dtype=z.dtype)
      y = y[0] + np.arange(rows)*y[1]
   elif len(y) != rows:
      raise ValueError(xyerr % 'y')
   elif y.dtype != z.dtype:
      y = y.astype(z.dtype)

   if xunit is None:  xunit = 'None'
   if yunit is None:  yunit = 'None'
   if zunit is None:  zunit = 'None'
   if sys.version_info[0] == 2 and isinstance(dataname,basestring):
      zname = dataname
   elif sys.version_info[0] == 3 and isinstance(dataname,str):
      zname = dataname
   else:
      zname = 'z'

   try:
      ncform = np.int32(ncform)
      if ncform == 4:
         ncformat = 'NETCDF4'
      elif ncform == 3:
         ncformat = 'NETCDF3_CLASSIC'
      else:
         print("ncform must be 3 or 4.  Defaulting to 4")
         ncformat = 'NETCDF4'
   except:
      if ncform not in ncformoptions:
         raise ValueError('%s ncform not recognized' % str(ncform))
      else:
         ncformat = ncform

   try:
      fn = Dataset(filename,'w',format=ncformat)
      fn.createDimension('x',cols)
      fn.createDimension('y',rows)
      fn.createVariable('x',x.dtype,('x',))
      fn.createVariable('y',y.dtype,('y',))
      fn.createVariable('z',z.dtype,('y','x'),fill_value=null)

      fn.variables['x'].long_name = 'x'
      fn.variables['y'].long_name = 'y'
      fn.variables['z'].long_name = zname

      fn.variables['x'].units = xunit
      fn.variables['y'].units = yunit
      fn.variables['z'].units = zunit

      fn.variables['x'].actual_range = [np.min(x), np.max(x)]
      fn.variables['y'].actual_range = [np.min(y), np.max(y)]      
      fn.variables['z'].actual_range = [np.min(z), np.max(z)]

      fn.variables['x'][:] = x
      fn.variables['y'][:] = y
      if z.size > maxio:
         for i in xrange(rows):
            fn.variables['z'][i,:] = z[i,:]
      else:
         fn.variables['z'][:,:] = z
   except:
      raise
   finally:
      fn.close()

###========================================================================
class _npdtype2gdaldtype():
   def __init__(self):
      self.gdal2numpy = {   'GDT_Byte'      :   'uint8',
               'GDT_UInt16'    :   'uint16',
               'GDT_Int16'     :   'int16',
               'GDT_UInt32'    :   'uint32',
               'GDT_Int32'     :   'int32',
               'GDT_Float32'   :   'float32',
               'GDT_Float64'   :   'float64',
               'GDT_CInt16'    :   'complex64',
               'GDT_CInt32'    :   'complex64',
               'GDT_CFloat32'  :   'complex64',
               'GDT_CFloat64'  :   'complex128'  }
      self.gdal_dtypes = self.gdal2numpy.keys()
      self.numpy2gdal = {}
      for k,v in self.gdal2numpy.iteritems():
         if k != 'GDT_CInt16' and k != 'GDT_CInt32':
            self.numpy2gdal[v] = k  
      self.numpy_dtypes = self.numpy2gdal.keys()     
      
         


