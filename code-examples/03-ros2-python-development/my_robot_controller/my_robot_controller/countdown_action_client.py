import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from my_robot_controller.action import Countdown # Import custom action

class CountdownActionClient(Node):
    def __init__(self):
        super().__init__('countdown_action_client')
        self._action_client = ActionClient(self, Countdown, 'countdown')
        self.get_logger().info('Countdown action client started.')

    def send_goal(self, target_count):
        self.get_logger().info('Waiting for action server...')
        self._action_client.wait_for_server()

        goal_msg = Countdown.Goal()
        goal_msg.target_count = target_count

        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: Final Count={result.final_count}, Success={result.success}')
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Feedback: Current Count={feedback_msg.feedback.current_progress}') # Corrected field name

def main(args=None):
    rclpy.init(args=args)
    node = CountdownActionClient()
    node.send_goal(5) # Send a goal to countdown from 5
    rclpy.spin(node)

if __name__ == '__main__':
    main()
