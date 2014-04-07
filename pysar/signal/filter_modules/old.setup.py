
import numpy as np
from distutils.core import setup, Extension

# Specify source files
sources = ['filter_modc.cpp']

# Specify include directory: point to numpy directory
npdir = '/'.join(np.__file__.split('/')[:-1]) + '/core/include/numpy'
IDIR = [npdir]

# Specify any libraries
LIBDIR = []

# Specify any C flags
CFLAGS = ['-std=c99','-lm','-O2','-lpthread']

module = Extension('filter_modc', include_dirs = IDIR, extra_compile_args = CFLAGS,
                   library_dirs = LIBDIR, sources = sources)

# Build the module
setup(name = 'filter_modc',
      version = '0.1',
      description = 'Collection of filters',
      author = 'B. Minchew',
      author_email = 'bminchew@caltech.edu',
      py_modules = ['filter_modc'],
      ext_modules = [module])

