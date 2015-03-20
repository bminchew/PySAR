#include "medfilt.h"
/************************************************************************************/

/*=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-*/
void* f_medfilter2d(void* arg) {
   specific* s = (specific *) arg;
   long rgwhalf = (long) s->pr->rgwhalf;
   long azwhalf = (long) s->pr->azwhalf;
   long winsize = (long) s->pr->winsize;
   long left, right, top, bot;
   long cols = (long) s->pr->cols;
   long lines = (long) s->pr->lines;
   long ind, k, kh, ind0, indf;
   long zero = 0;
   float curval, outval;
   float null = s->pr->null;
   float eps = std::numeric_limits<float>::epsilon();
   std::vector<float> chip;
   chip.resize(winsize);

   for (long i = s->begline; i <= s->endline; ++i) {
      top = std::max(zero,i-azwhalf);
      bot = std::min(lines-1,i+azwhalf);
      for (long j = 0; j < cols; ++j) {
         left  = std::max(zero,j-rgwhalf);
         right = std::min(cols-1,j+rgwhalf);
         k = 0;
         for (long p = top; p <= bot; ++p) {
            for (long q = left; q <= right; ++q) {
                ind = p*cols + q;
                curval = s->pr->image[ind];
                if (std::abs(curval-null) > eps && std::isfinite(curval)) {
                    chip[k] = curval;
                    ++k;
                }
            }
         }
         kh = k/2;
         if (k == 0) {
            if (std::isfinite(null)) {
                outval = null;
            } else {
                outval = -9999.;
            }
         } else if (k == 1) {
            outval = chip[0];
         } else if (k % 2 == 0) {
            std::partial_sort(chip.begin(),chip.begin()+kh,chip.begin()+k);
            outval = 0.5*(chip[kh-1]+chip[kh]);
         } else {
            std::nth_element(chip.begin(),chip.begin()+kh,chip.begin()+k);
            outval = chip[kh];
         }
         s->pr->outarr[i*cols+j] = outval;
      }
   }
}
/*=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-*/

void* d_medfilter2d(void* arg) {
   specific* s = (specific *) arg;
   long rgwhalf = (long) s->pr->rgwhalf;
   long azwhalf = (long) s->pr->azwhalf;
   long winsize = (long) s->pr->winsize;
   long left, right, top, bot;
   long cols = (long) s->pr->cols;
   long lines = (long) s->pr->lines;
   long ind, k, kh, ind0, indf;
   long zero = 0;
   double curval, outval;
   double null = s->pr->null;
   double eps = std::numeric_limits<double>::epsilon();
   std::vector<double> chip;
   chip.resize(winsize);

   for (long i = s->begline; i <= s->endline; ++i) {
      top = std::max(zero,i-azwhalf);
      bot = std::min(lines-1,i+azwhalf);
      for (long j = 0; j < cols; ++j) {
         left  = std::max(zero,j-rgwhalf);
         right = std::min(cols-1,j+rgwhalf);
         k = 0;
         for (long p = top; p <= bot; ++p) {
            for (long q = left; q <= right; ++q) {
                ind = p*cols + q;
                curval = s->pr->d_image[ind];
                if (std::abs(curval-null) > eps && std::isfinite(curval)) {
                    chip[k] = curval;
                    ++k;
                }
            }
         }
         kh = k/2;
         if (k == 0) {
            if (std::isfinite(null)) {
                outval = null;
            } else {
                outval = -9999.;
            }
         } else if (k == 1) {
            outval = chip[0];
         } else if (k % 2 == 0) {
            std::partial_sort(chip.begin(),chip.begin()+kh,chip.begin()+k);
            outval = 0.5*(chip[kh-1]+chip[kh]);
         } else {
            std::nth_element(chip.begin(),chip.begin()+kh,chip.begin()+k);
            outval = chip[kh];
         }
         s->pr->d_outarr[i*cols+j] = outval;
      }
   }
}
/*=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-*/
void spawn_medfilt_workers(struct problem *p,int precision) {
   if (p->numthrd < 1) { p->numthrd = 1; }
   long brick = p->lines / p->numthrd;
   if ( brick < 1 ) { brick = 1; }
   if ( brick < p->azwhalf+p->rgwhalf ) {// no sense spawning threads on small blocks
      brick = p->azwhalf+p->rgwhalf;
      if (p->lines < p->cols ) {
         p->numthrd = p->lines / brick;
      } else {
         p->numthrd = p->cols / brick;
      }
   }

   specific spc[p->numthrd];
   pthread_t threads[p->numthrd];
   pthread_mutex_init(&p->lock,0);

   int status;
   for (int tid=0; tid < p->numthrd; ++tid ) {
      spc[tid].id = tid;
      spc[tid].pr = p;
      spc[tid].brick = brick;
      spc[tid].begline = tid*brick;
      spc[tid].endline = (tid+1)*brick - 1;
      if ( tid == p->numthrd - 1) { spc[tid].endline = p->lines - 1; }
      if (precision == 1) {
            status = pthread_create(&(spc[tid].descriptor),NULL, f_medfilter2d, &spc[tid]);
      } else if (precision == 2) {
            status = pthread_create(&(spc[tid].descriptor),NULL, d_medfilter2d, &spc[tid]);
      } else {
            printf("invalid precision %d. Returning without doing anything\n",precision);
            status = 1;
      }
      if (status) { printf("error %d in pthread_create\n\n",status); }
   }

   int rc;
   for (int tid=0; tid < p->numthrd; ++tid ) {
      rc = pthread_join(spc[tid].descriptor,NULL);
      assert(rc == 0);
   }
}

/*=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-*/


