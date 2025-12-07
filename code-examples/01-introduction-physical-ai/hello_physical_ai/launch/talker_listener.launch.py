from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='hello_physical_ai',
            executable='talker',
            name='sim_talker'
        ),
        Node(
            package='hello_physical_ai',
            executable='listener',
            name='sim_listener'
        )
    ])
