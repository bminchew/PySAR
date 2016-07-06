'''
Geo tools
'''
from __future__ import print_function, division
import sys,os
import numpy as np

__all__ = ['radius_lat','greatCircDist','distance2line','distance2lineseg']

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

def distance2line(vert1,vert2,point):
    '''
    Calculate the distance of a point from a line

    Parameters
    ----------
    vert1           :       array-like
                            2D coordinate (x,y) of one point that defines the line 
    vert2           :       array-like
                            2D coordinate (x,y) of another point that defines the line
    point           :       array-like
                            2D coordinate (x,y) of the point of interest
    '''
    x0, x1, x2 = np.float64(point[0]),np.float64(vert1[0]),np.float64(vert2[0])
    y0, y1, y2 = np.float64(point[1]),np.float64(vert1[1]),np.float64(vert2[1])

    dist = np.abs((y2-y1)*x0 - (x2-x1)*y0 + x2*y1 -x1*y2)/np.sqrt((y2-y1)**2 + (x2-x1)**2)
    return dist
    
def distance2lineseg(vert1,vert2,point):
    '''
    Calculate the distance of a point from a line segment

    Parameters
    ----------
    vert1           :       array-like
                            2D coordinate (x,y) of one vertex
    vert2           :       array-like
                            2D coordinate (x,y) of the other vertex
    point           :       array-like
                            2D coordinate (x,y) of the point of interest
    ''' 
    v1 = np.array(vert1,dtype=np.float64)
    v2 = np.array(vert2,dtype=np.float64)
    p = np.array(point,dtype=np.float64)

    if all(v1 == v2):
        raise ValueError('vertices are collocated')
    elif all(v1 == p) or all(v2 == p):
        return 0.
    elif np.arccos(np.dot((p - v1)/np.linalg.norm(p - v1),(v2 - v1)/np.linalg.norm(v2 - v1))) > 0.5*np.pi:
        return np.linalg.norm(p - v1)
    elif np.arccos(np.dot((p - v2)/np.linalg.norm(p - v2),(v1 - v2)/np.linalg.norm(v1 - v2))) > 0.5*np.pi:
        return np.linalg.norm(p - v2)
    else:
        return distance2line(v1,v2,p)
