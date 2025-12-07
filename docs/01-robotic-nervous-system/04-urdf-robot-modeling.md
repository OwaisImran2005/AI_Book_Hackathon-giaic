# Chapter 4: URDF Robot Modeling

:::info Chapter Info
**Module**: The Robotic Nervous System | **Duration**: 4 hours | **Difficulty**: Intermediate
:::

## Learning Objectives
By the end of this chapter, you will:
1. Understand the purpose and structure of URDF (Unified Robot Description Format) files.
2. Be able to define a robot's kinematic and visual properties using URDF.
3. Learn to incorporate collision models for realistic simulation.
4. Gain proficiency in visualizing URDF models in ROS 2.

## Prerequisites
- Completed Chapter 3: ROS 2 Python Development, with a good grasp of ROS 2 concepts and Python development.
- Basic understanding of 3D geometry concepts (e.g., coordinate systems, transformations).

## What You'll Build
In this chapter, you will build a complete URDF model of a simple robotic arm, specifically a two-link manipulator. This model will include:
- Defined links (physical segments of the robot).
- Defined joints (connections between links, allowing motion).
- Visual properties (how the robot looks).
- Collision properties (how the robot interacts with the environment).

---

## Introduction: Describing Your Robot

Before a robot can move, perceive, or interact with its environment, we need a precise way to describe its physical characteristics. This description is crucial for various aspects of robotics, including:

*   **Kinematics**: Understanding how the robot's joints and links move in relation to each other.
*   **Dynamics**: Simulating the robot's motion under various forces and torques.
*   **Visualization**: Rendering a realistic representation of the robot in simulation and graphical tools.
*   **Collision Detection**: Preventing the robot from self-colliding or colliding with its environment.
*   **Path Planning**: Generating collision-free trajectories for the robot to follow.

In the ROS ecosystem, the **Unified Robot Description Format (URDF)** serves as the standard for describing a robot's physical structure. URDF is an XML-based file format that allows you to define the kinematic and dynamic properties, visual appearance, and collision models of a robot. It's a powerful tool that enables seamless integration of your robot model across different ROS tools and simulation environments.

While URDF is excellent for describing the robot itself, it's typically used in conjunction with other formats like **SRDF (Semantic Robot Description Format)** for more complex aspects like joint groups, end-effectors, and collision checking, and **Xacro (XML Macros)** to make URDF files more modular and readable. In this chapter, we will focus on the fundamentals of URDF, laying the groundwork for more advanced robot modeling.

You will learn how to break down your robot into its constituent parts (links) and define how these parts are connected (joints). We'll cover the essential tags within a URDF file and walk through the process of creating a model for a simple robotic arm. By the end, you'll be able to create functional URDF descriptions that can be visualized and used in ROS 2-based applications.

## Core Concepts: The Anatomy of a URDF File

A URDF file is an XML document structured around two primary elements: `<link>` and `<joint>`. These elements define the rigid bodies of your robot and how they are connected.

### 1. The `<robot>` Tag

The entire URDF document is encapsulated within a single `<robot>` tag, which has a mandatory `name` attribute.

```xml
<robot name="my_robot">
  <!-- Links and Joints go here -->
</robot>
```

### 2. Links: The Rigid Bodies

A `<link>` element defines a rigid body part of your robot. Each link represents a segment (e.g., a base, a forearm, a gripper finger) and has properties related to its physical characteristics and how it appears visually. A link must have a `name` attribute.

Inside a `<link>` tag, you can define three optional but crucial sub-elements:

*   **`<visual>`**: Describes how the link looks.
    *   **`<geometry>`**: Defines the shape of the link (e.g., `box`, `cylinder`, `sphere`, or `mesh` for custom 3D models).
        ```xml
        <visual>
          <geometry>
            <box size="0.1 0.1 0.5" />
          </geometry>
          <material name="blue">
            <color rgba="0 0 0.8 1" />
          </material>
        </visual>
        ```
    *   **`<origin>`**: Specifies the `xyz` (position) and `rpy` (roll, pitch, yaw rotation) offset of the visual element relative to the link's origin.
    *   **`<material>`**: Defines the color or texture of the link.

*   **`<collision>`**: Describes the physical shape of the link used for collision detection. It also contains `<geometry>` and `<origin>` tags, which are typically simplified versions of their visual counterparts to reduce computational load during collision checks.
    ```xml
    <collision>
      <geometry>
        <box size="0.1 0.1 0.5" />
      </geometry>
    </collision>
    ```
