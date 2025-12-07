# Instructor Guide: Physical AI & Humanoid Robotics

This guide provides instructors with resources, teaching notes, and assessment rubrics to effectively deliver the "Physical AI & Humanoid Robotics: From Simulation to Reality" course.

## Course Overview

**Target Audience**: Students, AI practitioners, and hobbyists with a foundational understanding of Python and AI/ML concepts.

**Course Goal**: To provide a comprehensive, hands-on guide to building, simulating, and controlling intelligent embodied systems that interact with the physical world.

**Key Learning Outcomes**:
*   Master ROS 2 for robotic control.
*   Build digital twins using Gazebo, Unity, and NVIDIA Isaac Sim.
*   Integrate AI with robotics, including perception and navigation.
*   Develop Vision-Language-Action (VLA) systems using LLMs and voice control.
*   Implement a capstone autonomous humanoid robot.

## Teaching Notes by Module

### Module 1: The Robotic Nervous System
*   **Focus**: Foundations of ROS 2 and robot modeling (URDF). Essential for all subsequent modules.
*   **Key Concepts**: ROS 2 nodes, topics, services, actions, parameters. URDF links, joints, visuals, collisions.
*   **Discussion Points**:
    *   Why is a middleware like ROS 2 necessary for robotics?
    *   Differences between ROS 1 and ROS 2 (emphasize real-time, security, DDS).
    *   The importance of accurate robot modeling.
*   **Common Pitfalls**: Environment setup issues (sourcing, dependencies), XML syntax errors in URDF.
*   **Activity Ideas**:
    *   Live demo of `rqt_graph`.
    *   Challenge students to model a simple object (e.g., a chair) in URDF.

### Module 2: The Digital Twin
*   **Focus**: Simulation environments (Gazebo, Unity, Isaac Sim). Bridging URDF to simulation.
*   **Key Concepts**: Gazebo components, physics engines, sensor simulation. Unity `ArticulationBody`, ROS-TCP-Connector.
*   **Discussion Points**:
    *   The "sim-to-real" gap and how to mitigate it.
    *   Trade-offs between different simulators (Gazebo for physics, Unity for graphics, Isaac Sim for AI/synthetic data).
*   **Common Pitfalls**: Physics parameters leading to unstable simulations, ROS 2-simulator communication issues.
*   **Activity Ideas**:
    *   Challenge students to create a simple obstacle course in Gazebo.
    *   Demonstrate a simple control loop where a ROS 2 node controls a Unity-simulated joint.

### Module 3: The AI Robot Brain
*   **Focus**: Advanced perception (Isaac ROS VSLAM) and autonomous navigation (Nav2).
*   **Key Concepts**: VSLAM principles, hardware acceleration, costmaps, global/local planning.
*   **Discussion Points**:
    *   How GPUs accelerate perception tasks.
    *   The role of Docker in managing complex dependencies for AI robotics.
    *   Challenges in real-time mapping and localization.
*   **Common Pitfalls**: Docker setup issues, Nav2 parameter tuning, sensor data misconfiguration.
*   **Activity Ideas**:
    *   Guide students through tuning a Nav2 parameter and observing its effect.
    *   Discuss different VSLAM algorithms and their suitability for various environments.

### Module 4: Vision-Language-Action
*   **Focus**: Integrating voice control (Whisper) and cognitive planning (LLMs) with robotics.
*   **Key Concepts**: ASR, NLU, prompt engineering, LLM-based planning, action orchestration.
*   **Discussion Points**:
    *   The ethical implications of LLM-controlled robots.
    *   The future of human-robot natural language interaction.
    *   Limitations of current LLM planners.
*   **Common Pitfalls**: LLM prompt engineering, API key management, latency issues.
*   **Activity Ideas**:
    *   Brainstorm new robot skills that an LLM could orchestrate.
    *   Have students critique a robot's response to an ambiguous voice command.

## Assessment Rubrics

### General Criteria
*   **Code Quality**: Readability, comments, adherence to ROS 2 best practices.
*   **Functionality**: Code executes without errors, meets requirements.
*   **Understanding**: Ability to explain concepts, troubleshoot issues.
*   **Problem Solving**: Approach to debugging, creative solutions.

### Project-Specific Rubrics

**Module Project 1 (Voice-Controlled Robot Arm - Conceptual):**
-   **Environment Setup**: ROS 2 is correctly installed and sourced.
-   **URDF Model**: Robot model is valid and visualized in Rviz2.
-   **ROS 2 Nodes**: Basic publisher/subscriber nodes are functional.

**Module Project 2 (Simulated Robotic Arm in Gazebo):**
-   **Gazebo World**: Custom Gazebo world is created and functional.
-   **Robot Spawning**: URDF arm is correctly spawned and visible in Gazebo.
-   **ROS 2 Control**: Arm is controllable via ROS 2 commands in Gazebo.

**Module Project 3 (Autonomous Robot Navigation in Isaac Sim):**
-   **Isaac Sim Setup**: Isaac Sim environment and robot are configured.
-   **VSLAM Implementation**: VSLAM is running and providing localization.
-   **Nav2 Integration**: Robot navigates autonomously to a goal.

**Module Project 4 (Autonomous Humanoid with Voice Control - Capstone):**
-   **VLA Pipeline**: All components (Whisper, LLM, Nav2, Isaac Sim) are integrated.
-   **Command Execution**: Humanoid executes multi-step voice commands.
-   **Error Handling**: Basic error handling is implemented.

## Additional Instructor Resources

*(This section will be populated with links to external teaching materials, additional exercises, and advanced topics during the "Final Phase: Polish & Cross-Cutting Concerns" tasks.)*
