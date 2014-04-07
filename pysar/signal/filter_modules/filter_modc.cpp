
#include <Python.h>
#include <arrayobject.h>
#include <assert.h>
#include <pthread.h>

PyMODINIT_FUNC init_filter_modc(void);

PyDoc_STRVAR(filter_modc__doc__,
"\nA collection of filters\n\n\
Filters\n\
-------\n\
filt = boxfilter1d(input,window)             -->  1D boxcar moving average filter\n\
filt = boxfilter2d(input,window0,window1)    -->  2D boxcar moving average filter\n\n");

// 1D boxcar 
PyDoc_STRVAR(boxfilter1d__doc__,
"\n1D boxcar moving average filter\n\n\
Usage:  output = boxfilter1d(input,window)\n\
\n\
Parameters\n\
----------\n\
input  :    1d array, float\n\
            Data to be filtered in a 1D array\n\
window :    int\n\
            Filter window size in number of samples\n\
\n\
Output\n\
------\n\
output :    1d array, float\n\
            Filtered data; same size and shape as input\n\n");


//******************************************************************************************
struct problem {
      int cols, lines, azwindow, rgwindow;
      int azwhalf, rgwhalf, numthrd, rank, size;
      long arrsz;

      float *image;
      float *temp;
      float *out;

      double *dimage;
      double *dtemp;
      double *dout;

      pthread_mutex_t lock;
   };  

struct specific {
      int id, brick;
      int begline, endline;
      int begcol, endcol;
      pthread_t descriptor;
      problem* pr; 
   };  
//*****************************************************************************************




static PyObject *boxfilter1d(PyObject *self, PyObject *args) {

   PyArrayObject *in_array, *out_array;
   int wind;
   double sum, scale;

   // Get tuple of arguments
   if (!PyArg_ParseTuple(args, "O!i", &PyArray_Type, &in_array, &wind))
      return NULL;

   npy_intp n = in_array->dimensions[0];
   npy_intp m = in_array->dimensions[1]; 
   
   if (m > n) { n = m; }

   // create C arrays
   out_array = (PyArrayObject *) PyArray_EMPTY(1, &n, NPY_FLOAT, 0);
   float *in = (float *) in_array->data;
   float *out = (float *) out_array->data;

   // filter
   wind *= 0.5;
   scale = 1.0f/ (2.*wind+1.);
   // left edge
   sum = in[0] * wind;
   for (int j = 0; j < wind+1; ++j) {
      sum += in[j];
   }   
   out[0] = sum * scale;

   for (int j = 1; j < wind+1; ++j) {
      sum += in[j+wind];
      sum -= in[0];
      out[j] = sum * scale;
   }   

   // body
   for (int j = wind+1; j < n-wind; ++j) {
      sum += in[j+wind];
      sum -= in[j-wind-1];
      out[j] = sum * scale;
   }   

   // right edge
   for (int j = n-wind; j < n; ++j) {
      sum += in[n-1];
      sum -= in[j-wind-1];
      out[j] = sum * scale;
   }   


   return PyArray_Return(out_array); 
}


/*========================*/   
  
PyDoc_STRVAR(d_boxfilter1d__doc__,
             "\n1D boxcar moving average filter (double precision)\n\n\
             Usage:  output = d_boxfilter1d(input,window)\n\
             \n\
             Parameters\n\
             ----------\n\
             input  :    1d array, double\n\
             Data to be filtered in a 1D array\n\
             window :    int\n\
             Filter window size in number of samples\n\
             \n\
             Output\n\
             ------\n\
             output :    1d array, double\n\
             Filtered data; same size and shape as input\n\n");