*   **`<inertial>`**: Defines the mass and inertia properties of the link, essential for physics simulation.
    *   **`<mass>`**: The mass of the link in kilograms.
    *   **`<inertia>`**: A 3x3 inertia matrix defined by its 6 unique components (`ixx`, `ixy`, `ixz`, `iyy`, `iyz`, `izz`). For simple shapes, you can use online calculators or approximations.
        ```xml
        <inertial>
          <mass value="1.0" />
          <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01" />
        </inertial>
        ```

### 3. Joints: The Connections

A `<joint>` element defines the connection between two links, specifying how one link moves relative to another. A joint must have a `name` and a `type` attribute.

Key attributes and sub-elements of a `<joint>` tag:

*   **`type`**: Defines the degrees of freedom of the joint. Common types include:
    *   `fixed`: No movement between the links (e.g., the base of a robot to the world).
    *   `revolute`: Rotation around a single axis (e.g., an elbow joint). Has `limit` tags for min/max angle.
    *   `continuous`: Revolute joint with no upper or lower limits.
    *   `prismatic`: Translational movement along a single axis (e.g., a linear actuator). Has `limit` tags for min/max position.
*   **`<parent>`**: Specifies the `link` that this joint is attached to (the link "closer to the base").
*   **`<child>`**: Specifies the `link` that this joint connects (the link "further from the base").
*   **`<origin>`**: Defines the `xyz` (position) and `rpy` (roll, pitch, yaw rotation) offset of the child link's frame relative to the parent link's frame. This is crucial for positioning the child link correctly.
*   **`<axis>`**: Defines the axis of rotation for revolute/continuous joints or the axis of translation for prismatic joints.
*   **`<limit>`**: For `revolute` and `prismatic` joints, defines the `lower` and `upper` bounds of motion, `effort` (max force/torque), and `velocity` (max joint velocity).
*   **`<calibration>`**: Defines the hardware calibration limits.
*   **`<dynamics>`**: Defines friction and damping properties.
*   **`<safety_controller>`**: Defines parameters for a safety controller.

## Hands-On Tutorial: Modeling a Two-Link Manipulator

We will create a URDF model for a simple robotic arm with two revolute joints. This will illustrate the concepts of links, joints, and their properties.

### Robot Description

Our robotic arm will consist of:
*   **`base_link`**: A fixed base.
*   **`link1`**: Connected to the `base_link` by `joint1`.
*   **`link2`**: Connected to `link1` by `joint2`.

Both `joint1` and `joint2` will be `revolute` joints, allowing rotation around the Z-axis.

### Step 1: Create a ROS 2 Package for Robot Description

Navigate to your ROS 2 workspace `src` directory (e.g., `~/ros2_ws/src`).
Create a new package called `my_robot_description`:

```bash
ros2 pkg create --build-type ament_cmake my_robot_description
```
We use `ament_cmake` because URDF files are typically processed by CMake.

### Step 2: Define the URDF File

Create a `urdf` directory inside your `my_robot_description` package:
```bash
mkdir my_robot_description/urdf
```
Create the file `my_robot_description/urdf/two_link_arm.urdf` with the following content:

