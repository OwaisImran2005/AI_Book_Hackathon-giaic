# Chapter 9: Isaac ROS Perception Code Examples

This directory provides a guide for setting up your Isaac ROS Docker environment and utilizing Isaac ROS packages for perception tasks, as described in Chapter 9: Isaac ROS Perception of the "Physical AI & Humanoid Robotics" book. Due to the nature of Docker and its interaction with the host system, direct automated execution of these steps is not feasible via this workflow. Instead, this `README.md` outlines the necessary manual steps and provides command snippets for setting up Isaac ROS.

## Manual Setup Steps (Isaac ROS Docker Environment)

Please follow these steps to set up your Isaac ROS Docker environment:

### Part 1: Isaac ROS Docker Environment Setup

### Step 1: Install Docker and NVIDIA Container Toolkit

If you haven't already, install Docker and the NVIDIA Container Toolkit on your Ubuntu host machine.

```bash
# Install Docker
sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
newgrp docker # You might need to log out and log back in for this to take effect

# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -fsSL https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt update
sudo apt install -y nvidia-container-toolkit
sudo systemctl restart docker
```

### Step 2: Pull Isaac ROS Docker Image

Pull the appropriate Isaac ROS Docker image (e.g., for ROS 2 Humble):

```bash
docker pull nvcr.io/nvidia/ros:humble-desktop-cuda-jammy
```

### Step 3: Run the Isaac ROS Docker Container

```bash
docker run -it --rm --network host --privileged \
    --runtime nvidia \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix/:/tmp/.X11-unix:rw \
    -v /dev:/dev \
    --name isaac_ros_container \
    nvcr.io/nvidia/ros:humble-desktop-cuda-jammy /bin/bash
```
This command launches an interactive Docker container with GPU access, network host mode (important for ROS 2 communication with Isaac Sim), and display forwarding.

### Part 2: Isaac Sim Setup for VSLAM

In Isaac Sim, you need a robot with an RGB-D camera and IMU. We'll use the pre-built `Carter` robot for simplicity, which has these sensors.

### Step 4: Launch Isaac Sim with Carter Robot

1.  Launch Isaac Sim.
2.  Go to `File > Open` and open `Isaac/Robots/Carter/carter.usd`.
    *   *(Alternatively, create a new scene and add `carter.usd` from the Content browser.)*
3.  Ensure the `omni.isaac.ros2_bridge` extension is enabled.

### Part 3: Running Isaac ROS Visual SLAM

### Step 5: Install `isaac_ros_visual_slam` in Container

Inside your `isaac_ros_container` Docker environment:
```bash
# Clone the Isaac ROS Visual SLAM repository
cd ~/ros2_ws/src
git clone https://github.com/NVIDIA-AI-IOT/isaac_ros_visual_slam.git
git clone https://github.com/NVIDIA-AI-IOT/isaac_ros_common.git # Common dependencies

# Build the workspace
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src --rosdistro humble -y
colcon build --packages-select isaac_ros_visual_slam isaac_ros_common

# Source the workspace
source install/setup.bash
```

### Step 6: Launch VSLAM Node

Inside the `isaac_ros_container` (in your `~/ros2_ws`):

```bash
ros2 launch isaac_ros_visual_slam isaac_ros_visual_slam_carter.launch.py
```
This launch file is typically provided within the `isaac_ros_visual_slam` package and is configured for the Carter robot.

### Step 7: Visualize VSLAM Output in Rviz2

Open a *new* terminal on your Ubuntu host machine (not in the Docker container), source your ROS 2 environment, and launch Rviz2:

```bash
source /opt/ros/humble/setup.bash
rviz2
```
In Rviz2, add a "Pose" display for the `/visual_slam/tracking/slam_pose` topic and a "PointCloud2" display for the `/visual_slam/tracking/map_cloud` topic. You should see Carter's estimated pose and a growing map of its environment as it moves in Isaac Sim.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
