# `my_gazebo_worlds` ROS 2 Package

This package contains Gazebo world definitions and launch files for simulating a robotic arm. It demonstrates the fundamental concepts of integrating URDF models into Gazebo and launching the simulation environment. This example is part of Chapter 5: Gazebo Fundamentals of the "Physical AI & Humanoid Robotics" book.

## Contents

-   `worlds/empty_arm_world.world`: A simple Gazebo world file containing a sun and a ground plane.
-   `launch/spawn_mobile_robot.launch.py`: A ROS 2 launch file to start Gazebo with `empty_arm_world.world` and spawn the `mobile_robot` from the `my_robot_description` package.

## Usage

To launch Gazebo with the `empty_arm_world` and spawn your mobile robot:

```bash
ros2 launch my_gazebo_worlds spawn_mobile_robot.launch.py
```

Gazebo GUI should open, displaying the empty world with your mobile robot.

## Verification

-   Verify that the Gazebo GUI launches successfully.
-   Confirm that the `mobile_robot` model appears in the Gazebo simulation environment.
-   Use the Gazebo GUI tools to inspect the robot model.
-   Use `ros2 topic list` and `ros2 topic echo /range_sensor/out` to verify sensor data.
-   Publish to `/cmd_vel` topic to control the robot: `ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.2, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.5}}" -1`
## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