```xml
<?xml version="1.0"?>
<robot name="two_link_arm">

  <!-- ============================================= -->
  <!-- BASE LINK                                     -->
  <!-- This is the fixed base of the robot           -->
  <!-- ============================================= -->
  <link name="base_link">
    <visual>
      <geometry>
        <cylinder radius="0.05" length="0.1" />
      </geometry>
      <material name="grey">
        <color rgba="0.7 0.7 0.7 1" />
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.05" length="0.1" />
      </geometry>
    </collision>
    <inertial>
      <mass value="0.1" />
      <inertia ixx="0.0001" ixy="0.0" ixz="0.0" iyy="0.0001" iyz="0.0" izz="0.0001" />
    </inertial>
  </link>

  <!-- ============================================= -->
  <!-- JOINT 1: Connects base_link to link1          -->
  <!-- ============================================= -->
  <joint name="joint1" type="revolute">
    <parent link="base_link" />
    <child link="link1" />
    <origin xyz="0 0 0.05" rpy="0 0 0" /> <!-- Offset to top of base_link -->
    <axis xyz="0 0 1" /> <!-- Rotation around Z-axis -->
    <limit lower="-1.57" upper="1.57" effort="100" velocity="0.5" />
    <dynamics friction="0.1" damping="0.01" />
  </joint>

  <!-- ============================================= -->
  <!-- LINK 1                                        -->
  <!-- First arm segment                             -->
  <!-- ============================================= -->
  <link name="link1">
    <visual>
      <origin xyz="0 0 0.25" rpy="0 0 0" /> <!-- Visual centered on link, so offset by half length -->
      <geometry>
        <box size="0.05 0.05 0.5" />
      </geometry>
      <material name="blue">
        <color rgba="0 0 0.8 1" />
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 0.25" rpy="0 0 0" />
      <geometry>
        <box size="0.05 0.05 0.5" />
      </geometry>
    </collision>
    <inertial>
      <mass value="0.5" />
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.001" />
    </inertial>
  </link>

  <!-- ============================================= -->
  <!-- JOINT 2: Connects link1 to link2              -->
  <!-- ============================================= -->
  <joint name="joint2" type="revolute">
    <parent link="link1" />
    <child link="link2" />
    <origin xyz="0 0 0.5" rpy="0 0 0" /> <!-- Offset to end of link1 -->
    <axis xyz="0 0 1" /> <!-- Rotation around Z-axis -->
    <limit lower="-1.57" upper="1.57" effort="100" velocity="0.5" />
    <dynamics friction="0.1" damping="0.01" />
  </joint>

  <!-- ============================================= -->
  <!-- LINK 2                                        -->
  <!-- Second arm segment                            -->
  <!-- ============================================= -->
  <link name="link2">
    <visual>
      <origin xyz="0 0 0.25" rpy="0 0 0" />
      <geometry>
        <box size="0.05 0.05 0.5" />
      </geometry>
      <material name="green">
        <color rgba="0 0.8 0 1" />
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 0.25" rpy="0 0 0" />
      <geometry>
        <box size="0.05 0.05 0.5" />
      </geometry>
    </collision>
    <inertial>
      <mass value="0.3" />
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.001" />
    </inertial>
  </link>

</robot>
```

### Step 3: Configure `CMakeLists.txt` to Install the URDF

Open `my_robot_description/CMakeLists.txt`.
Add the following lines to install the `urdf` directory:

```cmake
install(DIRECTORY urdf
  DESTINATION share/${PROJECT_NAME}
)
```
You can place this after `ament_export_dependencies(rclpy)`.

### Step 4: Visualize the URDF Model

To visualize your URDF model, you need to build the package and then use `rviz2`.

1.  **Build the package**: Navigate to your workspace root (`~/ros2_ws`) and run:
    ```bash
    colcon build --packages-select my_robot_description
    source install/setup.bash
    ```
