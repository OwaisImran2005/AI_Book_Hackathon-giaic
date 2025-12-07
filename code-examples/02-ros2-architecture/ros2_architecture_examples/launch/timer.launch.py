from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ros2_architecture_examples',
            executable='minimal_timer',
            name='minimal_timer_node'
        )
    ])
