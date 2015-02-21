
import numpy as np

def calcGmat(x,y,n,w=1):
   deg = np.arange(n+2)
   a = np.zeros((len(x),deg.sum()))
   cnt = -1
   xu = 1
   for u in deg:
      yv = 1
      for v in np.arange(n-u+1):
         cnt += 1
         a[:,cnt] = w*xu*yv
         if v < n-u:
            yv *= y
      if u < deg[-1]:
         xu *= x
   return a


def L1norm(p,a,d):
   pro = np.dot(a,p)
   return np.sum(np.abs(pro-d))


def polyfit2d(x,y,d,n,p=2,w=False,cor=-1,N=36):
   """
      Fits an n-order 2d polynomial to the given data d using an 
         L^p norm ( default p = 2; max(order) = 5 ) 
         w   = bool (True to weight by correlation...must provide cor image)
         cor = correlation image
         N   = number of pixels in look window
      Outputs: 
         array c = [c_0x^0y^0, c_1x^0y^1,..., c_nx^0y^n, 
            c_(n+1)x^1y^0, ..., c_(2n)x^1y(n-1), ..., c_(-1)x^ny^0]
   """

   if p != 1 and p != 2:
      print('p = %d is not implemented; defaulting to p = 2' % p)
      p = 2
   if w and len(cor) <= 1:
      print('You must provide a correlation image for weighting...calculating unweighted')
      w = False

   if w:
      cor = cor**2
      cor = 1/np.sqrt( 1./(2.*N)* (1. - cor)/cor )
      d = cor*d
   else:
      cor = 1

   a = calcGmat(x=x,y=y,n=n,w=cor)     

   if p == 1:
      from scipy.optimize import fmin
      deg = np.arange(n+2)
      init = np.linalg.lstsq(a,d)[0]
      s = fmin(L1norm,init,args=(a,d),ftol=1e-9,xtol=1e-6,maxiter=100000,
                  maxfun=10000,full_output=1,disp=1)
      return s[0]
   else:
      return np.linalg.lstsq(a,d)[0]



def subtract_surf(d,c,null):
   """
      Subtracts surface from entire image 
      d = original data array
      c = array of coefficients from polyfit2d
   """
   from pysar.insar._subsurf import subsurf
   lenarr = np.cumsum(np.arange(1,6))
   n = np.abs(len(c)-lenarr).argmin()

   dsp = np.shape(d)

   x = np.arange(dsp[1],dtype=np.float32)
   y = np.arange(dsp[0],dtype=np.float32)
   x,y = np.meshgrid(x,y)

   d = np.float64(d.flatten())
   x = x.flatten()
   y = y.flatten()

   subsurf(d=d,x=x,y=y,c=c,deg=n,nul=null)
   return np.float32(np.reshape(d,(-1,dsp[1])))











