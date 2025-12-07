# Chapter 7: Unity Integration

:::info Chapter Info
**Module**: The Digital Twin | **Duration**: 4 hours | **Difficulty**: Advanced
:::

## Learning Objectives
By the end of this chapter, you will:
1. Understand the advantages of using Unity for high-fidelity robotics simulation.
2. Be able to set up a Unity project for ROS 2 integration using the `ROS-TCP-Connector`.
3. Learn to import URDF models into Unity and configure their physical properties using `ArticulationBody`.
4. Gain proficiency in establishing two-way communication between ROS 2 nodes and Unity.

## Prerequisites
- Completed Module 1 (Chapters 1-4) and Chapter 5: Gazebo Fundamentals.
- Basic familiarity with Unity Editor interface.
- A system with an NVIDIA GPU is highly recommended for optimal Unity performance, especially with high-fidelity graphics.

## What You'll Build
In this chapter, you will integrate your two-link robotic arm (from Chapter 4) into a Unity environment. This will involve:
- Creating a new Unity project and importing the necessary robotics packages.
- Importing and configuring your URDF robotic arm in Unity.
- Establishing ROS 2 communication to control the arm from a ROS node.

---

## Introduction: High-Fidelity Simulations with Unity

You've experienced the power of Gazebo for physics-accurate robot simulation. However, while Gazebo excels in simulating physics and sensors, there are scenarios where higher visual fidelity, advanced rendering capabilities, or integration with specific visualization tools are paramount. This is where a robust game engine like **Unity** becomes an invaluable asset for robotics development.

Unity is a versatile real-time 3D development platform widely used for games, architectural visualization, and interactive experiences. Its strength lies in its powerful rendering pipeline, extensive asset store, and ability to create highly realistic and visually rich environments. For robotics, Unity offers:

*   **High Visual Fidelity**: Create stunningly realistic environments and robot models, which is crucial for training perception algorithms and human-robot interaction studies.
*   **Advanced Physics Engine**: Unity's PhysX engine provides robust physics simulation, comparable to dedicated physics engines.
*   **Integrated Development Environment**: A comprehensive editor that simplifies scene composition, asset management, and scripting.
*   **Extensibility**: Through C# scripting and dedicated robotics packages, Unity can be extended to support complex robotics workflows.
*   **ROS Integration**: Official and community-supported packages enable seamless communication between Unity and ROS 2.

In this chapter, we will guide you through integrating your ROS 2-controlled robotic arm into a Unity environment. You will learn to set up a Unity project, import your URDF model, and leverage Unity's `ArticulationBody` component for accurate joint control. Crucially, we will establish robust two-way communication between your ROS 2 nodes and the Unity simulation, allowing you to command your robot from ROS and receive simulated sensor feedback from Unity. By combining ROS 2's powerful robotics ecosystem with Unity's high-fidelity simulation capabilities, you will unlock a new level of realism and control for your Physical AI projects.

## Core Concepts: Unity for Robotics

Unity's approach to robotics simulation leverages its game development capabilities while adapting them for the specific demands of robot control and data generation.

### 1. Unity Robotics Packages

The Unity Robotics ecosystem provides several key packages that facilitate ROS 2 integration:

*   **`ROS-TCP-Connector`**: The primary package for establishing a TCP/IP connection between a Unity application and a ROS 2 system. It allows Unity to publish and subscribe to ROS 2 topics, call services, and interact with the ROS 2 graph.
*   **`ROS-Unity-Integration`**: A meta-package that brings together various tools, including the `ROS-TCP-Connector`, and provides examples for common robotics tasks.
*   **`URDF-Importer`**: An essential tool for importing robots described in URDF files directly into Unity, automatically generating the necessary `ArticulationBody` components and colliders.
*   **`Robotics-Visualizations`**: Provides tools within Unity to visualize ROS 2 data types (e.g., TF transforms, sensor messages) directly in the editor or during runtime.

These packages are available through Unity's Package Manager, simplifying their installation and management.

### 2. `ArticulationBody`: Simulating Robot Joints

Unity's standard `Rigidbody` component is suitable for simulating individual rigid bodies, but for kinematic chains like robotic arms or wheeled robots, the `ArticulationBody` component is far more powerful and accurate.

*   **Kinematic Chains**: `ArticulationBody` is designed to simulate interconnected rigid bodies with configurable joints, forming a kinematic chain.
*   **Joint Types**: Supports various joint types (Fixed, Prismatic, Revolute, Spherical) with configurable limits, drives (motors), and damping/friction properties.
*   **Physics Accuracy**: Provides more stable and accurate simulation of complex joint interactions compared to manually linking `Rigidbody` components.
*   **Drives**: Each joint can have a configurable drive (e.g., Position, Velocity, or Force drive) that allows you to control the joint's movement.

