"""
mask_tools.py  :  Tools for creating and manipulating masks 

Contents
--------
poly2mask(polygon,imdim,imtype=np.float32)
xy2mask(polygon,imdim,imtype=np.float32)
ll2mask(latlon,imdim,corner,spacing,imtype=np.float32)
buffermask(mask,width,dx=1.,dy=1.)
"""
from __future__ import print_function, division
import numpy as np

__all__ = ['poly2mask','xy2mask','ll2mask','buffermask']

###==================================================================================
def poly2mask(polygon,imdim,imtype=np.float32):
   """
   poly2mask(polygon,imdim,imtype=np.float32)

   Generate a region-of-interest mask from a polygon.  

   Parameters
   ----------
   polygon     :     {int or float} list of tuples 
                     polygon vertices; format [(x0,y0),...,(xn,yn)]
   imdim       :     {int} list, tuple, or ndarray
                     image dimension (x,y) or (columns,rows)
   imtype      :     {str or numpy type} (Optional)
                     data type for output image [np.float32]

   Output
   ------
   mask        :     ndarray
                     mask array astype(imtype)

   Notes
   -----
   *  Values inside polygon will be True or 1 depending on imtype
 
   """
   try:
      from PIL import Image, ImageDraw
   except:
      raise ImportError('poly2mask.py requires PIL.')

   if polygon[-1] != polygon[0]:  polygon.append(polygon[0])

   nx, ny = imdim[0], imdim[1]
   img = Image.new('L', (nx,ny), 0) 
   ImageDraw.Draw(img).polygon(polygon, outline=1, fill=1)
   try:
      mask = np.array(img, dtype=imtype)
   except:
      mask = np.array(img)
      try:
         mask = mask.astype(imtype)
      except:
         raise TypeError('imtype is not a valid data type')
   del img
   return mask 
   
###==================================================================================
def ll2mask(latlon,imdim,corner,spacing,imtype=np.float32):
   """
   ll2mask(latlon,imdim,corner,spacing,imtype=np.float32)

   Generate a region-of-interest mask from a polygon whose vertices are given in lat/lon.

   Parameters
   ----------
   latlon      :  {int or float} list of tuples
                  polygon vertices in degrees lat/lon; format: [(lat0,lon0),...,(latn,lonn)]
   imdim       :  {int} list, tuple, or ndarray
                  image dimension (x,y) or (columns,rows)
   corner      :  {int or float} list, tuple, or ndarray
                  lat and lon of one image corner; format: [lat,lon]
   spacing     :  {int or float} list, tuple, or ndarray
                  grid spacing (see notes below); format: [lat_space, lon_space]
   imtype      :  {str or numpy type} (Optional)
                  data type for output image [np.float32]

   Output 
   ------
   mask        :  ndarray
                  mask array astype(imtype)

   Notes
   -----
   *  Values inside polygon will be True or 1 depending on imtype
   *  Spacing is sign-sensitive. The sign of spacing values defines the corner.  
      Ex. [-lat_space,lon_space] is the upper left corner (i.e. stepping one pixel
      in lat and lon from the corner means going south and east)  

   """
   polygon = [None]*len(latlon)
   for i,ent in enumerate(latlon):
      x = (ent[1] - corner[1]) / spacing[1]
      y = (ent[0] - corner[0]) / spacing[0]
      polygon[i] = (x,y)
   return poly2mask(polygon=polygon,imdim=imdim,imtype=imtype)

###==================================================================================
def xy2mask(polygon,imdim,imtype=np.float32):
   """ 
   xy2mask(polygon,imdim,imtype=np.float32)

   Generate a region-of-interest mask from a polygon given in xy image coordinates.  

   Parameters
   ----------
   polygon     :     {int or float} list of tuples 
                     polygon vertices; format [(x0,y0),...,(xn,yn)]
   imdim       :     {int} list, tuple, or ndarray
                     image dimension (x,y) or (columns,rows)
   imtype      :     {str or numpy type} (Optional)
                     data type for output image [np.float32]

   Output
   ------
   mask        :     ndarray
                     mask array astype(imtype)

   Notes
   -----
   *  Values inside polygon will be True or 1 depending on imtype
 
   """
   return poly2mask(polygon=polygon,imdim=imdim,imtype=imtype)

###==================================================================================
def buffermask(mask,width,dx=1.,dy=1.):
    '''
    buffermask(mask,width,dx=1.,dy=1.)

    Add or remove a buffer zone from a binary mask

    Parameters
    ----------
    mask    :   ndarray
                binary mask (ROI values assumd = 1)
    width   :   float
                width of buffer zone (> 0 for outer buffer; < 0 for inner)
    dx      :   float
                grid spacing in x direction [1]
    dy      :   float
                grid spacing in y direaction [1]
    '''
    from pysar.signal import boxfilter
    if np.abs(width) < np.finfo(np.float32).eps:
        raise ValueError('width must not be 0')

    mtype = mask.dtype
    if mask.ndim == 1:
        window = int(np.abs(width//dx))
        fmask = boxfilter.boxcar1d(mask.astype(np.float32),window)
    elif mask.ndim == 2:
        window = [int(np.abs(width//dx)), int(np.abs(width//dy))]
        fmask = boxfilter.boxcar2d(mask.astype(np.float32),window) 
 
    if np.sign(width) == -1:
        onemask = fmask > 0.99
    else:
        onemask = fmask > 0.01
    fmask = 0.
    fmask[onemask] = 1.
    return fmask.astype(mtype)


