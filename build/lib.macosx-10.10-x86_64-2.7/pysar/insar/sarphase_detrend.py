#!/usr/bin/env python
"""
sarphase_detrend.py  :  Fits a surface to an (masked) image and then removes the surface
                        from the entire image

usage::

   $ sarphase_detrend.py image_file cols [options]

Parameters
----------
image_file           :  image file 
cols                 :  number of columns (or samples) in the image

Options
-------
-o order             :  polynomial order for the fitted surface [1]
-c cor_file          :  correlation filename; optionally append minimum correlation threshold [0.3]
-m mask_file         :  mask filename; optionally append value to exclude [1]
-f out_file          :  output filename [image_file + .flat]
-s bool              :  output best-fit surface [False]
-n value             :  data null value [0]
-w bool              :  weight data by correlation values prior to fitting (see notes) [True]
-p norm              :  L^p norm {1 or 2} [2] 
-x factor            :  column decimation factor [30]
-y factor            :  row decimation factor [column decimation factor]

Notes
-----
*  values should be appended with a comma with no spaces on either side
*  weighting is only applied if correlation file is given 
*  correlation threshold is not considered if weighting is applied (i.e. unless '-w False' is given)
"""
from __future__ import print_function, division
import sys,os
import getopt
import numpy as np
import pysar.insar._phase_detrend_sup as sup

###==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==###
def main(args):
   print('\nRunning phase_detrend.py\n')
   detrend = DeTrend(args)
   detrend.read_data()
   detrend.setup_data()
   detrend.remove_surf()  
   detrend.write_data() 

###==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==###
class DeTrend():
   def __init__(self,args):
      opts, args = getopt.gnu_getopt(args, 'f:o:p:c:m:n:x:y:w:s:')

      self.unwf  = args[0]
      self.cols  = np.int32(args[1])
      self.corf  = None
      self.maskf = None

      # set defaults
      self.order   = 1
      self.cthresh = 0.3
      self.maskval = 1
      self.rowdec  = 30
      self.coldec  = -1
      self.outf    = self.unwf + '.flat'
      self.null    = 0
      self.pnorm   = 2
      self.wbool   = True
      self.sbool   = False
      self.Nlook   = 1

      self.corarr = None
      # assign option values 
      for o,a in opts:
         if o == '-f':
            self.outf = a
         elif o == '-c':
            cc = a.split(',')
            self.corf = cc[0]
            if len(cc) > 1:
               self.cthresh = np.float32(cc[1])
         elif o == '-m':
            cc = a.split(',')
            self.maskf = cc[0]
            if len(cc) > 1:
               self.maskval = np.int32(cc[1])
         elif o == '-y':
            self.rowdec = np.int32(a)
         elif o == '-x':
            self.coldec = np.int32(a)
         elif o == '-o':
            self.order = np.int32(a)
         elif o == '-p':
            self.pnorm = np.int32(a)
         elif o == '-n':
            self.null = np.float64(a)
         elif o == '-w':
            if 'F' in a or 'f' in a:
               self.wbool = False
         elif o == '-s':
            if 't' in a.lower():
               self.sbool = True

      if self.coldec < 0:
         self.coldec = self.rowdec
      if self.rowdec < 1 or self.coldec < 1:
         self.rowdec, self.coldec = 1, 1
      if self.order > 4:
         print('Requested order > max order; Setting to max order = 4')
         self.order = 4

   ###--------------------------------------###
   def read_data(self):
      print('reading data files')
      eps = np.finfo(np.float32).eps 
      ceps = 1. - eps
      # read in correlation data and mask values less than threshold 
      if self.corf is not None:
         fid = open(self.corf,'r')
         data = np.fromfile(fid, dtype=np.float32).reshape(-1,self.cols) 
         fid.close()
         
         if self.wbool:   # if weighting = True, set cor threshold so that all correlation values are included
            self.cthresh = 0.
            self.corarr = data.copy()
            self.corarr[self.corarr < eps] = eps
            self.corarr[self.corarr > ceps] = ceps 
         self.mask = data > self.cthresh
      else:
         self.wbool = False

      # read in mask file and combine with correlation mask created above
      if self.maskf is not None:
         fid = open(self.maskf,'r')
         data = np.fromfile(fid, dtype=np.float32).reshape(-1,self.cols)
         fid.close()
         
         if self.corf is not None:
            self.mask *= data != self.maskval
         else:
            self.mask = data != self.maskval

      # read in data (this wipes out the correlation data in order to save memory)
      fid = open(self.unwf,'r')
      self.unw = np.fromfile(fid, dtype=np.float32).reshape(-1,self.cols)
      fid.close()

      if self.maskf is not None:
         self.mask *= np.abs(self.unw - self.null) > eps
      elif self.corf is not None:
         self.mask *= np.abs(self.unw - self.null) > eps
      else:
         self.mask = np.abs(self.unw - self.null) > eps

      self.lines = np.shape(self.unw)[0]
      print('done reading')

   ###--------------------------------------###
   def setup_data(self):
      print('decimating')
      xstart,ystart = self.coldec-1, self.rowdec-1
      x = np.arange(xstart, self.cols, self.coldec)
      y = np.arange(ystart, self.lines, self.rowdec)
      x,y = np.meshgrid(x,y)
      x = x.flatten()
      y = y.flatten()

      self.d = self.unw[y,x].copy()
      self.d, self.x, self.y = self.d[self.mask[y,x]], x[self.mask[y,x]], y[self.mask[y,x]]

      if self.wbool:
         self.corarr = self.corarr[y,x]
         self.corarr = self.corarr[self.mask[y,x]]

   ###--------------------------------------###
   def remove_surf(self):
      print('calculating coefficients: ')
      print('        order = %d' % self.order)
      print('        using %d points' % len(self.d))
      c = sup.polyfit2d(x=self.x,y=self.y,d=self.d,n=self.order,p=self.pnorm,
         w=self.wbool,cor=self.corarr,N=self.Nlook)
      del self.d, self.x, self.y

      if self.sbool:
         dc = self.unw.copy()
      print('removing the best-fit surface')
      self.unw = sup.subtract_surf(d=self.unw,c=c,null=self.null)
      if self.sbool:
         self.surf = dc - self.unw
         self.surf[self.unw==self.null] = self.null

   ###--------------------------------------###
   def write_data(self):
      print('writing')
      fid = open(self.outf,'w')
      self.unw.flatten().tofile(fid)
      fid.close()
      
      if self.sbool:
         fid = open(self.outf+'.surf','w')
         self.surf.flatten().tofile(fid)
         fid.close()

###==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==--==### 
if __name__ == '__main__':
   args = sys.argv[1:]
   if len(args) < 2:
      print(__doc__)
      sys.exit()
   main(args)



