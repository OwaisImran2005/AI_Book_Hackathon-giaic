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
