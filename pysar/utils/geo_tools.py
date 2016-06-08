'''
Geo tools
'''
from __future__ import print_function, division
import sys,os
import numpy as np

__all__ = ['radius_lat','greatCircDist']

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

def greatCircDist(lat0,lon0,lat,lon,a=6378.137,b=6356.7523):
    '''
    Calculate the Great Circle distance between two points given in degrees latitude and longitude

    Parameters
    ----------
    lat0 and lat    :       float
                            Reference and secondary latitudes in degrees 
    lon0 and lon    :       float
                            Reference and secondary longitudes in degress
    a,b             :       float
                            semi-major and semi-minor axis [Earth values]
    '''
    d2r = np.pi/180.
    Re = radius_lat(lat0,a=a,b=b)
    dist = 2.*Re*np.arcsin(np.sqrt(np.sin(0.5*d2r*(lat-lat0))**2 +
                np.cos(d2r*lat0)*np.cos(d2r*lat)*np.sin(0.5*d2r*(lon-lon0))**2))
    return dist 
