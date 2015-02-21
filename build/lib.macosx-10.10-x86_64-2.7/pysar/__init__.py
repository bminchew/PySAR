"""
                  ~~~  PySAR  ~~~
      Python-based toolbox for post-processing
      synthetic aperture radar (SAR) data

PySAR is a general-purpose set of tools for common post-processing
tasks involving the use of SAR data.  Interferometric SAR (InSAR)
and Polarimetric SAR (PolSAR) tools are included along with tools that
are useful for processing 1D data sets, such as GPS and seismic data.

Contents:
   :ref:`image`
   :ref:`insar`
"""

#Copyright (C) 2013   Brent M. Minchew
#--------------------------------------------------------------------
#GNU Licensed
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#--------------------------------------------------------------------

import signal
import math
import image
import polsar
import insar
import utils 
import etc
import version
import plot

__version__ = version.version
__all__ = ['signal','math','image','polsar','insar','utils','etc','version','plot']
