"""
Additional exceptions
"""

__all__ = ['InputError','InSARCorrBoundsError','cptError',
        'GdalError','NetcdfError','H5pyError']

###===========================================================
class InputError(Exception):
   pass

###----------------------------------------
class InSARCorrBoundsError(Exception):
   pass

###----------------------------------------
class cptError(Exception):
   pass

###----------------------------------------
class GdalError(Exception):
   pass

###----------------------------------------
class NetcdfError(Exception):
   pass

###----------------------------------------
class H5pyError(Exception):
   pass

###----------------------------------------
