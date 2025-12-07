# Chapter 2: ROS 2 Architecture

:::info Chapter Info
**Module**: The Robotic Nervous System | **Duration**: 3 hours | **Difficulty**: Beginner
:::

## Learning Objectives
By the end of this chapter, you will:
1. Understand the core architectural components of ROS 2, including nodes, topics, services, and actions.
2. Be able to use fundamental ROS 2 command-line tools for introspection and debugging.
3. Comprehend the publish-subscribe communication model and its role in distributed robotics.
4. Learn how to launch and manage multiple ROS 2 nodes.

## Prerequisites
- Completed Chapter 1: Introduction to Physical AI, with a working ROS 2 development environment.
- Basic familiarity with terminal commands.

## What You'll Build
In this chapter, you will build and launch a simple ROS 2 system consisting of multiple communicating nodes. This will include:
- A basic ROS 2 publisher node.
- A basic ROS 2 subscriber node.
- A ROS 2 launch file to orchestrate these nodes.

---

## Introduction: The Nervous System of a Robot

Just as a human body has a nervous system that coordinates actions, interprets sensations, and enables thought, a complex robot requires a sophisticated architecture to manage its various components. This is where the Robot Operating System 2 (ROS 2) comes into play. ROS 2 is not an operating system in the traditional sense (like Ubuntu or Windows); rather, it is a flexible framework for writing robot software. It provides a collection of tools, libraries, and conventions that simplify the task of building complex and robust robot applications.

Developed to address the limitations of its predecessor, ROS 1, ROS 2 brings significant improvements in areas like real-time communication, multi-robot systems, and security, making it suitable for a wider range of industrial and research applications. It abstracts away much of the low-level communication and hardware interfacing, allowing roboticists to focus on the higher-level logic of robot behavior.

Imagine a humanoid robot: it has cameras for vision, motors for movement, an IMU for balance, and various other sensors. Each of these components needs to communicate, share data, and receive commands. ROS 2 provides the infrastructure for this inter-component communication, turning a collection of disparate hardware and software modules into a cohesive, intelligent system.

In this chapter, we will dissect the core architectural concepts of ROS 2. We will explore how individual software modules, called **nodes**, communicate with each other using **topics**, **services**, and **actions**. We'll also get hands-on with fundamental ROS 2 command-line tools that allow us to inspect, debug, and understand the flow of information within a running ROS 2 system. By the end, you will have a clear mental model of how ROS 2 acts as the "nervous system" coordinating the intelligent behaviors of a robot.

## Core Concepts: ROS 2 Building Blocks

ROS 2's architecture is built upon a distributed communication graph, where independent processes (nodes) can exchange information. This modularity is a key strength, allowing different parts of the robot's software to be developed, tested, and run independently.

### 1. Nodes: The Brain Cells of ROS 2

A **Node** is an executable process that performs computations. In a typical robot system, you might have:
*   A node to control the motors.
*   A node to read data from a LiDAR sensor.
*   A node to process camera images and detect objects.
*   A node to plan a robot's path.

Each node in ROS 2 is designed to be small, modular, and perform a specific task. This approach fosters code reusability and simplifies debugging, as you can isolate issues to individual nodes. Nodes communicate with each other to achieve complex behaviors.

### 2. Topics: The Publish-Subscribe Backbone

**Topics** are the most common way for nodes to asynchronously exchange real-time data. This uses a **publish-subscribe** (pub/sub) communication model:
*   A node that produces data (e.g., a camera node producing image frames) **publishes** messages to a named topic.
*   One or more nodes that consume this data (e.g., an object detection node or a display node) **subscribe** to that same topic.

Key characteristics of topics:
*   **Asynchronous**: Publishers don't wait for subscribers to receive messages.
*   **One-to-many**: One publisher can have multiple subscribers, and multiple publishers can publish to the same topic (though this is less common for data streams).
*   **Message Types**: Each topic uses a predefined `message type` (e.g., `sensor_msgs/msg/Image` for camera images, `std_msgs/msg/String` for simple text). Message types define the structure of the data being sent.
*   **Middleware**: ROS 2 uses Data Distribution Service (DDS) as its underlying communication middleware, which enables efficient, real-time, and secure communication across different platforms.

### 3. Services: Synchronous Request-Response

**Services** are used for synchronous, request-response communication between nodes. When a client node needs a specific computation or action performed by a server node, it sends a **request** and waits for a **response**.
*   **Client**: The node that makes the request.
*   **Server**: The node that provides the service and sends back a response.

Services are useful for:
*   Triggering an action (e.g., "Take a picture").
*   Querying information (e.g., "What is the robot's current pose?").
*   Performing a one-time calculation.

Unlike topics, services are typically one-to-one communication. Each service has a defined `service type` which specifies the structure of both the request and the response messages.

### 4. Actions: Long-Running Asynchronous Tasks

**Actions** are designed for long-running tasks that provide periodic feedback and can be preempted (canceled). They combine aspects of topics and services:
*   **Goal**: The request to start a long-running task (similar to a service request).
*   **Feedback**: Periodic updates on the progress of the task (similar to a topic).
*   **Result**: The final outcome of the task (similar to a service response).

