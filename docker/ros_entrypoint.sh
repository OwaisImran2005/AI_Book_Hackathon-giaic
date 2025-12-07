#!/bin/bash
set -e

# Setup ROS 2 environment
source "/opt/ros/$ROS_DISTRO/setup.bash"

# If a ROS 2 workspace is present, source its setup file
if [ -d "/ros2_ws/install" ]; then
  source "/ros2_ws/install/setup.bash"
fi

# Execute the command given as arguments
exec "$@"
