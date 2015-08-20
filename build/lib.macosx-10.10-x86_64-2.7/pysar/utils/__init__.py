'''
Utils (:mod:`pysar.utils`)
==========================

.. currentmodule:: pysar.utils

Functions
---------

SAR-specific tools (:mod:`pysar.utils.sartools`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated/

   inc2range         Computes range bin for a given incidence angle
   range2inc         Computes incidence angle for a given range bin
   alpha_hh          HH Bragg scattering coefficient for an untilted plane
   alpha_vv          VV Bragg scattering coefficient for an untilted plane

General tools (:mod:`pysar.utils.gen_tools`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autosummary::
   :toctree: generated/

   d2r               Degrees to radians
   r2d               Radians to degrees
   acosd             Return arccos in degrees
   asind             Return arcsin in degrees
   cosd              cos([degrees])
   sind              sin([degrees])
   iscomplex         Test for complex values 
   anycomplex        Tests for any complex values in an array
   allcomplex        Tests for all complex values in an array
   typecomplex       Tests for any valid type of complex value

Geographic tools (:mod:`pysar.utils.geo_tools`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autosummary::
    :toctree: generated/

   radius_lat        Planet radius at latitude  

Scripts
-------

None
'''
import sys,os
import numpy as np
from gen_tools import *
from geo_tools import *
from sartools import *

