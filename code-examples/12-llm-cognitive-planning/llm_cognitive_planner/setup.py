from setuptools import find_packages, setup

package_name = 'llm_cognitive_planner'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'openai'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='user@example.com',
    description='LLM Cognitive Planning examples for the Physical AI Book - Chapter 12.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'cognitive_planner = llm_cognitive_planner.cognitive_planner_node:main',
        ],
    },
)
