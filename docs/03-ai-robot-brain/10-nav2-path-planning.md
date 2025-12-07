# Chapter 10: Nav2 Path Planning

:::info Chapter Info
**Module**: The AI Robot Brain | **Duration**: 5 hours | **Difficulty**: Advanced
:::

## Learning Objectives
By the end of this chapter, you will:
1. Understand the core components and architecture of the Nav2 stack for autonomous navigation in ROS 2.
2. Be able to configure global and local planners to generate collision-free paths.
3. Learn to utilize costmaps for environmental representation and obstacle avoidance.
4. Gain proficiency in integrating Nav2 with localization (e.g., VSLAM from Chapter 9) to enable autonomous robot movement.
5. Troubleshoot common Nav2 issues.

## Prerequisites
- Completed Chapter 9: Isaac ROS Perception, with a working VSLAM setup for a simulated mobile robot.
- Basic understanding of ROS 2 launch files and parameter configuration.
- Familiarity with coordinate frames and TF transforms.

## What You'll Build
In this chapter, you will enable your simulated mobile robot to navigate autonomously in an unknown environment within Isaac Sim. This will involve:
- Setting up the Nav2 stack for your robot.
- Configuring global and local planners.
- Creating and managing costmaps based on sensor data.
- Sending navigation goals to your robot and observing autonomous movement.

---

## Introduction: Guiding Robots to Their Destination

You've equipped your simulated mobile robot with a powerful perception system using Isaac ROS, enabling it to understand its environment and localize itself. The next crucial step for any autonomous robot is to be able to **navigate** that environment, moving from a starting point to a goal while avoiding obstacles. This is the domain of the **Nav2 stack**, ROS 2's robust and highly configurable framework for autonomous mobile robot navigation.

The Nav2 stack builds upon the foundational concepts of ROS 2 communication (nodes, topics, services, actions) and integrates various algorithms for localization, path planning, and control. It acts as the "brain" that translates high-level navigation goals into a sequence of low-level motor commands that the robot can execute. Whether your robot needs to deliver packages in a warehouse, explore an unknown terrain, or interact with humans in a dynamic space, Nav2 provides the tools to achieve these tasks autonomously.

In this chapter, we will dissect the core components of the Nav2 stack, understanding how they work together to achieve navigation. You will learn how to configure different types of planners (global and local) that generate paths and avoid obstacles, and how **costmaps** are used to represent the environment around the robot. Crucially, we will integrate Nav2 with the VSLAM output from Chapter 9, allowing your robot to localize itself and navigate based on its perceived map. By the end of this chapter, you will be able to send navigation goals to your simulated robot in Isaac Sim, and watch it intelligently and autonomously find its way to the destination.

## Core Concepts: The Nav2 Stack Architecture

The Nav2 stack is highly modular, comprising several independent nodes that communicate via ROS 2 interfaces. The entire system is orchestrated by a **Behavior Tree Navigator**, which defines the high-level logic for handling navigation tasks, including path planning, obstacle avoidance, and recovery behaviors.

### 1. Behavior Tree Navigator

The **Behavior Tree Navigator** is the top-level orchestrator. It uses XML-defined behavior trees to execute navigation tasks. A behavior tree is a hierarchical, state-machine-like structure that defines how a robot should behave. It allows for flexible and robust logic, including sequence, fallback, and parallel nodes, for tasks like:
*   Receiving a navigation goal.
*   Localizing the robot.
*   Calling a global planner.
*   Calling a local planner.
*   Executing recovery behaviors if navigation fails.

### 2. Global Planner

The **Global Planner** is responsible for generating a collision-free path from the robot's current position to a distant goal within the known map. It typically uses algorithms like Dijkstra's, A*, or Hybrid A* to find an optimal path, considering static obstacles.
*   **Input**: Robot's current pose, goal pose, static map.
*   **Output**: A global plan (a sequence of poses/waypoints).
*   **Common Planners**: `NavFn` (classic Dijkstra-like), `SmacPlanner` (A*, Hybrid A*).

### 3. Local Planner (Controller)

The **Local Planner**, often referred to as the **Controller**, is responsible for navigating the robot along the global path while avoiding dynamic obstacles and staying within local costmap boundaries. It operates at a higher frequency than the global planner, making real-time adjustments.
*   **Input**: Global plan, local costmap, robot's current pose.
*   **Output**: Velocity commands (`geometry_msgs/msg/Twist`) for the robot's motors.
*   **Common Controllers**: `DWBLocalPlanner` (Dynamic Window Bouncing), `TEBLocalPlanner` (Timed-Elastic Band), `MPPIController` (Model Predictive Path Integral).

