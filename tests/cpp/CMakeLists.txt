project( test_setuptools_cpp )

set(CMAKE_EXPORT_COMPILE_COMMANDS 1)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_BUILD_TYPE "Release")
set(CMAKE_MACOSX_RPATH 1)

set(PYTHON_INCLUDE_DIR "" CACHE STRING "Path containing Python.h header")
cmake_minimum_required(VERSION 2.8.11)
message(STATUS "PYTHON_INCLUDE_DIR=${PYTHON_INCLUDE_DIR}")

add_subdirectory(pybind11)  # Using a submodule

pybind11_add_module(
        compiled SHARED
        src/test_pkg.cpp
)

target_include_directories(
        compiled PRIVATE
        "${CMAKE_CURRENT_SOURCE_DIR}/include"
        "${PYTHON_INCLUDE_DIR}"
        "${CMAKE_CURRENT_SOURCE_DIR}/pybind11"
)
