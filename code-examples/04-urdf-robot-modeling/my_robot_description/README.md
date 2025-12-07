# `my_robot_description` ROS 2 Package

This package contains the URDF (Unified Robot Description Format) model for a simple two-link robotic arm. It demonstrates the fundamental concepts of defining a robot's kinematic, visual, and collision properties using URDF. This example is part of Chapter 4: URDF Robot Modeling of the "Physical AI & Humanoid Robotics" book.

## Contents

-   `urdf/two_link_arm.urdf`: The URDF file defining the two-link robotic arm.

## Setup

1.  **Navigate to your ROS 2 Workspace**: Ensure you are in the `src` directory of your ROS 2 workspace (e.g., `~/ros2_ws/src`).
2.  **Clone this Repository**: Place this `my_robot_description` package within your ROS 2 workspace `src` directory.
    ```bash
    # Example: If your workspace is ~/ros2_ws
    cd ~/ros2_ws/src
    # Assuming you have cloned the main book's code-examples repository
    cp -r /path/to/ai-native-book/code-examples/04-urdf-robot-modeling/my_robot_description .
    ```
3.  **Install Dependencies**:
    ```bash
    rosdep install -i --from-path src --rosdistro humble -y
    ```
4.  **Build the Package**:
    ```bash
    cd ~/ros2_ws
    colcon build --packages-select my_robot_description
    ```
5.  **Source the Setup Files**:
    ```bash
    source install/setup.bash
    ```
6.  **Install `urdf_tutorial`**: If you haven't already, install the `urdf_tutorial` package which provides tools for URDF visualization.
    ```bash
    sudo apt install ros-humble-urdf-tutorial
    ```

## Usage

To visualize the `two_link_arm.urdf` model using `rviz2` and control its joints with a GUI:

```bash
ros2 launch urdf_tutorial display.launch.py model:=$(ros2 pkg prefix my_robot_description)/share/my_robot_description/urdf/two_link_arm.urdf
```

This command will launch `rviz2` and a `joint_state_publisher_gui`. You can manipulate the sliders in the GUI to move the joints of your robotic arm and observe the changes in `rviz2`.

## Verification

-   Observe the `rviz2` window to ensure your two-link arm model is displayed correctly.
-   Use the sliders in the `joint_state_publisher_gui` to move `joint1` and `joint2`, verifying that the arm moves as expected.
-   Check `ros2 node list` to see `robot_state_publisher` and `joint_state_publisher_gui` running.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
