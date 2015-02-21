from os.path import join
import numpy as np
import sys,os

def configuration(parent_package='',top_path=None):
   from numpy.distutils.misc_util import Configuration
   config = Configuration('polsar', parent_package, top_path)

   npdir = np.get_include() + '/numpy'
   CFLAGS = ['-lm','-O2','-lpthread']

   config.add_library('pdpack', 
         sources=['src/pdpack.cpp'],
         headers=['src/decomp.h'],
         extra_compile_args=CFLAGS)
   config.add_extension('_decomp_modc',
         sources=['src/decomp_modc.cpp'],
            depends=['src/decomp.h'],
            libraries=['pdpack'],
            library_dirs=[],
            include_dirs=[npdir,'src'],
            extra_compile_args=CFLAGS)
   return config

if __name__ == '__main__':
   from distutils.dir_util import remove_tree
   from numpy.distutils.core import setup
   if os.path.exists('./build'):  
      remove_tree('./build')
   setup(**configuration(top_path='').todict())

