

================
Functionrefactor
================

Functionrefactor is a python script that removes C++ templates, and moves function implementations to the source file.

This can be of use if you would like to write a class prototype/draft, without explicitly going back and forth between header file to correct both every time you change something. Instead code it all in one or more C++ header files and then use this script to generate the cleaned up hpp and cpp files.

As a plus this approach allows removing templates, note that an option will be added in the future to disable this feature.

================================
Replacing template parameters
================================


Functionrefactor removes templates from C++ code by replacing the template argument with an using statement or constexpr. The reason for doing this is not because C++ are not useful! But it's because too much reliance on them will turn the compiler sluggish. In my case, I have a project that has too many templates where not all of them were strictly required, and this prompted me to write this script to actually deal with that issue.

For example on the example below the precision type is going to be replaced with a using statement and the function implementation will be moved in the cpp file. Of course anywhere that class is referenced with it’s template arguments it will need to be modified, as the functionrefactor only modifies one header file.



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

================================
Moving function Implementations
================================

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
Installation through PIP will be added shortly, at the moment you can launch the program by running the functionrefactor.py file by either providing a launcher file (see further below for expected format).

    python3 functionrefactor.py {path to json launcher file}

    python3 functionrefactor.py {path to input header file} {path to output hpp} {path to output cpp}

Alternatively you can do a local pip install from the functionrfactor root folder and then launching it as before.

    *sudo* pip install ./

Laucher file
------------

The laucher file is a json file, that can convert multiple files.

The root element is the "launcher" key that is an array of inputs to be processed.

Each file processed can have its own properties or they can be default for all of them. The script simply looks for certain keys either at the single launch case or one level below in the json file. Failing to find anything in the launcher file the default settings.json is used in the project functionrefactor folder.

    {
       "launcher":[
          {"input":"test.hpp","active":true, "hpp_out":"out", "cpp_out":"out", "overwrite":true},
          {"input":"inactive.hpp", "active=":false, "hpp_out":"out", "cpp_out":"out", "overwrite":false}
       ],
       "option_key": false
    }


Contributing
------------

Any suggestions, problems or contributions are welcome, just contact me in github.


License
------------

MIT