static PyObject *d_boxfilter1d(PyObject *self, PyObject *args) {
    
    PyArrayObject *in_array, *out_array;
    int wind;
    double sum, scale;
    
    // Get tuple of arguments
    if (!PyArg_ParseTuple(args, "O!i", &PyArray_Type, &in_array, &wind))
        return NULL;
    
    npy_intp n = in_array->dimensions[0];
    npy_intp m = in_array->dimensions[1];
    
    if (m > n) { n = m; }
    
    // create C arrays
    out_array = (PyArrayObject *) PyArray_EMPTY(1, &n, NPY_FLOAT64, 0);
    double *in = (double *) in_array->data;
    double *out = (double *) out_array->data;
   
    // filter
    wind *= 0.5;
    scale = 1.0/ (2.*wind+1.);
    // left edge
    sum = in[0] * wind;
    for (int j = 0; j < wind+1; ++j) {
        sum += in[j];
    }
    out[0] = sum * scale;
    
    for (int j = 1; j < wind+1; ++j) {
        sum += in[j+wind];
        sum -= in[0];
        out[j] = sum * scale;
    }
    
    // body
    for (int j = wind+1; j < n-wind; ++j) {
        sum += in[j+wind];
        sum -= in[j-wind-1];
        out[j] = sum * scale;
    }   
    
    // right edge
    for (int j = n-wind; j < n; ++j) {
        sum += in[n-1];
        sum -= in[j-wind-1];
        out[j] = sum * scale;
    }   
    
    return PyArray_Return(out_array); 
}



/*=====================================================================================*/

// 2d boxcar 

PyDoc_STRVAR(boxfilter2d__doc__,
"\n2D boxcar moving average filter\n\n\
Usage:  output = boxfilter2d(input,width,window0,window1)\n\
\n\
Parameters\n\
----------\n\
input   :   1d array, float\n\
            Data to be filtered passed as a 1D array\n\
width   :   int\n\
            Number of columns in original 2D data array\n\
window0 :   int\n\
            Filter window size along rows [samples]\n\
window1 :   int\n\
            Filter window size down columns [samples]\n\
\n\
Output\n\
------\n\
output :    1d array, float\n\
            Filtered data; same size and shape as input\n\n");

static PyObject *boxfilter2d(PyObject *self, PyObject *args) {

   PyArrayObject *in_array, *out_array, *temp_array;
   int wind0, wind1, wind, rows, cols, icols, rcols, ind;
   double sum, scale;

   // Get tuple of arguments
   if (!PyArg_ParseTuple(args, "O!iii", &PyArray_Type, &in_array, &cols, &wind0, &wind1))
      return NULL;

   npy_intp n = in_array->dimensions[0];
   rows = n/cols;

   // create C arrays
   temp_array = (PyArrayObject *) PyArray_EMPTY(1, &n, NPY_FLOAT, 0); 
   out_array = (PyArrayObject *) PyArray_EMPTY(1, &n, NPY_FLOAT, 0);
   float *in   = (float *) in_array->data;
   float *out  = (float *) out_array->data;
   float *temp = (float *) temp_array->data;

   // filter along x
   wind = 0.5*wind0;
   scale = 1.0/ (2.*wind+1.);

   for (int i = 0; i < rows; ++i) {
      //printf("i/rows = %d/%d \n",i,rows);
      icols = i*cols;
      // left edge
      sum = in[icols] * wind;
      for (int j = 0; j < wind+1; ++j) {
         sum += in[icols+j];
      }   
      temp[icols] = sum * scale;

      for (int j = 1; j < wind+1; ++j) {
         ind = icols+j;
         sum += in[ind+wind];
         sum -= in[icols];
         temp[ind] = sum * scale;
      }   

      // body
      for (int j = wind+1; j < cols-wind; ++j) {
         ind = icols+j;
         sum += in[ind+wind];
         sum -= in[ind-wind-1];
         temp[ind] = sum * scale;
      }   

      // right edge
      for (int j = cols-wind; j < cols; ++j) {
         ind = icols+j;
         sum += in[icols+cols-1];
         sum -= in[ind-wind-1];
         temp[ind] = sum * scale;
      }   
   }   

   // filter along y
   wind = 0.5*wind1;
   scale = 1.0/ (2.*wind+1.);
   rcols = wind*cols;

   for (int j = 0; j < cols; ++j) {
      // top edge
      sum = temp[j] * wind;
      for (int i = 0; i <= wind; ++i) {
         sum += temp[i*cols+j];
      }
      out[j] = sum * scale;

      for (int i = 1; i <= wind; ++i) {
         ind = i*cols+j;
         sum += temp[ind+rcols];
         sum -= temp[j];
         out[ind] = sum * scale;
      }

      // body
      for (int i = wind+1; i < rows-wind; ++i) {
         ind = i*cols+j;
         sum += temp[ind+rcols];
         sum -= temp[ind-rcols-cols];
         out[ind] = sum * scale;
      }

      // bottom edge
      for (int i = rows-wind; i < rows; ++i) {
         ind = i*cols+j;
         sum += temp[(rows-1)*cols+j];
         sum -= temp[ind-rcols-cols];
         out[ind] = sum * scale;
      }
   }

   return PyArray_Return(out_array);
}



