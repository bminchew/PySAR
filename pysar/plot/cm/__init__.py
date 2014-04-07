"""
cm
--

Colormap tools and additional colormaps from :ref:`http://soliton.vm.bytemark.co.uk/pub/cpt-city/` 
in matplotlib format

.. currentmodule:: pysar.plot.cm

Functions
---------

.. autosummary::
   :toctree: generated/

   cpt2python           Convert GMT-style CPT files to matplotlib colormap
   cpt2cmap             Convert GMT-style CPT files to matplotlib colormap

Scripts
-------

None

Native functions
----------------

"""
from __future__ import print_function, division

import sys,os
import cPickle
import cpt_tools
import numpy as np
import matplotlib as mpl
import matplotlib.cbook as cbook
import matplotlib.colors as colors
from cpt_tools import *
from _cpt_defs import preload, cptfldr, cptdic, specialcpt, mpl_noinclude
from matplotlib.cm import ma, datad, cubehelix, _generate_cmap
from matplotlib.cm import _reverser, revcmap, _reverse_cmap_spec, ScalarMappable

__all__ = ['cpt_tools','load_gmt','load_idl','load_kst',
            'load_h5','load_gist','load_ij','load_imagej',
            'load_ncl','load_grass','get_options','options']

def load_gmt():
   import gmt
def load_idl():
   import idl
def load_kst():
   import kst
def load_h5():
   import h5
def load_gist():
   import gist
def load_ij():
   import imagej as ij
def load_imagej():
   import imagej
def load_ncl():
   import ncl
def load_grass():
   import grass

###==========================================================================

def get_options():
   '''
   Print available colormaps
   '''
   print(cptdic.keys())

def options():
   '''
   Print available colormaps
   '''
   get_options()

###-----------------------------------------------------------
###-----------------------------------------------------------
try:
   t_cdict = _read_pkl()
   cmap_d = _cmap_d_from_dict(t_cdict)
except:
   mpl_cd = _get_matplotlib_dicts(mpldict=datad)
   t_cdic = _cdict_from_cpt()
   cmap_d = _cmap_d_from_dict(dict(mpl_cd,**t_cdic))
   try: # try to write the pickle file of functions to improve performance next time
      _write_pkl(dict(mpl_cd,**t_cdic))
   except:
      pass 
locals().update(cmap_d)






