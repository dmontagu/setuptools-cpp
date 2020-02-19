#include "test_pkg.hpp"


int add(int i, int j) {
    return i + j;
}

PYBIND11_MODULE(compiled, m) {
    m.doc() = "pybind11 example plugin";

    m.def("add", &add, "A function which adds two numbers", "i"_a, "j"_a);
}
