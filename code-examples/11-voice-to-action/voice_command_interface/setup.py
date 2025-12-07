from setuptools import find_packages, setup

package_name = 'voice_command_interface'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'openai', 'SpeechRecognition', 'pyaudio'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='user@example.com',
    description='Voice-to-Action examples for the Physical AI Book - Chapter 11.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'whisper_asr_node = voice_command_interface.whisper_asr_node:main',
            'command_interpreter = voice_command_interface.command_interpreter_node:main',
        ],
    },
)