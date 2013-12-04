cmake_minimum_required(VERSION 2.8)

set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)
set(X86 1)
set(PI 0)

find_package(OpenCV REQUIRED)
find_package(Boost REQUIRED COMPONENTS python)
find_package(PythonLibs REQUIRED)

include_directories(${Boost_INCLUDE_DIRS} /usr/include/python2.7
                        ${PYTHON_INCLUDE_DIRS})

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_CXX_FLAGS "-g -Wall")

add_subdirectory(src)
