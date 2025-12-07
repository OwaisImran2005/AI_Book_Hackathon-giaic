import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # Get the share directory of your robot description package
    my_robot_description_share_dir = get_package_share_directory('my_robot_description')
    
    # Path to your Xacro file
    xacro_file = os.path.join(my_robot_description_share_dir, 'xacro', 'mobile_robot.xacro')

    # Convert Xacro to URDF
    robot_description_content = os.popen(f'xacro {xacro_file}').read()

    # Start Gazebo server and client
    gazebo_ros_launch_dir = get_package_share_directory('gazebo_ros')
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(gazebo_ros_launch_dir, 'launch', 'gazebo.launch.py')),
        launch_arguments={'world': os.path.join(get_package_share_directory('my_gazebo_worlds'), 'worlds', 'empty_arm_world.world')}.items()
    )

    # Node to publish the robot model to /robot_description
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_content}], # Use converted Xacro content
        remappings=[
            ('/joint_states', 'joint_states'), # Standard remapping
        ]
    )

    # Node to spawn the robot entity in Gazebo
    spawn_entity_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'mobile_robot'],
        output='screen'
    )

    return LaunchDescription([
        gazebo_launch,
        robot_state_publisher_node,
        spawn_entity_node,
    ])