### 4. Costmaps

**Costmaps** are 2D or 3D grid representations of the environment, assigning costs to cells based on proximity to obstacles. They are crucial for both global and local planning.
*   **Global Costmap**: A large map of the entire environment, used by the global planner.
*   **Local Costmap**: A smaller, dynamic map centered around the robot, continuously updated with sensor data (e.g., LiDAR, depth cameras), used by the local planner for immediate obstacle avoidance.
*   **Inflation Layer**: Expands obstacles in the costmap, creating a safety margin around them based on the robot's footprint.

### 5. Localization

Accurate **localization** (knowing the robot's precise position and orientation within a map) is fundamental for navigation. Nav2 can integrate with various localization sources:
*   **AMCL (Adaptive Monte Carlo Localization)**: For known maps (from `map_server`).
*   **SLAM Toolbox**: For simultaneous localization and mapping (if a map is being built simultaneously).
*   **VSLAM/Visual Odometry**: As we implemented in Chapter 9, VSLAM can provide pose estimates that Nav2 can consume.

### 6. Recovery Behaviors

Nav2 includes **recovery behaviors** to help the robot get unstuck or recover from navigation failures. These can include:
*   **Spin**: Rotate in place to clear local obstacles.
*   **Backup**: Move backward.
*   **Clear Costmap**: Reset local costmap.

## Hands-On Tutorial: Autonomous Navigation with Nav2

We will configure the Nav2 stack for your simulated mobile robot in Isaac Sim. This tutorial assumes you have completed Chapter 9 and have a working VSLAM setup providing localization data.

### Part 1: Nav2 Installation and Setup

### Step 1: Install Nav2

Inside your Isaac ROS Docker environment (or your ROS 2 development machine):

```bash
sudo apt update
sudo apt install -y ros-humble-navigation2 ros-humble-nav2-bringup
```

### Step 2: Create a ROS 2 Package for Nav2 Configuration

Navigate to your ROS 2 workspace `src` directory (e.g., `~/ros2_ws/src`).
Create a new package called `my_nav2_bringup`:

```bash
ros2 pkg create --build-type ament_cmake my_nav2_bringup --dependencies nav2_bringup launch_ros
```
*(Note: We use `ament_cmake` build type for packages that primarily contain configuration files and launch files.)*

### Step 3: Define Nav2 Configuration (`nav2_params.yaml`)

Create a `config` directory inside `my_nav2_bringup`:
```bash
mkdir my_nav2_bringup/config
```
Create the file `my_nav2_bringup/config/nav2_params.yaml` with the following content. This is a basic configuration; parameters will need tuning for specific robots/environments.

```yaml
# nav2_params.yaml
# Global configuration for Nav2 stack

amcl:
  ros__parameters:
    use_sim_time: true # Important for simulated environments
    set_initial_pose: true
    initial_pose:
      x: 0.0
      y: 0.0
      z: 0.0
      yaw: 0.0

bt_navigator:
  ros__parameters:
    use_sim_time: true
    default_bt_xml_filename: "behavior_trees/navigate_w_replanning_and_recovery.xml"
    goal_blackboard_timeout: 1.2

local_costmap:
  local_costmap:
    ros__parameters:
      update_frequency: 5.0
      publish_frequency: 2.0
      global_frame: odom
      robot_base_frame: base_link
      use_sim_time: true
      # ... other parameters ...
      plugins: ["obstacle_layer", "inflation_layer"]
      obstacle_layer:
        plugin: "nav2_costmap_2d::ObstacleLayer"
        parameters:
          # Assuming you have a range sensor publishing to /range_sensor/out
          # Or replace with your LiDAR/Depth camera topics
          range_sensor_in: {topic: "/range_sensor/out", sensor_frame: "range_sensor_link"}
      inflation_layer:
        plugin: "nav2_costmap_2d::InflationLayer"
        parameters:
          inflation_radius: 0.5

global_costmap:
  global_costmap:
    ros__parameters:
      update_frequency: 1.0
      publish_frequency: 1.0
      global_frame: map
      robot_base_frame: base_link
      use_sim_time: true
      # ... other parameters ...
      plugins: ["static_layer", "inflation_layer"]
      static_layer:
        plugin: "nav2_costmap_2d::StaticLayer"
      inflation_layer:
        plugin: "nav2_costmap_2d::InflationLayer"
        parameters:
          inflation_radius: 0.5

planner_server:
  ros__parameters:
    use_sim_time: true
    default_server_name: "planner_server"
    # Select your global planner (e.g., NavFn, SmacPlanner)
    default_planner_plugin: "nav2_navfn_planner::NavfnPlanner"
    # ... other parameters ...

controller_server:
  ros__parameters:
    use_sim_time: true
    default_server_name: "controller_server"
    # Select your local controller (e.g., DWBLocalPlanner, MPPIController)
    default_controller_plugin: "nav2_dwb_controller::DwbpController"
    # ... other parameters ...
    # Configure robot kinematics
    min_vel_x: -0.2
    max_vel_x: 0.5
    max_vel_theta: 1.0
    min_vel_theta: -1.0
    # Add other DWB specific parameters if using DWBLocalPlanner
    # ...
```
*(Note: This `nav2_params.yaml` is a simplified example. A full configuration would require more detailed parameters for each plugin.)*

### Step 4: Create a Launch File to Bring Up Nav2

Create a `launch` directory inside `my_nav2_bringup`:
```bash
mkdir my_nav2_bringup/launch
```
Create the file `my_nav2_bringup/launch/nav2_bringup.launch.py` with the following content:

```python
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from nav2_common.launch import RewrittenYaml


def generate_launch_description():
    # Get the launch directory
    bringup_dir = get_package_share_directory('nav2_bringup')
    my_nav2_bringup_dir = get_package_share_directory('my_nav2_bringup')

    # Create the launch configuration variables
    namespace = LaunchConfiguration('namespace')
    use_sim_time = LaunchConfiguration('use_sim_time')
    autostart = LaunchConfiguration('autostart')
    params_file = LaunchConfiguration('params_file')
    default_bt_xml_filename = LaunchConfiguration('default_bt_xml_filename')
    map_subscribe_transient_local = LaunchConfiguration('map_subscribe_transient_local')
    
    # Optional: Initial pose for AMCL if not using VSLAM for initial pose
    # initial_pose_x = LaunchConfiguration('initial_pose_x')
    # initial_pose_y = LaunchConfiguration('initial_pose_y')
    # initial_pose_yaw = LaunchConfiguration('initial_pose_yaw')

    lifecycle_nodes = ['controller_server',
                       'planner_server',
                       'recoveries_server',
                       'bt_navigator',
                       'waypoint_follower']

    # Rewrite the YAML file with robot_id as namespace for all params
    param_substitutions = {
        'default_bt_xml_filename': default_bt_xml_filename,
        'autostart': autostart,
        'map_subscribe_transient_local': map_subscribe_transient_local,
        # 'initial_pose.x': initial_pose_x,
        # 'initial_pose.y': initial_pose_y,
        # 'initial_pose.yaw': initial_pose_yaw,
    }

    # Pass the Nav2 params file.
    configured_params = RewrittenYaml(
            source_file=params_file,
            root_key=namespace,
            param_rewrites=param_substitutions,
            convert_types=True)

    stdout_linebuf_envvar = SetEnvironmentVariable('RCUTILS_LOGGING_BUFFERED_STREAM', '1')

    declare_namespace_cmd = DeclareLaunchArgument(
        'namespace',
        default_value='',
        description='Top-level namespace')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true')

    declare_autostart_cmd = DeclareLaunchArgument(
        'autostart', default_value='true',
        description='Automatically startup the nav2 stack')

    declare_params_file_cmd = DeclareLaunchArgument(
        'params_file',
        default_value=os.path.join(my_nav2_bringup_dir, 'config', 'nav2_params.yaml'),
        description='Full path to the ROS2 parameters file to use')

    declare_bt_xml_cmd = DeclareLaunchArgument(
        'default_bt_xml_filename',
        default_value=os.path.join(
            get_package_share_directory('nav2_bt_navigator'),
            'behavior_trees', 'navigate_w_replanning_and_recovery.xml'),
        description='Full path to the behavior tree xml file to use')

    declare_map_subscribe_transient_local_cmd = DeclareLaunchArgument(
        'map_subscribe_transient_local', default_value='false',
        description='Whether to set the map subscriber QoS profile to transient local')

    # Add here the VSLAM localization node or similar
    # In a real scenario, VSLAM (from Chapter 9) would publish to /odom or /tf
    # and /initialpose might be used. For simplicity, we assume VSLAM provides accurate /odom
    # and Nav2 consumes it.
    
    # Nav2 Lifecycle Manager
    nav_group = GroupAction([
        stdout_linebuf_envvar,
        Node(
            package='nav2_controller',
            executable='controller_server',
            output='screen',
            parameters=[configured_params],
            remappings=[('cmd_vel', '/cmd_vel')],
            arguments=['--ros-args', '--log-level', 'info'],
        ),
        Node(
            package='nav2_planner',
            executable='planner_server',
            name='planner_server',
            output='screen',
            parameters=[configured_params],
            arguments=['--ros-args', '--log-level', 'info'],
        ),
        Node(
            package='nav2_recoveries',
            executable='recoveries_server',
            name='recoveries_server',
            output='screen',
            parameters=[configured_params],
            arguments=['--ros-args', '--log-level', 'info'],
        ),
        Node(
            package='nav2_bt_navigator',
            executable='bt_navigator',
            name='bt_navigator',
            output='screen',
            parameters=[configured_params],
            arguments=['--ros-args', '--log-level', 'info'],
        ),
        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_navigation',
            output='screen',
            arguments=['--ros-args', '--log-level', 'info'],
            parameters=[{'autostart': autostart,
                         'node_names': lifecycle_nodes}]
        )
    ])

    # Bring up the nav2 stack
    return LaunchDescription([
        declare_namespace_cmd,
        declare_use_sim_time_cmd,
        declare_autostart_cmd,
        declare_params_file_cmd,
        declare_bt_xml_cmd,
        declare_map_subscribe_transient_local_cmd,
        nav_group
    ])
```
*(Note: This launch file is a simplified version of `nav2_bringup` and assumes the robot's URDF, `robot_state_publisher`, and `odom` source (e.g., from VSLAM or Gazebo's diff_drive_controller) are already handled externally. It does not include `map_server` or `amcl` as we're focusing on Nav2's core planning based on VSLAM-provided odometry.)*