When you import a URDF model using the `URDF-Importer`, it automatically converts URDF joints and links into Unity `GameObject`s with `ArticulationBody` components attached.

### 3. ROS 2 Communication in Unity

The `ROS-TCP-Connector` enables seamless communication:

*   **Publisher**: A Unity script can create a publisher to send messages (e.g., simulated sensor data) to a ROS 2 topic.
*   **Subscriber**: A Unity script can create a subscriber to receive messages (e.g., robot commands) from a ROS 2 topic.
*   **Services**: Unity can act as a service client or server, making or responding to requests.
*   **Message Generation**: The `ROS-TCP-Connector` includes a message generation tool that converts ROS 2 `.msg`, `.srv`, and `.action` definitions into C# classes that can be used directly in Unity scripts.

This integration allows your existing ROS 2 control nodes (written in Python or C++) to directly command a robot simulated in Unity and receive its simulated sensor feedback.

## Hands-On Tutorial: Unity Control of a Two-Link Arm

We will create a Unity project, import your two-link robotic arm, and set up ROS 2 communication to control its joints.

### Part 1: Unity Project Setup

### Step 1: Install Unity and Robotics Packages

1.  **Install Unity Hub**: Download and install Unity Hub from the official Unity website.
2.  **Install Unity Editor**: Install a compatible version of the Unity Editor (e.g., 2022.3 LTS or newer).
3.  **Create New Project**: Open Unity Hub, click "New Project", select a 3D Core template, and name it `MyRobotSimulation`.
4.  **Install Robotics Packages**:
    *   Open your Unity project.
    *   Go to `Window > Package Manager`.
    *   Click the `+` icon in the top-left corner and select "Add package from git URL...".
    *   Add the following packages one by one:
        *   `https://github.com/Unity-Technologies/ROS-TCP-Connector.git`
        *   `https://github.com/Unity-Technologies/URDF-Importer.git`
        *   `https://github.com/Unity-Technologies/ROS-Unity-Integration.git` (optional, for examples)

### Step 2: Import URDF Robot Model

1.  **Export URDF**: Ensure your `my_robot_description` ROS 2 package (from Chapter 4) is built and sourced.
2.  **Copy URDF**: Copy your `two_link_arm.urdf` file (and any associated meshes) into your Unity project's `Assets` folder (e.g., `Assets/URDFs/two_link_arm.urdf`).
3.  **Import with URDF Importer**:
    *   In Unity, go to `Robotics > URDF Importer > Import URDF`.
    *   Select your `two_link_arm.urdf` file.
    *   Ensure "Import as Articulation Body" is checked.
    *   Click "Import".
    Your robotic arm should now appear in your Unity scene as a `GameObject` hierarchy with `ArticulationBody` components.

### Step 3: Setup ROS Connection in Unity

1.  **Add `ROSConnection` Manager**:
    *   In the Unity Hierarchy window, right-click and select `Create Empty`. Rename it to `ROSConnectionManager`.
    *   Select this `GameObject`. In the Inspector window, click "Add Component" and search for `ROSConnection`.
    *   Set the `ROS IP Address` to your ROS 2 machine's IP address (or `127.0.0.1` if running ROS 2 locally).
    *   Set the `ROS Port` to `10000` (default for `ROS-TCP-Connector`).
