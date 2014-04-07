import sys,os
import numpy as np

def configuration(parent_package='',top_path=None):
   from numpy.distutils.misc_util import Configuration
   config = Configuration('insar', parent_package, top_path)

   CFLAGS = ['-lm','-O2','-lpthread','-fPIC']
   npdir = np.get_include() + '/numpy'
   config.add_extension('_subsurf',sources=['_subsurf.f'],
            libraries=[],
            library_dirs=[],
            include_dirs=[],
            extra_compile_args=['-O3']) 
   return config

if __name__ == '__main__':
   from distutils.dir_util import remove_tree
   from numpy.distutils.core import setup
   if os.path.exists('./build'):  
      remove_tree('./build')
   setup(**configuration(top_path='').todict())