/*=======================*/

PyDoc_STRVAR(d_boxfilter2d__doc__,
             "\n2D boxcar moving average filter (double precision)\n\n\
             Usage:  output = d_boxfilter2d(input,width,window0,window1)\n\
             \n\
             Parameters\n\
             ----------\n\
             input   :   1d array, double \n\
             Data to be filtered passed as a 1D array\n\
             width   :   int\n\
             Number of columns in original 2D data array\n\
             window0 :   int\n\
             Filter window size along rows [samples]\n\
             window1 :   int\n\
             Filter window size down columns [samples]\n\
             \n\
             Output\n\
             ------\n\
             output :    1d array, double \n\
             Filtered data; same size and shape as input\n\n");

static PyObject *d_boxfilter2d(PyObject *self, PyObject *args) {
    
    PyArrayObject *in_array, *out_array, *temp_array;
    int wind0, wind1, wind, rows, cols, icols, rcols, ind;
    double sum, scale;
    
    // Get tuple of arguments
    if (!PyArg_ParseTuple(args, "O!iii", &PyArray_Type, &in_array, &cols, &wind0, &wind1))
        return NULL;
    
    npy_intp n = in_array->dimensions[0];
    rows = n/cols;
    
    // create C arrays
    temp_array = (PyArrayObject *) PyArray_EMPTY(1, &n, NPY_FLOAT64, 0);
    out_array = (PyArrayObject *) PyArray_EMPTY(1, &n, NPY_FLOAT64, 0);
    double *in   = (double *) in_array->data;
    double *out  = (double *) out_array->data;
    double *temp = (double *) temp_array->data;
    
    // filter along x
    wind = 0.5*wind0;
    scale = 1.0/ (2.*wind+1.);
    
    for (int i = 0; i < rows; ++i) {
        icols = i*cols;
        // left edge
        sum = in[icols] * wind;
        for (int j = 0; j < wind+1; ++j) {
            sum += in[icols+j];
        }
        temp[icols] = sum * scale;
        
        for (int j = 1; j < wind+1; ++j) {
            ind = icols+j;
            sum += in[ind+wind];
            sum -= in[icols];
            temp[ind] = sum * scale;
        }
        
        // body
        for (int j = wind+1; j < cols-wind; ++j) {
            ind = icols+j;
            sum += in[ind+wind];
            sum -= in[ind-wind-1];
            temp[ind] = sum * scale;
        }
        
        // right edge
        for (int j = cols-wind; j < cols; ++j) {
            ind = icols+j;
            sum += in[icols+cols-1];
            sum -= in[ind-wind-1];
            temp[ind] = sum * scale;
        }
    }
    
    // filter along y
    wind = 0.5*wind1;
    scale = 1.0/ (2.*wind+1.);
    rcols = wind*cols;
    
    for (int j = 0; j < cols; ++j) {
        // top edge
        sum = temp[j] * wind;
        for (int i = 0; i <= wind; ++i) {
            sum += temp[i*cols+j];
        }
        out[j] = sum * scale;
        
        for (int i = 1; i <= wind; ++i) {
            ind = i*cols+j;
            sum += temp[ind+rcols];
            sum -= temp[j];
            out[ind] = sum * scale;
        }
        
        // body
        for (int i = wind+1; i < rows-wind; ++i) {
            ind = i*cols+j;
            sum += temp[ind+rcols];
            sum -= temp[ind-rcols-cols];
            out[ind] = sum * scale;
        }
        
        // bottom edge
        for (int i = rows-wind; i < rows; ++i) {
            ind = i*cols+j;
            sum += temp[(rows-1)*cols+j];
            sum -= temp[ind-rcols-cols];
            out[ind] = sum * scale;
        }
    }
    
    return PyArray_Return(out_array);
}


