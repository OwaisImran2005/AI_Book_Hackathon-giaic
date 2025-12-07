# Cloud Setup Guide

This guide provides instructions for setting up cloud-based development environments to run the tutorials and projects in this book. This is an alternative if you do not have access to the recommended local hardware.

## Supported Cloud Platforms

*(This section will be populated with specific cloud platform recommendations, instance types, and setup instructions during the "Final Phase: Polish & Cross-Cutting Concerns" tasks.)*

## General Cloud Setup Steps

1.  **Choose a Cloud Provider**: Select a cloud provider that offers GPU-accelerated instances (e.g., AWS, Google Cloud, Azure).
2.  **Select Instance Type**: Choose an instance type with adequate CPU, RAM, and GPU resources. Refer to the [Hardware Guide](./hardware-guide.md) for minimum recommendations.
3.  **Operating System**: Launch an instance with Ubuntu 22.04 LTS.
4.  **SSH Access**: Configure SSH access to your instance.
5.  **Install NVIDIA Drivers**: Install the appropriate NVIDIA GPU drivers and CUDA toolkit for your instance.
6.  **Clone Repository**: Clone the book's companion code repository:
    ```bash
    git clone https://github.com/specifykit/ai-native-book-code-examples.git # Placeholder URL
    ```
7.  **Install Dependencies**: Follow the environment setup instructions in Module 1 to install ROS 2, Gazebo, and other required software.

## Running Docker Containers in the Cloud

Docker containers provide a consistent and isolated environment, making them ideal for cloud-based development. The book provides Dockerfiles to set up your ROS 2 and Isaac ROS environments.

### 1. Build the Docker Image (Example: ROS 2 Humble)

First, you need to build the Docker image for your desired environment. Navigate to the `docker/` directory of the book's code examples on your cloud instance.

```bash
cd /path/to/ai-native-book/docker
docker build -t ros2_humble_dev -f Dockerfile.ros2_humble .
```
This command builds an image named `ros2_humble_dev` using the `Dockerfile.ros2_humble`.

### 2. Run the Docker Container

Once the image is built, you can run a container from it. This command launches an interactive container with necessary privileges and mounts for graphical applications if needed.

```bash
docker run -it --rm --privileged \
    --network host \
    --runtime nvidia \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v /path/to/your/ros2_ws:/ros2_ws:rw \
    --name ros2_dev_container \
    ros2_humble_dev bash
```
**Explanation of parameters:**
-   `-it`: Interactive and pseudo-TTY.
-   `--rm`: Remove container after exit.
-   `--privileged`: Gives extended privileges (often needed for robotics simulations).
-   `--network host`: Allows the container to use the host's network stack (important for ROS 2 discovery).
-   `--runtime nvidia`: Enables GPU access within the container (requires NVIDIA Container Toolkit on host).
-   `-e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:rw`: Enables graphical forwarding for GUI applications (e.g., Rviz2, Gazebo).
-   `-v /path/to/your/ros2_ws:/ros2_ws:rw`: Mounts your local ROS 2 workspace into the container, so you can edit code on the host and build/run in the container. **Replace `/path/to/your/ros2_ws` with the actual path to your workspace.**
-   `--name ros2_dev_container`: Assigns a name to your container.
-   `ros2_humble_dev`: The name of the Docker image to use.
-   `bash`: Runs a bash shell inside the container.

### 3. Develop Inside the Container

Once inside the container, your ROS 2 environment will be sourced, and your mounted workspace (`/ros2_ws`) will be available. You can then proceed with building and running your ROS 2 packages as if you were on a native Ubuntu installation.

### 4. Isaac ROS Specific Containers

For Isaac ROS development, you would typically use NVIDIA's pre-built Isaac ROS Docker images (as discussed in Chapter 9). The process is similar: pull the image and run it with GPU and network configurations.

```bash
docker pull nvcr.io/nvidia/ros:humble-desktop-cuda-jammy
docker run -it --rm --network host --privileged \
    --runtime nvidia \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix/:/tmp/.X11-unix:rw \
    -v /path/to/your/ros2_ws:/ros2_ws:rw \
    --name isaac_ros_dev_container \
    nvcr.io/nvidia/ros:humble-desktop-cuda-jammy bash
```
*(Remember to replace `/path/to/your/ros2_ws`.)*
