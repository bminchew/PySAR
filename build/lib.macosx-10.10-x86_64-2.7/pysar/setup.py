
def configuration(parent_package='',top_path=None):
   from numpy.distutils.misc_util import Configuration
   config = Configuration('pysar',parent_package,top_path)
   config.add_subpackage('image')
   config.add_subpackage('insar')
   config.add_subpackage('math')
   config.add_subpackage('polsar')
   config.add_subpackage('signal')
   config.add_subpackage('utils')
   config.add_subpackage('plot')
   config.add_subpackage('etc')
   config.make_config_py()
   return config

if __name__ == '__main__':
   from numpy.distutils.core import setup
   setup(**configuration(top_path='').todict())
