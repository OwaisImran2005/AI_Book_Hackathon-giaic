import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from my_robot_controller.action import Countdown # Import custom action
import time

class CountdownActionServer(Node):
    def __init__(self):
        super().__init__('countdown_action_server')
        self._action_server = ActionServer(
            self,
            Countdown,
            'countdown',
            self.execute_callback)
        self.get_logger().info('Countdown action server started.')

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        feedback_msg = Countdown.Feedback()
        initial_count = goal_handle.request.target_count
        
        for i in range(initial_count, 0, -1):
            feedback_msg.current_progress = i # Corrected field name
            self.get_logger().info(f'Feedback: {feedback_msg.current_progress}')
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1) # Simulate work

        goal_handle.succeed()
        result = Countdown.Result()
        result.final_count = 0
        result.success = True
        self.get_logger().info('Goal succeeded!')
        return result

def main(args=None):
    rclpy.init(args=args)
    node = CountdownActionServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