/*=====================================*/

PyDoc_STRVAR(tr_boxfilter2d__doc__,
             "\n2D boxcar moving average filter (threaded)\n\n\
             Usage:  output = d_boxfilter2d(input,width,window0,window1,numthrd)\n\
             \n\
             Parameters\n\
             ----------\n\
             input   :   1d array, float \n\
             Data to be filtered passed as a 1D array\n\
             width   :   int\n\
             Number of columns in original 2D data array\n\
             window0 :   int\n\
             Filter window size along rows [samples]\n\
             window1 :   int\n\
             Filter window size down columns [samples]\n\
             numthrd :   int\n\
             Number of threads\n\
             \n\
             Output\n\
             ------\n\
             output :    1d array, float \n\
             Filtered data; same size and shape as input\n\n");


// filtering routines 
void* boxfilter_x(void* arg) {
   specific* s = (specific *) arg;
   int cols = s->pr->cols;
   int lines = s->pr->lines;
   int rgwhalf = s->pr->rgwhalf;
   long ind, icols;
   double scale = 1.0 / (2.*rgwhalf+1.);
   double sum;

   for (int i = s->begline; i <= s->endline; ++i) {
      icols = i*cols;
      // left edge
      sum = s->pr->image[icols] * rgwhalf;
      for (int j = 0; j < rgwhalf+1; ++j) {
         sum += s->pr->image[icols+j];
      }
      s->pr->temp[icols] = sum * scale;

      for (int j = 1; j < rgwhalf+1; ++j) {
         ind = icols+j;
         sum += s->pr->image[ind+rgwhalf];
         sum -= s->pr->image[icols];
         s->pr->temp[ind] = sum * scale;
      }

      // body
      for (int j = rgwhalf+1; j < cols-rgwhalf; ++j) {
         ind = icols+j;
         sum += s->pr->image[ind+rgwhalf];
         sum -= s->pr->image[ind-rgwhalf-1];
         s->pr->temp[ind] = sum * scale;
      }

      // right edge
      for (int j = cols-rgwhalf; j < cols; ++j) {
         ind = icols+j;
         sum += s->pr->image[icols+cols-1];
         sum -= s->pr->image[ind-rgwhalf-1];
         s->pr->temp[ind] = sum * scale;
      }
   }
}


void* boxfilter_y(void* arg) {

   specific* s = (specific *) arg;
   int cols = s->pr->cols;
   int lines = s->pr->lines;
   int azwhalf = s->pr->azwhalf;
   long ind;
   long rcols = azwhalf*cols;
   double scale = 1.0 / (2*azwhalf+1);
   double sum;

   for (int j = s->begcol; j <= s->endcol ; ++j) {
      // top edge
      sum = s->pr->temp[j] * azwhalf;
      for (int i = 0; i <= azwhalf; ++i) {
         sum += s->pr->temp[i*cols+j];
      }
      s->pr->out[j] = sum * scale;

      for (int i = 1; i <= azwhalf; ++i) {
         ind = i*cols+j;
         sum += s->pr->temp[ind+rcols];
         sum -= s->pr->temp[j];
         s->pr->out[ind] = sum * scale;
      }

      // body
      for (int i = azwhalf+1; i < lines-azwhalf; ++i) {
         ind = i*cols+j;
         sum += s->pr->temp[ind+rcols];
         sum -= s->pr->temp[ind-rcols-cols];
         s->pr->out[ind] = sum * scale;
      }

      // bottom edge
      for (int i = lines-azwhalf; i < lines; ++i) {
         ind = i*cols+j;
         sum += s->pr->temp[(lines-1)*cols+j];
         sum -= s->pr->temp[ind-rcols-cols];
         s->pr->out[ind] = sum * scale;
      }
   }
}

