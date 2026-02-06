cmake_minimum_required(VERSION 3.18)
project(bspricer_cpp LANGUAGES CXX)

find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(bspricer_cpp bspricer_cpp.cpp)
target_compile_features(bspricer_cpp PRIVATE cxx_std_17)
