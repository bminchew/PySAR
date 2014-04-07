/*


*/
#include <complex>
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <algorithm>
#include <vector>
#include "Eigen/Dense"
#include <pthread.h>

#ifndef STRUCT_FD_PROBLEM
#define STRUCT_FD_PROBLEM
struct problem {
   // inputs and properties
   int numthrd, len, matform;
   float *hhhh;
   float *vvvv;
   float *hvhv;
   std::complex<float> *hhhv;
   std::complex<float> *hhvv;
   std::complex<float> *hvvv;
   // outputs
   float *out;

   pthread_mutex_t lock;
   };  
#endif

#ifndef STRUCT_FD_SPECIFIC
#define STRUCT_FD_SPECIFIC
struct specific {
   int id, brick;
   int begind, endind;
   pthread_t descriptor;
   problem* pr; 
   };  
#endif

#ifndef FUNC_FREE_DURDEN_SOLVER
#define FUNC_FREE_DURDEN_SOLVER
void free_durden_solver(float *hhhh, float *vvvv, float *hvhv,
      std::complex<float> *hhvv, float *out, int len, int numthrd);
#endif

#ifndef FUNC_FREEDURD
#define FUNC_FREEDURD
void* freedurd(void* arg);
#endif

#ifndef FUNC_FD_SPAWN_WORKERS
#define FUNC_FD_SPAWN_WORKERS
void spawn_fd_workers(struct problem *p);
#endif

#ifndef FUNC_HAALPHA
#define FUNC_HAALPHA
void* haalpha(void* arg);
#endif

#ifndef FUNC_HAALP_SPAWN_WORKERS
#define FUNC_HAALP_SPAWN_WORKERS
void spawn_haalp_workers(struct problem *p);
#endif

