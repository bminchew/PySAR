#!/usr/bin/env python
"""
sarcorrelation.py       :     Calculates interferometric correlation

usage::

   $  sarcorrelation.py int_file amp_input [options]

Parameters
----------
int_file          :     complex interferogram file
amp_input         :     amplitude file(s); one of:
                           -a bip_amp (bit-interleaved amplitude file)
                           -s amp1_file amp2_file 
                           -p power1_file power2_file

Options
-------
-o output_file    :     name of ouput file [sarcor.out]
-c str_option     :     output real amplitude (str_option = 'a'), real phase (str_option = 'p'), 
                        in radians or complex (str_option = 'c') correlation ['a']
-n value          :     data null value (float only) [0]  

Notes
-----
*  input data is assumed to be single precision 

"""
from __future__ import print_function, division
import sys,os
import numpy as np
from pysar.etc.excepts import InputError
np.seterr(divide='ignore')

###==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==###
def main(args):
   cor = Correlation(args)
   cor.read_data()
   cor.calculate()
   cor.write_data()

###==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==###
class Correlation():
   def __init__(self,args):
      self.intfile = args[0]
      self.null = 0.      

      self.ampow = 'a'
      self.ampfile = None
      self.amp1file, self.amp2file = None, None

      self.outfile = 'sarcor.out'
      self.outap = 'a'

      for i,a in enumerate(args[1:]):
         if a == '-a':
            self.ampfile = args[2+i]  # 2 because I skip the first argument in args
         elif a == '-s':
            self.amp1file = args[2+i]
            self.amp2file = args[3+i]  
         elif a == '-p':
            self.amp1file = args[2+i]
            self.amp2file = args[3+i]  
            self.ampow = 'p'

         elif a == '-o':
            self.outfile = args[2+i]
         elif a == '-c':
            self.outap = args[2+i]
         elif a == '-n':
            try:
               self.null = np.float32(args[2+i])
            except:
               raise InputError('null value must be float; %s given' % args[2+i])
      self._check_args()

   ###--------------------------------------###
   def _check_args(self):
      if self.ampfile is None:
         if self.amp1file is None or self.amp2file is None:
            errstr = 'a single bil amplitude file or two real-valued amplitude or power files '
            errstr += 'must be provided'
            raise InputError(errstr)

      if self.outap != 'a' and self.outap != 'p' and self.outap != 'c':
         errstr = "unrecognized option %s for output type; " % self.outap
         errstr += "must be 'a' for amplitude, 'p' for phase, or 'c' for complex" 
         raise InputError(errstr)

   ###--------------------------------------###
   def read_data(self):
      print('reading')
      fid = open(self.intfile,'r')
      self.igram = np.fromfile(fid,dtype=np.complex64)
      fid.close()

      if self.ampfile is None:
         fid = open(self.amp1file,'r')
         self.amp1 = np.fromfile(fid,dtype=np.float32)
         fid.close() 

         fid = open(self.amp2file,'r')
         self.amp2 = np.fromfile(fid,dtype=np.float32)
         fid.close() 
      else:
         fid = open(self.ampfile,'r')
         amp = np.fromfile(fid,dtype=np.float32)
         fid.close()
         self.amp1, self.amp2 = amp[::2], amp[1::2] 
      
   ###--------------------------------------###
   def calculate(self):
      print('calculating correlation')
      redonull, redozero = False, False

      teps = 2.*np.finfo(np.float32).eps
      nullmask = np.abs(self.igram - self.null) < teps
      nullmask += np.abs(self.amp1 - self.null) < teps
      nullmask += np.abs(self.amp2 - self.null) < teps

      zeromask  = self.amp1 < teps
      zeromask += self.amp2 < teps

      if len(nullmask[nullmask]) > 1:
         redonull = True
         self.amp1[nullmask], self.amp2[nullmask] = 1., 1.

      if len(zeromask[zeromask]) > 1:
         redozero = True
         self.amp1[zeromask], self.amp2[zeromask] = 1., 1.

      if self.ampow == 'a':
         self.cor = self.igram/(self.amp1*self.amp2)    
      else:
         self.cor = self.igram/(np.sqrt(self.amp1*self.amp2)) 

      if self.outap == 'a':
         self.cor = np.abs(self.cor)
      elif self.outap == 'p':
         self.cor = np.arctan2(self.cor.imag,self.cor.real)

      if redonull:
         self.cor[nullmask] = self.null
      if redozero:
         self.cor[zeromask] = self.null
      
   ###--------------------------------------###
   def write_data(self):
      print('writing')
      fid = open(self.outfile,'w')
      self.cor.tofile(fid)
      fid.close()

###==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==###
if __name__ == '__main__':
   args = sys.argv[1:]
   if len(args) < 3:
      print(__doc__)
      sys.exit()
   main(args)