### Step 5: Configure `CMakeLists.txt` to Install Config and Launch Files

Open `my_nav2_bringup/CMakeLists.txt`.
Add the following lines to install the `config` and `launch` directories:

```cmake
install(DIRECTORY config
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)
```
You can place these after `ament_export_dependencies(nav2_bringup launch_ros)`.

### Part 2: Running Nav2 with Isaac Sim and VSLAM

### Step 6: Build the Nav2 Configuration Package

Inside your Isaac ROS Docker environment (or your ROS 2 development machine):
```bash
cd ~/ros2_ws
colcon build --packages-select my_nav2_bringup
source install/setup.bash
```

### Step 7: Launch Isaac Sim, VSLAM, and Nav2

1.  **Launch Isaac Sim**: Start Isaac Sim with your mobile robot (e.g., Carter) from Chapter 9. Ensure the ROS 2 Bridge is active and publishing sensor data required for VSLAM (e.g., camera, IMU).
2.  **Launch VSLAM**: In your Isaac ROS Docker environment, launch the VSLAM node (e.g., `ros2 launch isaac_ros_visual_slam isaac_ros_visual_slam_carter.launch.py`). This should publish `odom` information (or a similar pose estimate).
3.  **Launch Nav2**: In a *separate* terminal within your Isaac ROS Docker environment, launch the Nav2 stack:
    ```bash
    ros2 launch my_nav2_bringup nav2_bringup.launch.py use_sim_time:=true
    ```
