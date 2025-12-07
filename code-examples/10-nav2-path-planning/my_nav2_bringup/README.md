# `my_nav2_bringup` ROS 2 Package

This package contains configuration files and launch scripts for setting up and running the Nav2 stack for autonomous navigation. It demonstrates how to integrate Nav2 with a simulated mobile robot, using localization data (e.g., from VSLAM) to enable autonomous path planning and obstacle avoidance. This example is part of Chapter 10: Nav2 Path Planning of the "Physical AI & Humanoid Robotics" book.

## Contents

-   `config/nav2_params.yaml`: Configuration file for the Nav2 stack, including parameters for costmaps, planners, controllers, and behavior trees.
-   `launch/nav2_bringup.launch.py`: A ROS 2 launch file to start the core Nav2 nodes.

## Setup

1.  **Navigate to your ROS 2 Workspace**: Ensure you are in the `src` directory of your ROS 2 workspace (e.g., `~/ros2_ws/src`).
2.  **Clone this Repository**: Place this `my_nav2_bringup` package within your ROS 2 workspace `src` directory.
    ```bash
    # Example: If your workspace is ~/ros2_ws
    cd ~/ros2_ws/src
    # Assuming you have cloned the main book's code-examples repository
    cp -r /path/to/ai-native-book/code-examples/10-nav2-path-planning/my_nav2_bringup .
    ```
3.  **Install Nav2**: If you haven't already, install the Nav2 stack:
    ```bash
    sudo apt update
    sudo apt install -y ros-humble-navigation2 ros-humble-nav2-bringup
    ```
4.  **Install Dependencies**:
    ```bash
    rosdep install -i --from-path src --rosdistro humble -y
    ```
5.  **Build the Package**:
    ```bash
    cd ~/ros2_ws
    colcon build --packages-select my_nav2_bringup
    ```
6.  **Source the Setup Files**:
    ```bash
    source install/setup.bash
    ```

## Usage

This package is designed to be used in conjunction with a simulated mobile robot (e.g., in Isaac Sim) that provides localization data (e.g., from VSLAM as implemented in Chapter 9).

### 1. Launch Isaac Sim and VSLAM

First, launch your simulated mobile robot in Isaac Sim and ensure your VSLAM node (from Chapter 9) is running and publishing accurate odometry/pose information.

### 2. Launch Nav2

In a *separate* terminal within your Isaac ROS Docker environment (or your ROS 2 development machine):

```bash
ros2 launch my_nav2_bringup nav2_bringup.launch.py use_sim_time:=true
```

### 3. Launch Rviz2 (for Visualization and Goal Setting)

In your Ubuntu host machine (not in the Docker container), source your ROS 2 environment and launch Rviz2:

```bash
source /opt/ros/humble/setup.bash
rviz2
```
Configure Rviz2:
*   Set `Fixed Frame` to `map` (or `odom`).
*   Add `RobotModel` display.
*   Add `Map` display (if you have a map, e.g., from VSLAM or `map_server`).
*   Add `Path` display (for global and local plans: `/planner_server/global_plan`, `/controller_server/local_plan`).
*   Add `Costmap` displays (for global and local costmaps).
*   Add `Pose` display for `/amcl_pose` (from AMCL localization, if used).

### 4. Send Navigation Goals

In Rviz2, use the "2D Goal Pose" tool:
1.  Click the "2D Goal Pose" button.
2.  Click on a desired target location in the map and drag to set the robot's final orientation.
The robot should then start navigating autonomously to that goal.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