static PyObject *tr_boxfilter2d(PyObject *self, PyObject *args) {

   PyArrayObject *image_array, *out_array, *temp_array;
   problem p;

   if (!PyArg_ParseTuple(args, "O!iiii", &PyArray_Type, &image_array, &p.cols, 
            &p.azwindow, &p.rgwindow, &p.numthrd))
      return NULL;

   npy_intp n = image_array->dimensions[0];
   p.lines = n/p.cols;
   p.arrsz = p.cols*p.lines;

   // create C array
   out_array = (PyArrayObject *) PyArray_EMPTY(1, &n, NPY_FLOAT, 0); 
   temp_array = (PyArrayObject *) PyArray_EMPTY(1, &n, NPY_FLOAT, 0); 
   p.image = (float *) image_array->data;
   p.temp  = (float *) temp_array->data;
   p.out   = (float *) out_array->data;

   if (p.numthrd < 1) { p.numthrd = 1; }
   p.rgwhalf = (int) p.rgwindow/2;
   p.azwhalf = (int) p.azwindow/2;

   // set up threads 
   int brick = p.lines / p.numthrd ;
   if ( brick < 1 ) { brick = 1; }
   if ( brick < p.azwhalf+p.rgwhalf ) {// no sense spawning threads on small blocks
      brick = p.azwhalf+p.rgwhalf;
      if (p.lines < p.cols ) {
         p.numthrd = p.lines / brick;
      } else {
         p.numthrd = p.cols / brick;
      }
   }

   // split up into threads
   specific spc[p.numthrd];
   pthread_t threads[p.numthrd];
   pthread_mutex_init(&p.lock,0);

   for (int tid=0; tid < p.numthrd; tid++ ) {   
      spc[tid].id = tid;
      spc[tid].pr = &p; 
      spc[tid].brick = brick;
      spc[tid].begline = tid*brick;
      spc[tid].endline = (tid+1)*brick - 1;
      if ( tid == p.numthrd - 1) { spc[tid].endline = p.lines-1; }
      int status = pthread_create(&(spc[tid].descriptor),NULL,boxfilter_x,&spc[tid]);
         if (status) {  printf("error %d in pthread_create\n\n",status);  }
   }

   int rc;
   for (int tid=0;tid<p.numthrd;tid++) {
      rc = pthread_join(spc[tid].descriptor,NULL);
      assert(0 == rc);
   }

   brick = p.cols / p.numthrd;
   for (int tid=0;tid<p.numthrd;tid++) {
      spc[tid].brick = brick;
      spc[tid].begcol = tid*brick;
      spc[tid].endcol = (tid+1)*brick - 1;
      if ( tid == p.numthrd - 1) { spc[tid].endcol = p.cols-1; }
      int status = pthread_create(&(spc[tid].descriptor),NULL,boxfilter_y,&spc[tid]);
         if (status) {  printf("error %d in pthread_create\n\n",status);  }
   }

   for (int tid=0;tid<p.numthrd;tid++) {
      rc = pthread_join(spc[tid].descriptor,NULL); 
      assert(0 == rc);
   }

   return PyArray_Return(out_array);
}


/*=====================================*/