4.  **Launch Rviz2**: In your Ubuntu host machine (not in the Docker container), source your ROS 2 environment and launch Rviz2:
    ```bash
    source /opt/ros/humble/setup.bash
    rviz2
    ```
    Configure Rviz2:
    *   Set `Fixed Frame` to `map` (or `odom`).
    *   Add `RobotModel` display.
    *   Add `Map` display (if you have a map).
    *   Add `Path` display (for global and local plans: `/planner_server/global_plan`, `/controller_server/local_plan`).
    *   Add `Costmap` displays (for global and local costmaps).
    *   Add `Pose` display for `/amcl_pose` (from AMCL localization, if used).

### Step 8: Send Navigation Goals

With Nav2 running and Rviz2 displaying your robot and maps, you can send navigation goals.
In Rviz2, use the "2D Goal Pose" tool:
1.  Click the "2D Goal Pose" button.
2.  Click on a desired target location in the map and drag to set the robot's final orientation.
The robot should then start navigating autonomously to that goal.

## Deep Dive: Tuning Nav2 for Optimal Performance

Tuning Nav2 parameters is crucial for optimal performance, especially in diverse environments and with different robot kinematics.

*   **Costmap Parameters**:
    *   `update_frequency`, `publish_frequency`: Control how often costmaps are updated and published.
    *   `inflation_radius`: The radius around obstacles in which costs increase. A larger radius makes the robot keep a greater distance.
    *   `footprint`: Accurately define your robot's shape to ensure safe planning.
*   **Planner Parameters**:
    *   `tolerance`: How close the robot needs to get to the global path.
    *   `min_x_velocity_threshold`: Minimum linear velocity.
    *   `max_vel_x`, `max_vel_theta`: Maximum linear and angular velocities.
