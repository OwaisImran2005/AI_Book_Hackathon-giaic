# `hello_physical_ai` ROS 2 Package

This package contains a simple publisher-subscriber example in ROS 2 using Python. It demonstrates the basic communication mechanism within ROS 2, where a `talker` node publishes messages on a topic, and a `listener` node subscribes to and receives those messages.

This example is part of the "Physical AI & Humanoid Robotics" book, specifically designed for Chapter 1: Introduction to Physical AI, to help beginners understand the fundamental concepts of ROS 2 communication.

## Contents

-   `hello_physical_ai/publisher_member_function.py`: A ROS 2 node that publishes "Hello ROS 2 World" messages to the `/topic` topic.
-   `hello_physical_ai/subscriber_member_function.py`: A ROS 2 node that subscribes to the `/topic` topic and prints received messages.
-   `launch/talker_listener.launch.py`: A ROS 2 launch file to start both the `talker` and `listener` nodes simultaneously.

## Setup

1.  **Navigate to your ROS 2 Workspace**: Ensure you are in the `src` directory of your ROS 2 workspace (e.g., `~/ros2_ws/src`).
2.  **Clone this Repository**: Place this `hello_physical_ai` package within your ROS 2 workspace `src` directory.
    ```bash
    # Example: If your workspace is ~/ros2_ws
    cd ~/ros2_ws/src
    # Assuming you have cloned the main book's code-examples repository
    cp -r /path/to/ai-native-book/code-examples/01-introduction-physical-ai/hello_physical_ai .
    ```
3.  **Install Dependencies**:
    ```bash
    rosdep install -i --from-path src --rosdistro humble -y
    ```
4.  **Build the Package**:
    ```bash
    cd ~/ros2_ws
    colcon build --packages-select hello_physical_ai
    ```
5.  **Source the Setup Files**:
    ```bash
    source install/setup.bash
    ```

## Usage

### 1. Running Nodes Separately

You can run the publisher and subscriber nodes in separate terminals:

**Terminal 1 (Publisher):**
```bash
ros2 run hello_physical_ai talker
```

**Terminal 2 (Subscriber):**
```bash
ros2 run hello_physical_ai listener
```

You should see the `talker` publishing messages and the `listener` receiving them.

### 2. Running Nodes using a Launch File

You can also launch both nodes simultaneously using the provided launch file:

```bash
ros2 launch hello_physical_ai talker_listener.launch.py
```

This will start both nodes, and you should see messages being published and heard in the same terminal output.

## Verification

-   Observe the terminal output when running the nodes: the `talker` node should display "Publishing:..." messages, and the `listener` node should display "I heard:..." messages, confirming inter-node communication.
-   Use `ros2 topic list` to see the `/topic` topic.
-   Use `ros2 node list` to see `minimal_publisher` and `minimal_subscriber` nodes.
-   Use `ros2 topic echo /topic` to independently verify messages on the topic.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
