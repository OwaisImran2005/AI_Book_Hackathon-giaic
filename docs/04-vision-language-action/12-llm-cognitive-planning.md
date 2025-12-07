# Chapter 12: LLM Cognitive Planning

:::info Chapter Info
**Module**: Vision-Language-Action | **Duration**: 5 hours | **Difficulty**: Advanced
:::

## Learning Objectives
By the end of this chapter, you will:
1. Understand the role of Large Language Models (LLMs) in high-level cognitive planning for robotics.
2. Learn prompt engineering strategies to elicit step-by-step action plans from LLMs.
3. Be able to integrate LLM outputs with ROS 2 action servers to execute complex tasks.
4. Gain proficiency in structuring robot capabilities as "skills" that can be orchestrated by an LLM.

## Prerequisites
- Completed Chapter 11: Voice-to-Action, with a working voice command interface.
- Intermediate Python programming skills and a good understanding of ROS 2.
- An OpenAI API key (or access to a similar LLM service).

## What You'll Build
In this chapter, you will build an LLM-powered cognitive planner for your robot. This will involve:
- Creating a ROS 2 node that sends transcribed text commands to an LLM.
- Designing a prompt that guides the LLM to generate a sequence of robotic actions.
- Parsing the LLM's response and triggering ROS 2 actions to execute the plan.

---

## Introduction: The Robot's Inner Monologue

In the previous chapter, you taught your robot to "hear" by transcribing human voice commands into text. But how does a robot translate a complex command like "pick up the red cube and place it on the blue square" into a sequence of concrete actions? This is the domain of **cognitive planning**, a higher-level reasoning process that involves understanding the goal, breaking it down into achievable steps, and sequencing those steps logically.

Traditionally, robotic planning has relied on symbolic planners like PDDL (Planning Domain Definition Language), which require a highly structured representation of the world and the robot's capabilities. While powerful, these planners can be brittle and require significant manual effort to define. The recent explosion of **Large Language Models (LLMs)** offers a paradigm-shifting alternative. LLMs, trained on vast amounts of human knowledge, possess remarkable common-sense reasoning abilities that can be harnessed for robotic planning.

This chapter guides you through the exciting process of using LLMs as the "cognitive brain" for your robot. You learn how to design **prompts** that effectively communicate the robot's state, its available skills, and the user's high-level goal to an LLM. We explore strategies for guiding the LLM to generate a sequence of executable actions and how to parse this plan back into a format that your ROS 2 system can understand and execute. By the end of this chapter, your robot will not only understand what you say but will also be able to "think" about how to accomplish your requests, marking a significant leap toward truly intelligent and autonomous behavior.

## Core Concepts: LLM-Powered Robotic Planning

Using an LLM for robotic planning involves treating the LLM as a "planner-as-a-service" that takes a high-level goal and generates a sequence of low-level actions.

### 1. Prompt Engineering for Robotics

The key to successful LLM-based planning lies in **prompt engineering**. A well-crafted prompt provides the LLM with the necessary context to generate a useful and executable plan. A typical prompt for robotic planning might include:

*   **System Role**: "You are a helpful robotic assistant that helps a user accomplish tasks. Your responses should be a sequence of commands that the robot can execute."
*   **Environment Description**: Information about the current state of the world, including the robot's location, and the position and properties of relevant objects.
*   **Robot Capabilities (Skills)**: A description of the robot's available actions or "skills". This is crucial for grounding the LLM's plan in the robot's actual abilities.
*   **User's Command**: The transcribed text from the voice command interface.
*   **Output Format Instructions**: Explicit instructions on how the LLM should format its response (e.g., a JSON array of commands, a numbered list).

### 2. Structuring Robot Skills

For an LLM to generate a meaningful plan, it needs to know what the robot can do. We can define a set of robot **skills** as high-level actions that are implemented as ROS 2 action servers or service servers.

Example skills for a mobile manipulator:
*   `navigate_to(location)`
*   `pick_up(object)`
*   `place_on(object, location)`
*   `detect_object(object_type)`

By providing these skills in the prompt, we constrain the LLM's output to a set of actions that the robot can actually perform.

### 3. Parsing and Executing the Plan

Once the LLM generates a plan (e.g., a JSON array of commands), a ROS 2 node (the "cognitive planner") needs to:
1.  **Parse the response**: Extract the sequence of commands and their parameters.
2.  **Validate the plan**: Ensure the plan is syntactically correct and the commands are valid.
3.  **Execute the plan**: Sequentially call the corresponding ROS 2 action servers or service servers to execute each step of the plan.
4.  **Handle feedback and errors**: Monitor the execution of each step and handle any failures or unexpected outcomes.

