# Chapter 3: ROS 2 Python Development

:::info Chapter Info
**Module**: The Robotic Nervous System | **Duration**: 4 hours | **Difficulty**: Intermediate
:::

## Learning Objectives
By the end of this chapter, you will:
1. Understand the structure of a ROS 2 Python package and how to create one.
2. Be able to write ROS 2 nodes in Python for various communication patterns (publishers, subscribers, service clients, service servers, action clients, action servers).
3. Learn to define and use custom message, service, and action types.
4. Gain proficiency in debugging ROS 2 Python applications.

## Prerequisites
- Completed Chapter 2: ROS 2 Architecture, with a solid understanding of ROS 2 concepts (nodes, topics, services, actions, parameters).
- Intermediate Python programming skills.

## What You'll Build
In this chapter, you will build a complete ROS 2 Python package that demonstrates advanced communication patterns. This will include:
- A custom ROS 2 Python package (`my_robot_controller`).
- A publisher node for sending robot commands.
- A subscriber node for receiving sensor feedback.
- A service server and client for synchronous requests.
- An action server and client for long-running tasks.

---

## Introduction: Bringing Robots to Life with Python

In the previous chapter, you gained a theoretical understanding of ROS 2 architecture and explored its components using command-line tools. Now, it's time to translate that knowledge into executable code. Python, with its readability, extensive libraries, and rapid development capabilities, is an excellent choice for developing ROS 2 applications, especially for higher-level control, data processing, and AI integration.

This chapter guides you through the process of developing ROS 2 nodes using Python. You'll learn how to create your own ROS 2 packages, define custom communication interfaces (messages, services, actions), and implement various communication patterns that form the backbone of any complex robotic system. We go beyond simple publisher-subscriber examples to cover synchronous services and long-running actions, providing you with the tools to build sophisticated robot behaviors. Effective debugging is a critical skill for any developer, especially in robotics where software interacts with unpredictable hardware and environments. Therefore, we also cover essential debugging techniques for ROS 2 Python applications, helping you quickly identify and resolve issues. By the end of this chapter, you will be proficient in writing Python code that makes your robots perceive, reason, and act in the physical world.

## Core Concepts: Building ROS 2 Python Packages

Before writing our first lines of code, let's understand the typical structure of a ROS 2 Python package and the tools involved.

### 1. ROS 2 Package Structure for Python

A typical ROS 2 Python package (`ament_python` build type) includes:
*   **`package.xml`**: Defines metadata (name, version, description, dependencies, maintainer, license) about the package.
*   **`setup.py`**: A Python script that tells `setuptools` how to install the package, including defining executable entry points (nodes) and data files.
*   **`<package_name>/`**: A Python module with the same name as the package, containing the actual Python source code for your nodes.
*   **`resource/<package_name>`**: A marker file for `ament_python`.
*   **`launch/`**: Contains Python launch files for orchestrating multiple nodes.
*   **`test/`**: Contains unit and integration tests for the package.
*   **`msg/`, `srv/`, `action/`**: Directories for custom message, service, and action definitions.

### 2. The `rclpy` Library

`rclpy` is the Python client library for ROS 2. It provides the necessary API to interact with the ROS 2 graph, allowing you to create nodes, publishers, subscribers, clients, servers, and action clients/servers. `rclpy` wraps the underlying `rcl` (ROS Client Library) written in C, which in turn interacts with the DDS middleware.

### 3. Custom Messages, Services, and Actions

While ROS 2 provides many standard message types (`std_msgs`, `sensor_msgs`, etc.), you will often need to define your own custom types for specific data structures or robot-specific commands.

*   **Custom Messages (`.msg` files)**: Define the structure of data exchanged on topics.
    ```
    # msg/MyMessage.msg
    int32 data
    string message_text
    ```
*   **Custom Services (`.srv` files)**: Define the request and response structure for services. A `---` separates the request from the response.
    ```
    # srv/MyService.srv
    int32 request_data
    string request_message
    ---
    int32 response_data
    string response_message
    ```
*   **Custom Actions (`.action` files)**: Define the goal, result, and feedback structure for actions. Separated by `---`.
    ```
    # action/MyAction.action
    int32 target_value
    ---
    int32 final_value
    bool success
    ---
    int32 current_progress
    ```
After defining these files, you need to add them to `package.xml` and `CMakeLists.txt` (even for Python packages, to generate language-specific bindings) and then build the package.

## Hands-On Tutorial: Building a ROS 2 Python Controller

We will create a new ROS 2 Python package called `my_robot_controller` that demonstrates various communication patterns.

### Step 1: Create a New ROS 2 Python Package

