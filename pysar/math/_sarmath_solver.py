"""
_sarmath_solver

Module containing the Solver class

"""
from __future__ import print_function, division
import sys,os
import numpy as np
from math import pi
from pysar.utils.gen_tools import typecomplex

class Solver():
   """

   Solver:  Calculates the output values for the command line tool sarmath.py

   Parameters
   ----------
   datalist    :  sarmath class
                  Class _sarmath_tools.Databank(pars)
   pars        :  sarmath class
                  Class _sarmath_tools.Parse_command_line(args)

   """

   def __init__(self,pars,data):
      singlelist = ['sqrt','abs','amp','power','phase',
                     'num_nan','num_inf','num_neginf','num_posinf',
                     'dB','dBi','ln','log','log10','exp','10pow',
                     'max','min','std','var','mean','med',
                     'isnan','notnan']
      doublelist = ['add','sub','mult','div','pow','mod','root','xmult',
                     'addphz','subphz','xcor','xcor_amp','xcor_phase',
                     'null2nan','nan2null','inf2null',
                     'gt','ge','lt','le','eq','ne',
                     'log_b','hypot','num_null']
      triplelist = ['null2null','num2null','num2num']

      if len(pars.action) < 1: 
         raise NotImplementedError('Invalid action.')

      if len(data.data) < 2:
         answer, i = data.data[0], 0
         while i < len(pars.action):
            answer = self._singledata(answer,pars.action[i])
            i += 1
      else:
         ind, i = 0, 0
         while i < len(pars.action): 
            if pars.action[i] in singlelist:
               answer = self._singledata(data.data[ind],pars.action[i]) 
            elif pars.action[i] in triplelist:
               answer = self._tripledata(data.data[ind],data.data[ind+1],data.data[ind+2],pars.action[i])
               ind += 2
            elif pars.action[i] == 'hypot' and pars.args.index('-hypot') == ind+3:
               answer = self._tripledata(data.data[ind],data.data[ind+1],data.data[ind+2],pars.action[i])
               ind += 2
            elif pars.action[i] == 'eq' and pars.args.index('-eq') == ind+3:
               answer = self._tripledata(data.data[ind],data.data[ind+1],data.data[ind+2],pars.action[i])
               ind += 2
            elif pars.action[i] == 'ne' and pars.args.index('-ne') == ind+3:
               answer = self._tripledata(data.data[ind],data.data[ind+1],data.data[ind+2],pars.action[i])
               ind += 2
            else:
               answer = self._doubledata(data.data[ind],data.data[ind+1],pars.action[i])
               ind += 1
            data.data[ind] = answer
            i += 1
      self.answer = answer 

   def _singledata(self,data,action):
      if action == 'sqrt':
         return np.sqrt(data)
      elif action == 'abs':  #astype(np.abs(data[0]).dtype): hack to ensure right type is returned
         return np.abs(data)
      elif action == 'amp':
         return np.abs(data) 
      elif action == 'power':
         return np.abs(data)**2
      elif action == 'phase':
         if not typecomplex(data):  
            return np.zeros_like(data)
         else:  
            return np.arctan2(data.imag,data.real)
      elif action == 'num_nan':
         return np.sum(np.isnan(data))
      elif action == 'num_inf':
         return np.sum(np.isinf(data))
      elif action == 'num_neginf':
         return np.sum(np.isneginf(data))
      elif action == 'num_posinf':
         return np.sum(np.isposinf(data))
      elif action == 'dB':
         return 10.*np.log10(data)
      elif action == 'dBi':
         return 10.**(data/10.)
      elif action == 'ln' or action == 'log':
         return np.log(data)
      elif action == 'log10':
         return np.log10(data)
      elif action == 'exp':
         return np.exp(data)
      elif action == '10pow':
         return 10**data
      elif action == 'max':
         return np.max(data)
      elif action == 'min':
         return np.min(data)
      elif action == 'std':
         return np.std(data)
      elif action == 'var':
         return np.var(data)
      elif action == 'mean':
         return np.mean(data)
      elif action == 'med':
         return np.median(data)
      elif action == 'isnan':
         return np.isnan(data)
      elif action == 'notnan':
         return -np.isnan(data)
      else:
         return data

   ###--------------------------------------------------------------------------
   def _doubledata(self,data1,data2,action):
      if action == 'add':
         return data1 + data2
      elif action == 'sub':
         return data1 - data2
      elif action == 'mult':
         return data1 * data2
      elif action == 'div':
         return data1 / data2
      elif action == 'hypot':
         return np.hypot(data1,data2)
      elif action == 'pow':
         return data1**data2
      elif action == 'mod':
         return data1 % data2
      elif action == 'root':
         return data1**(1./data2)
      elif action == 'xmult':
         return data1*np.conj(data2)
      elif action == 'xcor' or action == 'xcor_amp' or action == 'xcor_phase':
         cor = (data1*np.conj(data2))/np.sqrt( data1*np.conj(data1) * data2*np.conj(data2))
         if action == 'xcor':
            return cor
         elif action == 'xcor_amp':
            return np.abs(cor)
         elif action == 'xcor_phase':
            if not typecomplex(data):  return np.zeros_like(cor)
            else:  return np.arctan2(cor.imag,cor.real)
      elif action == 'null2nan':
         mask = self._genmask(data1=data1,data2=data2,tol=1.e-7)
         data1[mask] = np.nan
         return data1
      elif action == 'nan2null':
         data1[np.isnan(data1)] = data2
         return data1
      elif action == 'inf2null':
         data1[np.isinf(data1)] = data2
         return data1   
      elif action == 'num_null':
         mask = self._genmask(data1=data1,data2=data2,tol=1.e-7)
         return np.sum(mask)
      elif action == 'gt':
         mask = data1 > data2
         return mask.astype(data1.dtype)
      elif action == 'ge':
         mask = data1 >= data2 
         return mask.astype(data1.dtype)
      elif action == 'lt':
         mask = data1 < data2 
         return mask.astype(data1.dtype) 
      elif action == 'le':
         mask = data1 <= data2 
         return mask.astype(data1.dtype)
      elif action == 'eq':
         mask = np.abs(data1 - data2) < 1.e-7 
         return mask.astype(data1.dtype)
      elif action == 'ne':
         mask = np.abs(data1 - data2) > 1.e-7
         return mask.astype(data1.dtype) 
      elif action == 'log_b':
         return np.log(data1)/np.log(data2) 
      elif action == 'subphz':
         return data1*np.exp(-1j*data2) 
      elif action == 'addphz':
         return data1*np.exp(1j*data2)  
      else:
         print('unrecognized option', action)

   ###-------------------------------------------------------------------------
   def _tripledata(self,data1,data2,data3,action):
      if action == 'hypot':
         return np.hypot(np.hypot(data1,data2),data3)
      elif action == 'null2null' or action == 'num2null' or action == 'num2num':
         mask = self._genmask(data1=data1,data2=data2,tol=1.e-7)
         data1[mask] = data3
         return data1
      elif action == 'eq':
         mask = self._genmask(data1=data1,data2=data2,tol=data3)
         return mask.astype(data1.dtype)   
      elif action == 'ne': 
         mask = self._genmask(data1=data1,data2=data2,tol=data3)
         return (-mask).astype(data1.dtype)  
      else:
         print('unrecognized option', action) 

   ###-------------------------------------------------------------------------
   def _genmask(self,data1,data2,tol=1.e-7):
      return np.abs(data1 - data2) < tol

   ###-------------------------------------------------------------------------




