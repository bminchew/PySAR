#!/opt/local/Library/Frameworks/Python.framework/Versions/2.7/Resources/Python.app/Contents/MacOS/Python

"""
sarfilter.py:  Boxcar filter for 2D images   

Usage::

  sarfilter.py infile samples [outfile] [options]

Options
-------
-a value   :      int
                  number of looks across the image
-d value   :      int
                  number of looks down the image
-n value   :      float
                  null value (will be reset on output)
-z value   :      float
                  set null to value prior to filtering 
-t value   :      str
                  data type (see notes for options)
-i         :     
                  ouput NaN in place of null value

Notes
-----
*  -a and/or -d must be defined
*  if one of -a or -d are defined, the filter window will be square
*  if outfile is not given, infile will be overwritten
*  -n value must be given for -i option to work 
*  data types options  ['f','float','d','double','c','complex','cf','complexfloat',
               'cd','complexdouble'].  Default = float

"""
from __future__ import print_function, division
import sys,os
import getopt
import numpy as np
from pysar.signal import boxfilter
from pysar.etc.excepts import InputError

def main():
   pars = Params()

   with open(pars.infile,'r') as fid:
      data = np.fromfile(fid,dtype=pars.dtype).reshape(-1,pars.cols)

   out = boxfilter.boxcar2d(data=data,window=pars.win,null=pars.null,
               nullset=pars.nullset,thread='auto',numthrd=8,tdthrsh=1e5)

   if pars.outnan:
      nullmask = np.abs(out - pars.null) < 1.e-7
      out[nullmask] = np.nan

   with open(pars.outfile,'w') as fid:
      out.flatten().tofile(fid)

class Params():
   def __init__(self):
      opts, args = getopt.gnu_getopt(sys.argv[1:], 'a:d:n:z:t:is')
    
      self.infile = args[0]
      self.cols = np.int32(args[1])
      try:
         self.outfile = args[2]
      except:
         self.outfile = self.infile

      self.lx,self.ld,self.null = None, None, None
      self.verbose,self.outnan = 1, False
      self.nullset = None
      dtype = 'float'
      for o,a in opts:
         if o == '-a':
            self.lx = np.int32(a)
         elif o == '-d':
            self.ld = np.int32(a)
         elif o == '-n':
            self.null = np.float64(a)
         elif o == '-z':
            self.nullset = np.float64(a)
         elif o == '-i':
            self.outnan = True
         elif o == '-s':
            self.verbose = 0
         elif o == '-t':
            dtype = a.strip()

      if self.outnan and self.null == None:
         raise InputError('Null value must be defined to output NaN in its place')

      if self.lx and self.ld:
         self.win = [self.lx,self.ld]
      elif self.lx == None and self.ld:
         self.win = self.ld
      elif self.ld == None and self.lx:
         self.win = self.lx
      else:
         raise InputError('At least one window dimension must be defined')

      types = ['f','float','r4','d','double','r8','c','complex','c8','cf','complexfloat',
               'cd','complexdouble','c16']
      atype = [np.float32, np.float32, np.float32, np.float64, np.float64, np.float64, 
               np.complex64, np.complex64, np.complex64,
               np.complex64, np.complex64, np.complex128, 
               np.complex128, np.complex128]
      try:
         self.dtype = atype[ types.index( dtype ) ]
      except:
         print('unsupported data type: ' + dtype)
         print('  supported data types are: ' + ', '.join(types)) 
         sys.exit()


if __name__ == '__main__':
   args = sys.argv[1:]
   if len(args) < 3:
      print(__doc__)
      sys.exit()
   main()

      
         
  





