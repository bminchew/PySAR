! file: looks_mod.f90
!
   subroutine look2d_real(datain,inlen,cols,lkaz,lkrg,dataout,outlen,xnull,nullval,verbose)
!
!  2D Incoherent averaging (looking) routine
!
!     build command:  f2py -c -m looks_mod looks_mod.f90 --opt="-O3" --f90exec=/usr/bin/gfortran
   implicit none
   integer        cols,lkaz,lkrg,xnull,verbose
   integer        rtlk,lflk,uplk,dnlk,wrdcnt
   integer        cntv(cols),ii,jj,kk,cc,zz
   integer        inlen,outlen,lind,rind
   integer        lines,lino,colso,ni
   real*4         nullval,datain(inlen)
   real*4         dataout(outlen),inv(cols)
   real*8         ksum,n,divc,kvec(cols)

!f2py intent(in)     :: datain(inlen)
!f2py intent(in)     :: width,wind0,wind1,xnull,nullval,verbose
!f2py intent(out)    :: dataout(outlen)
   
   if (mod(lkrg,2).ne.0) then
      rtlk = (lkrg - 1)/2
      lflk = rtlk
   else
      rtlk = lkrg/2
      lflk = lkrg/2 - 1 
   endif

   if (mod(lkaz,2).ne.0) then
      uplk = (lkaz - 1)/2
      dnlk = uplk
   else
      uplk = lkaz/2 - 1 
      dnlk = lkaz/2
   endif

   lines = int(dble(inlen)/dble(cols))
   colso = int(dble(cols)/dble(lkrg))
   lino  = int(dble(lines)/dble(lkaz))
   n = dble(lkrg)*dble(lkaz)
   ni = int(n)


   wrdcnt = 0 
   cc = 0

   do ii=(uplk+1),(lines-dnlk),lkaz

      wrdcnt = wrdcnt + 1 
      if (verbose.eq.1) call print_status(wrdcnt,lino,2) 

      kvec = 0
      if (xnull.eq.0) then
         do zz=(ii-uplk),(ii+dnlk)
            kvec = kvec + dble(datain((zz-1)*cols+1:zz*cols))
         enddo
      else
         cntv = 0
         do zz=(ii-uplk),(ii+dnlk)
            inv(1:cols) = datain((zz-1)*cols+1:zz*cols)
            do kk=1,cols
               if (inv(kk).ne.nullval) then
                  cntv(kk)=cntv(kk)+1
               else
                  inv(kk) = 0
               endif
            enddo
            kvec = kvec + dble(inv)
         enddo
      endif

      do jj=(lflk+1),(cols-rtlk),lkrg
         cc = cc + 1
         lind = jj - lflk
         rind = jj + rtlk
         ksum = dble(sum(kvec(lind:rind)))

         if (xnull.eq.0) then
            dataout(cc) = sngl(ksum/n)
         else
            divc = sum(dble(cntv(lind:rind)))
            if (divc.ne.0) then
               dataout(cc) = sngl(ksum/divc)
            else
               dataout(cc) = nullval
            endif
         endif
      enddo
   enddo
   if (verbose.eq.1) print *,''
   end

!  =================================================================================

   subroutine look2d_double(datain,inlen,cols,lkaz,lkrg,dataout,outlen,xnull,nullval,verbose)
!
!  2D Incoherent averaging (looking) routine
!
!     build command:  f2py -c -m looks_mod looks_mod.f90 --opt="-O3" --f90exec=/usr/bin/gfortran
   implicit none
   integer        cols,lkaz,lkrg,xnull,verbose
   integer        rtlk,lflk,uplk,dnlk,wrdcnt
   integer        cntv(cols),ii,jj,kk,cc,zz
   integer        inlen,outlen,lind,rind
   integer        lines,lino,colso,ni
   real*8         nullval,datain(inlen)
   real*8         dataout(outlen),inv(cols)
   real*8         ksum,n,divc,kvec(cols)

