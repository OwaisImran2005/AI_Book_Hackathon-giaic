cmake_minimum_required(VERSION 3.8 FATAL_ERROR)
project(my_robot_description)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

find_package(ament_cmake REQUIRED)
find_package(joint_state_publisher_gui REQUIRED)
find_package(robot_state_publisher REQUIRED)
find_package(rviz2 REQUIRED)
find_package(xacro REQUIRED)

install(DIRECTORY urdf
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY xacro
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
