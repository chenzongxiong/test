cmake_minimum_required(VERSION 3.1)
project(zmqtest)

set (CMAKE_CXX_STANDARD 11)
find_package(PkgConfig)
pkg_check_modules(PC_LIBZMQ QUIET libzmq)

find_library(zmq_lib NAMES zmq
             PATHS ${PC_LIBZMQ_LIBDIR} ${PC_LIBZMQ_LIBRARY_DIRS})

if(zmq_lib)
    set(ZeroMQ_FOUND ON)
endif()

if(NOT ZeroMQ_FOUND)
    message(FATAL_ERROR "ZeroMQ was NOT found!")
endif()

add_executable(
  client.bin
  client.cpp
  )

add_executable(
  server.bin
  server.cpp
  )

target_link_libraries(client.bin
  ${zmq_lib}
  )
target_link_libraries(server.bin
  ${zmq_lib}
  )

add_executable(
  sysinfo.bin
  sysinfo.cpp
  )

add_executable(
  metrics.bin
  metrics.cpp
  )
