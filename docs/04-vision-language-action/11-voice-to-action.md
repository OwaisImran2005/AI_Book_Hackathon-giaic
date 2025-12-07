# Chapter 11: Voice-to-Action

:::info Chapter Info
**Module**: Vision-Language-Action | **Duration**: 4 hours | **Difficulty**: Advanced
:::

## Learning Objectives
By the end of this chapter, you will:
1. Understand the role of Automatic Speech Recognition (ASR) in human-robot interaction.
2. Be able to integrate OpenAI Whisper for high-accuracy speech-to-text conversion.
3. Learn to create ROS 2 nodes for processing audio input and publishing text commands.
4. Gain proficiency in basic Natural Language Understanding (NLU) for extracting robotic intent from voice commands.

## Prerequisites
- Completed Module 3 (Chapters 8-10), with a working simulated robot in Isaac Sim.
- Basic understanding of audio processing concepts.
- An OpenAI API key (or access to a local Whisper model).

## What You'll Build
In this chapter, you will build a foundational voice control system for your robot. This will involve:
- Setting up a microphone and audio capture.
- Implementing a ROS 2 node to capture audio and send it to OpenAI Whisper.
- Receiving transcribed text from Whisper and publishing it to a ROS 2 topic.
- A basic ROS 2 node that interprets simple text commands.

---

## Introduction: Speaking to Robots

Imagine a future where you can simply tell your robot what to do, using natural language, just as you would instruct another person. "Robot, pick up the red cube and place it on the table." This seemingly simple interaction involves a complex chain of perception, cognition, and action, starting with understanding human speech. The ability for robots to interpret voice commands, often referred to as **Voice-to-Action**, is a critical component of intuitive human-robot interaction and a key enabler for advanced Physical AI systems.

Until recently, robust and accurate Automatic Speech Recognition (ASR) was a challenging problem, especially in noisy environments or for diverse accents. However, advancements in deep learning have led to breakthroughs, with models like **OpenAI Whisper** achieving near human-level accuracy across a wide range of languages and domains. Integrating such powerful ASR capabilities into a robotic system transforms how humans can interact with their intelligent counterparts.

This chapter guides you through the process of bridging the gap between spoken language and robotic action. We begin by exploring the principles of ASR and its specific challenges in robotics contexts. You then learn how to integrate OpenAI Whisper into a ROS 2-based robotic system, setting up a pipeline to capture audio, send it for transcription, and receive text commands. Finally, we introduce basic Natural Language Understanding (NLU) techniques to extract the robot's intended action from the transcribed text, laying the groundwork for the cognitive planning discussed in the next chapter. By the end, your simulated robot will be able to "hear" and "understand" simple voice instructions, bringing it one step closer to truly autonomous and intelligent behavior.

## Core Concepts: Automatic Speech Recognition (ASR) and Whisper

### 1. Automatic Speech Recognition (ASR)

ASR is the process by which spoken words are converted into text. For robotics, ASR systems need to be:

*   **Accurate**: Misinterpretations can lead to incorrect or dangerous robot actions.
*   **Robust**: Able to handle variations in speaker, accent, background noise, and speech speed.
*   **Low Latency**: For real-time interaction, the transcription needs to happen quickly.

Traditional ASR systems often relied on acoustic models, pronunciation models, and language models. Modern ASR, especially with deep learning, typically uses end-to-end neural networks that learn directly from audio-text pairs.

### 2. OpenAI Whisper

OpenAI Whisper is a general-purpose ASR model that achieves high accuracy and robustness across many languages. It was trained on a massive dataset of diverse audio and corresponding transcriptions, making it highly generalized.

**Key features of Whisper for robotics:**

*   **Multilingual**: Can transcribe in many languages and translate non-English speech into English.
*   **Robustness**: Handles various audio conditions, including background noise and different recording qualities.
*   **Transformer-based**: Utilizes a Transformer architecture, which excels at sequence-to-sequence tasks.
*   **API or Local Models**: Available via an easy-to-use API or can be run locally (depending on hardware and model size). For real-time robotics, local deployment is often preferred to minimize latency and ensure privacy.

