# `voice_command_interface` ROS 2 Package

This package contains Python examples demonstrating a basic Voice-to-Action pipeline using OpenAI Whisper for Automatic Speech Recognition (ASR). It is designed to complement Chapter 11: Voice-to-Action of the "Physical AI & Humanoid Robotics" book.

## Contents

-   `voice_command_interface/whisper_asr_node.py`: A ROS 2 node that captures audio from a microphone, sends it to the OpenAI Whisper API for transcription, and publishes the resulting text to a ROS 2 topic.
-   `voice_command_interface/command_interpreter_node.py`: A ROS 2 node that subscribes to the transcribed text and interprets simple commands, publishing them as `RobotCommand` messages.

## Setup

1.  **Navigate to your ROS 2 Workspace**: Ensure you are in the `src` directory of your ROS 2 workspace (e.g., `~/ros2_ws/src`).
2.  **Clone this Repository**: Place this `voice_command_interface` package within your ROS 2 workspace `src` directory. You will also need the `my_robot_controller` package (from Chapter 3) in your workspace.
    ```bash
    # Example: If your workspace is ~/ros2_ws
    cd ~/ros2_ws/src
    # Assuming you have cloned the main book's code-examples repository
    cp -r /path/to/ai-native-book/code-examples/11-voice-to-action/voice_command_interface .
    cp -r /path/to/ai-native-book/code-examples/03-ros2-python-development/my_robot_controller .
    ```
3.  **Install Dependencies**:
    ```bash
    pip install openai SpeechRecognition pyaudio
    rosdep install -i --from-path src --rosdistro humble -y
    ```
    You might need to install `portaudio` for microphone access: `sudo apt install portaudio19-dev python3-pyaudio`
4.  **Build the Package**:
    ```bash
    cd ~/ros2_ws
    colcon build --packages-select voice_command_interface my_robot_controller
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

1.  **Run Whisper ASR Node**: In one terminal, launch the speech recognition node.
    ```bash
    ros2 run voice_command_interface whisper_asr_node
    ```
2.  **Run Command Interpreter Node**: In a second terminal, launch the command interpreter.
    ```bash
    ros2 run voice_command_interface command_interpreter
    ```
3.  **Verify Robot Command Topic**: In a third terminal, you can monitor the robot command topic.
    ```bash
    ros2 topic echo /robot_command_topic
    ```
4.  **Speak Commands**: Speak commands like "move forward", "turn left", "stop" into your microphone when the `whisper_asr_node` prompts "Say something!".

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
