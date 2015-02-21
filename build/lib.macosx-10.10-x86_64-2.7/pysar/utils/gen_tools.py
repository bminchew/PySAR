'''
General tools
'''
from __future__ import print_function, division
import sys,os
import numpy as np
import numpy.core.numeric as _nx
from math import pi

__all__ = ['d2r','r2d','acosd','arccosd','asind','arcsind','cosd','sind',
            'iscomplex','anycomplex','allcomplex','typecomplex']
###---------------------------------------------------------------------------------------------
def d2r(n):
   """ 
   degrees to radians 
   """
   return n*pi/180.
###---------------------------------------------------------------------------------------------
def r2d(n):
   """ 
   radians to degrees
   """
   return n*180./pi
###---------------------------------------------------------------------------------------------
def acosd(n):
   """ 
   t [degrees] = arccos(n)
   """
   return r2d(np.arccos(n))
def arccosd(n):
   """ 
   t [degrees] = arccos(n)
   """
   return acosd(n)
###---------------------------------------------------------------------------------------------
def asind(n):
   """ 
   t [degrees] = arcsin(n)
   """
   return r2d(np.arcsin(n))
def arcsind(n):
   """ 
   t [degrees] = arcsin(n) 
   """
   return asind(n)
###---------------------------------------------------------------------------------------------
def cosd(n):
   """ 
   t = cos(n [degrees])
   """
   return np.cos(d2r(n))
###---------------------------------------------------------------------------------------------
def sind(n):
   """ 
   t = sin(n [degrees])
   """
   return np.sin(d2r(n))

###---------------------------------------------------------------------------------------------
def iscomplex(n):
   """Tests for complexity...returns np.iscomplex(n)
   """
   return np.iscomplex(n)

###---------------------------------------------------------------------------------------------

def anycomplex(n):
   """ Tests for any complexity
   """
   return np.any(np.iscomplex(n))

###---------------------------------------------------------------------------------------------
def allcomplex(n):
   """ Tests for all complexity
   """
   return np.all(np.iscomplex(n))

###---------------------------------------------------------------------------------------------
def typecomplex(n):
   """ tests for any type complex
   """
   nx = _nx.asanyarray(n)
   return issubclass(nx.dtype.type, _nx.complexfloating)
