cmake_minimum_required(VERSION 3.4...3.18)

#-----------------------------------------#
project(hipopybind)

#-----------------------------------------#
# Add LZ4 dependency
add_compile_definitions(__LZ4__)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/hipo/lz4/lib)

#-----------------------------------------#
# Add HIPO dependency
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/hipo)

#-----------------------------------------#
# Add pybind11 dependency and module
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/pybind11)

#-----------------------------------------#
file (GLOB SOURCE_FILES "hipo/hipo4/*.cpp")
file (GLOB HEADER_FILES "hipo/hipo4/*.h")
file (GLOB PYTHON_FILES "src/*.cpp" "src/*.h")
file (GLOB LZ4SRC_FILES "hipo/lz4/lib/*.c")
file (GLOB LZ4HDR_FILES "hipo/lz4/lib/*.h")

pybind11_add_module(hipopybind
	${SOURCE_FILES}
	${HEADER_FILES}
	${PYTHON_FILES}
    ${LZ4SRC_FILES}
    ${LZ4HDR_FILES}
)

# EXAMPLE_VERSION_INFO is defined by setup.py and passed into the C++ code as a
# define (VERSION_INFO) here.
target_compile_definitions(hipopybind
                           PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})

#-----------------------------------------#
# Link header files from subdirectories
target_include_directories(hipopybind PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
