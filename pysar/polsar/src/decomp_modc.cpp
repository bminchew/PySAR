/*  decomp_modc.cpp

Polarimetric SAR decomposition routines.  

*/
#include <Python.h>
#include <arrayobject.h>
#include "decomp.h"

PyMODINIT_FUNC init_decomp_modc(void);

PyDoc_STRVAR(decomp_modc__doc__,
"\nPolarimetric SAR decomposition routines\n\n\
Functions\n\
---------\n\
[Ps, Pd, Pv] = free_durden(hhhh,vvvv,hvhv,hhvv)\n\
[H, A, alpha]  = cloude_pot(t11,t22,t33,t12,t13,t23,0) or\n\
[H, A, alpha]  = cloude_pot(hhhh,vvvv,hvhv,hhhv,hhvv,hvvv,1) \n\
\n");

// Freeman-Durden 3-component Decomposition (ref: Freeman and Durden, 1998) 
PyDoc_STRVAR(free_durden__doc__,
"\nFreeman-Durden 3-component Decomposition\n\n\
Usage::\n\
\n\
   [Ps, Pd, Pv] = free_durden(hhhh,vvvv,hvhv,hhvv)\n\
\n\
Parameters\n\
----------\n\
hhhh  :  1d numpy array; float\n\
         horizontal co-polarized power\n\
vvvv  :  1d numpy array; float\n\
         vertical co-polarized power\n\
hvhv  :  1d numpy array; float\n\
         cross-polarized power\n\
hhvv  :  1d numpy array; complex\n\
         co-polarized cross product\n\
\n\
Outputs\n\
-------\n\
Ps    :  1d numpy array; float\n\
         surface-scattered power\n\
Pd    :  1d numpy array; float\n\
         double-bounce power\n\
Pv    :  1d numpy array; float\n\
         volume-scattered power\n\
\n\
Notes\n\
-----\n\
* Outputs are given in a single array with values appended in the order described above\n\
\n");

/**************************************************************************************/

static PyObject *free_durden(PyObject *self, PyObject *args) {

   PyArrayObject *in_hhhh, *in_vvvv, *in_hvhv, *in_hhvv, *output;
   problem p;

   if (!PyArg_ParseTuple(args, "O!O!O!O!i", &PyArray_Type, &in_hhhh, &PyArray_Type, &in_vvvv,
            &PyArray_Type, &in_hvhv, &PyArray_Type, &in_hhvv, &p.numthrd))
      return NULL;

   npy_intp n  = in_hhhh->dimensions[0];
   npy_intp tn = 3*n;
   p.len = (int) n;
    
   // create C array
   output = (PyArrayObject *) PyArray_EMPTY(1, &tn, NPY_FLOAT32, 0);

   p.hhhh = (float *) in_hhhh->data;
   p.vvvv = (float *) in_vvvv->data;
   p.hvhv = (float *) in_hvhv->data;
   p.hhvv = (std::complex<float> *) in_hhvv->data;
   p.out  = (float *) output->data;
  
   Py_BEGIN_ALLOW_THREADS;
 
   spawn_fd_workers(&p);

   Py_END_ALLOW_THREADS;

   return PyArray_Return(output);
}

/*=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=*/
PyDoc_STRVAR(cloude_pot__doc__,
"\nCloude-Pottier H/A/alpha Decomposition\n\n\
Usage::\n\
\n\
   [H, A, alpha] = cloude_pot(t11,t22,t33,t12,t13,t23,0) \n\
or \n\
   [H, A, alpha] = cloude_pot(hhhh,vvvv,hvhv,hhhv,hhvv,hvvv,1) \n\
\n\
Parameters\n\
----------\n\
t11   :  1d numpy array; float\n\
         |HH + VV|^2 Pauli surface scattering parameter\n\
t22   :  1d numpy array; float\n\
         |HH - VV|^2 Pauli double-bounce parameter\n\
t33   :  1d numpy array; float\n\
         4|HV|^2 cross-polarized power\n\
t12   :  1d numpy array; complex\n\
         (HH + VV)(HH - VV)*\n\
t13   :  1d numpy array; complex\n\
         2HV(HH + VV)*\n\
t23   :  1d numpy array; complex\n\
         2HV(HH - VV)*\n\
\n\
hhhh  :  1d numpy array; float\n\
         horizontal co-polarized power\n\
vvvv  :  1d numpy array; float\n\
         vertical co-polarized power\n\
hvhv  :  1d numpy array; float\n\
         cross-polarized power\n\
hhhv  :  1d numpy array; complex\n\
         cross product\n\
hhvv  :  1d numpy array; complex\n\
         co-polarized cross product\n\
hvvv  :  1d numpy array; complex\n\
         cross product\n\
\n\
Outputs\n\
-------\n\
H     :  1d numpy array; float\n\
         entropy\n\
A     :  1d numpy array; float\n\
         anisotropy\n\
alpha :  1d numpy array; float\n\
         alpha\n\
\n\
Notes\n\
-----\n\
* Outputs are given in a single array with values appended in the order described above\n\
\n");

/**************************************************************************************/
static PyObject *cloude_pot(PyObject *self, PyObject *args) {

   PyArrayObject *in_hhhh, *in_vvvv, *in_hvhv, *in_hhhv, *in_hhvv, *in_hvvv, *output;
   problem p;

   if (!PyArg_ParseTuple(args, "O!O!O!O!O!O!ii", &PyArray_Type, &in_hhhh, &PyArray_Type, &in_vvvv,
            &PyArray_Type, &in_hvhv, &PyArray_Type, &in_hhhv, &PyArray_Type, &in_hhvv, 
            &PyArray_Type, &in_hvvv, &p.matform, &p.numthrd))
      return NULL;

   npy_intp n  = in_hhhh->dimensions[0];
   npy_intp tn = 3*n;
   p.len = (int) n;

   // create C array
   output = (PyArrayObject *) PyArray_EMPTY(1, &tn, NPY_FLOAT32, 0);

   p.hhhh = (float *) in_hhhh->data;
   p.vvvv = (float *) in_vvvv->data;
   p.hvhv = (float *) in_hvhv->data;
   p.hhhv = (std::complex<float> *) in_hhhv->data;
   p.hhvv = (std::complex<float> *) in_hhvv->data;
   p.hvvv = (std::complex<float> *) in_hvvv->data;
   p.out  = (float *) output->data;

   Py_BEGIN_ALLOW_THREADS;

   spawn_haalp_workers(&p);

   Py_END_ALLOW_THREADS;

   return PyArray_Return(output);
}



/*=====================================================================================*/
static PyMethodDef decomp_modc_methods[] = {
   {"free_durden", (PyCFunction) free_durden, METH_VARARGS | METH_KEYWORDS, free_durden__doc__},
   {"cloude_pot", (PyCFunction) cloude_pot, METH_VARARGS | METH_KEYWORDS, cloude_pot__doc__},
   {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC init_decomp_modc(void) {
   (void) Py_InitModule3("_decomp_modc", decomp_modc_methods, decomp_modc__doc__);
   import_array();
};












