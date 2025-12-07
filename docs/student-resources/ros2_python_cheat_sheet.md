# ROS 2 Python Cheat Sheet

This cheat sheet provides a quick reference for common ROS 2 commands and Python code snippets.

## ROS 2 CLI Commands

### Workspace Management
-   `colcon build`: Build packages in the current workspace.
-   `colcon build --packages-select <pkg_name>`: Build a specific package.
-   `source install/setup.bash`: Source the workspace to make packages available.
-   `rosdep install -i --from-paths src --rosdistro humble -y`: Install package dependencies.

### Node/Topic/Service/Action Introspection
-   `ros2 node list`: List active ROS 2 nodes.
-   `ros2 node info <node_name>`: Get info about a specific node.
-   `ros2 topic list`: List active ROS 2 topics.
-   `ros2 topic info <topic_name>`: Get info about a specific topic.
-   `ros2 topic echo <topic_name>`: Display messages on a topic.
-   `ros2 service list`: List active ROS 2 services.
-   `ros2 service type <service_name>`: Get type of a service.
-   `ros2 action list`: List active ROS 2 actions.

### Communication Tools
-   `ros2 topic pub <topic> <msg_type> <args>`: Publish data to a topic.
-   `ros2 service call <service> <srv_type> <args>`: Call a service.

## ROS 2 Python (rclpy) Snippets

### Node Initialization
```python
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node_name')
        self.get_logger().info('My node started!')

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node) # Keep node alive
    node.destroy_node()
    rclpy.shutdown()
```

### Publisher
```python
from std_msgs.msg import String

self.publisher_ = self.create_publisher(String, 'my_topic', 10)
timer_period = 0.5
self.timer = self.create_timer(timer_period, self.timer_callback)

def timer_callback(self):
    msg = String()
    msg.data = 'Hello ROS 2!'
    self.publisher_.publish(msg)
    self.get_logger().info(f'Publishing: {msg.data}')
```

### Subscriber
```python
from std_msgs.msg import String

self.subscription = self.create_subscription(String, 'my_topic', self.listener_callback, 10)

def listener_callback(self, msg):
    self.get_logger().info(f'I heard: {msg.data}')
```

### Service Server
```python
from my_package.srv import MyService # Custom service type

self.srv = self.create_service(MyService, 'my_service', self.service_callback)

def service_callback(self, request, response):
    response.result = request.input_data * 2
    self.get_logger().info(f'Request: {request.input_data}, Response: {response.result}')
    return response
```

### Service Client
```python
from my_package.srv import MyService

self.cli = self.create_client(MyService, 'my_service')
while not self.cli.wait_for_service(timeout_sec=1.0):
    self.get_logger().info('Service not available, waiting again...')

request = MyService.Request()
request.input_data = 10
future = self.cli.call_async(request)
rclpy.spin_until_future_complete(self, future)
result = future.result()
self.get_logger().info(f'Service call result: {result.result}')
```

### Launch File Example
```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_package',
            executable='my_node',
            name='my_node_instance'
        ),
        Node(
            package='my_package',
            executable='another_node',
            name='another_node_instance'
        )
    ])
```

*(More content will be added here.)*
