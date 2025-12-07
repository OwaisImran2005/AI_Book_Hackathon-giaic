import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from builtin_interfaces.msg import Time


class MinimalTimer(Node):

    def __init__(self):
        super().__init__('minimal_timer')
        self.publisher_ = self.create_publisher(String, 'time_topic', 10)
        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.get_logger().info('MinimalTimer node started, publishing time to /time_topic')

    def timer_callback(self):
        msg = String()
        current_time = self.get_clock().now().to_msg()
        msg.data = f'Current time: {current_time.sec}.{current_time.nanosec:09d}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    minimal_timer = MinimalTimer()
    rclpy.spin(minimal_timer)
    minimal_timer.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
