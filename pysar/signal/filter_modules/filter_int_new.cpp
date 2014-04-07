
#include <iostream>
#include <fstream>
#include <algorithm>
#include <vector>
#include <string>
#include <sys/time.h>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>  
#include <assert.h>
#include "/home/bminchew/Utilities/C/utils/Utilities.h"

//******************************************************************************************

struct problem {
      int cols, lines, azwindow, rgwindow;
      int azwhalf, rgwhalf, numthrd, rank, size;
      long arrsz;

      std::vector<float> image;
      std::vector<float> temp;

      pthread_mutex_t lock;
   };

struct specific {
      int id, brick;
      int begline, endline;
      int begcol, endcol;
      pthread_t descriptor;
      problem* pr;
   };


//******************************************************************************************

// filtering routines 
void* boxfilter_x(void* arg) {
   specific* s = (specific *) arg;
   int cols = s->pr->cols;
   int lines = s->pr->lines;
   int rgwhalf = s->pr->rgwhalf;
   long ind, icols;
   double sumr, sumi;
   double scale = 1.0f / (2.*rgwhalf+1.);
   
   for (int i = s->begline; i <= s->endline; ++i) {
      icols = 2*i*cols;
      // left edge
      sumr = s->pr->image[icols] * rgwhalf;
      sumi = s->pr->image[icols+1] * rgwhalf;
      for (int j = 0; j < 2*(rgwhalf+1); j+=2) {
         sumr += s->pr->image[icols+j];
         sumi += s->pr->image[icols+j+1];
      }
      s->pr->temp[icols] = sumr * scale;
      s->pr->temp[icols+1] = sumi * scale;

      for (int j = 2; j < 2*(rgwhalf+1); j+=2) {
         ind = icols+j;
         sumr += s->pr->image[ind+2*rgwhalf];
         sumi += s->pr->image[ind+2*rgwhalf+1];
         sumr -= s->pr->image[icols];
         sumi -= s->pr->image[icols+1];
         s->pr->temp[ind] = sumr * scale;
         s->pr->temp[ind+1] = sumi * scale;
      }   

      // body
      for (int j = 2*(rgwhalf+1); j < 2*(cols-rgwhalf); j+=2) {
         ind = icols+j;
         sumr += s->pr->image[ind+2*rgwhalf];
         sumi += s->pr->image[ind+2*rgwhalf+1];
         sumr -= s->pr->image[ind-2*(rgwhalf-1)];
         sumi -= s->pr->image[ind-2*(rgwhalf-1)+1];
         s->pr->temp[ind] = sumr * scale;
         s->pr->temp[ind+1] = sumi * scale;
      }   

      // right edge
      for (int j = cols-rgwhalf; j < cols; ++j) {
         ind = icols+j;
         sumr += s->pr->image[icols+2*(cols-1)];
         sumi += s->pr->image[icols+2*(cols-1)+1];
         sumr -= s->pr->image[ind-rgwhalf-1];
         sumi -= s->pr->image[ind-2*(rgwhalf-1)+1];
         s->pr->temp[ind] = sumr * scale;
         s->pr->temp[ind+1] = sumi * scale;
      }   
   }   
}

