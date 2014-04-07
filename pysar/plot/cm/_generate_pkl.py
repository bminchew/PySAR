"""
Colormap tools 
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

###==========================================================================

mpl_cd = _get_matplotlib_dicts(mpldict=datad)
t_cdic = _cdict_from_cpt()
cmap_d = _cmap_d_from_dict(dict(mpl_cd,**t_cdic))
_write_pkl(dict(mpl_cd,**t_cdic))






