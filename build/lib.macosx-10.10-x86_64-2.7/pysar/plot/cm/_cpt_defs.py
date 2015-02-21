import sys,os

__all__ = ['preload','cptfldr','cptdic','specialcpt','mpl_noinclude_t','mpl_noinclude','mpl_special']



preload = ['dem','fire','publue','dkbluedkred','stern_special']



specialcpt = {'dem' : 'dem_screen.cpt'}  # color palettes with special names

tempf = '/'.join(__file__.split('/')[:-1])
if len(tempf) < 1: tempf = '.' 
cptfldr = tempf + '/cpt/'

try:
   cptlist = os.listdir(cptfldr)
except:
   raise IOError('%s is not a valid cpt folder' % cptfldr)

cptdic = {}
for cpt in cptlist:
   if '.cpt' in cpt:
      cptdic[cpt.split('.cpt')[0]] = cpt 
cptdic = dict(cptdic, **specialcpt)

mpl_noinclude_t = ['gist_gray','gist_heat','gist_yarg','flag','prism','gnuplot',
         'gnuplot2','ocean','afmhot','rainbow','cubehelix']
mpl_noinclude = []
for ent in mpl_noinclude_t:
   mpl_noinclude.append(ent)
   mpl_noinclude.append(ent+'_r')


mpl_special = mpl_noinclude
