#include "decomp.h"
/**************************************************************************************/

void* freedurd(void* arg) {
   specific* s = (specific *) arg;
   float thresh = 1.e-7;
   double fs,fd,hh,vv,hv,hvm;
   std::complex <double> alpha, alpha1, alpha2;
   std::complex <double> beta, beta1, beta2, hhvv, h;

   beta = 0.; alpha = 0.;   // deal with null values

   for (long i = s->begind; i < s->endind; ++i) {
      hv   = (double) s->pr->hvhv[i];
      hh   = (double) s->pr->hhhh[i] - 3.*hv;
      vv   = (double) s->pr->vvvv[i] - 3.*hv;
      hhvv = (std::complex <double>) s->pr->hhvv[i] - hv;

      if ( real(s->pr->hhvv[i]) > thresh ) {
         alpha = -1.; hvm = 1.;
         h = (vv + hhvv) / (hh - vv);
         beta1 = (1. + sqrt(1. + 4.*h*(1.+h)))/(2.*h);
         beta2 = (1. - sqrt(1. + 4.*h*(1.+h)))/(2.*h);
         if ( std::abs(abs(beta1)-1.) > std::abs(abs(beta2)-1.) ) {
            beta = beta1;
         } else {
            beta = beta2;
         }

         fs = (hh - vv) / (abs(beta)*abs(beta) - 1.);
         fd = vv - fs;

      } else if ( real(s->pr->hhvv[i]) < -1.*thresh ) {
         beta = 1.; hvm = 1.;
         h = (vv - hhvv) / (hh - vv);
         alpha1 = (-1. + sqrt(1. + 4.*h*(1.+h)))/(2.*h);
         alpha2 = (-1. - sqrt(1. + 4.*h*(1.+h)))/(2.*h);
         if ( std::abs(abs(alpha1)-1.) > std::abs(abs(alpha2)-1.) ) {
            alpha = alpha1;
         } else {
            alpha = alpha2;
         }

         fd = (hh - vv) / (abs(alpha)*abs(alpha) - 1.);
         fs = vv - fd;

      } else {
         fd = 0.; fs = 0.; hvm = 0.;
      }

      s->pr->out[i] = fs*(1. + abs(beta)*abs(beta));
      s->pr->out[i+s->pr->len] = fd*(1. + abs(alpha)*abs(alpha));
      s->pr->out[i+2*s->pr->len] = hvm * 8.*s->pr->hvhv[i];
   }
}

/*------------------------------------------------------------------------------------*/
void spawn_fd_workers(struct problem *p) {
   if (p->numthrd < 1) { p->numthrd = 1; }
   long brick = p->len / p->numthrd;
   if (brick < 10000) { p->numthrd = 1; }

   specific spc[p->numthrd];
   pthread_t threads[p->numthrd];
   pthread_mutex_init(&p->lock,0);

   for (int tid=0; tid < p->numthrd; ++tid ) {
      spc[tid].id = tid;
      spc[tid].pr = p;
      spc[tid].brick = brick;
      spc[tid].begind = tid*brick;
      spc[tid].endind = (tid+1)*brick;
      if ( tid == p->numthrd - 1) { spc[tid].endind = p->len - 1; }
      int status = pthread_create(&(spc[tid].descriptor),NULL, freedurd, &spc[tid]);
         if (status) { printf("error %d in pthread_create\n\n",status); }
   }

   int rc;
   for (int tid=0; tid < p->numthrd; ++tid ) {
      rc = pthread_join(spc[tid].descriptor,NULL);
      assert(rc == 0);
   }
}

/*------------------------------------------------------------------------------------*/

void free_durden_solver(float *hhhh, float *vvvv, float *hvhv,
   std::complex<float> *hhvv, float *out, int len, int numthrd) {

   problem p;
   p.hhhh = hhhh;
   p.vvvv = vvvv;
   p.hvhv = hvhv;
   p.hhvv = hhvv;
   p.out  = out;
   p.len  = len;
   p.numthrd = numthrd;

   spawn_fd_workers(&p);
}

/*=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-*/