### 3. Audio Processing for ASR

For an ASR system to work effectively, the audio input needs to be correctly captured and processed:

*   **Microphone Input**: Robots will typically use microphones to capture ambient sound.
*   **Sampling Rate**: The number of samples of audio carried per second (e.g., 16 kHz, 44.1 kHz). Consistency is important.
*   **Audio Format**: Raw audio data needs to be in a format that the ASR model expects (e.g., mono, WAV, certain bit depth).
*   **Silence Detection**: Removing long periods of silence can improve ASR performance and reduce processing time.

### 4. Basic Natural Language Understanding (NLU) for Commands

Once speech is transcribed into text, the robot needs to understand the intent and extract relevant information. Simple NLU can involve:

*   **Keyword Spotting**: Identifying specific keywords (e.g., "move", "pick up", "stop") that trigger predefined robot behaviors.
*   **Slot Filling**: Extracting parameters associated with an action (e.g., "red cube" for `object`, "table" for `location`).
*   **Command Templates**: Matching transcribed text against a set of predefined command structures.

## Hands-On Tutorial: Building a ROS 2 Voice-to-Text Pipeline

We will build a ROS 2 pipeline that captures audio, sends it to OpenAI Whisper for transcription, and publishes the resulting text to a ROS 2 topic.

### Part 1: OpenAI Whisper Setup

### Step 1: Obtain an OpenAI API Key

1.  Go to the [OpenAI API website](https://openai.com/api/).
2.  Sign up for an account.
3.  Generate a new API key from your user settings.
4.  Keep your API key secure. You will typically set it as an environment variable:
    ```bash
    export OPENAI_API_KEY="YOUR_API_KEY"
    ```
    Add this to your `~/.bashrc` (or equivalent) for persistence.

### Step 2: Install OpenAI Python Client

Inside your ROS 2 development environment (Ubuntu):
```bash
pip install openai SpeechRecognition pyaudio
```
*   `openai`: The official Python client for OpenAI APIs.
*   `SpeechRecognition`: A Python library that provides an easy-to-use interface for various ASR engines, including a local Whisper model (if you choose that route) or for capturing microphone input.
*   `pyaudio`: Required by `SpeechRecognition` for microphone access.

### Part 2: ROS 2 Audio Capture and Whisper Transcription Node

### Step 3: Create a ROS 2 Python Package for Voice-to-Action

Navigate to your ROS 2 workspace `src` directory (e.g., `~/ros2_ws/src`).
Create a new package called `voice_command_interface`:

```bash
ros2 pkg create --build-type ament_python voice_command_interface --dependencies rclpy std_msgs
```

### Step 4: Implement Audio Recorder and Whisper Node

Create `voice_command_interface/voice_command_interface/whisper_asr_node.py` with the following content:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import speech_recognition as sr
import openai
import os
import io

class WhisperASRNode(Node):
    def __init__(self):
        super().__init__('whisper_asr_node')
        self.publisher_ = self.create_publisher(String, 'voice_command_text', 10)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.openai_client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        # Create a timer to continuously listen for audio
        self.timer = self.create_timer(5.0, self.listen_callback) # Listen every 5 seconds

        self.get_logger().info('Whisper ASR Node started. Listening for voice commands...')
        if not os.environ.get("OPENAI_API_KEY"):
            self.get_logger().error("OPENAI_API_KEY environment variable not set. Transcription will fail.")

    def listen_callback(self):
        try:
            with self.microphone as source:
                self.get_logger().info("Say something!")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, phrase_time_limit=4) # Listen for up to 4 seconds
            
            # Use OpenAI Whisper API for transcription
            audio_data = io.BytesIO(audio.get_wav_data())
            audio_data.name = 'audio.wav' # OpenAI API expects a file-like object with a name

            response = self.openai_client.audio.transcriptions.create(
                model="whisper-1", # or "base", "small" if running locally
                file=audio_data,
                response_format="text"
            )
            
            transcribed_text = response.strip()
            if transcribed_text:
                msg = String()
                msg.data = transcribed_text
                self.publisher_.publish(msg)
                self.get_logger().info(f'Transcribed: "{transcribed_text}"')

        except sr.UnknownValueError:
            self.get_logger().warn("Whisper could not understand audio")
        except sr.RequestError as e:
            self.get_logger().error(f"Could not request results from Whisper service; {e}")
        except Exception as e:
            self.get_logger().error(f"An unexpected error occurred: {e}")