This creates a powerful loop where a high-level command is decomposed into a sequence of executable skills, bridging the gap between natural language and robotic action.

## Hands-On Tutorial: Building an LLM Cognitive Planner

We will create a ROS 2 node that takes transcribed text, sends it to an LLM, and orchestrates the execution of a plan.

### Part 1: Setting up the LLM Cognitive Planner

### Step 1: Create a ROS 2 Python Package

Navigate to your ROS 2 workspace `src` directory (e.g., `~/ros2_ws/src`).
Create a new package called `llm_cognitive_planner`:

```bash
ros2 pkg create --build-type ament_python llm_cognitive_planner --dependencies rclpy std_msgs my_robot_controller
```
*(We depend on `my_robot_controller` to use its action definitions for plan execution.)*

### Step 2: Implement the Cognitive Planner Node

Create `llm_cognitive_planner/llm_cognitive_planner/cognitive_planner_node.py` with the following content:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.action import ActionClient
from my_robot_controller.action import Countdown # Reusing Countdown action for simplicity
import openai
import os
import json

class CognitivePlannerNode(Node):
    def __init__(self):
        super().__init__('cognitive_planner_node')
        self.subscription = self.create_subscription(
            String,
            'voice_command_text',
            self.voice_command_callback,
            10)
        self.openai_client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        # Action client to execute the plan
        self._action_client = ActionClient(self, Countdown, 'countdown')

        self.get_logger().info('LLM Cognitive Planner Node started. Waiting for voice commands...')

    def voice_command_callback(self, msg):
        self.get_logger().info(f'Received voice command: "{msg.data}"')
        
        # Call LLM to generate a plan
        plan = self.generate_plan(msg.data)
        
        if plan:
            self.execute_plan(plan)

    def generate_plan(self, command_text):
        prompt = f"""
        You are a helpful robotic assistant. Your task is to take a user's command and break it down into a sequence of executable robot skills.

        Available robot skills:
        - countdown(target_count: int): A simple action that counts down from a given number.

        User command: "{command_text}"

        Your response should be a JSON array of commands. For example:
        [
            {{"skill": "countdown", "parameters": {{"target_count": 5}}}},
            {{"skill": "countdown", "parameters": {{"target_count": 3}}}}
        ]

        If the command is unclear or cannot be mapped to the available skills, return an empty JSON array.
        """

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4", # Or gpt-3.5-turbo for faster responses
                messages=[
                    {"role": "system", "content": prompt},
                ],
                response_format={"type": "json_object"}
            )
            
            plan_json = response.choices[0].message.content
            self.get_logger().info(f'LLM generated plan: {plan_json}')
            return json.loads(plan_json)

        except Exception as e:
            self.get_logger().error(f"Error generating plan from LLM: {e}")
            return None

    def execute_plan(self, plan):
        if not isinstance(plan, list):
            self.get_logger().error("Plan is not a list of commands.")
            return

        for command in plan:
            skill = command.get("skill")
            parameters = command.get("parameters")

            if skill == "countdown":
                self.execute_countdown_action(parameters.get("target_count", 0))
            else:
                self.get_logger().warn(f"Unknown skill: {skill}")

    def execute_countdown_action(self, target_count):
        self.get_logger().info(f"Executing countdown action with target: {target_count}")
        
        goal_msg = Countdown.Goal()
        goal_msg.target_count = target_count

        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected by action server')
            return

        self.get_logger().info('Goal accepted by action server')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Action result: {result.success}')
    
    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Action feedback: {feedback_msg.feedback.current_progress}')


