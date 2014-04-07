/*


*/
#include <complex>
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <algorithm>
#include <vector>
#include <pthread.h>

#ifndef STRUCT_CONEFILT_PROBLEM
#define STRUCT_CONEFILT_PROBLEM
struct problem {
      int cols, lines;
      int numthrd, rank, size;
      long arrsz;

      float dx, dy, null;
      float *win;
      float *image;
      float *temp;
      float *out;

      double ddx, ddy, dnull;
      double *dimage;
      double *dtemp;
      double *dout;

      pthread_mutex_t lock;
   };  
#endif

#ifndef STRUCT_CONEFILT_SPECIFIC
#define STRUCT_CONEFILT_SPECIFIC
struct specific {
      int id, brick;
      int begline, endline;
      int begcol, endcol;
      pthread_t descriptor;
      problem* pr;
   };
#endif

#ifndef FUNC_CONE2D
#define FUNC_CONE2D
void* f_cone2d(void* arg);
#endif

#ifndef FUNC_CONEFILT_SPAWN_WORKERS
#define FUNC_CONEFILT_SPAWN_WORKERS
void spawn_conefilt_workers(struct problem *p);
#endif