def main(args=None):
    rclpy.init(args=args)
    node = WhisperASRNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```
Add entry point in `setup.py`: `'whisper_asr_node = voice_command_interface.whisper_asr_node:main',`

### Step 5: Implement Simple Command Interpreter Node

Create `voice_command_interface/voice_command_interface/command_interpreter_node.py` with the following content:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from my_robot_controller.msg import RobotCommand # Reuse custom command message from Chapter 3

class CommandInterpreterNode(Node):
    def __init__(self):
        super().__init__('command_interpreter_node')
        self.subscription = self.create_subscription(
            String,
            'voice_command_text',
            self.listener_callback,
            10)
        self.subscription # prevent unused variable warning

        self.robot_command_publisher = self.create_publisher(RobotCommand, 'robot_command_topic', 10)
        self.get_logger().info('Command Interpreter Node started. Waiting for voice commands...')

    def listener_callback(self, msg):
        self.get_logger().info(f'Received voice command: "{msg.data}"')
        
        # Basic NLU: Keyword Spotting and Slot Filling
        text_command = msg.data.lower()
        robot_command_msg = RobotCommand()
        robot_command_msg.linear_velocity_x = 0.0
        robot_command_msg.angular_velocity_z = 0.0

        if "move forward" in text_command:
            robot_command_msg.command_type = "move"
            robot_command_msg.linear_velocity_x = 0.5
            self.get_logger().info("Interpreted: Move Forward")
        elif "turn left" in text_command:
            robot_command_msg.command_type = "turn"
            robot_command_msg.angular_velocity_z = 0.5
            self.get_logger().info("Interpreted: Turn Left")
        elif "turn right" in text_command:
            robot_command_msg.command_type = "turn"
            robot_command_msg.angular_velocity_z = -0.5
            self.get_logger().info("Interpreted: Turn Right")
        elif "stop" in text_command:
            robot_command_msg.command_type = "stop"
            self.get_logger().info("Interpreted: Stop")
        else:
            robot_command_msg.command_type = "unknown"
            self.get_logger().warn(f"Interpreted: Unknown command '{text_command}'")

        self.robot_command_publisher.publish(robot_command_msg)


def main(args=None):
    rclpy.init(args=args)
    node = CommandInterpreterNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```
Add entry point in `setup.py`: `'command_interpreter = voice_command_interface.command_interpreter_node:main',`

### Step 6: Build and Test

Navigate to your workspace root (`~/ros2_ws`) and build your package:
```bash
colcon build --packages-select voice_command_interface
source install/setup.bash # Re-source to find new executables
```

## Usage

1.  **Ensure OpenAI API Key is Set**:
    ```bash
    export OPENAI_API_KEY="YOUR_API_KEY" # Replace with your actual key
    ```
2.  **Run Whisper ASR Node**:
    ```bash
    ros2 run voice_command_interface whisper_asr_node
    ```
3.  **Run Command Interpreter Node**:
    ```bash
    ros2 run voice_command_interface command_interpreter
    ```
4.  **Speak Commands**: Speak into your microphone when prompted by the `whisper_asr_node` ("Say something!"). Try commands like "Move forward", "Turn left", "Stop".
5.  **Verify Interpretation**: Observe the output from `command_interpreter_node` to see how it interprets your commands and publishes `RobotCommand` messages. You can also `ros2 topic echo /robot_command_topic`.

## Deep Dive: Local Whisper Models and Alternatives

While the OpenAI Whisper API is convenient, for real-time applications or privacy-sensitive contexts, running a local Whisper model might be preferred.

