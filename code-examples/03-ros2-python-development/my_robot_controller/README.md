# `my_robot_controller` ROS 2 Package

This package contains Python examples demonstrating various ROS 2 communication patterns: publishers, subscribers, service clients/servers, and action clients/servers. It is designed to complement Chapter 3: ROS 2 Python Development of the "Physical AI & Humanoid Robotics" book.

## Contents

### Custom Interfaces

-   `msg/RobotCommand.msg`: Custom message for robot movement commands.
-   `srv/AddTwoInts.srv`: Custom service for adding two integers.
-   `action/Countdown.action`: Custom action for a countdown task.

### Nodes

-   `my_robot_controller/command_publisher.py`: Publishes `RobotCommand` messages.
-   `my_robot_controller/sensor_subscriber.py`: Subscribes to generic sensor feedback (using `std_msgs/msg/String`).
-   `my_robot_controller/add_two_ints_server.py`: Provides the `AddTwoInts` service.
-   `my_robot_controller/add_two_ints_client.py`: Calls the `AddTwoInts` service.
-   `my_robot_controller/countdown_action_server.py`: Implements the `Countdown` action.
-   `my_robot_controller/countdown_action_client.py`: Calls the `Countdown` action.

## Setup

1.  **Navigate to your ROS 2 Workspace**: Ensure you are in the `src` directory of your ROS 2 workspace (e.g., `~/ros2_ws/src`).
2.  **Clone this Repository**: Place this `my_robot_controller` package within your ROS 2 workspace `src` directory.
    ```bash
    # Example: If your workspace is ~/ros2_ws
    cd ~/ros2_ws/src
    # Assuming you have cloned the main book's code-examples repository
    cp -r /path/to/ai-native-book/code-examples/03-ros2-python-development/my_robot_controller .
    ```
3.  **Install Dependencies**:
    ```bash
    rosdep install -i --from-path src --rosdistro humble -y
    ```
4.  **Build the Package**: **IMPORTANT:** You must build the package after creating custom messages, services, or actions so that the Python bindings are generated.
    ```bash
    cd ~/ros2_ws
    colcon build --packages-select my_robot_controller
    ```
5.  **Source the Setup Files**:
    ```bash
    source install/setup.bash
    ```

## Usage

### 1. Publisher and Subscriber

**Terminal 1 (Publisher):**
```bash
ros2 run my_robot_controller command_publisher
```

**Terminal 2 (Subscriber):**
```bash
ros2 run my_robot_controller sensor_subscriber
```
*(Note: `sensor_subscriber` will not show output unless a node publishes to `/sensor_feedback_topic`. Refer to Practice Exercise 1 in Chapter 3 to implement a publisher for it.)*

### 2. Service Server and Client

**Terminal 1 (Service Server):**
```bash
ros2 run my_robot_controller add_two_ints_server
```

**Terminal 2 (Service Client):**
```bash
ros2 run my_robot_controller add_two_ints_client 5 7
```
Replace `5` and `7` with any two integers.

### 3. Action Server and Client

**Terminal 1 (Action Server):**
```bash
ros2 run my_robot_controller countdown_action_server
```

**Terminal 2 (Action Client):**
```bash
ros2 run my_robot_controller countdown_action_client
```
The client will send a goal to countdown from 5.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