!f2py intent(in)     :: datain(inlen)
!f2py intent(in)     :: width,wind0,wind1,xnull,nullval,verbose
!f2py intent(out)    :: dataout(outlen)
   
   if (mod(lkrg,2).ne.0) then
      rtlk = (lkrg - 1)/2
      lflk = rtlk
   else
      rtlk = lkrg/2
      lflk = lkrg/2 - 1 
   endif

   if (mod(lkaz,2).ne.0) then
      uplk = (lkaz - 1)/2
      dnlk = uplk
   else
      uplk = lkaz/2 - 1 
      dnlk = lkaz/2
   endif

   lines = int(dble(inlen)/dble(cols))
   colso = int(dble(cols)/dble(lkrg))
   lino  = int(dble(lines)/dble(lkaz))
   n = dble(lkrg)*dble(lkaz)
   ni = int(n)


   wrdcnt = 0 
   cc = 0 

   do ii=(uplk+1),(lines-dnlk),lkaz

      wrdcnt = wrdcnt + 1 
      if (verbose.eq.1) call print_status(wrdcnt,lino,2) 

      kvec = 0 
      if (xnull.eq.0) then
         do zz=(ii-uplk),(ii+dnlk)
            kvec = kvec + datain((zz-1)*cols+1:zz*cols)
         enddo
      else
         cntv = 0
         do zz=(ii-uplk),(ii+dnlk)
            inv(1:cols) = datain((zz-1)*cols+1:zz*cols)
            do kk=1,cols
               if (inv(kk).ne.nullval) then
                  cntv(kk)=cntv(kk)+1
               else
                  inv(kk) = 0
               endif
            enddo
            kvec = kvec + inv
         enddo
      endif

      do jj=(lflk+1),(cols-rtlk),lkrg
         cc = cc + 1
         lind = jj - lflk
         rind = jj + rtlk
         ksum = dble(sum(kvec(lind:rind)))

         if (xnull.eq.0) then
            dataout(cc) = ksum/n
         else
            divc = sum(dble(cntv(lind:rind)))
            if (divc.ne.0) then
               dataout(cc) = ksum/divc
            else
               dataout(cc) = nullval
            endif
         endif
      enddo
   enddo
   if (verbose.eq.1) print *,''
   end

!  =================================================================================

   subroutine look2d_cmplx(datain,inlen,cols,lkaz,lkrg,dataout,outlen,xnull,nullval,verbose)
   !
   !  2D Incoherent averaging (looking) routine for single-precision complex images
   !
   implicit none
   integer        cols,lkaz,lkrg,xnull,verbose
   integer        rtlk,lflk,uplk,dnlk,wrdcnt
   integer        cntv(cols),ii,jj,kk,cc,zz
   integer        inlen,outlen,lind,rind
   integer        lines,lino,colso,ni
   complex*8      nullval,datain(inlen)
   complex*8      dataout(outlen),inv(cols)
   complex*16     ksum,n,divc,kvec(cols)

!f2py intent(in)     :: datain(inlen)
!f2py intent(in)     :: width,wind0,wind1,xnull,nullval,verbose
!f2py intent(out)    :: dataout(outlen)

   if (mod(lkrg,2).ne.0) then
      rtlk = (lkrg - 1)/2
      lflk = rtlk
   else
      rtlk = lkrg/2
      lflk = lkrg/2 - 1
   endif

   if (mod(lkaz,2).ne.0) then
      uplk = (lkaz - 1)/2
      dnlk = uplk
   else
      uplk = lkaz/2 - 1
      dnlk = lkaz/2
   endif

   lines = int(dble(inlen)/dble(cols))
   colso = int(dble(cols)/dble(lkrg))
   lino  = int(dble(lines)/dble(lkaz))
   n = dble(lkrg)*dble(lkaz)
   ni = int(n)


   wrdcnt = 0
   cc = 0

   do ii=(uplk+1),(lines-dnlk),lkaz

      wrdcnt = wrdcnt + 1
      if (verbose.eq.1) call print_status(wrdcnt,lino,2) 

      kvec = 0
      if (xnull.eq.0) then
         do zz=(ii-uplk),(ii+dnlk)
            kvec = kvec + dcmplx(datain((zz-1)*cols+1:zz*cols))
         enddo
      else
         cntv = 0
         do zz=(ii-uplk),(ii+dnlk)
            inv(1:cols) = datain((zz-1)*cols+1:zz*cols)
            do kk=1,cols
               if (inv(kk).ne.nullval) then
                  cntv(kk)=cntv(kk)+1
               else
                  inv(kk) = 0
               endif
            enddo
            kvec = kvec + dcmplx(inv)
         enddo
      endif

      do jj=(lflk+1),(cols-rtlk),lkrg
         cc = cc + 1
         lind = jj - lflk
         rind = jj + rtlk
         ksum = dcmplx(sum(kvec(lind:rind)))

         if (xnull.eq.0) then
            dataout(cc) = cmplx(ksum/n)
         else
            divc = sum(dble(cntv(lind:rind)))
            if (divc.ne.0) then
               dataout(cc) = cmplx(ksum/divc)
            else
               dataout(cc) = cmplx(nullval)
            endif
         endif
      enddo
   enddo
   if (verbose.eq.1) print *,''
   end

