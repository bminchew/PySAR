"""
Work with cpt files in Python

"""

import sys,os
import cPickle
import numpy as np
import matplotlib as mpl 
import matplotlib.cbook as cbook
import matplotlib.colors as colors
from _cpt_defs import preload, cptfldr, cptdic, specialcpt, mpl_noinclude
from matplotlib.cm import ma, datad, cubehelix, _generate_cmap
from matplotlib.cm import _reverser, revcmap, _reverse_cmap_spec, ScalarMappable

__all__ = ['cptError','_stitch_gmt_hsv','cpt2python','_get_cm_from_cpt',
         '_get_cm_from_pkl','get_cmap','cpt2cmap','_read_pkl','_write_pkl',
         '_read_json','_write_json','_cmap_d_from_cpt','_cmap_d_from_dict',
         '_cdict_from_cpt','_get_matplotlib_cmaps','_get_matplotlib_dicts']

###==========================================================================
class cptError(Exception):
   pass

###==========================================================================
def _stitch_gmt_hsv(colstring,splitter='-'):
   sp = colstring.split(splitter)
   if splitter == '-' and len(sp) > 3:
      temp = sp
      sp, i = [], 0
      while i < len(temp):
         if temp[i][-1] == 'e' or temp[i][-1] == 'E':
            sp.append(temp[i] + temp[i+1])
            i += 2
         else:
            sp.append(temp[i])
            i += 1
   return sp


def cpt2python(cptfile):
   """
   Convert GMT-stype CPT file to python colormap.  This routine is modified from a 
   routine contained in the scipy cookbook. 
   """
   fid = open(cptfile,'r')
   reads = fid.readlines()
   fid.close()

   x = np.empty(len(reads),dtype=np.float32)
   r,g,b = np.empty_like(x),np.empty_like(x),np.empty_like(x)
   colormod = 'RGB'
   i = 0
   for read in reads:
      if len(read.lstrip()) > 0:
         row = read.split()
         if read.lstrip()[0] == '#':
            if 'COLOR_MODEL' in read: colormod = row[-1]
         elif 'B' != row[0] and 'F' != row[0] and 'N' != row[0]:
            if '/' not in row[1] and '-' not in row[1]:
               x[i] = np.float32(row[0])
               r[i] = np.float32(row[1])
               g[i] = np.float32(row[2])
               b[i] = np.float32(row[3])
               xt = np.float32(row[4])
               rt = np.float32(row[5])
               gt = np.float32(row[6])
               bt = np.float32(row[7])
            elif len(row) == 4:
               if '-' in row[1]:
                  spl = '-'
                  colormod = 'HSV'
               else:
                  spl = '/'
               x[i] = np.float32(row[0])
               rs = _stitch_gmt_hsv(row[1],splitter=spl)
               r[i] = np.float32(rs[0])
               g[i] = np.float32(rs[1])
               b[i] = np.float32(rs[2])
               xt = np.float32(row[2])
               rs = _stitch_gmt_hsv(row[3],splitter=spl)
               rt = np.float32(rs[0])
               gt = np.float32(rs[1])
               bt = np.float32(rs[2])
            else:
               raise cptError('Unsupported cpt format...revise file to form x1 r1 g1 b1 x2 r2 g2 b2')
            i += 1
   x[i], r[i], g[i], b[i] = xt, rt, gt, bt
   i += 1
   x, r, g, b = x[:i], r[:i], g[:i], b[:i]

   if colormod == 'HSV' or colormod == 'hsv':
      import colorsys
      for i in xrange(len(r)):
         r[i], g[i], b[i] = colorsys.hsv_to_rgb(r[i]/360.,g[i],b[i])
   elif colormod == 'RGB' or colormod == 'rgb':
      r /= 255.; g /= 255.; b /= 255.
   else:
      raise NotImplementedError('%s color system is not supported' % colormod)

   x -= x[0]
   x /= x[-1]

   red, blue, green = [None]*len(x), [None]*len(x), [None]*len(x)
   for i in xrange(len(x)):
      red[i] = (x[i],r[i],r[i])
      blue[i] = (x[i],b[i],b[i])
      green[i] = (x[i],g[i],g[i])
   cd = {'red' : red, 'green' : green, 'blue' : blue}
   return cd


###-----------------------------------------------------------
def _get_cm_from_cpt(filename,cmapname='colormap',lutsize=None,inverse=False):
   if not lutsize:
      import matplotlib as mpl 
      lutsize = mpl.rcParams['image.lut'] 
   cdict = cpt2python(filename)
   if inverse: cdict = _reverse_cmap_spec(cdict)
   return colors.LinearSegmentedColormap(cmapname,cdict,lutsize) 

