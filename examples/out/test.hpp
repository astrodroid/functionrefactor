
#pragma once
//namespace comment
namespace Controller {
//this comment should not appear in the cpp file as it's not near something that is going to be move there
//comments here
using precision = float;
//class description here
class PID {
    precision error_0 = 0;
    precision error_1 = 0;
    precision Kc;
    precision ti;
    precision td;
public:
    PID(precision _Kcprecision _tiprecision _td); /* ... */
    //more useful and witty comments here
    precision velocity_algorithm_PI(precision errorprecision dt);
};
} // namespace Controller

