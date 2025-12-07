# Vision-Language-Action (VLA) Reference Card

This card provides a quick overview of the Vision-Language-Action (VLA) pipeline and key components for humanoid robotics.

## VLA Pipeline Overview

**Human Command (Voice)**
  ↓
**ASR (Automatic Speech Recognition)** - e.g., OpenAI Whisper (Chapter 11)
  ↓
**Text Command**
  ↓
**LLM Cognitive Planner** - e.g., GPT-4 (Chapter 12)
  ↓
**Action Sequence** - (Parsed from LLM, executed via ROS 2 Actions/Services)
  ↓
**Robot Execution** - Simulated Humanoid in Isaac Sim (Chapter 8, Capstone Chapter 13)

## Key Components & Technologies

### 1. Speech-to-Text (ASR)
-   **Tool**: OpenAI Whisper (API or local models).
-   **Function**: Converts spoken human commands into text.
-   **ROS 2 Node**: `whisper_asr_node` (from `voice_command_interface` package - Chapter 11).
-   **Output**: `std_msgs/msg/String` on `/voice_command_text` topic.

### 2. Cognitive Planning (LLM)
-   **Tool**: Large Language Models (LLMs) like OpenAI GPT-4.
-   **Function**: Interprets text commands, robot state, and available skills to generate a sequence of robot actions.
-   **ROS 2 Node**: `cognitive_planner_node` (from `llm_cognitive_planner` package - Chapter 12).
-   **Input**: `std_msgs/msg/String` from `/voice_command_text`.
-   **Output**: ROS 2 Action Goals (e.g., `my_robot_controller/action/Countdown` or custom actions).
-   **Prompt Engineering**: Crucial for defining robot skills and output format (e.g., JSON).

### 3. Robot Skills (ROS 2 Actions/Services)
-   **Examples**: `countdown`, `move_to_waypoint`, `grasp_object`, `look_at`.
-   **Implementation**: ROS 2 Action Servers or Service Servers.
-   **Packages**: Typically implemented in robot-specific controller packages (e.g., `my_robot_controller` - Chapter 3).

### 4. Simulation Environment
-   **Tool**: NVIDIA Isaac Sim (Chapter 8).
-   **Function**: High-fidelity simulation of humanoid robots, environments, and sensors.
-   **Integration**: `omni.isaac.ros2_bridge` for ROS 2 communication.

### 5. Perception & Navigation
-   **Perception Tool**: Isaac ROS VSLAM (Chapter 9).
-   **Navigation Tool**: Nav2 Stack (Chapter 10).
-   **Function**: Provides robot localization, mapping, and autonomous path planning.
-   **Integration**: Consumes sensor data from Isaac Sim, publishes `/odom` (or `/tf`) for Nav2.

## Important Considerations

-   **`OPENAI_API_KEY`**: Ensure environment variable is set for LLM/Whisper API usage.
-   **ROS 2 Environment**: Always source your ROS 2 workspace before running nodes.
-   **Hardware**: NVIDIA GPU is essential for Isaac Sim and Isaac ROS.
-   **Docker**: Isaac ROS often runs in Docker containers for dependency management.
-   **Grounding**: LLM plans must be grounded in actual robot capabilities.
-   **Error Handling**: Implement checks for ASR errors, LLM plan validity, and execution failures.

*(More content will be added here.)*
