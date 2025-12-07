import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        # Create a publisher to the 'topic' topic with a queue size of 10
        # The String message type is used to send simple text messages
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        # Create a timer that calls the timer_callback function every 0.5 seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        # Create a String message
        msg = String()
        # Set the message data to a formatted string
        msg.data = 'Hello ROS 2 World: %d' % self.i
        # Publish the message
        self.publisher_.publish(msg)
        # Log the published message for debugging
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1


def main(args=None):
    # Initialize the ROS 2 Python client library
    rclpy.init(args=args)

    # Create an instance of the MinimalPublisher node
    minimal_publisher = MinimalPublisher()

    # Spin the node, allowing its callbacks to be called
    # This will keep the node alive until it's explicitly shut down or Ctrl+C is pressed
    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # This is important to free up resources
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
