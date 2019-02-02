cmake_minimum_required(VERSION 3.0.2)
project(zmqtest)

find_package(PkgConfig)
pkg_check_modules(PC_LIBZMQ QUIET libzmq)
find_library(ZeroMQ_LIBRARY NAMES libzmq.dylib
             PATHS ${PC_LIBZMQ_LIBDIR} ${PC_LIBZMQ_LIBRARY_DIRS})
find_library(ZeroMQ_STATIC_LIBRARY NAMES libzmq.a
             PATHS ${PC_LIBZMQ_LIBDIR} ${PC_LIBZMQ_LIBRARY_DIRS})

if(ZeroMQ_LIBRARY AND ZeroMQ_STATIC_LIBRARY)
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
  ${ZeroMQ_STATIC_LIBRARY}
  )
target_link_libraries(server.bin
  ${ZeroMQ_STATIC_LIBRARY}
  )
