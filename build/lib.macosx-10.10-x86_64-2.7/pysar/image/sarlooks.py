#!/usr/bin/env python

"""
sarlooks.py:   Basic multilooking for 2D images  

Usage::

  sarlooks.py infile samples outfile [options]

Options
-------
-a value   :     number of looks across the image
-d value   :     number of looks down the image
-n value   :     null value to exclude from the filter
-t value   :     data type (see notes for options)
-i         :     ouput NaN in place of null value
-s         :     run in silent mode (verbosity = 0)

Notes
-----
*  -a and/or -d must be defined
*  if one of -a or -d are defined, the filter window will be square
*  -n value must be given for -i option to work 
*  data types options:  ['f','float','d','double','c','complex','cf','complexfloat',
               'cd','complexdouble'].  Default = float

"""
from __future__ import print_function, division
import sys,os
import getopt
import numpy as np
from pysar.image import looks

def main():
   pars = Params()

   fid = open(pars.infile,'r')
   data = np.fromfile(fid,dtype=pars.dtype).reshape(-1,pars.cols)
   fid.close()

   out = looks.look(data=data,win=pars.win,null=pars.null,verbose=pars.verbose)

   if pars.outnan:
      nullmask = np.abs(out - pars.null) < 1.e-7
      out[nullmask] = np.nan

   fid = open(pars.outfile,'w')
   out.flatten().tofile(fid)
   fid.close()

class Params():
   def __init__(self):
      opts, args = getopt.gnu_getopt(sys.argv[1:], 'a:d:n:t:is')
    
      self.infile = args[0]
      self.cols = np.int32(args[1])
      self.outfile = args[2]
      self.lx,self.ld,self.null = None, None, None
      self.verbose,self.outnan = 1, False
      dtype = 'float'
      for o,a in opts:
         if o == '-a':
            self.lx = np.int32(a)
         elif o == '-d':
            self.ld = np.int32(a)
         elif o == '-n':
            self.null = np.float32(a)
         elif o == '-i':
            self.outnan = True
         elif o == '-s':
            self.verbose = 0
         elif o == '-t':
            dtype = a.strip()

      if self.outnan and self.null == None:
         raise ValueError('Null value must be defined to output NaN in its place')

      if self.lx and self.ld:
         self.win = [self.lx,self.ld]
      elif self.lx == None and self.ld:
         self.win = self.ld
      elif self.ld == None and self.lx:
         self.win = self.lx
      else:
         raise ValueError('At least one window dimension must be defined')

      types = ['f','float','r4','d','double','r8','c','complex','c8','cf','complexfloat',
               'cd','complexdouble','c16']
      atype = [np.float32, np.float32, np.float32, np.float64, np.float64, np.float64, 
               np.complex64, np.complex64, np.complex64,
               np.complex64, np.complex64, np.complex128, 
               np.complex128, np.complex128]
      try:
         self.dtype = atype[ types.index( dtype ) ]
      except:
         errstr = 'unsupported data type: ' + dtype
         errstr += '\n  supported data types are: ' + ', '.join(types) 
         raise ValueError(errstr)

if __name__ == '__main__':
   args = sys.argv[1:]
   if len(args) < 3:
      print(__doc__)
      sys.exit()
   main()

      
         
  