void* boxfilter_y(void* arg) {

   specific* s = (specific *) arg;
   int cols = 2*s->pr->cols;
   int lines = s->pr->lines;
   int azwhalf = s->pr->azwhalf;
   long ind;
   long rcols = azwhalf*cols;
   double sumr, sumi;
   double scale = 1.0f / (2*azwhalf+1);

   for (int j = 2*s->begcol; j <= 2*s->endcol ; j+=2) {
      // top edge
      sumr = s->pr->temp[j] * azwhalf;
      sumi = s->pr->temp[j+1] * azwhalf;
      for (int i = 0; i <= azwhalf; ++i) {
         sumr += s->pr->temp[i*cols+j];  // cols is multiplied by 2 in the def
         sumi += s->pr->temp[i*cols+j+1];
      }
      s->pr->image[j] = sumr * scale;
      s->pr->image[j+1] = sumi * scale;

      for (int i = 1; i <= azwhalf; ++i) {
         ind = i*cols+j;
         sumr += s->pr->temp[ind+rcols];
         sumi += s->pr->temp[ind+rcols+1];
         sumr -= s->pr->temp[j];
         sumi -= s->pr->temp[j+1];
         s->pr->image[ind] = sumr * scale;
         s->pr->image[ind+1] = sumi * scale;
      }

      // body
      for (int i = azwhalf+1; i < lines-azwhalf; ++i) {
         ind = i*cols+j;
         sumr += s->pr->temp[ind+rcols];
         sumi += s->pr->temp[ind+rcols+1];
         sumr -= s->pr->temp[ind-rcols-cols];
         sumi -= s->pr->temp[ind-rcols-cols+1];
         s->pr->image[ind] = sumr * scale;
         s->pr->image[ind+1] = sumi * scale;
      }

      // bottom edge
      for (int i = lines-azwhalf; i < lines; ++i) {
         ind = i*cols+j;
         sumr += s->pr->temp[(lines-1)*cols+j];
         sumi += s->pr->temp[(lines-1)*cols+j+1];
         sumr -= s->pr->temp[ind-rcols-cols];
         sumi -= s->pr->temp[ind-rcols-cols+1];
         s->pr->image[ind] = sumr * scale;
         s->pr->image[ind+1] = sumi * scale;
      }
   }
}


//******************************************************************************************

int main(int argc, char *argv[]) {

   if (argc < 5 || argc > 9) {
      printf("\nMoving average (lowpass) filter for binary complex floating point images\n\n");
      printf("Usage:  filter_int_bm infile cols window outfile [options]\n\n");
      printf("    Options:\n");
      printf("          -a azimuth window size (default = window; i.e. square window)\n");
      printf("          -n number of threads (default = 4) \n\n");
      return 0;
   } 

   problem p;
   char * infile = (char *) argv[1] ;
   p.cols = (int) atof(argv[2]);
   p.rgwindow = (int) atof(argv[3]);
   char * outfile = (char *) argv[4] ;

   p.azwindow = p.rgwindow; 
   p.numthrd = 4;

   if (argc > 5) {
      for (int k = 5; k < argc; k += 2) {
         if (std::string(argv[k]) == "-a") {
            p.azwindow = (int) atof(argv[k+1]);
         } else if (std::string(argv[k]) == "-n") {
            p.numthrd = (int) atof(argv[k+1]);
         }
      }
   }

   if (p.numthrd < 1) { p.numthrd = 1; }
   p.rgwhalf = (int) p.rgwindow/2;
   p.azwhalf = (int) p.azwindow/2;

   // Open file for reading
   std::ifstream fid(infile, std::ios::in | std::ios::binary);
   // get number of lines
   fid.seekg(0, std::ios::end);
   p.lines = fid.tellg() / (sizeof(float)*2*p.cols);
   fid.seekg(0, std::ios::beg);

   printf("\nFiltering ::  %s\n\n", infile);
   printf("Lines    = %d \nColumns  = %d \n\n", p.lines, p.cols);

   // resize arrays
   p.arrsz = 2*p.lines*p.cols;
   p.image.resize(p.arrsz);
   p.temp.resize(p.arrsz);

   printf("1/3  Reading...\n");
   fid.read((char *)  &p.image[0], sizeof(float)*p.arrsz);
   fid.close();

   printf("2/3  Filtering...\n");
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

   printf("3/3  Writing...\n");
   std::ofstream fidw(outfile, std::ios::out | std::ios::binary); 
   fidw.write((char *) &p.image[0], sizeof(float)*p.arrsz);
   fidw.close();

   printf("\n Done \n\n"); 
   return 0;
}
