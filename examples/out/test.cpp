#import "test.hpp"

namespace Controller {

PID::PID(precision _Kc, precision _ti, precision _td) {
  Kc(_Kc), ti(_ti), td(_td) {}
  // more useful and witty comments here

  precision PID::velocity_algorithm_PI(precision error, precision dt) {
    auto OP = -Kc * (error - error_0) - Kc * (error)*dt / (ti * 60.0);
    error_1 = error_0;
    error_0 = error;
    return OP;
  }

}  // namespace Controller