Actions are ideal for tasks like:
*   Moving a robot to a target location (navigation).
*   Performing a complex manipulation sequence (picking and placing).
*   Running a scan of the environment.

A node acts as an **Action Client** to send a goal and receive feedback/result, while another node acts as an **Action Server** to process the goal, provide feedback, and send the final result.

### 5. Parameters: Dynamic Configuration

**Parameters** are dynamic configuration values that nodes can expose. They allow you to change a node's behavior without recompiling the code.
*   **Dynamic**: Parameters can be read and set at runtime.
*   **Centralized**: The ROS 2 parameter server allows other nodes and command-line tools to interact with a node's parameters.

Parameters are useful for:
*   Setting a robot's maximum speed.
*   Configuring sensor thresholds.
*   Switching between different algorithms within a node.

### ROS 2 Graph and Lifecycle

All these components (nodes, topics, services, actions, parameters) form the **ROS 2 graph**, representing the active communication and computation in the system.

ROS 2 also introduces **Lifecycle Nodes**, which provide a standardized way to manage the state transitions of a node (e.g., unconfigured, inactive, active, finalized). This is particularly important for robust, fault-tolerant robotic systems, especially in industrial applications where predictability and safety are paramount.

## Hands-On Tutorial: Exploring the ROS 2 Graph

In Chapter 1, you set up your ROS 2 development environment. Now, let's use some fundamental ROS 2 command-line tools to explore an existing ROS 2 system. We'll use the `hello_physical_ai` package you created in the previous chapter, which consists of a publisher (`talker`) and a subscriber (`listener`).

First, make sure your ROS 2 environment is sourced. If you close your terminal, you typically need to re-source:
```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash # Assuming your workspace is ~/ros2_ws
```

### Step 1: Launch the `hello_physical_ai` Example

We'll use the launch file you created to start both the publisher and subscriber nodes.
Open a new terminal and run:
```bash
ros2 launch hello_physical_ai talker_listener.launch.py
```
You should see output indicating that the `sim_talker` is publishing messages and the `sim_listener` is hearing them.

### Step 2: Inspecting Nodes

With the `talker_listener` launch file running, open a *new* terminal and make sure your ROS 2 environment is sourced.

To list all active ROS 2 nodes:
```bash
ros2 node list
```
You should see at least:
```
/sim_listener
/sim_talker
```
These are the names of the nodes we defined in our launch file.

To get more information about a specific node:
```bash
ros2 node info /sim_talker
```
This will show you which topics it publishes/subscribes to, which services it provides/uses, and its parameters.

### Step 3: Inspecting Topics

To list all active topics in the ROS 2 graph:
```bash
ros2 topic list
```
You should see `/topic`, `/parameter_events`, and `/rosout`.
*   `/topic`: This is our custom topic where the `sim_talker` publishes messages.
*   `/parameter_events`: A system topic for changes in node parameters.
*   `/rosout`: A system topic for logging messages.

To get detailed information about a topic, including its type and the nodes publishing/subscribing to it:
```bash
ros2 topic info /topic
```
You will see something like:
```
Type: std_msgs/msg/String
Publishers:
    /sim_talker
Subscribers:
    /sim_listener
```
This confirms our `sim_talker` is publishing `std_msgs/msg/String` messages to `/topic`, and our `sim_listener` is subscribing to it.

To view the messages being published on a topic in real-time:
```bash
ros2 topic echo /topic
```
You should see the "Hello ROS 2 World" messages being printed to the console as they are published.

### Step 4: Inspecting Services

While our `hello_physical_ai` example doesn't explicitly use services, system nodes provide them.
To list all active services:
```bash
ros2 service list
```
You'll see many services, mostly related to parameter management and node lifecycle.
To get information about a specific service:
```bash
ros2 service info /sim_talker/set_parameters
```
This will show you the service type and which node provides it.

### Step 5: Inspecting Parameters

To list all parameters available on a specific node (e.g., our `sim_talker`):
```bash
ros2 param list /sim_talker
```
You'll see parameters like `use_sim_time`.

