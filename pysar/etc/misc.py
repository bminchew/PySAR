"""
Miscellaneous add-ons
"""
import sys,os
import numpy as np

__all__ = ['progressbar','nrprint']

###===========================================================================
def progressbar(index,length,modval=2,prevbar=None):
   """ 
   Prints a wget-like progress bar to the screen

   ex.  [=====>      ] 50%

   Parameters
   ----------
   index       :     int or float
                     index value 
   length      :     int or float
                     length of iteration or loop (100% = 100*index/length)
   modval      :     int 
                     length of prog bar in characters = 100//modval [default = 2]
   prevbar     :     string or None
                     previous output string. This could save time as it won't
                        print to the screen unless the new progress bar is 
                        different from prevbar [default = None; prints every bar]

   """
   length = np.int32(length)
   index  = np.int32(index)
   modval = np.max([1,np.int32(modval)])
   percent = 100*index//length
   point = True
   prog = '[' 
   for i in np.arange(0,100+modval,modval):
      if i <= percent:
         prog += '=' 
      else:
         if i < 100 and point:
            prog += '>' 
            point = False
         else:
            prog += '=' 
            percent = 100
   prog += ']' 
   if prevbar != prog:
      sys.stdout.write("%s %3d%%\r" % (prog,percent))
      sys.stdout.flush()
      return prog    

###===========================================================================
def nrprint(string):
   """
   No (carriage) return print

   Parameter
   ---------
   string   :  str
               String to print

   """
   sys.stdout.write(string+'\r')
   sys.stdout.flush()

