from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'hello_physical_ai'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[py]*')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='user@example.com',
    description='A simple ROS 2 publisher and subscriber example for the Physical AI Book - Chapter 1.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'talker = hello_physical_ai.publisher_member_function:main',
            'listener = hello_physical_ai.subscriber_member_function:main',
        ],
    },
)
