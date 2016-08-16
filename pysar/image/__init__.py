'''
Image (:mod:`pysar.image`)
==========================

.. currentmodule:: pysar.image

Functions
---------

Decimate (look) 2D images (:mod:`pysar.image.looks`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated/

   look        Image decimation 
   look2D      Same as look

Generate a mask from a 2d polygon (:mod:`pysar.image.mask_tools`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated/

   poly2mask            Polygon in Cartesian coordinates
   ll2mask              Polygon in latitude/longitude coordinates
   xy2mask              Same as poly2mask
   buffermask           Expand or contract a mask 

Write some standard formats (:mod:`pysar.image.write`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated/

   writeHDF5            Write data to an HDF5 file
   writeNetCDF          Write data to a NetCDF file
   writeRaster          Write data to a raster file
   writeGeoTiff         Write data to a GeoTiff file
   writeBinary          Write data to a binary file
   writeMultiBand2d     Write 2D multiband data to a binary file

Read some standard formats (:mod:`pysar.image.read`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated/

   readHDF5             Read data from an HDF5 file
   readNetCDF           Read data from a NetCDF file
   readRaster           Read data from a GDAL-supported raster file

Scripts
-------

================     ======================================
`sarlooks`           2D image decimation
`sarfilter`          2D image filtering 
================     ======================================
'''
import numpy as np
from pysar.signal import boxfilter, conefilter

from read import *
from write import *
from mask_tools import *
from looks import *
import sarfilter
import sarlooks
