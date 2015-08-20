#!/usr/bin/env python

"""
Basic mathematical operations for SAR data in pseudo reverse Polish notation  

Usage forms (entry_i can be a file or number; output file is required only for array outputs)::

   $ sarmath.py entry_1 [entry_2] [entry_3] -function_1 [entry_i] [-function_2 ... -function_n] [= output_file]

   $ sarmath.py entry_1 operator entry_2 [-function_1 ... -function_n] [= output_file]

Operators
---------
   ==========    ====================================================================
   +, -, /       add, subract, divide 
   x, ., '*'     multiplication ('*' must be given as a string on Linux systems)
   ^             raise entry_1 to power entry_2
   %             mod entry_1 by entry_2
   ==========    ====================================================================

Functions
---------
   symbols:  f = file; r = float (double); i = int; c = complex
             adapt means the output corresponds to the input type
             a --> entry_1, b --> entry_2, and so on

   ==========  =========================  ================  ==========
   Name        Description                Input             Output 
   ==========  =========================  ================  ==========
   Arithmetic    
   add         addition                   2 x fric          adapt  
   sub         subtraction                2 x fric          adapt  
   mult        multiplication             2 x fric          adapt
   div         division                   2 x fric          adapt 
   ..
   Common
   hypot       sqrt(a**2 + b**2 [+c**2])  2[3] x fric       adapt
   pow         a**b                       2 x fric          adapt
   root        a**(1/b)                   2 x fric          adapt
   sqrt        sqrt(a)                    1 x fric          adapt
   abs         abs(a)                     1 x fric          adapt
   mod         a % b (a.k.a. mod(a,b))    2 x fric          adapt
   amp         abs(a)                     1 x fric          adapt
   power       abs(a)**2                  1 x fric          adapt
   phase       arctan2(a,b) [-pi,pi]      2 x fric          adapt   
   addphz      a*exp(+i*b)                2 x fric          adapt
   subphz      a*exp(-i*b)                2 x fric          adapt
   ..
   Statistic
   max         max(a)                     1 x fric          float
   min         min(a)                     1 x fric          float
   mean        mean(a)                    1 x fric          float
   med         median(a)                  1 x fric          float
   std         std(a) (std. dev.)         1 x fric          float
   var         var(a) (variance)          1 x fric          float
   xmult       a * conj(b)                2 x fric          adapt
   xcor        xmult/(abs(a)abs(b))       2 x fric          adapt
   xcor_amp    |xcor|                     2 x fric          adapt
   xcor_phase  arg(xcor)                  2 x fric          adapt
   .. 
   Logarithm
   log         log(a) (natural log)       1 x fric          adapt
   log10       log10(a) (base 10 log)     1 x fric          adapt
   log_b       log(a)/log(b) (base = b)   2 x fric          adapt
   exp         exp(a)                     1 x fric          adapt
   10pow       10**a                      1 x fric          adapt
   dB          10*log10(a)                1 x fric          adapt
   dBi         10**(a/10)                 1 x fric          adapt    
   ..
   Comparison
   gt          mask( a >  b )             1 x f, 1 x ric    adapt
   ge          mask( a >= b )             1 x f, 1 x ric    adapt
   lt          mask( a <  b )             1 x f, 1 x ric    adapt
   le          mask( a <= b )             1 x f, 1 x ric    adapt
   eq          mask( a == b )             1 x f, 1 x ric    adapt
   ne          mask( a != b )             1 x f, 1 x ric    adapt
   isnan       mask( isnan(a) )           1 x f, 1 x ric    adapt
   notnan      mask( -isnan(a) )          1 x f, 1 x ric    adapt
   ..
   Conversion  
   null2nan    a[a==b] = nan              1x f, 1x ric      adapt
   nan2null    a[isnan(a)] = b            1x f, 1x ric      adapt
   inf2null    a[isinf(a)] = b            1x f, 1x ric      adapt
   num2null    a[a==b] = c                1x f, 2x ric      adapt
   null2null   a[a==b] = c                1x f, 2x ric      adapt
   ..
   Enumerate
   num_null    sum( a ==  b )             1x f, 1x ric      int
   num_nan     sum( a ==  nan )           1 x fric          int 
   num_inf     sum( a == |inf|)           1 x fric          int
   num_neginf  sum( a == -inf )           1 x fric          int
   num_posinf  sum( a ==  inf )           1 x fric          int
   ==========  =========================  ================  ==========

Notes
-----
   * all files must be headerless binary

   * default file type is single-precision floating point (32-bit); 
         append type to filename for other types

   * append type or columns to any file as a comma separated list 
         with no whitespace (ex. file1,type,cols)

   * all operations are element-wise unless otherwise specified

   * operations are carried out in the order given (i.e. sarmath.py
         does not adhere to standard order of operations) 

Examples
--------
   Add 2 files::

      $ sarmath.py file_1 + file_2 = file_3
   
   or::
   
      $ sarmath.py file_1 file_2 -add = file_3

   Multiply a file by 2::

      $ sarmath.py file_1 x 2 = file_out

   or::

      $ sarmath.py file_1 2 -mult = file_out

   Divide two files, cube the quotient, and then multipy by 5::

      $ sarmath file_1 / file_2 3 -pow 5 -mult = file_out

   or::

      $ sarmath file_1 file_2 -div 3 -pow 5 -mult = file_out

   Get the max absolute value of the above example (note the lack of an output file)::

      $ sarmath file_1 / file_2 3 -pow 5 -mult -abs -max 

   Magnitude of a single-precision complex-valued data file::

      $ sarmath file_1,complex -abs = file_out

"""
from __future__ import print_function, division
import sys,os
import numpy as np
from pysar.math._sarmath_solver import Solver
from pysar.math._sarmath_tools import Databank, Parse_command_line, Writer


def main():
   pars = Parse_command_line(args=sys.argv[1:])
   datlist = Databank(pars=pars)
   output = Solver(pars=pars,data=datlist)
   Writer(output=output,pars=pars)  

if __name__=='__main__':
   if len(sys.argv) < 2:
      print(__doc__)
      sys.exit()
   main()


