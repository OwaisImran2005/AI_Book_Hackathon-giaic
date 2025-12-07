import rclpy
from rclpy.node import Node
from my_robot_controller.msg import RobotCommand # Import custom message

class CommandPublisher(Node):
    def __init__(self):
        super().__init__('command_publisher')
        self.publisher_ = self.create_publisher(RobotCommand, 'robot_command_topic', 10)
        timer_period = 1.0 # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = RobotCommand()
        msg.command_type = 'move'
        msg.linear_velocity_x = 0.5 * (self.i % 2) # Toggle between 0.0 and 0.5
        msg.angular_velocity_z = 0.0
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.command_type}" Vx={msg.linear_velocity_x}')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    node = CommandPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
