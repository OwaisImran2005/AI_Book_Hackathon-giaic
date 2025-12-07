import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        # Create a subscriber to the 'topic' topic with a queue size of 10
        # The String message type is used to receive simple text messages
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        # Log the received message data
        self.get_logger().info('I heard: "%s"' % msg.data)


def main(args=None):
    # Initialize the ROS 2 Python client library
    rclpy.init(args=args)

    # Create an instance of the MinimalSubscriber node
    minimal_subscriber = MinimalSubscriber()

    # Spin the node, allowing its callbacks to be called
    # This will keep the node alive until it's explicitly shut down or Ctrl+C is pressed
    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # This is important to free up resources
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
