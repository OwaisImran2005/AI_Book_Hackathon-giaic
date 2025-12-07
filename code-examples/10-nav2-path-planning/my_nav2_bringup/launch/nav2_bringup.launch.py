import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from nav2_common.launch import RewrittenYaml


def generate_launch_description():
    # Get the launch directory
    bringup_dir = get_package_share_directory('nav2_bringup')
    my_nav2_bringup_dir = get_package_share_directory('my_nav2_bringup')

    # Create the launch configuration variables
    namespace = LaunchConfiguration('namespace')
    use_sim_time = LaunchConfiguration('use_sim_time')
    autostart = LaunchConfiguration('autostart')
    params_file = LaunchConfiguration('params_file')
    default_bt_xml_filename = LaunchConfiguration('default_bt_xml_filename')
    map_subscribe_transient_local = LaunchConfiguration('map_subscribe_transient_local')
    
    # Optional: Initial pose for AMCL if not using VSLAM for initial pose
    # initial_pose_x = LaunchConfiguration('initial_pose_x')
    # initial_pose_y = LaunchConfiguration('initial_pose_y')
    # initial_pose_yaw = LaunchConfiguration('initial_pose_yaw')

    lifecycle_nodes = ['controller_server',
                       'planner_server',
                       'recoveries_server',
                       'bt_navigator',
                       'waypoint_follower']

    # Rewrite the YAML file with robot_id as namespace for all params
    param_substitutions = {
        'default_bt_xml_filename': default_bt_xml_filename,
        'autostart': autostart,
        'map_subscribe_transient_local': map_subscribe_transient_local,
        # 'initial_pose.x': initial_pose_x,
        # 'initial_pose.y': initial_pose_y,
        # 'initial_pose.yaw': initial_pose_yaw,
    }

    # Pass the Nav2 params file.
    configured_params = RewrittenYaml(
            source_file=params_file,
            root_key=namespace,
            param_rewrites=param_substitutions,
            convert_types=True)

    stdout_linebuf_envvar = SetEnvironmentVariable('RCUTILS_LOGGING_BUFFERED_STREAM', '1')

    declare_namespace_cmd = DeclareLaunchArgument(
        'namespace',
        default_value='',
        description='Top-level namespace')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true')

    declare_autostart_cmd = DeclareLaunchArgument(
        'autostart', default_value='true',
        description='Automatically startup the nav2 stack')

    declare_params_file_cmd = DeclareLaunchArgument(
        'params_file',
        default_value=os.path.join(my_nav2_bringup_dir, 'config', 'nav2_params.yaml'),
        description='Full path to the ROS2 parameters file to use')

    declare_bt_xml_cmd = DeclareLaunchArgument(
        'default_bt_xml_filename',
        default_value=os.path.join(
            get_package_share_directory('nav2_bt_navigator'),
            'behavior_trees', 'navigate_w_replanning_and_recovery.xml'),
        description='Full path to the behavior tree xml file to use')

    declare_map_subscribe_transient_local_cmd = DeclareLaunchArgument(
        'map_subscribe_transient_local', default_value='false',
        description='Whether to set the map subscriber QoS profile to transient local')

    # Add here the VSLAM localization node or similar
    # In a real scenario, VSLAM (from Chapter 9) would publish to /odom or /tf
    # and /initialpose might be used. For simplicity, we assume VSLAM provides accurate /odom
    # and Nav2 consumes it.
    
    # Nav2 Lifecycle Manager
    nav_group = GroupAction([
        stdout_linebuf_envvar,
        Node(
            package='nav2_controller',
            executable='controller_server',
            output='screen',
            parameters=[configured_params],
            remappings=[('cmd_vel', '/cmd_vel')],
            arguments=['--ros-args', '--log-level', 'info'],
        ),
        Node(
            package='nav2_planner',
            executable='planner_server',
            name='planner_server',
            output='screen',
            parameters=[configured_params],
            arguments=['--ros-args', '--log-level', 'info'],
        ),
        Node(
            package='nav2_recoveries',
            executable='recoveries_server',
            name='recoveries_server',
            output='screen',
            parameters=[configured_params],
            arguments=['--ros-args', '--log-level', 'info'],
        ),
        Node(
            package='nav2_bt_navigator',
            executable='bt_navigator',
            name='bt_navigator',
            output='screen',
            parameters=[configured_params],
            arguments=['--ros-args', '--log-level', 'info'],
        ),
        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_navigation',
            output='screen',
            arguments=['--ros-args', '--log-level', 'info'],
            parameters=[{'autostart': autostart,
                         'node_names': lifecycle_nodes}]
        )
    ])

    # Bring up the nav2 stack
    return LaunchDescription([
        declare_namespace_cmd,
        declare_use_sim_time_cmd,
        declare_autostart_cmd,
        declare_params_file_cmd,
        declare_bt_xml_cmd,
        declare_map_subscribe_transient_local_cmd,
        nav_group
    ])
