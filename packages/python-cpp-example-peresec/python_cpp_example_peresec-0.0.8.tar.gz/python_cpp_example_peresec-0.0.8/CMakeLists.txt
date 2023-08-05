# To start, we’ll define a project, set the source directory, and define a list of C++ sources without bindings.cpp. 
# (This list will come in handy later when we want build C++ tests independently of any Python bindings.)

cmake_minimum_required(VERSION 2.8.12)
project(python_cpp_example)
# Set source directory
set(SOURCE_DIR "src/python_cpp_example")
# Tell CMake that headers are also in SOURCE_DIR
include_directories(${SOURCE_DIR})
set(SOURCES "${SOURCE_DIR}/math.cpp")

# Next, we’ll tell CMake to add the pybind11 directory to our project and define an extension module. 
# This time, make sure bindings.cpp is added to the sources list.
# Generate Python module
add_subdirectory(lib/pybind11_mod)
pybind11_add_module(python_cpp_example ${SOURCES} "${SOURCE_DIR}/bindings.cpp")

# That’s all we need to instruct CMake to build our extension module. 
# Rather than run CMake directly, however, we’re going to configure Python’s built-in setuptools to build our package automatically via setup.py.
