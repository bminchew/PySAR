C file: _subsurf.f
      subroutine subsurf(d,x,y,c,lc,n,deg,nul)
C
C     Calculates and removes a polynomial surface, based on a given vector 
C        of coeffients
C
C     build command:  f2py -c -m subsurf subsurf.f 
C
C     subsurf is called by phase_detrend.py 
C
C
      integer*8 n,deg,cnt,i,j,lc
      real*4    x(n),y(n),m(n),v(n)
      real*8    nul,d(n),c(lc),xm(n),ym(n)

Cf2py intent(in) x,y,deg,nul,c
Cf2py intent(inout) d

C  setup the null vectors m and v 
      m = 1
      v = 0
      do i=1,n
         if (d(i).eq.nul) then
            m(i) = 0
            v(i) = nul
         endif
      enddo

C  calculate and remove surface
      cnt = 0
      xm = 1
      do i=0,deg+1
         ym = 1
         do j=0,deg-i
            cnt = cnt + 1
            d = d - ( c(cnt) * xm * ym )
            if (j.lt.(deg-i)) then
               ym = ym*y
            endif
         enddo
         if (i.lt.(deg+1)) then
            xm = xm*x
         endif
      enddo
C  restore null values
      d = d*m + v
      end
C end file _subsurf.f
