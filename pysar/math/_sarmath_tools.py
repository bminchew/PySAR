from __future__ import print_function, division
import sys,os
import numpy as np
from math import pi

__all__ = ['Databank','Parse_command_line','Writer']

def option_list():
   lis = ['add','sub','mult','div','hypot','pow','root','sqrt','abs','mod',
            'amp','power','phase','subphz','addphz',
            'xmult','xcor','xcor_amp','xcor_phase',
            'null2nan','nan2null','inf2null','null2null','num2null','num2num',
            'num_null','num_nan','num_inf','num_neginf','num_posinf',
            'gt','ge','lt','le','eq','ne','isnan','notnan',
            'dB','dBi','ln','log','log10','log_b','exp','10pow',
            'max','min','std','var','mean','med']
   operators = ['+','-','/','x','.','*','^','%']
   opaction  = ['add','sub','div','mult','mult','mult','pow','mod']
   typeabbrevs = ['float','r4','double','r8','complex','c8','dcomplex','c16','int','i4']
   types       = [np.float32, np.float32, np.float64, np.float64, np.complex64, np.complex64,
                     np.complex128, np.complex128, np.int32, np.int32]
   return lis,operators,opaction,typeabbrevs,types

###==============================================================================

class Databank():
   """ 
   Class:  Reads and stores data
   """
   def __init__(self,pars):
      self.data = []
      for i in np.arange(len(pars.items)):
         if pars.types[i] != 'scalar':
            fid = open(pars.items[i],'r')
            self.data.append( np.fromfile(fid,dtype=pars.types[i]) )
            fid.close()
         else:
            self.data.append(np.float64(pars.items[i]))


###==============================================================================

class Parse_command_line():
   """ 
   A class for parsing the command line and storing parameters 
   """

   def __init__(self,args):
      self.args = args
      opts, operators, opaction, typeabbrevs, nptypes = option_list()
      self.action, self.items = [], []
      self.maskfile, self.outfile = None, None
      self.rowoff, self.coloff = 0, 0
      self.cols, self.types = [], []
      self.attrib = {}
      filenum = 0
      argexcepts = ['pi','Pi','PI','2pi','2Pi','2PI','e']
      i = 0
      while i < len(args):
         a = args[i].strip()
         if a[0] == '-' and len(a) > 1 and self._testarg(a[1:]) and a[1:] not in argexcepts: 
            if a[1:] in opts:
               self.action.append( a[1:] )
            elif 'offrow12' in a:
               i += 1
               self.rowoff = -np.int32(args[i])
            elif 'offcol12' in a:
               i += 1
               self.coloff = -np.int32(args[i])
            elif 'offrow21' in a:
               i += 1
               self.rowoff = np.int32(args[i])
            elif 'offcol21' in a:
               i += 1
               self.coloff = np.int32(args[i])
            elif 'mask' in a:
               i += 1
               self.maskfile = args[i]

         elif a == '=':
            i += 1
            self.outfile = args[i]

         elif a in operators:
            try:
               self.action.append( opaction[ operators.index(a) ] )
            except ValueError:
               print(a + ' is not a valid operator')
               raise

         else:
            a = ','.join(k.strip() for k in a.split(',')).split(',')  # strip whitespace from entries in a
            self.items.append( a[0] )
            self.cols.append(None)
            self.types.append(None)

            try:
               fid = open(a[0],'r')
               fid.close()
               typ = np.float32   #  default type 

               if len(a) > 1:
                  j = 1
                  while j < len(a):
                     try:
                        b = np.int64(a[j])
                        self.cols[-1] = np.int64(a[j])
                     except:
                        try:
                           typ = nptypes[ typeabbrevs.index(a[j].strip()) ]
                        except ValueError:
                           print(a[j] + ' is not a valid type or an integer')
                           raise
                     j += 1
               self.types[-1] = typ
            except IOError:
               try:
                  b = np.float64(a[0])
                  self.types[-1] = 'scalar'

               except:
                  if 'pi' == a[0] or 'Pi' == a[0] or 'PI' == a[0]:
                     self.items[-1] = str(pi)
                     self.types[-1] = 'scalar'
                  elif '-pi' == a[0] or '-Pi' == a[0] or '-PI' == a[0]:
                     self.items[-1] = str(-pi)
                     self.types[-1] = 'scalar'
                  elif '2pi' == a[0] or '2Pi' == a[0] or '2PI' == a[0]:
                     self.items[-1] = str(2*pi)
                     self.types[-1] = 'scalar'
                  elif '-2pi' == a[0] or '-2Pi' == a[0] or '-2PI' == a[0]:
                     self.items[-1] = str(-2*pi)
                     self.types[-1] = 'scalar'
                  elif 'e' == a[0] or 'exp' == a[0] or 'EXP' == a[0]:
                     self.items[-1] = str(np.exp(1))
                     self.types[-1] = 'scalar'
                  elif '-e' == a[0]:
                     self.items[-1] = str(-np.exp(1))
                     self.types[-1] = 'scalar'
                  else:
                     print('Cannot open the file or convert ' + a[0] + ' to float')
                     raise 
         i += 1

   def _testarg(self,a):
      try:
         b = np.float64(a)
         return False
      except:
         return True


###==============================================================================

class Writer():
   """
   Writer:  Class to write the output file
   
   Parameters
   ----------
   output      :  ndarray 
                  Output array to be written to a file
   pars        :  sarmath class
                  Class containing the command parameters

   """

   def __init__(self,output,pars):
      if type(output.answer) != np.ndarray:
         print(output.answer)
      elif len(output.answer) == 1:
         print(output.answer)
      else:
         print('Writing...')
         fid = open(pars.outfile,'w')
         output.answer.flatten().tofile(fid)
         fid.close()
    
