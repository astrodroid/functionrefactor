#include "sourcefile.hpp"
#include <somelibrary>

#ifndef 01_HPP
#define 01_HPP

//this is a comment of some sort
namespace Super
{

/*
This is the class description: (if it had one)
"Lorem ipsum dolor sit amet, consectetur adipiscing elit,
sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum
dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
non proident, sunt in culpa qui officia deserunt mollit anim id est
laborum."


*/

template <typename T, int constant_value = 42>
class Stuff
{
    T           whatever;
    std::string text;
    float       value = 2.f;

    void pointless_function()
    {

        while (true)
        {
            std::cout << "I hope you like infinite loops, cause that's how you get infinite loops!("
                      << "\n";
        }
    }

public:
    Stuff()
        : text("")
        , value(10.0f)
        , whatever(0)
    {
    }

    float do_stuff()
    {
        whatever += 42;
        return value + whatever;
    }
};
}

#endif
//stop