# Chapter 7: Unity Integration Code Examples

This directory provides a guide for setting up Unity projects and integrating with ROS 2, as described in Chapter 7: Unity Integration of the "Physical AI & Humanoid Robotics" book. Due to the nature of Unity project files, direct automated creation of a fully functional Unity project is not feasible via this workflow. Instead, this `README.md` outlines the necessary manual steps and provides the code snippets for ROS 2 integration.

## Manual Setup Steps (Unity Project)

Please follow these steps to set up your Unity project and integrate with ROS 2:

### Part 1: Unity Project Setup

1.  **Install Unity Hub and Unity Editor**:
    *   Download and install [Unity Hub](https://unity.com/download) from the official Unity website.
    *   Install a compatible version of the Unity Editor (e.g., 2022.3 LTS or newer).
2.  **Create New Unity Project**:
    *   Open Unity Hub, click "New Project", select a `3D Core` template, and name your project `MyRobotSimulation`.
    *   Save this project to a location **outside** of your ROS 2 workspace and this book's code examples directory.
3.  **Install Unity Robotics Packages**:
    *   Open your `MyRobotSimulation` Unity project.
    *   Go to `Window > Package Manager`.
    *   Click the `+` icon in the top-left corner and select "Add package from git URL...".
    *   Add the following packages one by one:
        *   `https://github.com/Unity-Technologies/ROS-TCP-Connector.git`
        *   `https://github.com/Unity-Technologies/URDF-Importer.git`
        *   `https://github.com/Unity-Technologies/ROS-Unity-Integration.git` (optional, for examples)

### Part 2: Import URDF Robot Model

1.  **Export URDF**: Ensure your `my_robot_description` ROS 2 package (from Chapter 4) is built and sourced in your ROS 2 environment.
2.  **Copy URDF**: Copy your `two_link_arm.urdf` file (and any associated meshes) from `~/ros2_ws/src/my_robot_description/urdf/two_link_arm.urdf` into your Unity project's `Assets` folder (e.g., `Assets/URDFs/`).
3.  **Import with URDF Importer**:
    *   In Unity, go to `Robotics > URDF Importer > Import URDF`.
    *   Select your `two_link_arm.urdf` file from your Unity project's Assets.
    *   Ensure "Import as Articulation Body" is checked.
    *   Click "Import".
    Your robotic arm should now appear in your Unity scene as a `GameObject` hierarchy with `ArticulationBody` components.

### Part 3: Setup ROS Connection in Unity

1.  **Add `ROSConnection` Manager**:
    *   In the Unity Hierarchy window, right-click and select `Create Empty`. Rename it to `ROSConnectionManager`.
    *   Select this `GameObject`. In the Inspector window, click "Add Component" and search for `ROSConnection`.
    *   Set the `ROS IP Address` to your ROS 2 machine's IP address (or `127.0.0.1` if running ROS 2 locally).
    *   Set the `ROS Port` to `10000` (default for `ROS-TCP-Connector`).
2.  **Generate ROS 2 Messages**:
    *   In Unity, go to `Robotics > ROS TCP Connector > Generate ROS Messages`.
    *   This tool will automatically find your ROS 2 workspace and generate C# message types from your `.msg`, `.srv`, and `.action` files. This step is crucial for Unity scripts to understand ROS 2 data.
    *   *(Note: For our two-link arm, we'll mainly use standard ROS 2 messages for control.)*

### Part 4: Create a C# Script for Joint Control

1.  **Create C# Script**: In your Unity project's `Assets` folder, create a new C# script (e.g., `ArmController.cs`).
2.  **Attach to Robot**: Drag and drop this `ArmController.cs` script onto the root `GameObject` of your imported robotic arm in the Hierarchy.
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

### Part 5: Create a ROS 2 Python Publisher

This is a ROS 2 Python package that you will create in your ROS 2 workspace.

1.  **Create a new ROS 2 Python package**:
    ```bash
    ros2 pkg create --build-type ament_python unity_controller --dependencies rclpy std_msgs
    ```
2.  **Create `joint_publisher.py`**:
    *   Create a file `~/ros2_ws/src/unity_controller/unity_controller/joint_publisher.py` with the following content:
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
3.  **Update `setup.py`**:
    *   Add an entry point in `~/ros2_ws/src/unity_controller/setup.py` in the `console_scripts` list:
    ```python
                'joint_publisher = unity_controller.joint_publisher:main',
    ```
4.  **Build and Source**:
    ```bash
    cd ~/ros2_ws
    colcon build --packages-select unity_controller
    source install/setup.bash
    ```

### Part 6: Running the Simulation

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

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
