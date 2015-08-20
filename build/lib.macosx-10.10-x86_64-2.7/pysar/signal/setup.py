import sys,os
import numpy as np

# cythoncodes = list of tuples with format (source_without_ext, include_dirs_list)
cythoncodes = [('filtermod',[])]
CFLAGS = ['-lm','-O2','-lpthread','-fPIC'] 
cythcompiler = 'gcc'

def cythonize():
   try:
      from Cython.Compiler.Main import CompilationOptions, default_options, \
         compile, PyrexError
      from Cython.Compiler import Options
      import subprocess 

      for code in cythoncodes:
         source = code[0] + '.pyx'
         options = CompilationOptions(default_options)
         options.output_file = code[0] + '.c'
         options.include_path = code[1]
         Options.generate_cleanup_code = 3
         any_failures = False
         try:
            result = compile(source, options)
            if result.num_errors > 0: 
               any_failures = True
            if not any_failures:
               callist = [cythcompiler,'-shared','-fwrapv','-Wall','-fno-strict-aliasing']
               for x in CFLAGS:
                  callist.append(x)
               for x in code[1]:
                  callist.append('-L' + x)
               callist.append('-o')
               callist.append('_' + code[0] + '.so')
               callist.append(code[0] + '.c')
               subprocess.call(callist)
         except (EnvironmentError, PyrexError):
            e = sys.exc_info()[1]
            sys.stderr.write(str(e) + '\n')
            any_failures = True
         if any_failures:
            try:  os.remove(code[0] + '.c')
            except OSError: pass
   except:
      raise ValueError

def configuration(parent_package='',top_path=None):
   from numpy.distutils.misc_util import Configuration
   config = Configuration('signal', parent_package, top_path)

   CFLAGS = ['-lm','-O2','-lpthread','-fPIC']
   npdir = np.get_include() + '/numpy'
   config.add_extension('_filter_modc',sources=['filter_modules/filter_modc.cpp'],
            libraries=[],
            library_dirs=[],
            include_dirs=[npdir],
            extra_compile_args=CFLAGS)
   config.add_library('conefiltpack',
            sources=['filter_modules/conefilt.cpp'],
            headers=['filter_modules/conefilt.h'],
            extra_compile_args=CFLAGS)
   config.add_extension('_conefilt_modc',sources=['filter_modules/conefilt_modc.cpp'],
            depends=['filter_modules/conefilt.h'],
            libraries=['conefiltpack'],
            library_dirs=[],
            include_dirs=[npdir,'filter_modules'],
            extra_compile_args=CFLAGS) 
   config.add_library('medfiltpack',
            sources=['filter_modules/medfilt.cpp'],
            headers=['filter_modules/medfilt.h'],
            extra_compile_args=CFLAGS)
   config.add_extension('_medfilt_modc',sources=['filter_modules/medfilt_modc.cpp'],
            depends=['filter_modules/medfilt.h'],
            libraries=['medfiltpack'],
            library_dirs=[],
            include_dirs=[npdir,'filter_modules'],
            extra_compile_args=CFLAGS)
   config.add_extension('_xapiir_sub',sources=['filter_modules/xapiir_sub.f'],
            libraries=[],
            library_dirs=[],
            include_dirs=[],
            extra_compile_args=['-O3'])
   config.add_extension('_butter_bandpass',sources=['filter_modules/butter_bandpass.f'],
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
   cythonize()
   setup(**configuration(top_path='').todict())

