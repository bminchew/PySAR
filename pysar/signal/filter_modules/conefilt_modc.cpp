/*  conefilt_modc.cpp

Cone filter

*/
#include <Python.h>
#include <arrayobject.h>
#include "conefilt.h"

PyMODINIT_FUNC init_conefilt_modc(void);

PyDoc_STRVAR(conefilt_modc__doc__,

"\nTriangle and Cone filters\n\n\
Filters\n\
-------\n\
filtdata = conefilt2d(input,window,dx,dy,null)\n\
\n");

// 2D cone
PyDoc_STRVAR(fconefilt2d__doc__,
"\n2D cone filter\n\n\
usage:\n\
   output = fconefilt2d(input,window,cols,dx,dy,null,numthrd)\n\
\n\
Parameters\n\
----------\n\
input    :     1d array, float\n\
               Data to be filtered\n\
window   :     1d array, float\n\
               Window sizes; must be same size, shape, and type as input\n\
cols     :     int\n\
               number of columns in 2d array \n\
dx       :     float\n\
               spacing along x in input \n\
dy       :     float\n\
               spacing along y in input\n\
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
static PyObject *fconefilt2d(PyObject *self, PyObject *args) {

   PyArrayObject *in_array, *win, *output;
   problem p;

   // Get tuple of arguments
   if (!PyArg_ParseTuple(args, "O!O!ifffi", &PyArray_Type, &in_array, &PyArray_Type, &win, 
         &p.cols, &p.dx, &p.dy, &p.null, &p.numthrd))
      return NULL;

   npy_intp n = in_array->dimensions[0];
   p.lines = n/p.cols; 

   output = (PyArrayObject *) PyArray_EMPTY(1, &n, NPY_FLOAT32, 0);

   p.image = (float *) in_array->data;
   p.win   = (float *) win->data;
   p.out   = (float *) output->data;

   Py_BEGIN_ALLOW_THREADS;
   spawn_conefilt_workers(&p);
   Py_END_ALLOW_THREADS;

   return PyArray_Return(output);
}



/*=====================================================================================*/
static PyMethodDef conefilt_modc_methods[] = {
   {"fconefilt2d", (PyCFunction) fconefilt2d, METH_VARARGS | METH_KEYWORDS, fconefilt2d__doc__},
   {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC init_conefilt_modc(void) {
   (void) Py_InitModule3("_conefilt_modc", conefilt_modc_methods, conefilt_modc__doc__);
   import_array();
};