You can also get or set a parameter:
```bash
ros2 param get /sim_talker use_sim_time
ros2 param set /sim_talker use_sim_time true
```
(Note: Setting `use_sim_time` to `true` is often necessary when running nodes in simulation environments like Gazebo, which we'll cover later.)

### Step 6: Shutting Down

To stop the launch file and all its nodes, simply press `Ctrl+C` in the terminal where you ran `ros2 launch`.

## Deep Dive: Why ROS 2 vs. ROS 1

ROS 2 was developed to address several key limitations of ROS 1, making it more suitable for modern robotics challenges, especially in industrial and safety-critical applications.

**Key improvements in ROS 2:**

1.  **DDS (Data Distribution Service) Integration**: ROS 2 uses DDS as its communication middleware, replacing ROS 1's custom TCP/IP-based `ros_comm`. DDS is an open international standard for real-time systems, providing:
    *   **Quality of Service (QoS) Policies**: Fine-grained control over communication reliability, durability, and latency. Essential for critical systems.
    *   **Decentralized Architecture**: No single point of failure (like ROS 1's `roscore`).
    *   **Real-time Communication**: Better support for deterministic communication.
    *   **Security**: Built-in mechanisms for authentication, authorization, and encryption.

2.  **Multi-Robot Systems**: Designed from the ground up to support multiple robots communicating in the same environment, and seamlessly handle communication across different network segments.

3.  **Windows, macOS, and RTOS Support**: ROS 1 was primarily Linux-centric. ROS 2 expands support to Windows, macOS, and various real-time operating systems (RTOS), broadening its applicability.

4.  **Lifecycle Management**: Introduction of standard lifecycle states for nodes (unconfigured, inactive, active), enabling more robust and predictable system startup and shutdown.

5.  **Improved Build System**: `ament` build system (used with `colcon`) provides better cross-platform support and modularity compared to ROS 1's `catkin`.

6.  **Parameter System**: Enhanced parameter management with a cleaner API and dynamic parameter updates.

7.  **Actions**: A more sophisticated API for long-running, goal-oriented tasks with feedback and preemption capabilities, improving upon ROS 1's simple actions.

These advancements make ROS 2 a more powerful, flexible, and robust framework for developing the next generation of intelligent robotic systems.

## Troubleshooting: Common ROS 2 Architecture Issues

1.  **Issue**: `ros2: command not found`
    *   **Cause**: ROS 2 environment is not sourced.
    *   **Solution**: Run `source /opt/ros/humble/setup.bash` and `source ~/ros2_ws/install/setup.bash` (if applicable) in each new terminal. Add these to your `~/.bashrc` for persistence.
2.  **Issue**: Nodes cannot find topics or each other.
    *   **Cause**: ROS 2 `ROS_DOMAIN_ID` mismatch or network issues.
    *   **Solution**: Ensure `export ROS_DOMAIN_ID=<ID>` is set to the same value in all terminals. Check network connectivity.
3.  **Issue**: `ros2 launch` fails to find package or launch file.
    *   **Cause**: Package not built, not sourced, or incorrect path in launch file.
    *   **Solution**: Run `colcon build --packages-select <your_package_name>` from workspace root, then `source install/setup.bash`. Double-check the package and launch file names.
4.  **Issue**: Messages not appearing with `ros2 topic echo`.
    *   **Cause**: Publisher not running, topic name mismatch, or message type mismatch.
    *   **Solution**: Verify publisher node is running (`ros2 node list`). Check topic name (`ros2 topic list`) and message type (`ros2 topic info`).
5.  **Issue**: `ros2 run` command fails with `executable not found`.
    *   **Cause**: Executable not correctly defined in `setup.py` (for Python packages) or `CMakeLists.txt` (for C++ packages).
    *   **Solution**: Ensure `entry_points` in `setup.py` (for Python) or `install` directives in `CMakeLists.txt` (for C++) correctly register the executable. Rebuild and re-source.

## Practice Exercises

1.  **ROS 2 Introspection**:
    *   Launch the `talker_listener.launch.py` file again.
    *   In a separate terminal, use `ros2 topic list -t` to list topics with their types.
    *   Use `ros2 node info /sim_talker` and `ros2 node info /sim_listener` to understand their connections.
    *   Experiment with `ros2 param set /sim_talker use_sim_time true` and observe any changes (though not directly visible in this simple example).
2.  **Modify Communication**:
    *   Modify `publisher_member_function.py` to publish a different message (e.g., "Physical AI is awesome!").
    *   Rebuild the package (`colcon build --packages-select hello_physical_ai`) and re-source.
    *   Relaunch the nodes and verify the new message is received by the listener.
3.  **Add a Third Node**:
    *   Create a new Python file in `hello_physical_ai/hello_physical_ai` called `minimal_timer.py` that publishes the current time (using `std_msgs.msg.String` or `builtin_interfaces.msg.Time`) on a new topic `/time_topic` every 1 second.
    *   Update `setup.py` to register this new executable.
    *   Modify `talker_listener.launch.py` to also launch this new node.
    *   Rebuild, re-source, and launch the system to verify the new timer node is working.

## Summary

In this chapter, you've gained a fundamental understanding of ROS 2's architecture, learning about:
- The roles of nodes, topics, services, actions, and parameters.
- How to use key ROS 2 command-line tools for system introspection.
- The advantages of ROS 2 over its predecessor, ROS 1.

You built upon your development environment setup from Chapter 1 by launching and inspecting a basic ROS 2 publisher-subscriber system.

## Next Steps

In the next chapter, "ROS 2 Python Development," you will deepen your programming skills in ROS 2 by learning to create custom nodes, handle messages, and implement more complex robotic behaviors using Python.

➡️ Continue to [Chapter 3: ROS 2 Python Development](./03-ros2-python-development.md)

## Additional Resources
-   [ROS 2 Concepts Overview](https://docs.ros.org/en/humble/Concepts.html)
-   [ROS 2 CLI Tools](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools.html)
-   [DDS - Data Distribution Service](https://www.omg.org/dds/)