def _get_cm_from_pkl(filename,cmapname='colormap',lutsize=None,inverse=False):
   if not lutsize:
      import matplotlib as mpl 
      lutsize = mpl.rcParams['image.lut']
   pkl_file = open(filename, 'rb')
   cdict = pickle.load(pkl_file)
   pkl_file.close()
   if inverse: cdict = _reverse_cmap_spec(cdict)
   return colors.LinearSegmentedColormap(cmapname,cdict,lutsize)

###-----------------------------------------------------------
def get_cmap(name,lut=None):
   if name in cmap_d:
      if lut is None:
         return cmap_d[name]
      else:
         nm, inverse = name, False
         if name[-2:] == '_r': 
            nm, inverse = name[:-2], True
         return _get_cm_from_cpt(filename=cptfldr+cptdic[nm],cmapname=nm,
                     lutsize=lut,inverse=inverse)
###-----------------------------------------------------------
def cpt2cmap(filename,cmapname='colormap',lut=None,inverse=False):
   if not lut:
      import matplotlib as mpl 
      lut = mpl.rcParams['image.lut']
   cdict = cpt2python(filename)
   if inverse: cdict = _reverse_cmap_spec(cdict)
   return colors.LinearSegmentedColormap(cmapname,cdict,lut)

###----------------------------------------------------------
def _read_pkl():
   pkl_file = open(cptfldr+'cmaps.pkl', 'rb')
   cmapdict = cPickle.load(pkl_file)
   pkl_file.close()
   return cmapdict 

def _write_pkl(cmapdict):
   pkl_file = open(cptfldr+'cmaps.pkl', 'wb')
   cPickle.dump(cmapdict,pkl_file,-1)
   pkl_file.close()

def _read_json():
   import json
   json_file = open(cptfldr+'cmaps.json', 'rb')
   cmapdict = json.load(json_file)
   json_file.close()
   return cmapdict

def _write_json(cmapdict):
   import json
   json_file = open(cptfldr+'cmaps.pkl', 'wb')
   json.dump(cmapdict,json_file)
   json_file.close()

###----------------------------------------------------------
def _cmap_d_from_cpt():
   cmap_d = {}
   for k,v in cptdic.iteritems():
      cmap_d[k] = _get_cm_from_cpt(filename=cptfldr+v,cmapname=k,
               lutsize=lutsize,inverse=False)
      cmap_d[k+'_r'] = _get_cm_from_cpt(filename=cptfldr+v,cmapname=k,
               lutsize=lutsize,inverse=True)
   return cmap_d

def _cmap_d_from_dict(indict,lutsize=None):
   if lutsize is None:
      import matplotlib as mpl
      lutsize = mpl.rcParams['image.lut']
   cmap_d = {}
   for k,v in indict.iteritems():
      if 'red' in v:
         cmap_d[k] = colors.LinearSegmentedColormap(k,v,lutsize)
      else:
         cmap_d[k] = colors.LinearSegmentedColormap.from_list(k,v,lutsize)
   return cmap_d


def _cdict_from_cpt():
   import matplotlib as mpl
   lutsize = mpl.rcParams['image.lut']
   cdict = {}
   for k,v in cptdic.iteritems():
      cdict[k] = cpt2python(cptfldr+v)
      cdict[k+'_r'] = _reverse_cmap_spec(cdict[k])
   return cdict


###----------------------------------------------------------
def _get_matplotlib_cmaps(mpldict):
   lutsize = mpl.rcParams['image.lut']
   tempdic = {}
   for k,v in mpldict.iteritems():
      if k not in mpl_noinclude:
         tempdic[k] = _generate_cmap(k,lutsize)
      else:
         n = 100
         indices = np.linspace(0,1.,n)
         t_cmap = _generate_cmap(k,lutsize)
         t_cmapents = t_cmap(indices)
         t_cdict = {}
         for ki,key in enumerate(('red','green','blue')):
            t_cdict[key] = [ (indices[i], t_cmapents[i,ki], t_cmapents[i,ki]) for i in xrange(n) ]
         tempdic[k] = colors.LinearSegmentedColormap(k,t_cdict,lutsize)
   return tempdic

def _get_matplotlib_dicts(mpldict):
   lutsize = mpl.rcParams['image.lut']
   tempdic = {}
   for k,v in mpldict.iteritems():
      if k not in mpl_noinclude:
         tempdic[k] = v
      else:
         n = 100
         indices = np.linspace(0,1.,n)
         t_cmap = _generate_cmap(k,lutsize)
         t_cmapents = t_cmap(indices)
         t_cdict = {}
         for ki,key in enumerate(('red','green','blue')):
            t_cdict[key] = [ (indices[i], t_cmapents[i,ki], t_cmapents[i,ki]) for i in xrange(n) ]
         tempdic[k] = t_cdict
   return tempdic

###-----------------------------------------------------------

