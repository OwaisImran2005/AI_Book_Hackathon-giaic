# Video Demonstrations Plan and Scripts

This file will contain the plan and scripts for video demonstrations of the capstone projects.

## Capstone Project 1: Autonomous Humanoid with Voice Control

### Video Title: Voice-Controlled Humanoid: Pick and Place

### Objective:
Demonstrate the end-to-end Vision-Language-Action (VLA) pipeline, showing a simulated humanoid robot responding to natural language commands to perform a pick-and-place task.

### Script Outline:

1.  **Introduction (15s)**: Briefly introduce the concept of Physical AI and the goal of the demonstration: a humanoid robot controlled by voice.
2.  **Environment Setup (30s)**: Quick visual of Isaac Sim environment with the humanoid and a few objects (e.g., red cube, blue square).
3.  **Voice Command (15s)**: Human user speaks the command: "Robot, pick up the red cube and place it on the blue square."
4.  **ASR & LLM Planning (30s)**: Visualize (or show logs) the transcription by Whisper and the LLM generating the action plan.
5.  **Robot Execution (60s)**:
    *   Humanoid navigates to the red cube.
    *   Humanoid grasps the red cube.
    *   Humanoid navigates to the blue square.
    *   Humanoid places the red cube on the blue square.
6.  **Confirmation & Conclusion (15s)**: Humanoid confirms task completion. Recap of VLA pipeline.

### Required Shots:
-   Close-up of human speaking.
-   Isaac Sim viewport showing robot and objects.
-   Overlay of ROS 2 topic echoes for transcribed text, LLM plan, and robot commands.
-   Camera angles highlighting robot's navigation and manipulation.

*(Additional video plans and scripts will be added here.)*
