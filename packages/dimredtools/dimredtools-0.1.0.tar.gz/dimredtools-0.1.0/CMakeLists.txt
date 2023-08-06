cmake_minimum_required(VERSION 3.14)
# Project Details
set(PROJECT_NAME "DimRedTools")
set(PROJECT_VERSION 0.0.1)
set(PROJECT_EMAIL   "")
set(PROJECT_HOME    "")
set(PROJECT_DOCS    "")
set(PROJECT_CODE    "https://github.com/Keeper318/DimRedTools")
set(PROJECT_ISSUES  "")
set(PYPI_PACKAGE_NAME "dimredtools")
# Set Project Properties
project(${PROJECT_NAME} VERSION ${PROJECT_VERSION}
DESCRIPTION "A set of algorithms and data structures for dimensionality reduction"
LANGUAGES CXX)
# Set Global Properties
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(NOT CMAKE_BUILD_TYPE)
set(CMAKE_BUILD_TYPE Release)
endif()

set(ORIG_CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_LIBRARY_OUTPUT_DIRECTORY})

# Output Folders
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/bin)

# Options for DRT
option(DRT_BUILD_PYMODULE "DRT -Build Python Module" ON)
option(DRT_BUILD_TESTS "DRT - Build Tests" ON)
option(DRT_BUILD_BENCHMARKS "DRT - Build Benchmarks" ON)
option(DRT_BUILD_EXAMPLES "DRT - Build Examples" ON)
option(DRT_WITH_OPENMP "DRT - Build with OpenMP Support" ON)
option(DRT_BUILD_WERROR "DRT - Add Werror flag to build (turns warnings into errors)" OFF)

# Add any dependencies needed by our library
add_subdirectory("thirdparty")

# Build our library
add_subdirectory("src")

# Build examples if configured
if(DRT_BUILD_EXAMPLES)
    add_subdirectory("examples")
endif()

# Build tests if configured
if(DRT_BUILD_TESTS)
    add_subdirectory("tests")
endif()

# Build benchmarks if configured
if(DRT_BUILD_BENCHMARKS)
    add_subdirectory("bench")
endif()
