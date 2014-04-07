import sys,os

def make_pkl_file(cpt,here=None):
   import cPickle
   from matplotlib.cm import _reverser, revcmap, _reverse_cmap_spec
   backone=os.getcwd() + '/' + '/'.join(__file__.split('/')[:-2]) + '/'
   sys.path.append(backone)
   import cpt_tools

   if here is None:
      here=os.getcwd() + '/' + '/'.join(__file__.split('/')[:-1])
   if here[-1] != '/': here += '/'

   cdict = {}
   for ent in cpt:
      k = ent.split('.cpt')[0]
      cdict[k] = cpt_tools.cpt2python(here+ent)
      cdict[k+'_r'] = _reverse_cmap_spec(cdict[k])
   fid = open(here+'cmaps.pkl','wb')
   cPickle.dump(cdict,fid,-1)
   fid.close()

def cpt_files(here=None):
   if here is None:
      here=os.getcwd() + '/' + '/'.join(__file__.split('/')[:-1])
   ls = os.listdir(here)
   cpt = []
   junk = [cpt.append(x) for x in ls if x.endswith('.cpt')]
   return cpt

def configuration(parent_package='',top_path=None):
   from numpy.distutils.misc_util import Configuration
   config = Configuration('grass', parent_package, top_path)

   here=os.getcwd() + '/' + '/'.join(__file__.split('/')[:-1])
   ls = cpt_files(here)
   #make_pkl_file(ls)
   if here[-1] != '/': here += '/'
   for ent in ls:
      config.add_data_files(here+ent)
   config.add_data_files(here+'cmaps.pkl')
   config.make_config_py()
   return config

if __name__ == '__main__':
   from distutils.dir_util import remove_tree
   from numpy.distutils.core import setup
   if os.path.exists('./build'):  
      remove_tree('./build')
   setup(**configuration(top_path='').todict())

