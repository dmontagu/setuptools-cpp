#pragma once

#include <pybind11/pybind11.h>
//#include <pybind11/stl.h>

namespace py = pybind11;
using namespace py::literals;

int add(int i, int j);