Navigate to the `src` directory of your ROS 2 workspace (e.g., `~/ros2_ws/src`) and create the package:

```bash
ros2 pkg create --build-type ament_python my_robot_controller --dependencies rclpy std_msgs
```
This command creates:
*   A `my_robot_controller` directory.
*   A `package.xml` file.
*   A `setup.py` file.
*   A `my_robot_controller/my_robot_controller` Python module.

### Step 2: Define Custom Message

We'll define a custom message to represent a simple robot command (e.g., move forward/backward).
Create a `msg` directory inside `my_robot_controller`:
```bash
mkdir my_robot_controller/msg
```
Create the file `my_robot_controller/msg/RobotCommand.msg` with the following content:
```
# msg/RobotCommand.msg
string command_type  # e.g., "move", "stop", "turn"
float32 linear_velocity_x
float32 angular_velocity_z
```

Now, we need to tell `package.xml` and `setup.py` about this custom message.
Add the following lines to your `my_robot_controller/package.xml` inside the `<package>` tag, under `<depend>std_msgs</depend>`:
```xml
  <build_depend>rosidl_default_generators</build_depend>
  <exec_depend>rosidl_default_runtime</exec_depend>
  <member_of_group>rosidl_interface_packages</member_of_group>
```
And add these lines to `my_robot_controller/setup.py` below `zip_safe=True,`:
```python
    # For custom messages/services/actions
    generate_setup_file=True,
```
Then, add the custom message definition in `my_robot_controller/setup.py` in the `data_files` section, above `(os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[py]*')))`:
```python
        (os.path.join('share', package_name, 'msg'), glob('msg/*.msg')),
```

### Step 3: Implement Publisher Node

Create `my_robot_controller/my_robot_controller/command_publisher.py`:
```python
import rclpy
from rclpy.node import Node
from my_robot_controller.msg import RobotCommand # Import custom message

class CommandPublisher(Node):
    def __init__(self):
        super().__init__('command_publisher')
        self.publisher_ = self.create_publisher(RobotCommand, 'robot_command_topic', 10)
        timer_period = 1.0 # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = RobotCommand()
        msg.command_type = 'move'
        msg.linear_velocity_x = 0.5 * (self.i % 2) # Toggle between 0.0 and 0.5
        msg.angular_velocity_z = 0.0
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.command_type}" Vx={msg.linear_velocity_x}')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    node = CommandPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```
Add an entry point for this node in `my_robot_controller/setup.py` in the `console_scripts` list:
```python
            'command_publisher = my_robot_controller.command_publisher:main',
```

### Step 4: Implement Subscriber Node

Create `my_robot_controller/my_robot_controller/sensor_subscriber.py`:
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String # We'll just subscribe to a generic string for now
# from my_robot_controller.msg import SensorFeedback # Placeholder for future custom sensor feedback

class SensorSubscriber(Node):
    def __init__(self):
        super().__init__('sensor_subscriber')
        self.subscription = self.create_subscription(
            String, # Using String for simplicity, can be custom msg later
            'sensor_feedback_topic',
            self.listener_callback,
            10)
        self.subscription # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard sensor feedback: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    node = SensorSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```
Add an entry point for this node in `my_robot_controller/setup.py`:
```python
            'sensor_subscriber = my_robot_controller.sensor_subscriber:main',
```

### Step 5: Build and Test

Navigate to your workspace root (`~/ros2_ws`) and build your package:
```bash
colcon build --packages-select my_robot_controller
source install/setup.bash # Re-source to find new executables
```
Run your nodes in separate terminals:
```bash
ros2 run my_robot_controller command_publisher
```
```bash
ros2 run my_robot_controller sensor_subscriber
# (Note: sensor_subscriber will not receive anything until a publisher sends to 'sensor_feedback_topic')
```
For testing the custom message publisher:
```bash
ros2 topic echo /robot_command_topic
```

### Step 6: Debugging ROS 2 Python Applications

Debugging is an essential part of development. Here are common techniques:

1.  **`self.get_logger().info()`**: The simplest form of debugging. Use `info`, `warn`, `error`, `debug` levels.
    ```python
    self.get_logger().info('My variable: %s' % my_variable_value)
    ```
2.  **`ros2 log`**: View all ROS 2 log messages from all nodes.
    ```bash
    ros2 log
    ```
3.  **`pdb` (Python Debugger)**: For more interactive debugging, you can insert `breakpoint()` in your Python code (Python 3.7+).
    ```python
    import pdb; pdb.set_trace() # Insert this line where you want to pause execution
    ```
    Then run your node. When execution hits `breakpoint()`, it will pause and give you a `pdb` prompt in your terminal, where you can inspect variables, step through code, etc.
