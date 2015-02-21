#!/opt/local/Library/Frameworks/Python.framework/Versions/2.7/Resources/Python.app/Contents/MacOS/Python

"""
sardecomp_haa.py  :   Cloude-Pottier H/A/alpha decomposition (Cloude and Pottier, 1997)

usage::

   $ sardecomp_haa.py filename[s] [options] 

Parameters
----------
filename[s]          :  input filename or filenames (see notes for more info)

Options
-------
-c width             :  int  --  
                        image width (only needed if -f is given)
-f window            :  int or comma-separated list of ints (no brackets)  --  
                        filter window size; square if only one value is given
-m format            :  str {C or T}  --  
                        format of input data; C -> covariance, T -> coherency 
                        (if C is given, data should not be multiplied by any constants)
-o prefix            :  str  --  
                        prefix for output files [same as input prefix]

Notes
-----

* Only one filename is needed if all files follow a convention such that::

   < S_HH S_HH* >   -->  <prefix>hhhh<extension> *or* <prefix>HHHH<extension>
   < S_HH S_VV* >   -->  <prefix>hhvv<extension> *or* <prefix>HHVV<extension>
   
and so on for the six unique elements (upper tri) of the coherencey matrix C (aka C_3)
(see next note for a list of required channels)

* If all filenames are given, they should be in order hhhh, vvvv, hvhv, hhhv, hhvv, hvvv

* If coherency matrix (T) form is chosen, all six unique elements (upper tri) must be given
as separate files in order: t11, t22, t33, t12, t13, t23 (where t12 is first row, second
column entry of T)

* Input files are assumed to be headerless, single-precision (float) binary

* Image width is only needed if -f is called

References
----------

[1] Cloude, S. and Pottier, E., "An entropy based classification scheme for land applications of polarimetric SAR", *IEEE Trans. Geosci. Remote Sensing*, vol. 35, no. 1, pp. 68-78, Jan. 1997. 

[2] van Zyl, J. and Yunjin, K., *Synthetic Aperture Radar Polarimetry*, Wiley, Hoboken, NJ, 288 pages, 2011.

"""
from __future__ import print_function, division
import sys,os
import getopt
import numpy as np
from pysar.etc.excepts import InputError
from pysar.polsar.decomp import decomp_haa
from pysar.signal.boxfilter import boxcar2d

###===========================================================================================

def main(args):
   deco = FDdecomp(args)
   deco.read_data()
   deco.setup_data()
   deco.decomp()
   deco.write_data()
   print('Done with sardecomp_haa.py\n')

###===========================================================================================
class FDdecomp():
   def __init__(self,cargs):
      opts,args = getopt.gnu_getopt(cargs, 'c:f:o:m:') 

      # set defaults
      self.outpref = None
      self.cols, self.filter_window = None, None
      fchoices = ['hhhh','vvvv','hvhv','hhhv','hhvv','hvvv']
      self.fnames, self.data = {}, {}
      self.matform = 'C'
      matformopts = ['C','c','T','t']

      # check filenames
      if len(args) != 1 and len(args) != 6:
         istr  = 'Provide either 1 example filename or all 6 filenames. '
         istr += 'Number given = %d' % len(args)
         raise InputError(istr)

      # gather options
      for o,a in opts:
         if o == '-c':
            try: self.cols = np.int32(a)
            except: raise TypeError('argument for cols (-c) option must be convertable to int')
         elif o == '-f':
            flt = a.split(',')
            try: self.filter_window = [np.int32(x) for x in flt]
            except: raise TypeError('filter window dimensions must be convertable to int')
         elif o == '-o':
            self.outpref = a
         elif o == '-m':
            self.matform = a
            if self.matform not in matformopts:
               raise InputError('matform must be either C or T; %s given'%a)
            elif self.matform == 'c' or self.matform == 't':
               self.matform = self.matform.upper()

      if self.filter_window and not self.cols:
         raise InputError('option -c must be given with -f')

      if self.matform == 'T' and len(args) != 6:
         raise InputError('6 filenames must be given to use T matrix format; %s given' % str(len(args)))

      # get filenames
      if len(args) == 1:
         filesplit = None
         for x in fchoices:
            if x in args[0]:
               filesplit, upper = args[0].split(x), False
               break
            elif x.upper() in args[0]:
               filesplit, upper = args[0].split(x.upper()), True
               break
         if filesplit:
            for x in fchoices:
               if upper:  
                  self.fnames[x] = filesplit[0] + x.upper() + filesplit[1]
               else: 
                  self.fnames[x] = filesplit[0] + x + filesplit[1]
         else:
            istr  = '%s does not match expected formatting...check input or' % args[0] 
            istr += ' enter all filenames manually'
            raise InputError(istr)
      else:
         for i,x in enumerate(fchoices):
            self.fnames[x] = args[i]
  
      if not self.outpref:
         if 'HHHH' in self.fnames['hhhh']: 
            self.outpref = '_'.join(self.fnames['hhhh'].split('HHHH')) 
         else:
            self.outpref = '_'.join(self.fnames['hhhh'].split('hhhh')) 

      if self.outpref[-1] != '.': self.outpref += '.' 

   ###---------------------------------------------------------------------------------
   def read_data(self):
      rstr = 'Reading...'
      for k,v in self.fnames.iteritems():
         print("%s %s" % (rstr, v))
         try:
            fid = open(v,'r')
            if k == 'hhvv' or k == 'hvvv' or k == 'hhhv':
               self.data[k] = np.fromfile(fid,dtype=np.complex64)
            else:
               self.data[k] = np.fromfile(fid,dtype=np.float32)
            fid.close()
         except:
            raise IOError('cannot open file %s' % v)
      print('%s %s' % (rstr, 'Complete'))

   ###---------------------------------------------------------------------------------
   def setup_data(self):
      if self.filter_window:
         self._filter() 

   ###---------------------------------------------------------------------------------
   def _filter(self):
      print('Filtering...')
      for key in self.data.keys():
         self.data[key] = self.data[key].reshape(-1,self.cols)
         self.data[key] = boxcar2d(data=self.data[key], window=self.filter_window)
         self.data[key] = self.data[key].flatten()

   ###---------------------------------------------------------------------------------
   def decomp(self):
      print('Decomposing')
      self.data['ent'], self.data['ani'], self.data['alp'] = decomp_haa(hhhh=self.data['hhhh'], 
         vvvv=self.data['vvvv'], hvhv=self.data['hvhv'], hhhv=self.data['hhhv'], 
         hhvv=self.data['hhvv'], hvvv=self.data['hvvv'], matform=self.matform)

   ###---------------------------------------------------------------------------------
   def write_data(self):
      wstr = 'Writing...'
      outputs = ['ent','ani','alp']
      for i in outputs:
         print("%s %s" % (wstr, i))
         fid = open(self.outpref + i,'w')
         self.data[i].tofile(fid) 
         fid.close()
      print('%s %s' % (wstr, 'Complete')) 

###===========================================================================================
if __name__ == '__main__':
   args = sys.argv[1:]
   if len(args) < 1:
      print(__doc__)
      sys.exit()
   main(args)