!  =================================================================================

   subroutine look2d_dcmplx(datain,inlen,cols,lkaz,lkrg,dataout,outlen,xnull,nullval,verbose)
   !   
   !  2D Incoherent averaging (looking) routine for double-precision complex images
   !   
   implicit none
   integer        cols,lkaz,lkrg,xnull,verbose
   integer        rtlk,lflk,uplk,dnlk,wrdcnt
   integer        cntv(cols),ii,jj,kk,cc,zz
   integer        inlen,outlen,lind,rind
   integer        lines,lino,colso,ni
   complex*16     nullval,datain(inlen)
   complex*16     dataout(outlen),inv(cols)
   complex*16     ksum,n,divc,kvec(cols)

!f2py intent(in)     :: datain(inlen)
!f2py intent(in)     :: width,wind0,wind1,xnull,nullval,verbose
!f2py intent(out)    :: dataout(outlen)

   if (mod(lkrg,2).ne.0) then
      rtlk = (lkrg - 1)/2
      lflk = rtlk
   else
      rtlk = lkrg/2
      lflk = lkrg/2 - 1 
   endif

   if (mod(lkaz,2).ne.0) then
      uplk = (lkaz - 1)/2
      dnlk = uplk
   else
      uplk = lkaz/2 - 1 
      dnlk = lkaz/2
   endif

   lines = int(dble(inlen)/dble(cols))
   colso = int(dble(cols)/dble(lkrg))
   lino  = int(dble(lines)/dble(lkaz))
   n = dble(lkrg)*dble(lkaz)
   ni = int(n)

   wrdcnt = 0 
   cc = 0 

   do ii=(uplk+1),(lines-dnlk),lkaz

      wrdcnt = wrdcnt + 1 
      if (verbose.eq.1) call print_status(wrdcnt,lino,2) 

      kvec = 0 
      if (xnull.eq.0) then
         do zz=(ii-uplk),(ii+dnlk)
            kvec = kvec + datain((zz-1)*cols+1:zz*cols)
         enddo
      else
         cntv = 0
         do zz=(ii-uplk),(ii+dnlk)
            inv(1:cols) = datain((zz-1)*cols+1:zz*cols)
            do kk=1,cols
               if (inv(kk).ne.nullval) then
                  cntv(kk)=cntv(kk)+1
               else
                  inv(kk) = 0
               endif
            enddo
            kvec = kvec + inv
         enddo
      endif

      do jj=(lflk+1),(cols-rtlk),lkrg
         cc = cc + 1
         lind = jj - lflk
         rind = jj + rtlk
         ksum = dcmplx(sum(kvec(lind:rind)))

         if (xnull.eq.0) then
            dataout(cc) = ksum/n
         else
            divc = sum(dble(cntv(lind:rind)))
            if (divc.ne.0) then
               dataout(cc) = ksum/divc
            else
               dataout(cc) = nullval
            endif
         endif
      enddo
   enddo
   if (verbose.eq.1) print *,''
   end
!  ==============================================================================



!  ==============================================================================
   subroutine print_status(i,j,s)
   implicit none
   integer        i,j,s
!f2py intent(in) i,j,s
   if(mod((100*i)/j,s).eq.0.or.i.eq.j.or.i.eq.1) then
      write(*,FMT="(A1,A,t21,I4,A)",ADVANCE="NO") achar(13), &
         & "  Percent Complete: ", (100*i)/j, " %"
   endif
   end subroutine

!  =================================================================================

!  end file looks_mod.f90


