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
