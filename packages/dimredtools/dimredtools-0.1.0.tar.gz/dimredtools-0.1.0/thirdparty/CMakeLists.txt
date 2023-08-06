include(FetchContent)
# Put any LIBRARY dependencies in here
FetchContent_Declare(
  extern_pybind11
  GIT_REPOSITORY https://github.com/pybind/pybind11.git
  GIT_TAG        v2.10.0
)
FetchContent_Declare(
        extern_eigen
        URL https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz
)

# After the following call, the pybind11 library will be installed
FetchContent_MakeAvailable(extern_pybind11 extern_eigen)

# Nanobench and docttest will only be downloaded & installed if configured to do so with CMake Options
# This download occurs, with FetchContent_MakeAvailable call, in the "bench" and "tests" directory