def main(args=None):
    rclpy.init(args=args)
    node = CognitivePlannerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```
Add entry point in `setup.py`: `'cognitive_planner = llm_cognitive_planner.cognitive_planner_node:main',`

### Step 3: Build and Test

Navigate to your workspace root (`~/ros2_ws`) and build your package:
```bash
colcon build --packages-select llm_cognitive_planner
source install/setup.bash # Re-source to find new executables
```

## Usage

1.  **Ensure OpenAI API Key is Set**:
    ```bash
    export OPENAI_API_KEY="YOUR_API_KEY" # Replace with your actual key
    ```
2.  **Run Cognitive Planner Node**:
    ```bash
    ros2 run llm_cognitive_planner cognitive_planner
    ```
3.  **Run Supporting Nodes**:
    *   In separate terminals, run the `whisper_asr_node` (from Chapter 11) to provide voice commands, and the `countdown_action_server` (from Chapter 3) to execute the plan.
4.  **Speak Commands**: Speak a command like "Start a countdown from 5". The `whisper_asr_node` will transcribe this and publish it to `/voice_command_text`. The `cognitive_planner` will receive this text, call the LLM, and execute the `countdown` action.

## Deep Dive: Prompt Engineering and Few-Shot Learning

Effective prompt engineering is key to getting the best performance from LLMs.

*   **Few-Shot Learning**: Providing examples in the prompt (as we did with the JSON format) is a form of few-shot learning. It guides the LLM to produce the desired output format and structure.
*   **Role-Playing**: Assigning a role to the LLM (e.g., "You are a helpful robotic assistant") can improve the quality and relevance of its responses.
*   **Contextual Information**: The more context you provide about the environment and robot state, the better the LLM's plan will be. This can include:
    *   `robot_location: (x, y, z)`
    *   `objects_in_scene: [{name: "red_cube", position: (x1, y1, z1)}, {name: "blue_square", position: (x2, y2, z2)}]`
    *   `robot_gripper_state: "empty"`

## Troubleshooting: LLM Cognitive Planning Issues

1.  **Issue**: `OPENAI_API_KEY environment variable not set` error.
    *   **Cause**: You forgot to set the `OPENAI_API_KEY` environment variable.
    *   **Solution**: Run `export OPENAI_API_KEY="YOUR_API_KEY"` before launching the `cognitive_planner_node`. Add it to your `~/.bashrc` for persistence.
2.  **Issue**: LLM returns an empty plan or an incorrectly formatted response.
    *   **Cause**: The prompt is not clear enough, the user command is too ambiguous, or the LLM's "creativity" is too high.
    *   **Solution**:
        *   Refine your prompt to be more explicit about the desired output format.
        *   Provide more examples (few-shot learning).
        *   Adjust the `temperature` parameter in the OpenAI API call (lower values make the output more deterministic).
3.  **Issue**: Plan execution fails (action client does not get a response).
    *   **Cause**: The corresponding ROS 2 action server is not running or not reachable.
    *   **Solution**: Ensure the action server for each skill (e.g., `countdown_action_server`) is running and properly advertised in the ROS 2 graph.
4.  **Issue**: High latency between command and action.
    *   **Cause**: LLM API call latency can be significant.
    *   **Solution**: For real-time applications, consider using smaller, faster models (e.g., `gpt-3.5-turbo`), or exploring locally hosted or edge LLMs to reduce network latency.
5.  **Issue**: LLM "hallucinates" skills that don't exist.
    *   **Cause**: The prompt doesn't sufficiently constrain the LLM's output.
    *   **Solution**: Be very clear in your prompt about the *only* available skills. Add an explicit instruction like "Only use skills from the provided list."

## Practice Exercises

1.  **Add a New Skill**:
    *   Define a new ROS 2 action (e.g., `MoveTo.action` with `x`, `y`, `z` as goal).
    *   Implement an action server for this new skill.
    *   Update the prompt in `cognitive_planner_node.py` to include this new `move_to(x, y, z)` skill.
    *   Test it with a voice command like "Move to position 1, 2, 0".
2.  **Implement Plan Validation**:
    *   In `cognitive_planner_node.py`, add a validation step after receiving the plan from the LLM.
    *   Check if each command in the plan corresponds to a valid skill and has the correct parameters.
    *   Log an error if the plan is invalid.
3.  **Interactive Plan Confirmation**:
    *   Modify `cognitive_planner_node.py` to publish the generated plan to a new topic for user confirmation.
    *   Create a separate node that subscribes to this plan topic, prints it to the console, and waits for user input ("yes" or "no") before signaling the cognitive planner to proceed with execution.

## Summary

In this chapter, you've integrated a Large Language Model as a cognitive planner for your robot:
- You learned how to use prompt engineering to guide an LLM to generate action plans.
- You created a ROS 2 node that communicates with an LLM and orchestrates plan execution.
- You understood the importance of defining robot "skills" for the LLM to reason about.

This marks a significant step towards creating robots that can understand and act upon high-level, natural language instructions.

## Next Steps

In the final chapter of this module, "Capstone: Autonomous Humanoid," you will bring together all the components you've built—perception, navigation, voice control, and cognitive planning—to create a fully autonomous humanoid robot.

➡️ Continue to [Chapter 13: Capstone: Autonomous Humanoid](./13-capstone-autonomous-humanoid.md)

## Additional Resources
-   [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
-   [Prompt Engineering Guide](https://www.promptingguide.ai/)
-   [ROS 2 Actions Tutorial](https://docs.ros.org/en/humble/Tutorials/Intermediate/Writing-an-Action-Server-Client/Python.html)
