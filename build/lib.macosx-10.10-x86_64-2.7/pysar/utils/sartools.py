'''
SAR-specific tools
'''
from __future__ import print_function, division
import numpy as np
from gen_tools import *

__all__ = ['inc2range','range2inc','alpha_hh','alpha_vv']
###---------------------------------------------------------------------------------------------
def inc2range(inc,h=12495.,rho_0=13450.4278,Re=6371000.,xlook=3.,xspace=1.665514,units='deg'):
   """
      inc2range(inc, h=12495., rho_0=13450.4278, Re=6371000., xlook=3., xspace=1.665514, units='deg')

      Computes range bin for a given incidence angle
   
      Parameters
      ----------
      inc    : float
               incidence angle in units 
      h      : float
               platform altitude in meters [12495.0]
      rho_0  : float
               distance to first range bin in meters [13450.4278]
      Re     : float
               Earth radius in meters [6.371e6]
      xlook  : int
               number of range looks [3]
      xspace : float
               single-look range pixel spacing in meters [1.665514]
      units  : str
               incidence angle units: {'deg' or 'rad'} ['deg'] 

   """
   if not h > 0: raise ValueError('platform altitude must be > 0')
   if not rho_0 > 0: raise ValueError('rho_0 must be > 0')
   if not Re > 0: raise ValueError("Earth's radius must be > 0")
   if not xlook > 0: raise ValueError("xlook must be > 0")
   if not xspace > 0: raise ValueError("xspace must be > 0")

   if 'deg' in units:
      inc = d2r(inc)
   phi = inc + np.pi
   rho = Re*np.cos(phi) +  np.sqrt( (np.cos(phi)**2 - 1)*Re**2 + (h+Re)**2 )
   return np.int64(np.round((rho-rho_0)/(xlook*xspace)))

###---------------------------------------------------------------------------------------------
def range2inc(r,h=12495.,rho_0=13450.4278,Re=6371000.,xlook=3.,xspace=1.665514,units='deg'):
   """
      range2inc(r,h=12495.,rho_0=13450.4278,Re=6371000.,xlook=3.,xspace=1.665514,units='deg')

      Computes incidence angle for a given range bin

      Parameters
      ----------
      r      : int
               range bin
      h      : float
               platform altitude in meters [12495.0]
      rho_0  : float
               distance to first range bin in meters [13450.4278]
      Re     : float
               Earth radius in meters [6.371e6]
      xlook  : int
               number of range looks [3]
      xspace : float
               single-look range pixel spacing in meters [1.665514]
      units  : str
               incidence angle units: {'deg' or 'rad'} ['deg'] 

      Output
      ------
      inc    : float
               incidence angle [units]
   """
   if not r > 0: raise ValueError('r must be > 0')
   if not h > 0: raise ValueError('platform altitude must be > 0')
   if not rho_0 > 0: raise ValueError('rho_0 must be > 0')
   if not Re > 0: raise ValueError("Earth's radius must be > 0")
   if not xlook > 0: raise ValueError("xlook must be > 0")
   if not xspace > 0: raise ValueError("xspace must be > 0")
 
   rho = rho_0 + r * xlook * xspace
   inc = np.pi - np.arccos((-(h + Re)**2 + rho**2 + Re**2)/(2*rho*Re))
   if 'deg' in units:
      inc = r2d(inc)
   return inc

###---------------------------------------------------------------------------------------------
def alpha_hh(eps,theta,units='deg'):
   """  
      alpha_hh(eps, theta, units='deg') 

      HH Bragg scattering coefficient for an untilted plane

            alpha_hh = (cos(theta) - sqr)/(cos(theta) + sqr)

      where sqr = sqrt(eps - sin^2(theta)).

      Parameters
      ----------
      eps   :  complex, float, or ndarray 
               relative permittivity (dielectric constant)
      theta :  complex, float, or ndarray
               incidence angle in units
      units :  str
               incidence angle units: {'deg' or 'rad'} ['deg']

      Output
      ------
      alpha :  complex, float, or ndarray (depending on eps and theta)
               Bragg coefficient 

      Notes
      -----
      *  If both eps and theta are arrays, they must have the same shape. Output will be element-wise.

   """
   if 'rad' in units:
      theta *= 180/np.pi
   ci = cosd(theta)
   sis = (sind(theta))**2
   sqr = np.sqrt(eps - sis)
   return (ci - sqr)/(ci + sqr)

###---------------------------------------------------------------------------------------------
def alpha_vv(eps,theta,units='deg'):
   """  
      alpha_vv(eps,theta,units='deg')

      VV Bragg scattering coefficient for an untilted plane

         alpha_vv = (eps - 1.)*(sis - eps*(1+sis))/(eps*ci + sqr)**2

      where sqr = sqrt(eps - sin^2(theta)), ci = cosd(theta), sis = sind^2(theta).
      
      Parameters
      ----------
      eps   :  complex, float, or ndarray 
               relative permittivity (dielectric constant)
      theta :  complex, float, or ndarray
               incidence angle in units
      units :  str
               incidence angle units: {'deg' or 'rad'} ['deg']

      Output
      ------
      alpha :  complex, float, or ndarray (depending on eps and theta)
               Bragg coefficient 

      Notes
      -----
      *  If both eps and theta are arrays, they must have the same shape. Output will be element-wise.

   """
   if 'rad' in units:
      theta *= 180/np.pi
   ci = cosd(theta)
   sis = (sind(theta))**2
   sqr = np.sqrt(eps - sis)
   return (eps - 1.)*(sis - eps*(1+sis))/(eps*ci + sqr)**2


###---------------------------------------------------------------------------------------------
