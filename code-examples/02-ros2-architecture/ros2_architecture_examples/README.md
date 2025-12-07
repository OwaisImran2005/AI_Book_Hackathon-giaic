# `ros2_architecture_examples` ROS 2 Package

This package provides code examples and solutions for the practice exercises in Chapter 2: ROS 2 Architecture of the "Physical AI & Humanoid Robotics" book.

## Contents

-   `ros2_architecture_examples/minimal_timer.py`: A ROS 2 node that publishes the current time to the `/time_topic` topic every 1 second. This is a solution for Practice Exercise 3.
-   `launch/timer.launch.py`: A ROS 2 launch file to start the `minimal_timer` node.

## Practice Exercise Solutions

### Exercise 2: Modify Communication (Solution)

To solve this exercise, you would modify the `publisher_member_function.py` from the `hello_physical_ai` package (Chapter 1 examples) to publish a different message. For instance, change `msg.data = 'Hello ROS 2 World: %d' % self.i` to `msg.data = 'Physical AI is awesome! %d' % self.i`.

### Exercise 3: Add a Third Node (Solution)

The `minimal_timer.py` node in this package is the solution for Exercise 3. It publishes the current time on a new topic. The `timer.launch.py` is provided to launch this node.

## Setup

1.  **Navigate to your ROS 2 Workspace**: Ensure you are in the `src` directory of your ROS 2 workspace (e.g., `~/ros2_ws/src`).
2.  **Clone this Repository**: Place this `ros2_architecture_examples` package within your ROS 2 workspace `src` directory.
    ```bash
    # Example: If your workspace is ~/ros2_ws
    cd ~/ros2_ws/src
    # Assuming you have cloned the main book's code-examples repository
    cp -r /path/to/ai-native-book/code-examples/02-ros2-architecture/ros2_architecture_examples .
    ```
3.  **Install Dependencies**:
    ```bash
    rosdep install -i --from-path src --rosdistro humble -y
    ```
4.  **Build the Package**:
    ```bash
    cd ~/ros2_ws
    colcon build --packages-select ros2_architecture_examples
    ```
5.  **Source the Setup Files**:
    ```bash
    source install/setup.bash
    ```

## Usage

### Running the Minimal Timer Node

```bash
ros2 run ros2_architecture_examples minimal_timer
```
You can also use the launch file:
```bash
ros2 launch ros2_architecture_examples timer.launch.py
```

### Verifying the Timer Node

In a separate terminal, after launching the `minimal_timer` node:
```bash
ros2 topic list
# You should see /time_topic
ros2 topic echo /time_topic
```

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
