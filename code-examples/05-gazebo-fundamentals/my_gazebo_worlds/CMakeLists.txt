cmake_minimum_required(VERSION 3.8 FATAL_ERROR)
project(my_gazebo_worlds)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

find_package(ament_cmake REQUIRED)
find_package(gazebo_ros REQUIRED)
find_package(launch_ros REQUIRED)
find_package(my_robot_description REQUIRED) # For our URDF model

install(DIRECTORY worlds
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