2.  **Generate ROS 2 Messages**:
    *   In Unity, go to `Robotics > ROS TCP Connector > Generate ROS Messages`.
    *   This tool will automatically find your ROS 2 workspace and generate C# message types from your `.msg`, `.srv`, and `.action` files. This step is crucial for Unity scripts to understand ROS 2 data.
    *   *(Note: For our two-link arm, we'll mainly use standard ROS 2 messages for control.)*

### Part 2: ROS 2 Control in Unity

### Step 4: Create a C# Script for Joint Control

1.  **Create C# Script**: In your `Assets` folder, create a new C# script (e.g., `ArmController.cs`).
2.  **Attach to Robot**: Drag and drop this script onto the root `GameObject` of your imported robotic arm in the Hierarchy.
3.  **Implement Joint Control**: Open `ArmController.cs` and replace its content with the following:

```csharp
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Std; // For Float32 message (or your custom message)
// Add your custom message type if you defined one in ROS 2, e.g.:
// using RosMessageTypes.MyRobotController; // For RobotCommand message

public class ArmController : MonoBehaviour
{
    ROSConnection ros;
    public string rosTopicName = "joint_command"; // ROS topic to subscribe to
    public string jointName = "joint1"; // Name of the joint to control (e.g., joint1)
    
    private ArticulationBody articulationBody;

    void Start()
    {
        ros = ROSConnection.Get  Instance();
        // Register as a subscriber
        ros.Subscribe<Float32Msg>(rosTopicName, ReceiveJointCommand);
        // If using custom message:
        // ros.Subscribe<RobotCommandMsg>(rosTopicName, ReceiveRobotCommand);

        // Find the ArticulationBody for the specified joint
        articulationBody = FindArticulationBodyRecursive(transform, jointName);

        if (articulationBody == null)
        {
            Debug.LogError($"ArticulationBody for joint '{jointName}' not found!");
            enabled = false; // Disable script if joint not found
        } else {
            // Configure joint drive
            var jointDrive = articulationBody.xDrive;
            jointDrive.mode = ArticulationDriveMode.Position;
            jointDrive.stiffness = 10000;
            jointDrive.damping = 100;
            jointDrive.forceLimit = 100;
            articulationBody.xDrive = jointDrive;
        }
    }

    void ReceiveJointCommand(Float32Msg message)
    {
        if (articulationBody != null)
        {
            // Set the target position of the joint
            var jointDrive = articulationBody.xDrive;
            jointDrive.target = message.data;
            articulationBody.xDrive = jointDrive;
            Debug.Log($"Received command for {jointName}: {message.data}");
        }
    }

    // Helper function to find ArticulationBody by joint name recursively
    private ArticulationBody FindArticulationBodyRecursive(Transform parent, string name)
    {
        foreach (Transform child in parent)
        {
            if (child.name == name) // Joint names in Unity often match URDF joint names
            {
                ArticulationBody ab = child.GetComponent<ArticulationBody>();
                if (ab != null) return ab;
            }
            ArticulationBody found = FindArticulationBodyRecursive(child, name);
            if (found != null) return found;
        }
        return null;
    }
}
```
*(Note: This script is a basic example. You would need to create a separate script for each joint you want to control, or modify it to handle multiple joints and different message types.)*

### Part 3: ROS 2 Control Node (Python)

### Step 5: Create a ROS 2 Python Publisher

Create a new Python ROS 2 package (e.g., `unity_controller`) in your `~/ros2_ws/src`.
Create a node `joint_publisher.py` inside it.

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32 # For sending joint commands

class JointCommandPublisher(Node):
    def __init__(self):
        super().__init__('joint_command_publisher')
        self.publisher_ = self.create_publisher(Float32, 'joint_command', 10)
        self.timer_ = self.create_timer(1.0, self.timer_callback) # Publish every second
        self.angle = 0.0
        self.direction = 1

    def timer_callback(self):
        msg = Float32()
        msg.data = self.angle
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing joint command: {msg.data}')

        # Oscillate angle between -PI/2 and PI/2
        self.angle += self.direction * 0.1
        if self.angle > 1.57 or self.angle < -1.57:
            self.direction *= -1
            self.angle = max(-1.57, min(1.57, self.angle)) # Clamp value


def main(args=None):
    rclpy.init(args=args)
    node = JointCommandPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```
Add entry point in `setup.py` for `joint_publisher = unity_controller.joint_publisher:main`.

### Part 4: Running the Simulation

1.  **Start ROS 2 TCP Endpoint**: In your ROS 2 machine (Ubuntu terminal), run the `ros_tcp_endpoint` to establish the connection that Unity will use:
    ```bash
    ros2 launch ros_tcp_endpoint endpoint.launch.py
    ```
    *(Note: You might need to install `ros_tcp_endpoint` if it's not present: `sudo apt install ros-humble-ros-tcp-endpoint`)*
2.  **Start Unity ROS 2 Publisher**: In a *separate* ROS 2 terminal, launch your Python node:
    ```bash
    ros2 run unity_controller joint_publisher
    ```
3.  **Run Unity Simulation**: In the Unity Editor, click the "Play" button.

You should see the robotic arm in Unity moving in response to the commands from your ROS 2 Python node!

## Deep Dive: Advanced Unity Robotics Features

Unity offers many advanced features for more complex robotics simulations:

*   **Perception Sensors**: Configure highly realistic camera, LiDAR, and other sensors directly within Unity. These can be integrated with ROS 2 to publish sensor data.
*   **Domain Randomization**: Randomize scene properties (textures, lighting, object positions) to improve the robustness and generalization of AI models trained on synthetic data.
*   **Machine Learning Agents (ML-Agents)**: Unity's framework for training intelligent agents using reinforcement learning. Can be integrated with ROS 2 for complex behaviors.
*   **ROS 2 Bridge for URDF Import**: Provides more control over the URDF import process, including options for physics settings, colliders, and joint drive configurations.
*   **Robotics Visualizations Package**: For visualizing ROS 2 data (e.g., TF transforms, point clouds, odometry) directly within Unity.

## Troubleshooting: Unity Integration Issues

1.  **Issue**: Unity cannot connect to ROS 2 (`ROSConnectionManager` shows errors).
    *   **Cause**: Incorrect IP address/port, `ros_tcp_endpoint` not running, or firewall issues.
    *   **Solution**: Double-check `ROS IP Address` in `ROSConnectionManager` to match your ROS 2 machine's IP. Ensure `ros2 launch ros_tcp_endpoint endpoint.launch.py` is running. Temporarily disable firewalls to test.
2.  **Issue**: Robot arm does not move in Unity.
    *   **Cause**: Incorrect `jointName` in `ArmController.cs`, `ArticulationBody` not found, `ROSConnectionManager` not set up, or ROS 2 node not publishing.
    *   **Solution**: Verify `jointName` in your script matches the `GameObject` name of the joint in Unity. Check Unity Editor console for script errors. Ensure `joint_publisher` ROS 2 node is running and publishing (`ros2 topic echo /joint_command`).
3.  **Issue**: `RosMessageTypes` namespace not found in C# script.
    *   **Cause**: ROS 2 messages not generated in Unity, or script is in the wrong namespace.
    *   **Solution**: Go to `Robotics > ROS TCP Connector > Generate ROS Messages` in Unity. Ensure your C# script's `using` directives correctly match the generated message namespaces.
4.  **Issue**: `URDF Importer` fails or imports model incorrectly.
    *   **Cause**: Malformed URDF file, missing meshes, or incompatible Unity version.
    *   **Solution**: Validate your URDF file using `check_urdf`. Ensure all mesh files are correctly referenced and present in the Unity project `Assets` folder. Check Unity documentation for compatible URDF Importer versions.
5.  **Issue**: Unity simulation runs slowly or crashes.
    *   **Cause**: High polygon counts, unoptimized textures, complex physics interactions, or insufficient GPU resources.
    *   **Solution**: Simplify your 3D models. Optimize textures. Reduce the complexity of your Unity scene. Ensure your system meets recommended hardware specs, especially for GPU.

## Practice Exercises

1.  **Control the Second Joint**:
    *   Modify `ArmController.cs` to create a separate `ROSConnectionManager` and `ArmController` script instance for `joint2`.
    *   Create a new ROS 2 Python node that publishes commands for `joint2` to a different topic (e.g., `/joint_command2`).
    *   Run both ROS 2 publisher nodes and the Unity simulation to control both joints independently.
2.  **Publish Joint States from Unity**:
    *   Create a C# script in Unity that reads the current `ArticulationBody` joint positions of your arm.
    *   Use `ROSConnection` to publish these joint states to a ROS 2 topic (e.g., `/unity_joint_states`) using `sensor_msgs/msg/JointState`.
    *   Verify the published data using `ros2 topic echo /unity_joint_states` in a ROS 2 terminal.
3.  **Integrate a Simulated Camera**:
    *   Add a standard Unity Camera to your robot model in Unity.
    *   Create a C# script that captures the camera feed and uses `ROSConnection` to publish it to a ROS 2 topic (e.g., `/unity_camera_feed`) using `sensor_msgs/msg/Image`.
    *   Visualize the camera feed in ROS 2 using `rqt_image_view`.

## Summary

In this chapter, you've mastered the integration of ROS 2 with Unity for high-fidelity robotics simulation:
- You set up a Unity project and imported your URDF robot model.
- You configured `ArticulationBody` for accurate joint control.
- You established two-way communication between ROS 2 and Unity using the `ROS-TCP-Connector`.
- You learned to command your Unity-simulated robot from a ROS 2 Python node.

This powerful combination provides a visually rich and physically accurate platform for developing advanced Physical AI applications.

## Next Steps

In the next module, "The AI Robot Brain," you will delve into integrating NVIDIA Isaac with a simulated humanoid robot to implement AI-powered perception and navigation.

➡️ Continue to [Module 3: The AI Robot Brain](../03-ai-robot-brain/index.md)

## Additional Resources
-   [Unity Robotics Documentation](https://github.com/Unity-Technologies/Unity-Robotics-Hub/blob/main/docs/ROS_TCP_Connector.md)
-   [Unity ArticulationBody Documentation](https://docs.unity3d.com/Manual/class-ArticulationBody.html)
-   [ROS-TCP-Connector GitHub](https://github.com/Unity-Technologies/ROS-TCP-Connector)