4.  **`rqt_graph`**: A graphical tool to visualize the ROS 2 computation graph (nodes, topics, services). Very useful for understanding connections.
    ```bash
    rqt_graph
    ```
5.  **`ros2 doctor`**: A command-line tool that checks the health and configuration of your ROS 2 system, identifying common issues.
    ```bash
    ros2 doctor
    ```

## Deep Dive: Beyond Pub/Sub - Services and Actions in Python

Implementing services and actions in Python follows a similar pattern to pub/sub, using `rclpy` APIs.

### 1. Service Server and Client

We'll use a simple service to "add two integers".
First, define the custom service:
Create `my_robot_controller/srv/AddTwoInts.srv`:
```
# srv/AddTwoInts.srv
int64 a
int64 b
---
int64 sum
```
Update `my_robot_controller/package.xml` (similar to custom message, add `rosidl_default_generators` and `rosidl_default_runtime`).
Update `my_robot_controller/setup.py` (add `(os.path.join('share', package_name, 'srv'), glob('srv/*.srv')),` to `data_files`).

**Service Server (`my_robot_controller/my_robot_controller/add_two_ints_server.py`):**
```python
import rclpy
from rclpy.node import Node
from my_robot_controller.srv import AddTwoInts # Import custom service

class AddTwoIntsService(Node):
    def __init__(self):
        super().__init__('add_two_ints_server')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)
        self.get_logger().info('AddTwoInts service server started.')

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'Incoming request: a={request.a}, b={request.b}. Sending response: sum={response.sum}')
        return response

def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsService()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```
Add entry point in `setup.py`: `'add_two_ints_server = my_robot_controller.add_two_ints_server:main',`

**Service Client (`my_robot_controller/my_robot_controller/add_two_ints_client.py`):**
```python
import rclpy
from rclpy.node import Node
from my_robot_controller.srv import AddTwoInts # Import custom service
import sys

class AddTwoIntsClient(Node):
    def __init__(self):
        super().__init__('add_two_ints_client')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

def main(args=None):
    rclpy.init(args=args)
    if len(sys.argv) != 3:
        AddTwoIntsClient.get_logger().info('Usage: ros2 run my_robot_controller add_two_ints_client A B')
        sys.exit(1)
    
    client = AddTwoIntsClient()
    response = client.send_request(int(sys.argv[1]), int(sys.argv[2]))
    client.get_logger().info(f'Result of add_two_ints: for {sys.argv[1]} + {sys.argv[2]} = {response.sum}')
    client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```
Add entry point in `setup.py`: `'add_two_ints_client = my_robot_controller.add_two_ints_client:main',`

### 2. Action Server and Client

We'll use a simple action to "countdown".
First, define the custom action:
Create `my_robot_controller/action/Countdown.action`:
```
# action/Countdown.action
int32 target_count
---
int32 final_count
bool success
---
int32 current_count
```
Update `my_robot_controller/package.xml` (similar to custom message/service).
Update `my_robot_controller/setup.py` (add `(os.path.join('share', package_name, 'action'), glob('action/*.action')),` to `data_files`).

**Action Server (`my_robot_controller/my_robot_controller/countdown_action_server.py`):**
```python
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from my_robot_controller.action import Countdown # Import custom action
import time

class CountdownActionServer(Node):
    def __init__(self):
        super().__init__('countdown_action_server')
        self._action_server = ActionServer(
            self,
            Countdown,
            'countdown',
            self.execute_callback)
        self.get_logger().info('Countdown action server started.')

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        feedback_msg = Countdown.Feedback()
        initial_count = goal_handle.request.target_count
        
        for i in range(initial_count, 0, -1):
            feedback_msg.current_count = i
            self.get_logger().info(f'Feedback: {feedback_msg.current_count}')
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1) # Simulate work

        goal_handle.succeed()
        result = Countdown.Result()
        result.final_count = 0
        result.success = True
        self.get_logger().info('Goal succeeded!')
        return result

def main(args=None):
    rclpy.init(args=args)
    node = CountdownActionServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```
Add entry point in `setup.py`: `'countdown_action_server = my_robot_controller.countdown_action_server:main',`

**Action Client (`my_robot_controller/my_robot_controller/countdown_action_client.py`):**
```python
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from my_robot_controller.action import Countdown # Import custom action

class CountdownActionClient(Node):
    def __init__(self):
        super().__init__('countdown_action_client')
        self._action_client = ActionClient(self, Countdown, 'countdown')
        self.get_logger().info('Countdown action client started.')

    def send_goal(self, target_count):
        self.get_logger().info('Waiting for action server...')
        self._action_client.wait_for_server()

        goal_msg = Countdown.Goal()
        goal_msg.target_count = target_count

        self.get_logger().info('Sending goal...')
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: Final Count={result.final_count}, Success={result.success}')
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Feedback: Current Count={feedback_msg.feedback.current_count}')

def main(args=None):
    rclpy.init(args=args)
    node = CountdownActionClient()
    node.send_goal(5) # Send a goal to countdown from 5
    rclpy.spin(node)

if __name__ == '__main__':
    main()
```
Add entry point in `setup.py`: `'countdown_action_client = my_robot_controller.countdown_action_client:main',`

