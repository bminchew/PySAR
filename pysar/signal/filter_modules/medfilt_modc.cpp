/*  medfilt_modc.cpp

Median filter

*/
#include <Python.h>
#include <arrayobject.h>
#include "medfilt.h"

PyMODINIT_FUNC init_medfilt_modc(void);

PyDoc_STRVAR(medfilt_modc__doc__,

"\nMedian filters\n\n\
Filters\n\
-------\n\
output = f_medfilt2d(input,width,window_x,window_y,null,numthrd)\n\
output = d_medfilt2d(input,width,window_x,window_y,null,numthrd)\n\
\n");

// 2D median filter
PyDoc_STRVAR(fmedfilt2d__doc__,
"\n2D median filter\n\n\
usage:\n\
   output = f_medfilt2d(input,width,window_x,window_y,null,numthrd)\n\
\n\
Parameters\n\
----------\n\
input    :     1d array, float\n\
               data to be filtered\n\
width    :     int\n\
               number of columns in original 2D data array\n\
window_x :     int\n\
               window size in x-direction (along rows)\n\
window_y :     int\n\
               window size in y-direction (down columns) \n\
null     :     float\n\
               null value \n\
numthrd  :     int\n\
               number of pthreads\n\
\n\
Output\n\
------\n\
output   :     1d array, float\n\
               Filtered data; same size, shape, and type as input\n\n");

/**************************************************************************************/
static PyObject *f_medfilt2d(PyObject *self, PyObject *args) {

   PyArrayObject *in_array, *outarr;
   int precision;
   problem p;

   // Get tuple of arguments
   if (!PyArg_ParseTuple(args, "O!iiifi", &PyArray_Type, &in_array,
         &p.cols, &p.rgwindow, &p.azwindow, &p.null, &p.numthrd))
      return NULL;

   npy_intp n = in_array->dimensions[0];
   p.lines = n/p.cols;

   precision = 1;
   outarr = (PyArrayObject *) PyArray_EMPTY(1, &n, NPY_FLOAT32, 0);

   p.rgwhalf = (int) p.rgwindow/2;
   p.azwhalf = (int) p.azwindow/2;
   p.winsize = (int) (p.rgwhalf*2 + 1)*(p.azwhalf*2 + 1);

   if (p.numthrd < 1) { p.numthrd = 1; }

   p.image = (float *) in_array->data;
   p.outarr = (float *) outarr->data;

   Py_BEGIN_ALLOW_THREADS;
   spawn_medfilt_workers(&p,precision);
   Py_END_ALLOW_THREADS;

   return PyArray_Return(outarr);
}

// 2D double median filter
PyDoc_STRVAR(dmedfilt2d__doc__,
"\n2D median filter\n\n\
usage:\n\
   output = d_medfilt2d(input,width,window_x,window_y,null,numthrd)\n\
\n\
Parameters\n\
----------\n\
input    :     1d array, double\n\
               data to be filtered\n\
width    :     int\n\
               number of columns in original 2D data array\n\
window_x :     int\n\
               window size in x-direction (along rows)\n\
window_y :     int\n\
               window size in y-direction (down columns) \n\
null     :     float\n\
               null value \n\
numthrd  :     int\n\
               number of pthreads\n\
\n\
Output\n\
------\n\
output   :     1d array, double\n\
               Filtered data; same size, shape, and type as input\n\n");

/**************************************************************************************/
static PyObject *d_medfilt2d(PyObject *self, PyObject *args) {

   PyArrayObject *in_array, *outarr;
   int precision;
   problem p;

   // Get tuple of arguments
   if (!PyArg_ParseTuple(args, "O!iiifi", &PyArray_Type, &in_array,
         &p.cols, &p.rgwindow, &p.azwindow, &p.null, &p.numthrd))
      return NULL;

   npy_intp n = in_array->dimensions[0];
   p.lines = n/p.cols;

   precision = 2;
   outarr = (PyArrayObject *) PyArray_EMPTY(1, &n, NPY_FLOAT64, 0);

   p.rgwhalf = (int) p.rgwindow/2;
   p.azwhalf = (int) p.azwindow/2;
   p.winsize = (int) (p.rgwhalf*2 + 1)*(p.azwhalf*2 + 1);

   if (p.numthrd < 1) { p.numthrd = 1; }

   p.d_image = (double *) in_array->data;
   p.d_outarr = (double *) outarr->data;

   Py_BEGIN_ALLOW_THREADS;
   spawn_medfilt_workers(&p,precision);
   Py_END_ALLOW_THREADS;

   return PyArray_Return(outarr);
}


/*=====================================================================================*/
static PyMethodDef medfilt_modc_methods[] = {
   {"f_medfilt2d", (PyCFunction) f_medfilt2d, METH_VARARGS | METH_KEYWORDS, fmedfilt2d__doc__},
   {"d_medfilt2d", (PyCFunction) d_medfilt2d, METH_VARARGS | METH_KEYWORDS, dmedfilt2d__doc__},
   {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC init_medfilt_modc(void) {
   (void) Py_InitModule3("_medfilt_modc", medfilt_modc_methods, medfilt_modc__doc__);
   import_array();
};
