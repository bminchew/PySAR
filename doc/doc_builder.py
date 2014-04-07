#!/usr/bin/env python

'''
Build documentation 
'''
import sys,os
import subprocess

doautogen = True  # apply sphinx-autogen...should normally be True
if doautogen:
   here = os.getcwd()
   os.chdir('source')
   moddirs = os.listdir('.')
   for mod in moddirs:
      if os.path.isdir(mod) and not mod.startswith('_'):
         base = os.getcwd()
         os.chdir(mod)
         tmplist = os.listdir('.')
         rstfile = []
         for t in tmplist:
            if t.endswith('.rst'):
               rstfile.append(t)
         cstr = 'sphinx-autogen -o generated'.split() + rstfile       
         subprocess.call(cstr)     
         os.chdir(base)
   os.chdir(here)

subprocess.call('make clean'.split())
subprocess.call('make html'.split())


'''
oldstr = 'dt id='
newstr = 'dt class="funcall" id='
for root,dirs,files in os.walk('build/html'):
   for fil in files:
      if fil.endswith('.html'):
         fid = open('/'.join([root,fil]),'r')
         reads = fid.readlines()
         fid.close()


         fid = open('/'.join([root,fil]),'w')
         for read in reads:
            row = read
            if oldstr in read:
               row = row.replace(oldstr,newstr)
            fid.write(row)
         fid.close()
'''