PyDoc_STRVAR(dtr_boxfilter2d__doc__,
             "\n2D boxcar moving average filter (threaded, double precision)\n\n\
             Usage:  output = d_boxfilter2d(input,width,window0,window1,numthrd)\n\
             \n\
             Parameters\n\
             ----------\n\
             input   :   1d array, double \n\
             Data to be filtered passed as a 1D array\n\
             width   :   int\n\
             Number of columns in original 2D data array\n\
             window0 :   int\n\
             Filter window size along rows [samples]\n\
             window1 :   int\n\
             Filter window size down columns [samples]\n\
             numthrd :   int\n\
             Number of threads\n\
             \n\
             Output\n\
             ------\n\
             output :    1d array, double \n\
             Filtered data; same size and shape as input\n\n");


// filtering routines 
void* d_boxfilter_x(void* arg) {
   specific* s = (specific *) arg;
   int cols = s->pr->cols;
   int lines = s->pr->lines;
   int rgwhalf = s->pr->rgwhalf;
   long ind, icols;
   double scale = 1.0 / (2.*rgwhalf+1.);
   double sum;

   for (int i = s->begline; i <= s->endline; ++i) {
      icols = i*cols;
      // left edge
      sum = s->pr->dimage[icols] * rgwhalf;
      for (int j = 0; j < rgwhalf+1; ++j) {
         sum += s->pr->dimage[icols+j];
      }
      s->pr->dtemp[icols] = sum * scale;

      for (int j = 1; j < rgwhalf+1; ++j) {
         ind = icols+j;
         sum += s->pr->dimage[ind+rgwhalf];
         sum -= s->pr->dimage[icols];
         s->pr->dtemp[ind] = sum * scale;
      }

      // body
      for (int j = rgwhalf+1; j < cols-rgwhalf; ++j) {
         ind = icols+j;
         sum += s->pr->dimage[ind+rgwhalf];
         sum -= s->pr->dimage[ind-rgwhalf-1];
         s->pr->dtemp[ind] = sum * scale;
      }

      // right edge
      for (int j = cols-rgwhalf; j < cols; ++j) {
         ind = icols+j;
         sum += s->pr->dimage[icols+cols-1];
         sum -= s->pr->dimage[ind-rgwhalf-1];
         s->pr->dtemp[ind] = sum * scale;
      }
   }
}


void* d_boxfilter_y(void* arg) {

   specific* s = (specific *) arg;
   int cols = s->pr->cols;
   int lines = s->pr->lines;
   int azwhalf = s->pr->azwhalf;
   long ind;
   long rcols = azwhalf*cols;
   double scale = 1.0 / (2*azwhalf+1);
   double sum;

   for (int j = s->begcol; j <= s->endcol ; ++j) {
      // top edge
      sum = s->pr->dtemp[j] * azwhalf;
      for (int i = 0; i <= azwhalf; ++i) {
         sum += s->pr->dtemp[i*cols+j];
      }
      s->pr->dout[j] = sum * scale;

      for (int i = 1; i <= azwhalf; ++i) {
         ind = i*cols+j;
         sum += s->pr->dtemp[ind+rcols];
         sum -= s->pr->dtemp[j];
         s->pr->dout[ind] = sum * scale;
      }

      // body
      for (int i = azwhalf+1; i < lines-azwhalf; ++i) {
         ind = i*cols+j;
         sum += s->pr->dtemp[ind+rcols];
         sum -= s->pr->dtemp[ind-rcols-cols];
         s->pr->dout[ind] = sum * scale;
      }

      // bottom edge
      for (int i = lines-azwhalf; i < lines; ++i) {
         ind = i*cols+j;
         sum += s->pr->dtemp[(lines-1)*cols+j];
         sum -= s->pr->dtemp[ind-rcols-cols];
         s->pr->dout[ind] = sum * scale;
      }
   }
}

