"""
Butterworth filtering routines 

Contents
--------
butter(data,low,high,dt=None,df=None,order=4,zero_phase=False)       :  General Butterworth filter
bandpass(data,low,high,dt=None,df=None,order=4,zero_phase=False)     :  Bandpass
bandreject(data,low,high,dt=None,df=None,order=4,zero_phase=False)   :  Bandreject
lowpass(data,high,dt=None,df=None,order=4,zero_phase=False)          :  Lowpass
highpass(data,high,dt=None,df=None,order=4,zero_phase=False)         :  Highpass

taper(data,percent)                                                  :  Basic cosine taper

"""
from __future__ import print_function, division
import numpy as np
from _xapiir import callxapiir
from special import taper

__all__ = ['taper', 'butter','bandpass','bandreject','lowpass','highpass']

###===================================================================================
def butter(data,low=None,high=None,dt=None,df=None,order=4,zero_phase=False,reject=False):
   """
   Butterworth filter 

   butter(data,low=None,high=None,dt=None,df=None,order=4,zero_phase=False,reject=False)
   
   Parameters
   ----------
      data :      array
                  input data vector (real-valued)
      low  :      float
                  min frequency in passband [Hz] (default = None --> lowpass filter)
      high :      float
                  max frequency in passband [Hz] (default = None --> highpass filter)
      dt   :      float
                  sampling interval [sec]
      df   :      float
                  sampling frequency [Hz]
      order :     int
                  filter order (default = 4; max = 10)
      zero_phase: bool
                  True to run the filter fwd and rev for 0 phase shift (default = False)
      reject :    bool
                  True initializes a band reject instead of bandpass filter (default = False)

   Output
   ------
      F :         array {same size and type as data}
                  filtered data 

   Notes
   -----
      * dt or df must be defined (dt has priority)
      * low and/or high must be defined
         - if only low is defined, highpass filter is applied
         - if only high is defined, lowpass filter is applied
         - if low and high are defined, bandpass filter is applied unless reject==True
      * if reject == True, both high and low must be defined 

   """
   
   tp = 'BP'
   passes = 1
   nsamps = len(data)

   if not dt and not df: raise ValueError("dt or df must be defined")
   if not low and not high: raise ValueError("low and/or high must be defined")
   if not nsamps > 1: raise ValueError("data is a scalar")

   if dt is None:  dt = 1./df
   if zero_phase:  passes = 2
   if reject: 
      if not low or not high: 
         raise ValueError('low and high must be defined for bandreject')
      tp = 'BR'

   if low and not high:
      tp, high = 'HP', 1.
   elif not low and high:
      tp, low = 'LP', 1.

   data = callxapiir(data,nsamps,'BU',0.,0.,order,tp,low,high,dt,passes)
   return data

###===================================================================================
def bandpass(data,low,high,dt=None,df=None,order=4,zero_phase=False):
   """
   Butterworth bandpass filter 

   bandpass(data,low,high,dt=None,df=None,order=4,zero_phase=False)
   
   Parameters
   ----------
      data :      array
                  input data vector (real-valued)
      low  :      float
                  min frequency in passband [Hz] (default = None --> lowpass filter)
      high :      float
                  max frequency in passband [Hz] (default = None --> highpass filter)
      dt   :      float
                  sampling interval [sec]
      df   :      float
                  sampling frequency [Hz]
      order :     int
                  filter order (default = 4; max = 10)
      zero_phase: bool
                  True to run the filter fwd and rev for 0 phase shift (default = False)

   Output
   ------
      F :         array {same size and type as data}
                  filtered data 
 
   Notes
   -----
      * dt or df must be defined (dt has priority)

   """

   if not low or not high: raise ValueError('low and high must be defined for bandpass')
   return butter(data=data,low=low,high=high,dt=dt,df=df,order=order,zero_phase=zero_phase)

###===================================================================================
def lowpass(data,high,dt=None,df=None,order=4,zero_phase=False):
   """
   Butterworth lowpass filter 

   butter.lowpass(data,high,dt=None,df=None,order=4,zero_phase=False)
   
   Parameters
   ----------
      data :      array
                  input data vector (real-valued)
      high :      float
                  max frequency in passband [Hz] 
      dt   :      float
                  sampling interval [sec]
      df   :      float
                  sampling frequency [Hz]
      order :     int
                  filter order (default = 4; max = 10)
      zero_phase: bool
                  True to run the filter fwd and rev for 0 phase shift (default = False)

   Output
   ------
      F :         array {same size and type as data}
                  filtered data 

   Notes
   -----
      * dt or df must be defined (dt has priority)

   """
   if not high: raise ValueError('high must be defined for lowpass filter')
   return butter(data=data,high=high,dt=dt,df=df,order=order,zero_phase=zero_phase) 

###===================================================================================
def highpass(data,low,dt=None,df=None,order=4,zero_phase=False):
   """
   Butterworth highpass filter 

   highpass(data,low,dt=None,df=None,order=4,zero_phase=False)
   
   Parameters
   ----------
      data :      array
                  input data vector (real-valued)
      low  :      float
                  min frequency in passband [Hz] 
      dt   :      float
                  sampling interval [sec]
      df   :      float
                  sampling frequency [Hz]
      order :     int
                  filter order (default = 4; max = 10)
      zero_phase: bool
                  True to run the filter fwd and rev for 0 phase shift (default = False)

   Output
   ------
      F :         array {same size and type as data}
                  filtered data 

   Notes
   -----
      * dt or df must be defined (dt has priority)

   """

   if not low: raise ValueError('low must be defined for highpass filter')
   return butter(data=data,low=low,dt=dt,df=df,order=order,zero_phase=zero_phase) 

###===================================================================================
def bandreject(data,low,high,dt=None,df=None,order=4,zero_phase=False):
   """
   Butterworth bandreject filter 

   bandreject(data,low,high,dt=None,df=None,order=4,zero_phase=False)
  
   Parameters
   ----------
      data :      array
                  input data vector (real-valued)
      low  :      float
                  min frequency in passband [Hz] (default = None --> lowpass filter)
      high :      float
                  max frequency in passband [Hz] (default = None --> highpass filter)
      dt   :      float
                  sampling interval [sec]
      df   :      float
                  sampling frequency [Hz]
      order :     int
                  filter order (default = 4; max = 10)
      zero_phase: bool
                  True to run the filter fwd and rev for 0 phase shift (default = False)

   Output
   ------
      F :         array {same size and type as data}
                  filtered data 

   Notes
   -----
      * dt or df must be defined (dt has priority)
      * low and/or high must be defined
         - if only low is defined, highpass filter is applied
         - if only high is defined, lowpass filter is applied
         - if low and high are defined, bandpass filter is applied unless reject==True
      * if reject == True, both high and low must be defined 
 
   """

   if not low and not high: 
      raise ValueError('low and high must be defined for bandreject')
   data = butter(data=data,low=low,high=high,dt=dt,df=df,order=order,
               zero_phase=zero_phase,reject=True)
   return data







