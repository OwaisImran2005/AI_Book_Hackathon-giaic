cmake_minimum_required(VERSION 3.8 FATAL_ERROR)
project(my_nav2_bringup)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

find_package(ament_cmake REQUIRED)
find_package(nav2_bringup REQUIRED)
find_package(launch_ros REQUIRED)

install(DIRECTORY config
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
