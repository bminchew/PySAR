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

Generate a mask from a 2d polygon (:mod:`pysar.image.poly2mask`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated/

   poly2mask            Polygon in Cartesian coordinates
   ll2mask              Polygon in latitude/longitude coordinates
   xy2mask              Same as poly2mask

Write some standard formats (:mod:`pysar.image.write`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated/

   writeHDF5            Write binary data to an HDF5 file
   writeNetCDF          Write binary data to a NetCDF file
   writeRaster          Write binary data to a raster file
   writeGeoTiff         Write binary data to a GeoTiff file

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
from poly2mask import *
from looks import *
import sarfilter
import sarlooks
