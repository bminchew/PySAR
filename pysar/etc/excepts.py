"""
Additional exceptions
"""

__all__ = ['InputError','InSARCorrBoundsError','cptError',
        'GdalError','NetcdfError','H5pyError','BoneHeaded']

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
class BoneHeaded(Exception):
   pass
###----------------------------------------
