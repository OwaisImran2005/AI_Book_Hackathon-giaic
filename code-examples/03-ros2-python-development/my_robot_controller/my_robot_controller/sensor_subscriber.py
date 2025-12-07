import rclpy
from rclpy.node import Node
from std_msgs.msg import String # We'll just subscribe to a generic string for now
# from my_robot_controller.msg import SensorFeedback # Placeholder for future custom sensor feedback

class SensorSubscriber(Node):
    def __init__(self):
        super().__init__('sensor_subscriber')
        self.subscription = self.create_subscription(
            String, # Using String for simplicity, can be custom msg later
            'sensor_feedback_topic',
            self.listener_callback,
            10)
        self.subscription # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard sensor feedback: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    node = SensorSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
