/*

Moving average (boxcar) filter for complex-valued gridded data

*/

#include <iostream>
#include <fstream>
#include <algorithm>
#include <vector>
#include <string>
#include <sys/time.h>
#include <stdio.h>
#include <stdlib.h>
#include <complex>
#include <pthread.h>  
#include "/home/bminchew/Utilities/C/Eigen/Dense"

using namespace Eigen;
using namespace std;





//******************************************************************************************

struct problem {
      int cols, lines, azwindow, rgwindow, azwhalf, rgwhalf, numthrd, rank, size;
      long vals, chunk;
      double null;

      MatrixXcf invec;
      MatrixXcf meanvec;

      pthread_mutex_t lock;
   };

struct specific {
      int id, begline, endline, brick;
      pthread_t descriptor;
      problem* pr;
   };


//******************************************************************************************
 
void* filter_routine(void* arg) {

   specific* s = (specific *) arg;
   int cols = s->pr->cols;
   int lines = s->pr->lines;
   int azwhalf = s->pr->azwhalf;
   int rgwhalf = s->pr->rgwhalf;
   int left, right, top, bot, blkaz, blkrg;

   for (long i = s->begline; i <= s-> endline; ++i) {
      top = i - azwhalf;
      bot = i + azwhalf;
      if ( top < 0 ) { top = 0; }
      if ( bot >= lines ) { bot = lines - 1; }
      blkaz = bot - top + 1;

      for (long j=0; j < cols; ++j) {
         left  = j - rgwhalf;
         right = j + rgwhalf;
         if ( left < 0 ) { left = 0; }
         if ( right >= cols ) { right = cols - 1; }
         blkrg = right - left + 1;

         s->pr->meanvec(i,j) = s->pr->invec.block(top,left,blkaz,blkrg).mean();
      }
   }   
}

//******************************************************************************************

int main(int argc, char *argv[]) {

   if (argc < 5 || argc > 9) {
      printf("\nMoving average (lowpass) filter for complex interferograms\n\n");
      printf("Usage:  filter_int_bm infile cols window outfile [options]\n\n");
      printf("    Options:\n");
      printf("          -a azimuth window size (default = window; i.e. square window)\n");
      printf("          -n number of threads (default = 8) \n\n");
      return 0;
   } 

   problem p;
   char * infile = (char *) argv[1] ;
   p.cols = (int) atof(argv[2]);
   p.rgwindow = (int) atof(argv[3]);
   char * outfile = (char *) argv[4] ;

   p.azwindow = p.rgwindow; 
   p.numthrd = 8;

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
   ifstream fid(infile, ios::in | ios::binary);
   // get number of lines
   fid.seekg(0, ios::end);
   p.lines = fid.tellg() / (sizeof(complex<float>)*p.cols);
   fid.seekg(0, ios::beg);

   printf("\nFiltering ::  %s\n\n", infile);
   printf("Lines    = %d \nColumns  = %d \n\n", p.lines, p.cols);

   p.invec.resize(p.lines, p.cols);
   p.meanvec.resize(p.lines, p.cols);

   printf("1/3  Reading...\n");
   std::vector<complex<float> > tempv;
   tempv.resize(p.cols);
   for (long i = 0; i < p.lines; ++i) {
      fid.read((char *)  &tempv[0], sizeof(complex<float>)*p.cols);
      for (long j = 0; j < p.cols; ++j) {
         p.invec(i,j) = tempv[j];
      }
   }
   fid.close();

   // split up into threads
   specific spc[p.numthrd];
   pthread_t threads[p.numthrd];
   pthread_mutex_init(&p.lock,0);
    
   int brick = p.lines / p.numthrd ;
   if ( brick < 1 ) { brick = 1; }
 
   for (int tid=0; tid < p.numthrd; tid++ ) {   
      spc[tid].id = tid;
      spc[tid].pr = &p; 
      spc[tid].brick = brick;
      spc[tid].begline = tid*brick;
      spc[tid].endline = (tid+1)*brick - 1;
      if ( tid == p.numthrd - 1) { spc[tid].endline = p.lines-1; }
      int status = pthread_create(&(spc[tid].descriptor),NULL,filter_routine,&spc[tid]);
         if (status) {  printf("error %d in pthread_create\n\n",status);  }
   }

   printf("2/3  Filtering...\n");
   for (int tid=0;tid<p.numthrd;tid++)
   {
      pthread_join(spc[tid].descriptor,NULL);
   }

   printf("3/3  Writing...\n");
   ofstream fidw(outfile, ios::out | ios::binary); 
   for ( long i=0; i < p.lines; ++i) {
      for (long j=0; j < p.cols; ++j) {
         tempv[j] = p.meanvec(i,j);
      }
      fidw.write((char *) &tempv[0], sizeof(complex<float>)*p.cols);
   }
   fidw.close();
   printf("\n Done \n\n"); 

   return 0;
}
