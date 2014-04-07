import sys,os


def configuration(parent_package='',top_path=None):
   from numpy.distutils.misc_util import Configuration
   config = Configuration('plot', parent_package, top_path)
   config.add_subpackage('cm')
   config.make_config_py()
   return config

if __name__ == '__main__':
   from distutils.dir_util import remove_tree
   from numpy.distutils.core import setup
   if os.path.exists('./build'):  
      remove_tree('./build')
   setup(**configuration(top_path='').todict())

