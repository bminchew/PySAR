"""
Median filters

Functions
---------

medfilter2d(data,window,null=None)
"""
from __future__ import print_function, division
import numpy as np
from pysar.signal import _medfilt_modc

__all__ = ['medfilter2d','medfilt2d']

def medfilt2d(data,window,null=None,numthrd=8):
    '''
    medfilt2d(data,window,null=None,numthrd=8)

    2d median filter

    Parameters
    ----------
    data        :   2d array
                    array to be filtered
    window      :   int or 2-element array-like (x,y)
                    window size for filter. If int, window is square.
    null        :   float
                    null value to exclude from filter [None]
    numthrd     :   int
                    number of pthreads [8]

    Return
    ------
    data        :   2d array
                    filtered data; same size and shape as input
    '''
    return medfilter2d(data=data,window=window,null=null,numthrd=numthrd)

def medfilter2d(data,window,null=None,numthrd=8):
    '''
    medfilter2d(data,window,null=None,numthrd=8)

    2d median filter

    Parameters
    ----------
    data        :   2d array
                    array to be filtered
    window      :   int or 2-element array-like (x,y)
                    window size for filter. If int, window is square.
    null        :   float
                    null value to exclude from filter [None]
    numthrd     :   int
                    number of pthreads [8]

    Return
    ------
    data        :   2d array
                    filtered data; same size and shape as input
    '''
    if len(np.shape(data)) != 2:
        raise ValueError('input data must be 2d array')
    try:
        if len(np.shape(window)) == 2:
            winx = int(window[0])
            winy = int(window[1])
        elif len(np.shape(window)) == 1:
            winx = int(window[0])
            winy = winx
        else:
            raise ValueError('unsupported window size %d' % (len(window)))
    except TypeError:
        winx = int(window)
        winy = winx

    if null is None:
        nullv = -np.finfo(type(data[0][0])).max
    else:
        nullv = type(data[0][0])(null)

    drows, dcols = np.shape(data) 
    data = data.flatten()

    if data.dtype == np.float32:
        data = _medfilt_modc.f_medfilt2d(data.copy(),dcols,winx,winy,nullv,numthrd)
    elif data.dtype == np.float64:
        data = _medfilt_modc.d_medfilt2d(data.copy(),dcols,winx,winy,nullv,numthrd)
    else:
        raise TypeError('%s is not a supported data type' % (str(data.dtype)))

    return data.reshape(drows,dcols)

 
