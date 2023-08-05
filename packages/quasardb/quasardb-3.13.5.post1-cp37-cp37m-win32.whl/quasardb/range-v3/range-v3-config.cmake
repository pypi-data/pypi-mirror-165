# Generated by CMake

if("${CMAKE_MAJOR_VERSION}.${CMAKE_MINOR_VERSION}" LESS 2.5)
   message(FATAL_ERROR "CMake >= 2.6.0 required")
endif()
cmake_policy(PUSH)
cmake_policy(VERSION 2.6...3.18)
#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

if(CMAKE_VERSION VERSION_LESS 3.0.0)
  message(FATAL_ERROR "This file relies on consumers using CMake 3.0.0 or greater.")
endif()

# Protect against multiple inclusion, which would fail when already imported targets are added once more.
set(_targetsDefined)
set(_targetsNotDefined)
set(_expectedTargets)
foreach(_expectedTarget range-v3-concepts range-v3-meta range-v3)
  list(APPEND _expectedTargets ${_expectedTarget})
  if(NOT TARGET ${_expectedTarget})
    list(APPEND _targetsNotDefined ${_expectedTarget})
  endif()
  if(TARGET ${_expectedTarget})
    list(APPEND _targetsDefined ${_expectedTarget})
  endif()
endforeach()
if("${_targetsDefined}" STREQUAL "${_expectedTargets}")
  unset(_targetsDefined)
  unset(_targetsNotDefined)
  unset(_expectedTargets)
  set(CMAKE_IMPORT_FILE_VERSION)
  cmake_policy(POP)
  return()
endif()
if(NOT "${_targetsDefined}" STREQUAL "")
  message(FATAL_ERROR "Some (but not all) targets in this export set were already defined.\nTargets Defined: ${_targetsDefined}\nTargets not yet defined: ${_targetsNotDefined}\n")
endif()
unset(_targetsDefined)
unset(_targetsNotDefined)
unset(_expectedTargets)


# Create imported target range-v3-concepts
add_library(range-v3-concepts INTERFACE IMPORTED)

set_target_properties(range-v3-concepts PROPERTIES
  INTERFACE_COMPILE_OPTIONS "\$<\$<COMPILE_LANG_AND_ID:CXX,MSVC>:/permissive->;\$<\$<COMPILE_LANG_AND_ID:CUDA,MSVC>:-Xcompiler=/permissive->"
  INTERFACE_INCLUDE_DIRECTORIES "Z:/TeamCity/work/283bde3fda0d76e7/thirdparty/range-v3/include/"
  INTERFACE_LINK_LIBRARIES "range-v3-meta"
)

# Create imported target range-v3-meta
add_library(range-v3-meta INTERFACE IMPORTED)

set_target_properties(range-v3-meta PROPERTIES
  INTERFACE_COMPILE_OPTIONS "\$<\$<COMPILE_LANG_AND_ID:CXX,MSVC>:/permissive->;\$<\$<COMPILE_LANG_AND_ID:CUDA,MSVC>:-Xcompiler=/permissive->"
  INTERFACE_INCLUDE_DIRECTORIES "Z:/TeamCity/work/283bde3fda0d76e7/thirdparty/range-v3/include/"
)

# Create imported target range-v3
add_library(range-v3 INTERFACE IMPORTED)

set_target_properties(range-v3 PROPERTIES
  INTERFACE_COMPILE_OPTIONS "\$<\$<COMPILE_LANG_AND_ID:CXX,MSVC>:/permissive->;\$<\$<COMPILE_LANG_AND_ID:CUDA,MSVC>:-Xcompiler=/permissive->"
  INTERFACE_INCLUDE_DIRECTORIES "Z:/TeamCity/work/283bde3fda0d76e7/thirdparty/range-v3/include/"
  INTERFACE_LINK_LIBRARIES "range-v3-concepts;range-v3-meta"
)

# This file does not depend on other imported targets which have
# been exported from the same project but in a separate export set.

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
cmake_policy(POP)
