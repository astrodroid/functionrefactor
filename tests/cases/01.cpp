#import "01_in.hpp"

namespace Super {

void Stuff::pointless_function() {
  while (true) {
    std::cout << "I hope you like infinite loops, cause that's how you get "
                 "infinite loops!("
              << "\n";
  }
}
Stuff::Stuff() : text(""), value(10.0f), whatever(0) {}
float Stuff::do_stuff() {
  whatever += 42;
  return value + whatever;
}

}  // namespace Super

