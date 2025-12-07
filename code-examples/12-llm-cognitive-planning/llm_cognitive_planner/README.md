# `llm_cognitive_planner` ROS 2 Package

This package contains Python examples demonstrating a simple LLM-based cognitive planner for robotics. It is designed to complement Chapter 12: LLM Cognitive Planning of the "Physical AI & Humanoid Robotics" book.

## Contents

-   `llm_cognitive_planner/cognitive_planner_node.py`: A ROS 2 node that subscribes to transcribed text commands, sends them to an LLM (e.g., OpenAI's GPT-4) to generate a plan, and then executes that plan by calling ROS 2 action servers.

## Setup

1.  **Navigate to your ROS 2 Workspace**: Ensure you are in the `src` directory of your ROS 2 workspace (e.g., `~/ros2_ws/src`).
2.  **Clone this Repository**: Place this `llm_cognitive_planner` package within your ROS 2 workspace `src` directory. You will also need the `my_robot_controller` package (from Chapter 3) in your workspace.
    ```bash
    # Example: If your workspace is ~/ros2_ws
    cd ~/ros2_ws/src
    # Assuming you have cloned the main book's code-examples repository
    cp -r /path/to/ai-native-book/code-examples/12-llm-cognitive-planning/llm_cognitive_planner .
    cp -r /path/to/ai-native-book/code-examples/03-ros2-python-development/my_robot_controller .
    ```
3.  **Install Dependencies**:
    ```bash
    pip install openai
    rosdep install -i --from-path src --rosdistro humble -y
    ```
4.  **Build the Package**:
    ```bash
    cd ~/ros2_ws
    colcon build --packages-select llm_cognitive_planner my_robot_controller
    ```
5.  **Source the Setup Files**:
    ```bash
    source install/setup.bash
    ```
6.  **Set OpenAI API Key**:
    ```bash
    export OPENAI_API_KEY="YOUR_API_KEY" # Replace with your actual key
    ```

## Usage

1.  **Run Cognitive Planner Node**: In one terminal, launch the cognitive planner.
    ```bash
    ros2 run llm_cognitive_planner cognitive_planner
    ```
2.  **Run Supporting Nodes**: In separate terminals, run the `whisper_asr_node` (from Chapter 11) to provide voice commands, and the `countdown_action_server` (from Chapter 3) to execute the plan.
    ```bash
    ros2 run voice_command_interface whisper_asr_node
    ros2 run my_robot_controller countdown_action_server
    ```
3.  **Speak Commands**: Speak a command like "Start a countdown from 5" into your microphone when the `whisper_asr_node` prompts "Say something!". The `cognitive_planner` will receive this text, call the LLM, and execute the `countdown` action.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
