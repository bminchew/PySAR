"""
PySAR

Polarimetric SAR decomposition 

Contents
--------
decomp_fd(hhhh,vvvv,hvhv,hhvv,numthrd=None)  :  Freeman-Durden 3-component decomposition 

"""
from __future__ import print_function, division
import sys,os
import numpy as np
###===========================================================================================

def decomp_fd(hhhh,vvvv,hvhv,hhvv,null=None,numthrd=None,maxthrd=8):
   """
   Freeman-Durden 3-component decomposition

   Parameters
   ----------
   hhhh     :     ndarray
                  horizontally polarized power 
   vvvv     :     ndarray
                  vertically polarized power
   hvhv     :     ndarray
                  cross-polarized power
   hhvv     :     ndarray
                  co-polarized cross product (complex-valued)
   null     :     float or None
                  null value to exclude from decomposition 
   numthrd  :     int or None
                  number of pthreads; None sets numthrd based on the data array size [None]  
   maxthrd  :     int or None
                  maximum allowable numthrd [8]

   Returns
   -------
   ps       :     ndarray
                  surface-scattered power
   pd       :     ndarray
                  double-bounce power
   pv       :     ndarray
                  volume-scattered power

   Notes
   -----
   * arrays are returned with the same type as hhhh data

   Reference
   ---------
   1. Freeman, A. and Durden, S., "A three-component scattering model for polarimetric SAR data", *IEEE Trans. Geosci. Remote Sensing*, vol. 36, no. 3, pp. 963-973, May 1998. 

   """
   from pysar.polsar._decomp_modc import free_durden

   if not numthrd: 
      numthrd = np.max([len(hhhh)//1e5, 1]) 
      if numthrd > maxthrd: numthrd = maxthrd 
   elif numthrd < 1:
      raise ValueError('numthrd must be >= 1')

   if null:
      nullmask  = np.abs(hhhh-null) < 1.e-7
      nullmask += np.abs(vvvv-null) < 1.e-7
      nullmask += np.abs(hvhv-null) < 1.e-7
      nullmask += np.abs(hhvv-null) < 1.e-7
      hhvv[nullmask] = 0.

   hhhhtype = None
   if hhhh.dtype != np.float32:
      hhhhtype = hhhh.dtype
      hhhh = hhhh.astype(np.float32)
      vvvv = vvvv.astype(np.float32)
      hvhv = hvhv.astype(np.float32)
      hhvv = hhvv.astype(np.complex64)

   if not all({2-x for x in [hhhh.ndim, vvvv.ndim, hvhv.ndim, hhvv.ndim]}):
      hhhh, vvvv = hhhh.flatten(), vvvv.flatten()
      hvhv, hhvv = hvhv.flatten(), hhvv.flatten()

   P = free_durden(hhhh, vvvv, hvhv, hhvv, numthrd) 
   if hhhhtype: P = P.astype(hhhhtype)
   P = P.reshape(3,-1)

   if null: P[0,nullmask], P[1,nullmask], P[2,nullmask] = null, null, null

   return P[0,:], P[1,:], P[2,:]

###---------------------------------------------------------------------------------

def decomp_haa(hhhh,vvvv,hvhv,hhhv,hhvv,hvvv,matform='C',null=None,numthrd=None,maxthrd=8):
   """
   Cloude-Pottier H/A/alpha polarimetric decomposition 

   Parameters
   ----------
   hhhh     :     ndarray 
                  horizontal co-polarized power (or 0.5|HH + VV|^2 if matform = 'T') 
   vvvv     :     ndarray
                  vertical co-polarized power (or 0.5|HH - VV|^2 if matform = 'T') 
   hvhv     :     ndarray
                  cross-polarized power (2|HV|^2 for matform = 'T') 
   hhhv     :     ndarray
                  HH.HV* cross-product (or 0.5(HH+VV)(HH-VV)* for matform = 'T')
   hhvv     :     ndarray
                  HH.VV* cross-product (or HV(HH+VV)* for matform = 'T')
   hvvv     :     ndarray
                  HV.VV* cross-product (or HV(HH-VV)* for matform = 'T')
   matform  :     str {'C' or 'T'}
                  form of input matrix entries: 'C' for covariance matrix and
                  'T' for coherency matrix ['C'] (see ref. 1)
   null     :     float or None
                  null value to exclude from decomposition 
   numthrd  :     int or None
                  number of pthreads; None sets numthrd based on the data array size [None]  
   maxthrd  :     int or None
                  maximum allowable numthrd [8]

   Returns
   -------
   H        :     ndarray
                  entropy (H = -(p1*log_3(p1) + p2*log_3(p2) + p3*log_3(p3)) 
                  where pi = lam_i/(hhhh+vvvv+hvhv)) and lam is an eigenvalue 
   A        :     ndarray
                  anisotropy (A = (lam_2-lam_3)/(lam_2+lam_3) --> lam_1 >= lam_2 >= lam_3
   alpha    :     ndarray
                  alpha angle in degrees (see ref. 1)

   Notes
   -----
   * arrays are returned with the same type as hhhh data
   * if covariance matrix form is used, do not multiply entries by any constants 

   Reference
   ---------
   1. Cloude, S. and Pottier, E., "An entropy based classification scheme for land applications of polarimetric SAR", *IEEE Trans. Geosci. Remote Sensing*, vol. 35, no. 1, pp. 68-78, Jan. 1997. 

   """
   from pysar.polsar._decomp_modc import cloude_pot

   if matform == 'C' or matform == 'c':
      mtf = 1
   elif matform == 'T' or matform == 't':
      mtf = 0
   else:
      raise ValueError("matform must be 'C' or 'T'")

   if not numthrd:
      numthrd = np.max([len(hhhh)//1e5, 1])
      if numthrd > maxthrd: numthrd = maxthrd
   elif numthrd < 1:
      raise ValueError('numthrd must be >= 1')

   if null:
      nullmask  = np.abs(hhhh-null) < 1.e-7
      nullmask += np.abs(vvvv-null) < 1.e-7
      nullmask += np.abs(hvhv-null) < 1.e-7
      nullmask += np.abs(hhhv-null) < 1.e-7
      nullmask += np.abs(hhvv-null) < 1.e-7
      nullmask += np.abs(hvvv-null) < 1.e-7
      hhhh[nullmask], vvvv[nullmask] = 0., 0.
      hvhv[nullmask] = 0.

   hhhhtype = None
   if hhhh.dtype != np.float32:
      hhhhtype = hhhh.dtype
      hhhh = hhhh.astype(np.float32)
      vvvv = vvvv.astype(np.float32)
      hvhv = hvhv.astype(np.float32)
      hhhv = hhhv.astype(np.complex64)
      hhvv = hhvv.astype(np.complex64)
      hvvv = hvvv.astype(np.complex64)

   if not all({2-x for x in [hhhh.ndim, vvvv.ndim, hvhv.ndim, hhhv.ndim, hhvv.ndim, hvvv.ndim]}):
      hhhh, vvvv = hhhh.flatten(), vvvv.flatten()
      hvhv, hhvv = hvhv.flatten(), hhvv.flatten()
      hhhv, hvvv = hhhv.flatten(), hvvv.flatten()

   P = cloude_pot(hhhh, vvvv, hvhv, hhhv, hhvv, hvvv, mtf, numthrd)
   if hhhhtype: P = P.astype(hhhhtype)
   P = P.reshape(3,-1)

   if null: P[0,nullmask], P[1,nullmask], P[2,nullmask] = null, null, null

   return P[0,:], P[1,:], P[2,:]


def decomp_cp(hhhh,vvvv,hvhv,hhhv,hhvv,hvvv,matform='C',null=None,numthrd=None,maxthrd=8):
   __doc__ = decomp_haa.__doc__ 
   return decomp_haa(hhhh=hhhh,vvvv=vvvv,hvhv=hvhv,hhhv=hhhv,hhvv=hhvv,hvvv=hvvv,
            matform=matform,null=null,numthrd=numthrd,maxthrd=maxthrd)
