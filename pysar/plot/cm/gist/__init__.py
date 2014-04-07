import sys,os
import cPickle
import matplotlib.colors as colors
from pysar.etc.excepts import cptError
from pysar.plot.cm import cpt2python, _cmap_d_from_dict, _reverse_cmap_spec

def _read_pkl():
   here='/'.join(__file__.split('/')[:-1]) + '/'
   fid = open(here+'cmaps.pkl','rb')
   cmapdict = cPickle.load(fid)
   fid.close()
   return cmapdict

def _write_pkl(cdict):
   here='/'.join(__file__.split('/')[:-1]) + '/'
   fid = open(here+'cmaps.pkl','wb')
   cPickle.dump(cdict,fid,-1)
   fid.close()

def _cdict_from_cpt(cpt):
   """ cpt should be a list containing the cpt files """
   cdict = {}
   for ent in cpt:
      k = ent.split('.cpt')[0]
      cdict[k] = cpt2python(ent)
      cdict[k+'_r'] = _reverse_cmap_spec(cdict[k])  
   return cdict

def _get_cpt():
   cpt = []
   junk = [cpt.append(x) for x in ls if x.endswith('.cpt')] 
   return cpt

def get_options():
   keys = cdict.keys()
   keys.sort()
   newk = []
   junk = [newk.append(x) for x in keys if not x.endswith('_r')]
   print('_r extension returns the reversed colormap')
   for k in newk:
      print('%s, %s' % (k,k+'_r'))
   
def options():
   get_options()

try:
   cdict = _read_pkl()
   cmap_d = _cmap_d_from_dict(cdict)
except:
   print('could not read pickle file, loading cpt manually')
   ls = os.listdir('.')
   cpt = _get_cpt()
   cdict = _cdict_from_cpt(cpt)
   cmap_d = _cmap_d_from_dict(cdict)
   try:
      _write_pkl(cdict)
   except:
      pass 
locals().update(cmap_d) 