void* haalpha(void* arg) {
   specific* s = (specific *) arg; 

   double t11,t22,t33,hhhh,vvvv,hvhv;
   std::complex <double> t12,t13,t23,hhhv,hhvv,hvvv;

   double trt, entropy, ani, alpha;

   double log3i = 1./log(3.);
   double pi    = 4.*atan(1.);
   double r2d   = 180./pi;

   Eigen::Matrix3cd Tmat;
   Eigen::Matrix3cd Umat;
   Eigen::Vector3d pvec;

   for (long i = s->begind; i < s->endind; ++i) {

      if (s->pr->matform == 1) {

         hhhh = (double) s->pr->hhhh[i];
         vvvv = (double) s->pr->vvvv[i];
         hvhv = (double) s->pr->hvhv[i];
         
         hhhv = (std::complex <double>) s->pr->hhhv[i];
         hhvv = (std::complex <double>) s->pr->hhvv[i];
         hvvv = (std::complex <double>) s->pr->hvvv[i];

         t11 = 0.5 * (hhhh + 2.* real(hhvv) + vvvv);
         t22 = 0.5 * (hhhh - 2.* real(hhvv) + vvvv); 
         t33 = 2.* hvhv;

         t12 = std::complex <double> (0.5*(hhhh - vvvv),-imag(hhvv));
         t13 = hhhv + conj(hvvv);  
         t23 = hhhv - conj(hvvv);
 
      } else {
         t11 = s->pr->hhhh[i];
         t22 = s->pr->vvvv[i];
         t33 = s->pr->hvhv[i];
         
         t12 = s->pr->hhhv[i];
         t13 = s->pr->hhvv[i]; 
         t23 = s->pr->hvvv[i];
      }

      // calculate eigenvalues
      trt = t11 + t22 + t33;
      if (trt > 0.) {
         Tmat << t11, t12, t13, 
               conj(t12), t22, t23,
               conj(t13), conj(t23), t33;
         Eigen::SelfAdjointEigenSolver<Eigen::Matrix3cd> eigensolver(Tmat);
         if (eigensolver.info() != Eigen::Success) {
            printf("Eigen did not converge\nAborting...\n"); abort();
         }
         alpha = 0.;
         entropy = 0.;
         pvec = eigensolver.eigenvalues()/trt;
         Umat = eigensolver.eigenvectors();
         for (int j=0; j<3; ++j){
            entropy += pvec(j)*std::log(pvec(j));
            alpha += pvec(j)*std::acos(abs(Umat(0,j)));
         }
         alpha *= r2d;
         entropy *= -log3i; 
         ani = (pvec(1) - pvec(0))/(pvec(1) + pvec(0));

      } else {
         entropy = 0.; ani = 0.; alpha = 0.;
      }
      s->pr->out[i] = entropy;
      s->pr->out[i+s->pr->len] = ani;
      s->pr->out[i+2*s->pr->len] = alpha;

   }
} 
   
/*------------------------------------------------------------------------------------*/
void spawn_haalp_workers(struct problem *p) {
   if (p->numthrd < 1) { p->numthrd = 1; }
   long brick = p->len / p->numthrd;
   if (brick < 10000) { p->numthrd = 1; }

   specific spc[p->numthrd];
   pthread_t threads[p->numthrd];
   pthread_mutex_init(&p->lock,0);

   for (int tid=0; tid < p->numthrd; ++tid ) { 
      spc[tid].id = tid;
      spc[tid].pr = p;
      spc[tid].brick = brick;
      spc[tid].begind = tid*brick;
      spc[tid].endind = (tid+1)*brick;
      if ( tid == p->numthrd - 1) { spc[tid].endind = p->len - 1; }
      int status = pthread_create(&(spc[tid].descriptor),NULL, haalpha, &spc[tid]);
         if (status) { printf("error %d in pthread_create\n\n",status); }
   }   

   int rc; 
   for (int tid=0; tid < p->numthrd; ++tid ) { 
      rc = pthread_join(spc[tid].descriptor,NULL);
      assert(rc == 0); 
   }   
}



