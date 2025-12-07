from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'my_robot_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[py]*'))),
        (os.path.join('share', package_name, 'msg'), glob('msg/*.msg')),
        (os.path.join('share', package_name, 'srv'), glob('srv/*.srv')),
        (os.path.join('share', package_name, 'action'), glob('action/*.action')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='user@example.com',
    description='ROS 2 Python Development examples for the Physical AI Book - Chapter 3.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'command_publisher = my_robot_controller.command_publisher:main',
            'sensor_subscriber = my_robot_controller.sensor_subscriber:main',
            'add_two_ints_server = my_robot_controller.add_two_ints_server:main',
            'add_two_ints_client = my_robot_controller.add_two_ints_client:main',
            'countdown_action_server = my_robot_controller.countdown_action_server:main',
            'countdown_action_client = my_robot_controller.countdown_action_client:main',
        ],
    },
)
