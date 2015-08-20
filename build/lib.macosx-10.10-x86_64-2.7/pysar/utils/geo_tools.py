'''
Geo tools
'''
from __future__ import print_function, division
import sys,os
import numpy as np

__all__ = ['radius_lat']

def radius_lat(latitude,a=6378.137,b=6356.7523):
    '''
    Calculate the radius of a planet at a given latitude

    Parameters
    ----------
    latitude        :       float or array-like
                            Geodetic latitude in degrees
    a,b             :       float
                            semi-major and semi-minor axis [Earth values]
    '''
    d2r = np.pi/180.
    cosl = np.cos(latitude*d2r)
    sinl = np.sin(latitude*d2r)                            
    rad = np.sqrt(((a**2*cosl)**2 + (b**2*sinl)**2)/((a*cosl)**2 + (b*sinl)**2))
    return rad
