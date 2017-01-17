#pragma once

//namespace comment
namespace Controller
{

//this comment should not appear in the cpp file as it's not near something that is going to be move there


//comments here
template <typename precision = float>
//class description here
class PID
{
    precision error_0 = 0;
    precision error_1 = 0;
    precision Kc;
    precision ti;
    precision td;

public:
    PID(precision _Kc,precision _ti,precision _td): Kc(_Kc),ti(_ti),td(_td) {}
    
    /* ... */

    //more useful and witty comments here
    precision velocity_algorithm_PI(precision error, precision dt)
    {
        auto OP = -Kc * (error - error_0) - Kc * (error)*dt / (ti * 60.0);

        error_1 = error_0;
        error_0 = error;
        return OP;
    }

};
}
