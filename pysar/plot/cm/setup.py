import sys,os

def create_cm_pkl():
   here=os.getcwd() + '/' + '/'.join(__file__.split('/')[:-1])   
   pkl = here+'/cpt/cmaps.pkl'
   if os.path.exists(pkl):  os.remove(pkl)
   import _generate_pkl   

def id_cmaps():
   here=os.getcwd() + '/' + '/'.join(__file__.split('/')[:-1])
   ls = os.listdir(here)
   if here[-1] != '/': here += '/'
   out = []
   for ent in ls:
      if '.' not in ent and ent != 'cpt':
         if os.path.exists(here+ent+'/__init__.py'):
            if os.path.exists(here+ent+'/setup.py'):
               out.append(ent)
   return out

def configuration(parent_package='',top_path=None):
   from numpy.distutils.misc_util import Configuration
   config = Configuration('cm', parent_package, top_path)
   config.add_data_dir('cpt')
   ls = id_cmaps()
   for ent in ls:
      config.add_subpackage(ent)
   config.make_config_py()
   return config

if __name__ == '__main__':
   from distutils.dir_util import remove_tree
   from numpy.distutils.core import setup
   if os.path.exists('./build'):  
      remove_tree('./build')
   setup(**configuration(top_path='').todict())

