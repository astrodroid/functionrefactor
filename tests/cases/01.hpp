
#include "sourcefile.hpp"
#include <somelibrary>
#ifndef 01_HPP
#define 01_HPP

// this is a comment of some sort

namespace Super {
/*This is the class description: (if it had one)"Lorem ipsum dolor sit amet,
 * consectetur adipiscing elit,sed do eiusmod tempor incididunt ut labore et
 * dolore magna aliqua.Ut enim ad minim veniam, quis nostrud exercitation
 * ullamco laborisnisi ut aliquip ex ea commodo consequat.Duis aute irure dolor
 * in reprehenderit in voluptate velit esse cillumdolore eu fugiat nulla
 * pariatur. Excepteur sint occaecat cupidatatnon proident, sunt in culpa qui
 * officia deserunt mollit anim id estlaborum."*/
using T = change_this;
constexpr int constant_value = 42;
class Stuff {
  T whatever;
  std::string text;
  float value = 2.f;
  void pointless_function();
 public:
  Stuff();
  float do_stuff();
};

}  // namespace Super

#endif  // stop

