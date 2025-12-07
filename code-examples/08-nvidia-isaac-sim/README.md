# Chapter 8: NVIDIA Isaac Sim Code Examples

This directory provides a guide for setting up NVIDIA Isaac Sim projects and integrating with ROS 2, as described in Chapter 8: NVIDIA Isaac Sim of the "Physical AI & Humanoid Robotics" book. Due to the nature of Isaac Sim's graphical interface and project structure, direct automated creation of a fully functional Isaac Sim project is not feasible via this workflow. Instead, this `README.md` outlines the necessary manual steps and provides code snippets for ROS 2 integration.

## Manual Setup Steps (Isaac Sim Project)

Please follow these steps to set up your Isaac Sim project and integrate with ROS 2:

### Part 1: Isaac Sim Setup

1.  **Install NVIDIA Omniverse Launcher**: Download and install the [NVIDIA Omniverse Launcher](https://www.nvidia.com/omniverse/) for your operating system.
2.  **Install Isaac Sim**:
    *   Open the NVIDIA Omniverse Launcher.
    *   Navigate to the "Exchange" tab, search for "Isaac Sim," and click "Install."
    *   Ensure Docker is running on your system.
3.  **Launch Isaac Sim**: Launch Isaac Sim from the Omniverse Launcher.

### Part 2: Import URDF Robot Model

1.  **Copy URDF to Isaac Sim**:
    *   Locate your `two_link_arm.urdf` file (from `~/ros2_ws/src/my_robot_description/urdf/`).
    *   Copy this file and any associated mesh files into a directory accessible by Isaac Sim (e.g., within the `Isaac Sim Apps/isaac_sim-<version>/standalone_examples/robots/` directory, or a custom directory you configure in Isaac Sim).
2.  **Open Isaac Sim**: Launch Isaac Sim.
3.  **Import URDF**:
    *   Go to `File > Import > URDF`.
    *   Navigate to your `two_link_arm.urdf` file and select it.
    *   Review the import settings (e.g., set `merge fixed joints` to `True` for cleaner hierarchy).
    *   Click "Import".
    Your two-link arm should now appear in the Isaac Sim viewport.

### Part 3: Creating a Simple Scene

1.  **Add a Ground Plane**: Go to `Create > Physics > Ground Plane`.
2.  **Add a Cube**: Go to `Create > Primitives > Cube`.
    *   Move the cube around using the transform tools in the toolbar.
3.  **Run Simulation**: Click the "Play" button in the toolbar to start the physics simulation. Your robot and cube should react to gravity.

### Part 4: ROS 2 Integration with Isaac Sim

1.  **Enable ROS 2 Bridge Extension**:
    *   In Isaac Sim, go to `Window > Extensions`.
    *   Search for `omni.isaac.ros2_bridge` and ensure it is enabled.
    *   Restart Isaac Sim if prompted.
2.  **Python Script for ROS 2 Control (Example)**:
    *   You can write Python scripts to control your robot in Isaac Sim via ROS 2. Here's an example of a simple ROS 2 node that could control a joint in Isaac Sim:

    ```python
    # This script would run outside Isaac Sim, in your ROS 2 environment
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import Float32

    class IsaacJointController(Node):
        def __init__(self):
            super().__init__('isaac_joint_controller')
            self.publisher_ = self.create_publisher(Float32, '/isaac_joint_command', 10)
            self.timer_ = self.create_timer(1.0, self.timer_callback)
            self.angle = 0.0
            self.direction = 1

        def timer_callback(self):
            msg = Float32()
            msg.data = self.angle
            self.publisher_.publish(msg)
            self.get_logger().info(f'Publishing Isaac joint command: {msg.data}')

            self.angle += self.direction * 0.1
            if self.angle > 1.0 or self.angle < -1.0: # Example range
                self.direction *= -1
                self.angle = max(-1.0, min(1.0, self.angle))

    def main(args=None):
        rclpy.init(args=args)
        node = IsaacJointController()
        rclpy.spin(node)
        node.destroy_node()
        rclpy.shutdown()

    if __name__ == '__main__':
        main()
    ```
    *   **In Isaac Sim Python Script Editor**: You would write Python code to subscribe to `/isaac_joint_command` and apply the received values to the `ArticulationBody` of your robot. Refer to Isaac Sim documentation for details on their Python API for joint control.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
