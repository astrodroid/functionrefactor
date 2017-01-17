

==========
functionrefactor
==========

Functionrefactor is a python script that removes C++ templates, and moves function implementations to the source file.

==========
Replacing template parameters
==========


`Functionrefactor removes templates from C++ code by replacing the template argument with an using statement or constexpr.

For example on the example below the precision type is going to be replaced with a using statement and the function implementation will be moved in the cpp file. Of course anywhere that class is referenced with it’s template arguments it will need to be modified as the functionrefactor only modifies one header file.



.. code-block:: cpp

    /* PID.hpp */

    //comments here
    template <typename precision>
    class PID {
      precision error_0 = 0;
      precision error_1 = 0;
      precision Kc;
      precision ti;
      precision td;

     public:
      PID() {}
      /* ... */

      //more useful and witty comments here
      precision velocity_algorithm_PI(precision error, precision dt)
      {
        auto OP = -Kc * (error - error_0) - (Kc) * (error)*dt / (ti * 60.0);

        error_1 = error_0;
        error_0 = error;
        return OP;
      }
      /* ... */
    };

    However for the example above a float precision is adequate, making the template argument unnecessary. In practice you can just as well do all that manually, bit it gets too much tiresome if you have a large codebase to convert.

   functionrefactor replaces the template declaration with a using statement making the previous example as this:


  .. code-block:: cpp

        /* PID.hpp */


       using precision = change_this;
         //comments here
        class PID {
          precision error_0 = 0;
          precision error_1 = 0;
          precision Kc;
          precision ti;
          precision td;

         public:
          PID() {}
          /* ... */

          //more useful and witty comments here
          precision velocity_algorithm_PI(precision error, precision dt);
          /* ... */
        };

  .. code-block:: cpp
        /* PID.cpp */

          //more useful and witty comments here
        precision PID::velocity_algorithm_PI(precision error, precision dt)
        {
          auto OP = -Kc * (error - error_0) - (Kc) * (error)*dt / (ti * 60.0);

          error_1 = error_0;
          error_0 = error;
          return OP;
        }

Any constants declared within the template arguments are going to be replaced with a constexpr and any default values will be used in the using/constexpr expression.

==========
Moving function Implementations
==========

Besides converting the template, this also allows you to prototype a class interface and anything else you want in the header file and then this will automatically create the header file and cpp file for you.
This will not happen on all cases, it depends in what keywords have been used in the function declaration. For example by default (explicitly declared) inline functions are left in the header file, as set by the settings.json file.




Release Notes
-------------

* Version 0.0.0 is the first version and it only been tested against python 3.5-3.6, python 2.7 is not supported at this point. Testing has been done on linux and mac so far but windows should be OK. Any issues let me know.
* Features from C++11/14/17 have been included and tested for, but not all of them have been accounted for. If something important is missing do let me know.
* Clang-format is optional.  functionrefactor works just as well without it, but the output formatting will likely require to be formatted manually or another tool.
* Warning if anything is already present in the destination cpp file it will be overwritten.
* By default the functionrefactor replaces both templates and moves function implementations in the cpp file.


Usage
-----------------
**Instructions to follow**



Contributing
------------

Any suggestions, problems or contributions are welcome, just contact me in github.


License
------------

MIT