*   **Controller Parameters**:
    *   `min_vel_x`, `max_vel_x`, `max_vel_theta`: Similar to planners, but for the local controller.
    *   `xy_goal_tolerance`, `yaw_goal_tolerance`: How precisely the robot needs to reach the final goal position and orientation.
    *   `transform_tolerance`: Tolerance for TF lookups.

Nav2 provides extensive documentation for tuning these parameters. It often involves an iterative process of experimentation and observation.

## Troubleshooting: Nav2 Path Planning Issues

1.  **Issue**: Robot does not move after sending a goal.
    *   **Cause**: Incorrect localization, costmap issues, planner/controller configuration errors, or a stuck behavior tree.
    *   **Solution**:
        *   Verify localization: Ensure `/odom` is being published correctly (e.g., from VSLAM) and `robot_state_publisher` is running.
        *   Check costmaps in Rviz2: Ensure they are updated and reflect the environment.
        *   Check Nav2 logs: Look for errors from `planner_server` or `controller_server`.
        *   Verify `cmd_vel` output: Use `ros2 topic echo /cmd_vel` to see if the controller is sending velocity commands.
2.  **Issue**: Robot gets stuck frequently or exhibits oscillatory behavior.
    *   **Cause**: Local planner parameters are too aggressive or too conservative, or incorrect `inflation_radius`.
    *   **Solution**: Tune `inflation_radius` in costmaps. Adjust controller parameters like `max_vel_x`, `max_vel_theta`, and goal tolerances. Consider different local planner plugins.
3.  **Issue**: Global path is generated through obstacles.
    *   **Cause**: Static map not loaded correctly, global costmap not updated, or planner configuration issue.
    *   **Solution**: Ensure your map is being published (if using `map_server`). Verify `global_costmap` in Rviz2. Check global planner parameters in `nav2_params.yaml`.
4.  **Issue**: Nav2 nodes fail to start or crash.
    *   **Cause**: Incorrect parameter file paths, missing dependencies, or conflicting configurations.
    *   **Solution**: Check `nav2_params.yaml` path in the launch file. Ensure all Nav2 packages are installed. Review the error messages in the terminal output carefully.
5.  **Issue**: `use_sim_time` related issues.
    *   **Cause**: Misalignment between simulation time and ROS 2 clock.
    *   **Solution**: Ensure `use_sim_time: true` is consistently set in all relevant Nav2 nodes' parameters (`nav2_params.yaml`) and in your `ros2 launch` command arguments.

## Practice Exercises

1.  **Explore Different Planners/Controllers**:
    *   Modify your `nav2_params.yaml` to experiment with different `default_planner_plugin` (e.g., `nav2_smac_planner::SmacPlanner`) and `default_controller_plugin` (e.g., `nav2_mppi_controller::MPPIController`).
    *   Observe how these changes affect the robot's path generation and local navigation behavior.
2.  **Obstacle Avoidance Test**:
    *   In Isaac Sim, add dynamic obstacles (e.g., a simple cube that moves) to your robot's environment.
    *   Send a navigation goal and observe how Nav2 handles obstacle avoidance. Tune costmap parameters (`inflation_radius`) if the robot collides or gets stuck.
3.  **Goal Reaching Precision**:
    *   Experiment with `xy_goal_tolerance` and `yaw_goal_tolerance` parameters in your `nav2_params.yaml`.
    *   Observe how these changes affect the robot's precision in reaching the final goal pose.

## Summary

In this chapter, you've mastered autonomous navigation with the Nav2 stack:
- You gained a deep understanding of Nav2's modular architecture.
- You configured global and local planners for path generation and obstacle avoidance.
- You learned to utilize costmaps for environmental representation.
- You integrated Nav2 with VSLAM localization to achieve autonomous robot movement.
- You explored techniques for troubleshooting common Nav2 issues.

You can now confidently command your simulated mobile robot to navigate complex environments autonomously.

## Next Steps

You have now completed Module 3, equipping your robot with an AI brain capable of perception and navigation. In the next module, "Vision-Language-Action," you will learn to integrate large language models with your robotic system to enable natural language interaction and cognitive planning.

➡️ Continue to [Module 4: Vision-Language-Action](../04-vision-language-action/index.md)

## Additional Resources
-   [Nav2 Documentation](https://navigation.ros.org/)
-   [Nav2 Tutorials](https://navigation.ros.org/tutorials/index.html)
-   [ROS 2 Behavior Trees](https://www.behaviortree.dev/ros2_integration/)
