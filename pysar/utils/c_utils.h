
#include <cmath>

namespace Utilities {
   int round(double const value) {
      int ival = (int) value;
      if ( std::abs(value - ival) >= 0.5 ) {
         return ival + (int) (value/std::abs(value));
      } else {
         return ival;
      }
   }


   template<typename float_t, typename int_t>
   float_t machine_eps() {
      union {
         float_t f;
         int_t   i;
      } one, one_plus, little, last_little;

      one.f    = 1.;
      little.f = 1.;
      last_little.f = little.f;

      while(true) {
         one_plus.f = one.f;
         one_plus.f += little.f;
         if ( one.i != one_plus.i ) {
            last_little.f = little.f;
            little.f /= 2.;
         } else {
            return last_little.f;
         }
      }
   }


}