2.  **Launch `rviz2` with `joint_state_publisher_gui`**:
    ```bash
    ros2 launch urdf_tutorial display.launch.py model:=$(ros2 pkg prefix my_robot_description)/share/my_robot_description/urdf/two_link_arm.urdf
    ```
    *(Note: `urdf_tutorial` is a standard ROS 2 package that provides tools for URDF visualization. Make sure it's installed: `sudo apt install ros-humble-urdf-tutorial`)*

    This command will launch `rviz2` and a GUI that allows you to control the joints of your robotic arm. You should see your two-link arm model in the `rviz2` window, and you can manipulate `joint1` and `joint2` using the sliders.

### Step 5: Understanding `robot_state_publisher`

The `robot_state_publisher` is a ROS 2 node that reads the URDF file and the current joint states (from `joint_state_publisher`) and publishes the TF (Transform) tree of the robot. This TF tree describes the relationship between all the links of your robot and is crucial for navigation, perception, and manipulation.
The `display.launch.py` used above already includes `robot_state_publisher`.

## Deep Dive: Beyond URDF - Xacro and SDF

While URDF is powerful for describing a single robot, it has some limitations:

1.  **No Modularity**: URDF files can become very long and repetitive for complex robots with many similar parts.
2.  **No Conditional Logic**: You cannot use conditional statements to define different robot configurations.
3.  **Robot Only**: URDF is only for the robot; it cannot describe the environment or non-robot objects.

To address these, ROS developers often use:

*   **Xacro (XML Macros)**: Xacro is an XML macro language that allows you to write more modular, readable, and reusable URDF files. You can define macros for common robot components (e.g., a wheel, a sensor) and reuse them multiple times, passing parameters to customize them. This significantly reduces duplication and improves maintainability. Xacro files are processed into standard URDF before being used by ROS 2 tools.
*   **SDF (Simulation Description Format)**: SDF is a more comprehensive XML format for describing robots, environments, and objects for use in simulators like Gazebo. Unlike URDF, SDF can describe entire worlds, including terrain, lights, static objects, and multiple robots. It's often preferred for full simulation environments. You can often convert URDF to SDF for use in Gazebo.

For complex robot designs and rich simulation environments, a common workflow is to use Xacro to generate modular URDF files, and then use these URDF files within an SDF world for simulation.

## Troubleshooting: URDF Robot Modeling Issues

1.  **Issue**: `rviz2` shows "No tf data" or parts of the robot are missing.
    *   **Cause**: `robot_state_publisher` or `joint_state_publisher` are not running, or there's an issue with the TF tree.
    *   **Solution**: Ensure you launched `display.launch.py` correctly. Check `ros2 node list` for `robot_state_publisher` and `joint_state_publisher_gui`. Use `rqt_tf_tree` to visualize the TF tree and identify broken links.
2.  **Issue**: URDF parsing error (XML parsing failed).
    *   **Cause**: Syntax error in your URDF XML file.
    *   **Solution**: Carefully check your `two_link_arm.urdf` file for unmatched tags, typos, or incorrect attribute values. Use an XML validator tool if necessary. The error message from ROS 2 usually points to the line number.
3.  **Issue**: Joints don't move or move unexpectedly in `joint_state_publisher_gui`.
    *   **Cause**: Incorrect `lower`/`upper` limits, `axis` definition, or `origin` values in your `<joint>` tags.
    *   **Solution**: Double-check the `limit` values. Ensure the `axis` corresponds to the intended rotation/translation direction. Verify `origin` offsets are correct for placing the child link relative to the parent.
4.  **Issue**: Robot appears distorted or parts are not in the correct position.
    *   **Cause**: Incorrect `origin` values in `<visual>` or `<joint>` tags.
    *   **Solution**: The `origin` tag is critical. For `<visual>`, it positions the visual mesh relative to the link's origin. For `<joint>`, it positions the child link's origin relative to the parent. Adjust `xyz` and `rpy` values carefully.
5.  **Issue**: `ros2 launch urdf_tutorial display.launch.py` fails to find `urdf_tutorial`.
    *   **Cause**: `urdf_tutorial` package is not installed.
    *   **Solution**: Install it: `sudo apt install ros-humble-urdf-tutorial`.

## Practice Exercises

1.  **Extend the Robotic Arm**:
    *   Modify `two_link_arm.urdf` to add a third link (`link3`) and a corresponding `joint3`.
    *   Make `joint3` a revolute joint.
    *   Add a simple end-effector (e.g., a small box or cylinder) to `link3`.
    *   Visualize your extended arm in `rviz2`.
2.  **Change Joint Type**:
    *   Modify `joint2` in `two_link_arm.urdf` from `revolute` to `prismatic`.
    *   Adjust the `limit` values for a prismatic joint (e.g., `lower="0.0" upper="0.2"` for linear movement).
    *   Visualize the change in `rviz2`.
3.  **Add Collision Geometry**:
    *   For `link1` and `link2`, ensure their `<collision>` geometries are a simplified version of their `<visual>` geometries. For example, if a visual is a complex mesh, the collision could be a simpler box or cylinder that encloses it.
    *   Experiment with making a visual element transparent (`rgba="R G B A"` where `A` is less than 1) and try to visualize the collision geometry in `rviz2` (by adding a "RobotModel" display and enabling "Show Collisions").

## Summary

In this chapter, you've gained a fundamental understanding of URDF for robot modeling:
- You learned about the `<link>` and `<joint>` elements and their properties.
- You built a URDF model for a two-link robotic arm.
- You visualized your robot model using `rviz2` and `joint_state_publisher_gui`.
- You explored the concepts of Xacro and SDF for more advanced robot descriptions.

This knowledge is crucial for defining your robot's physical presence in simulations and for real-world deployment.

## Next Steps

In the next module, "The Digital Twin," you will take your URDF models and bring them to life in powerful simulation environments like Gazebo and Unity.

➡️ Continue to [Module 2: The Digital Twin](../02-digital-twin/index.md)

## Additional Resources
-   [ROS 2 URDF Tutorial](https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/URDF-Main.html)
-   [ROS 2 Xacro Tutorial](https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/Using-Xacro-to-Clean-Up-a-URDF-File.html)
-   [SDF Format Specification](http://sdformat.org/spec)