*   **Local Whisper Models**: The `SpeechRecognition` library can use local Whisper models. You would typically need to install `whisper` via `pip install whisper` and then specify the model size (e.g., `whisper.load_model("base")`). This requires significant GPU resources for larger models.
*   **Edge ASR**: For resource-constrained robots, specialized edge ASR models (e.g., NVIDIA Riva, Picovoice) offer on-device transcription with lower latency and computational overhead.
*   **Vosk**: Another open-source, offline ASR engine that can run on-device.

The choice between API, local models, or edge solutions depends on factors like latency requirements, privacy concerns, computational resources, and internet connectivity.

## Troubleshooting: Voice-to-Action Issues

1.  **Issue**: `OPENAI_API_KEY environment variable not set` error.
    *   **Cause**: You forgot to set the `OPENAI_API_KEY` environment variable.
    *   **Solution**: Run `export OPENAI_API_KEY="YOUR_API_KEY"` before launching the `whisper_asr_node`. Add it to your `~/.bashrc` for persistence.
2.  **Issue**: `whisper_asr_node` reports `UnknownValueError` or `RequestError`.
    *   **Cause**: Microphone issues, poor audio quality, or no internet connection (for OpenAI API).
    *   **Solution**:
        *   Verify your microphone is working and selected as the default input device.
        *   Reduce background noise.
        *   Check your internet connection if using the API.
        *   Ensure `pyaudio` and `SpeechRecognition` are installed correctly (`pip install pyaudio SpeechRecognition`).
3.  **Issue**: `command_interpreter_node` does not interpret commands correctly.
    *   **Cause**: Basic NLU logic is too simple, or voice commands are not matching keywords.
    *   **Solution**: Refine the keyword spotting and conditional logic in `command_interpreter_node.py`. Consider adding more synonyms or a more advanced NLU library for robust parsing.
4.  **Issue**: High latency in voice command processing.
    *   **Cause**: OpenAI API call latency, network delays, or processing time of `whisper_asr_node`.
    *   **Solution**: Optimize audio chunking and processing. Consider using local Whisper models (if available resources permit) or edge ASR solutions for lower latency.
5.  **Issue**: Python node crashes when trying to access microphone.
    *   **Cause**: Missing audio backend (`portaudio` library) or microphone permissions.
    *   **Solution**: Install `portaudio`: `sudo apt install portaudio19-dev python3-pyaudio`. Check system audio settings and ensure the ROS 2 application has microphone access.

## Practice Exercises

1.  **Integrate Local Whisper Model**:
    *   Modify `whisper_asr_node.py` to use a local Whisper model (e.g., `base` or `tiny`) instead of the OpenAI API. You'll need to `pip install whisper` first.
    *   Compare the latency and accuracy between the local model and the API.
2.  **Enhance Command Interpretation**:
    *   Extend `command_interpreter_node.py` to understand more complex commands, such as "Move forward 2 meters" or "Turn right at 90 degrees".
    *   Implement basic slot filling to extract numerical values or specific objects.
3.  **Text-to-Speech Feedback**:
    *   Integrate a Text-to-Speech (TTS) library (e.g., `gTTS` or `pyttsx3`) into `command_interpreter_node.py`.
    *   Make the robot "speak" its interpretation of the command (e.g., "Moving forward 0.5 meters").

## Summary

In this chapter, you've built a foundational Voice-to-Action pipeline for your robot:
- You understood the principles of ASR and its role in human-robot interaction.
- You integrated OpenAI Whisper for speech-to-text conversion.
- You created ROS 2 nodes for audio capture and text command publishing.
- You implemented basic NLU to interpret voice commands.

This enables your robot to understand spoken language, paving the way for more natural and intuitive interactions.

## Next Steps

In the next chapter, "LLM Cognitive Planning," you will learn how to leverage the immense power of Large Language Models to transform these simple text commands into complex, multi-step action plans for your robot.

➡️ Continue to [Chapter 12: LLM Cognitive Planning](./12-llm-cognitive-planning.md)

## Additional Resources
-   [OpenAI Whisper API Documentation](https://platform.openai.com/docs/api-reference/audio)
-   [SpeechRecognition Library Documentation](https://pypi.org/project/SpeechRecognition/)
-   [NVIDIA Riva (for on-device ASR)](https://developer.nvidia.com/riva)