static PyObject *dtr_boxfilter2d(PyObject *self, PyObject *args) {

   PyArrayObject *image_array, *out_array, *temp_array;
   problem p;

   if (!PyArg_ParseTuple(args, "O!iiii", &PyArray_Type, &image_array, &p.cols, 
            &p.azwindow, &p.rgwindow, &p.numthrd))
      return NULL;

   npy_intp n = image_array->dimensions[0];
   p.lines = n/p.cols;
   p.arrsz = p.cols*p.lines;

   // create C array
   out_array = (PyArrayObject *) PyArray_EMPTY(1, &n, NPY_FLOAT64, 0); 
   temp_array = (PyArrayObject *) PyArray_EMPTY(1, &n, NPY_FLOAT64, 0); 
   p.dimage = (double *) image_array->data;
   p.dtemp  = (double *) temp_array->data;
   p.dout   = (double *) out_array->data;

   if (p.numthrd < 1) { p.numthrd = 1; }
   p.rgwhalf = (int) p.rgwindow/2;
   p.azwhalf = (int) p.azwindow/2;

   // set up threads 
   int brick = p.lines / p.numthrd ;
   if ( brick < 1 ) { brick = 1; }
   if ( brick < p.azwhalf+p.rgwhalf ) {// no sense spawning threads on small blocks
      brick = p.azwhalf+p.rgwhalf;
      if (p.lines < p.cols ) {
         p.numthrd = p.lines / brick;
      } else {
         p.numthrd = p.cols / brick;
      }
   }

   // split up into threads
   specific spc[p.numthrd];
   pthread_t threads[p.numthrd];
   pthread_mutex_init(&p.lock,0);

   for (int tid=0; tid < p.numthrd; tid++ ) {   
      spc[tid].id = tid;
      spc[tid].pr = &p; 
      spc[tid].brick = brick;
      spc[tid].begline = tid*brick;
      spc[tid].endline = (tid+1)*brick - 1;
      if ( tid == p.numthrd - 1) { spc[tid].endline = p.lines-1; }
      int status = pthread_create(&(spc[tid].descriptor),NULL,d_boxfilter_x,&spc[tid]);
         if (status) {  printf("error %d in pthread_create\n\n",status);  }
   }

   int rc;
   for (int tid=0;tid<p.numthrd;tid++) {
      rc = pthread_join(spc[tid].descriptor,NULL);
      assert(0 == rc);
   }

   brick = p.cols / p.numthrd;
   for (int tid=0;tid<p.numthrd;tid++) {
      spc[tid].brick = brick;
      spc[tid].begcol = tid*brick;
      spc[tid].endcol = (tid+1)*brick - 1;
      if ( tid == p.numthrd - 1) { spc[tid].endcol = p.cols-1; }
      int status = pthread_create(&(spc[tid].descriptor),NULL,d_boxfilter_y,&spc[tid]);
         if (status) {  printf("error %d in pthread_create\n\n",status);  }
   }

   for (int tid=0;tid<p.numthrd;tid++) {
      rc = pthread_join(spc[tid].descriptor,NULL); 
      assert(0 == rc);
   }

   return PyArray_Return(out_array);
}





/*=====================================================================================*/
static PyMethodDef filter_modc_methods[] = {
   {"boxfilter2d", (PyCFunction) boxfilter2d, METH_VARARGS | METH_KEYWORDS, boxfilter2d__doc__},
   {"boxfilter1d", (PyCFunction) boxfilter1d, METH_VARARGS | METH_KEYWORDS, boxfilter1d__doc__},
   {"d_boxfilter1d", (PyCFunction) d_boxfilter1d, METH_VARARGS | METH_KEYWORDS,
         d_boxfilter1d__doc__},
   {"d_boxfilter2d", (PyCFunction) d_boxfilter2d, METH_VARARGS | METH_KEYWORDS, d_boxfilter2d__doc__},
   {"tr_boxfilter2d", (PyCFunction) tr_boxfilter2d, METH_VARARGS | METH_KEYWORDS, 
         tr_boxfilter2d__doc__},
   {"dtr_boxfilter2d", (PyCFunction) dtr_boxfilter2d, METH_VARARGS | METH_KEYWORDS, 
         dtr_boxfilter2d__doc__},
      {NULL, NULL, 0, NULL} 
};

PyMODINIT_FUNC init_filter_modc(void) {
   (void) Py_InitModule3("_filter_modc", filter_modc_methods, filter_modc__doc__);
   import_array();
};

 