## Troubleshooting: ROS 2 Python Development

1.  **Issue**: `ModuleNotFoundError: No module named 'my_robot_controller.msg'` (or `srv`, `action`)
    *   **Cause**: You forgot to build your package after creating custom message/service/action files, or forgot to re-source your workspace.
    *   **Solution**: Run `colcon build --packages-select my_robot_controller` from your workspace root, then `source install/setup.bash`.
2.  **Issue**: `colcon build` fails with `Could not find ament_cmake_auto` or similar errors related to `rosidl_default_generators`.
    *   **Cause**: Missing dependencies in `package.xml` for custom interfaces.
    *   **Solution**: Ensure `package.xml` includes `<build_depend>rosidl_default_generators</build_depend>`, `<exec_depend>rosidl_default_runtime</exec_depend>`, and `<member_of_group>rosidl_interface_packages</member_of_group>`.
3.  **Issue**: `rclpy.spin_until_future_complete` hangs for action client.
    *   **Cause**: Action server is not running or not reachable.
    *   **Solution**: Ensure your action server node is launched before the client attempts to send a goal. Check `ros2 node list` and `ros2 action list`.
4.  **Issue**: Python node crashes without clear error in terminal.
    *   **Cause**: Unhandled Python exception. ROS 2's Python logging might sometimes suppress detailed tracebacks.
    *   **Solution**: Run the node with `python3 -m pdb $(find-pkg-share my_robot_controller)/my_robot_controller/my_node.py` to use `pdb` or add `try...except` blocks in your node's callbacks to catch and log exceptions explicitly.
5.  **Issue**: `NameError: name 'MyCustomMessage' is not defined`.
    *   **Cause**: You didn't import your custom message type correctly.
    *   **Solution**: Ensure you have `from my_robot_controller.msg import MyCustomMessage` at the top of your Python file.

## Practice Exercises

1.  **Implement Sensor Feedback Publisher**:
    *   Create a new Python node in `my_robot_controller` called `sensor_publisher.py`.
    *   This node should publish `std_msgs/msg/String` messages to `/sensor_feedback_topic` every 0.5 seconds, simulating sensor data (e.g., "Temperature: 25.5C").
    *   Update `setup.py` and build your package.
    *   Launch both `command_publisher` and `sensor_subscriber` from this chapter, and your new `sensor_publisher`. Verify `sensor_subscriber` receives the feedback.
2.  **Extend RobotCommand Message**:
    *   Modify `my_robot_controller/msg/RobotCommand.msg` to include a `string frame_id` field.
    *   Modify `command_publisher.py` to set this `frame_id`.
    *   Rebuild your package and verify the new field appears when you `ros2 topic echo /robot_command_topic`.
3.  **Implement Simple Task Action**:
    *   Define a new action called `ExecuteTask.action` with a `string task_name` as a goal, `string current_status` as feedback, and `bool success` as a result.
    *   Implement an action server and an action client for this new action within `my_robot_controller`.
    *   The action server should "execute" the task by publishing feedback messages (e.g., "Task X: 25% complete", "Task X: 50% complete") and then return success/failure.
    *   Test your action server and client.

## Summary

In this chapter, you've significantly advanced your ROS 2 development skills by:
- Creating a complete ROS 2 Python package from scratch.
- Implementing nodes for publishers, subscribers, service servers, clients, action servers, and clients.
- Learning to define and use custom message, service, and action types.
- Gaining practical experience in debugging ROS 2 Python applications.

You now have a solid foundation in developing complex robotic behaviors using Python and ROS 2.

## Next Steps

In the next chapter, "URDF Robot Modeling," you will learn how to describe your robot's physical structure and properties, which is essential for simulation and control.

➡️ Continue to [Chapter 4: URDF Robot Modeling](./04-urdf-robot-modeling.md)

## Additional Resources
-   [ROS 2 Python Tutorials](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Programming-CPP-Python-Nodes/Python-Nodes-Basic.html)
-   [ROS 2 Custom Interfaces Tutorial](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Creating-Custom-ROS2-Interfaces.html)
-   [Python Debugger (pdb) Documentation](https://docs.python.org/3/library/pdb.html)
