cmake_minimum_required(VERSION 3.6)

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})

set(dependencies_folder "${CMAKE_SOURCE_DIR}/../dependencies/")
include(${dependencies_folder}/LouEngine/build/cmake/LouEngine.cmake)

add_dependency_subdirectory("LouEngine" "${dependencies_folder}")

set(dependencies
	"LouEngine"
)

generate_executable(name "PTyledGame" dependencies "${dependencies}" dependencies_folder "${dependencies_folder}")
