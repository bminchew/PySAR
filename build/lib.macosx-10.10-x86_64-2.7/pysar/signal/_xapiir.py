"""
Routine to call xapirr

Contents
--------
callxapiir(data,nsamps,aproto,trbndw,a,iord,type,flo,fhi,ts,passes)

"""
from __future__ import print_function, division
import numpy as np
import _xapiir_sub

__all__ = ['callxapiir']

def callxapiir(data,nsamps,aproto,trbndw,a,iord,type,flo,fhi,ts,passes):
   """
   Call Fortran subroutine xapiir

   callxapiir(data,nsamps,aproto,trbndw,a,iord,type,flo,fhi,ts,passes)

   XAPIIR -- SUBROUTINE:   IIR FILTER DESIGN AND IMPLEMENTATION

   AUTHOR:  Dave Harris
 
   LAST MODIFIED:  September 12, 1990
 
   ARGUMENTS:
   ----------
 
     DATA           REAL NUMPY ARRAY CONTAINING SEQUENCE TO BE FILTERED
                      ORIGINAL DATA DESTROYED, REPLACED BY FILTERED DATA
 
     NSAMPS         NUMBER OF SAMPLES IN DATA
 
 
     APROTO         CHARACTER*2 VARIABLE, CONTAINS TYPE OF ANALOG
                      PROTOTYPE FILTER
                      '(BU)TTER  ' -- BUTTERWORTH FILTER
                      '(BE)SSEL  ' -- BESSEL FILTER
                      'C1      ' -- CHEBYSHEV TYPE I
                      'C2      ' -- CHEBYSHEV TYPE II
 
     TRBNDW         TRANSITION BANDWIDTH AS FRACTION OF LOWPASS
                    PROTOTYPE FILTER CUTOFF FREQUENCY.  USED
                    ONLY BY CHEBYSHEV FILTERS.
 
     A              ATTENUATION FACTOR.  EQUALS AMPLITUDE
                    REACHED AT STOPBAND EDGE.  USED ONLY BY
                    CHEBYSHEV FILTERS.
 
     IORD           ORDER (#POLES) OF ANALOG PROTOTYPE
                    NOT TO EXCEED 10 IN THIS CONFIGURATION.  4 - 5
                    SHOULD BE AMPLE.
 
     TYPE           CHARACTER*2 VARIABLE CONTAINING FILTER TYPE
                      'LP' -- LOW PASS
                      'HP' -- HIGH PASS
                      'BP' -- BAND PASS
                      'BR' -- BAND REJECT
 
     FLO            LOW FREQUENCY CUTOFF OF FILTER (HERTZ)
                    IGNORED IF TYPE = 'LP'
 
     FHI            HIGH FREQUENCY CUTOFF OF FILTER (HERTZ)
                    IGNORED IF TYPE = 'HP'
 
     TS             SAMPLING INTERVAL (SECONDS)
 
     PASSES           INTEGER VARIABLE CONTAINING THE NUMBER OF PASSES
                    1 -- FORWARD FILTERING ONLY
                    2 -- FORWARD AND REVERSE (I.E. ZERO PHASE) FILTERING

     MAX_NT         MAX DATA ARRAY SIZE

   """

   max_nt = nsamps 
   origtype = data.dtype
   data = data.astype(np.float32)
   _xapiir_sub.xapiir(data,nsamps,aproto,trbndw,a,iord,type,flo,fhi,ts,passes,max_nt)
   data = data.astype(origtype)
   return data
