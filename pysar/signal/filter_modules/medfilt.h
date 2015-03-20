/*


*/
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <algorithm>
#include <vector>
#include <pthread.h>
#include <cmath>
#include <limits>

#ifndef STRUCT_MEDFILT_PROBLEM
#define STRUCT_MEDFILT_PROBLEM
struct problem {
      int cols, lines, azwindow, rgwindow;
      int azwhalf, rgwhalf, winsize, numthrd, rank, size;
      long arrsz;
      float null;

      float *image;
      float *outarr;

      double *d_image;
      double *d_outarr;

      pthread_mutex_t lock;
   };  
#endif

#ifndef STRUCT_MEDFILT_SPECIFIC
#define STRUCT_MEDFILT_SPECIFIC
struct specific {
      int id, brick;
      int begline, endline;
      int begcol, endcol;
      pthread_t descriptor;
      problem* pr;
   };
#endif

#ifndef FUNC_MED2D
#define FUNC_MED2D
void* f_medfilter2d(void* arg);
#endif

#ifndef FUNC_DMED2D
#define FUNC_DMED2D
void* d_medfilter2d(void* arg);
#endif

#ifndef FUNC_MEDFILT_SPAWN_WORKERS
#define FUNC_MEDFILT_SPAWN_WORKERS
void spawn_medfilt_workers(struct problem *p,int precision);
#endif
