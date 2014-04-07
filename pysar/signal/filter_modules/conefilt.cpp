#include "conefilt.h"
/************************************************************************************/

/*=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-*/
void* f_cone2d(void* arg) {
   specific* s = (specific *) arg;
   int cols = s->pr->cols;
   int lines = s->pr->lines;
   int left,right,top,bot,xwin,ywin,nonnull;
   float dx = s->pr->dx;
   float dy = s->pr->dy;
   float win,dist,xd,yd;
   double img,weight,sum,wtsum;

   for (int i = s->begline; i <= s->endline; ++i) {
      for (int j = 0; j < cols; ++j) {
         win = s->pr->win[i*cols+j];
         xwin = (int) (1. + 0.5*win/dx);
         ywin = (int) (1. + 0.5*win/dy);

         left = j - xwin;
         if (left < 0) { left = 0; }
         right = j + xwin;
         if (right >= cols) {right = cols - 1;}
         
         top = i - ywin;
         if (top < 0) { top = 0; }
         bot = i + ywin;
         if (bot >= lines) {bot = lines - 1;}      

         sum = 0.; 
         wtsum = 0.;
         nonnull = 0;
         for (int y = top; y <= bot; ++y) {
            yd = std::abs(y-i)*dy;
            for (int x = left; x <= right; ++x) {
               if (std::abs(s->pr->image[y*cols+x] - s->pr->null) > 1.e-7) {
                  nonnull = 1;
                  xd = std::abs(x-j)*dx;
                  dist = sqrt(xd*xd + yd*yd);
                  weight = (double) (1. - 2.*dist/win);
                  if (weight > 0.) {
                     img = (double) s->pr->image[y*cols+x];
                     sum += weight * img;    
                     wtsum += weight;
                  }
               }
            }
         }
         if (nonnull == 0) { 
            s->pr->out[i*cols+j] = s->pr->null; 
         } else {
            s->pr->out[i*cols+j] = (float) (sum/wtsum);
         }
      }
   }
}

/*=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-*/
void spawn_conefilt_workers(struct problem *p) {
   if (p->numthrd < 1) { p->numthrd = 1; }
   long brick = p->lines / p->numthrd;
  
   specific spc[p->numthrd];
   pthread_t threads[p->numthrd];
   pthread_mutex_init(&p->lock,0);

   for (int tid=0; tid < p->numthrd; ++tid ) { 
      spc[tid].id = tid;
      spc[tid].pr = p;
      spc[tid].brick = brick;
      spc[tid].begline = tid*brick;
      spc[tid].endline = (tid+1)*brick;
      if ( tid == p->numthrd - 1) { spc[tid].endline = p->lines - 1; }
      int status = pthread_create(&(spc[tid].descriptor),NULL, f_cone2d, &spc[tid]);
         if (status) { printf("error %d in pthread_create\n\n",status); }
   }   

   int rc; 
   for (int tid=0; tid < p->numthrd; ++tid ) { 
      rc = pthread_join(spc[tid].descriptor,NULL);
      assert(rc == 0); 
   }   
}   

/*=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-*/
 
