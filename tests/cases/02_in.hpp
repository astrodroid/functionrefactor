
#pragma once
#include <string>
#include <vector>

namespace A
{

class ABC
{
    float T;
    float S;
    int   x;
    int   y;

public:
    ABC() {}

    void test()
    {
        T += S;
        x += y;
        return;
    }
};
}

#endif
