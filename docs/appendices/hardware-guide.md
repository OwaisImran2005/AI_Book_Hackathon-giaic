# Hardware Guide

This section provides recommendations for hardware components necessary to follow the tutorials and build the projects in this book.

## Minimum Requirements

To ensure a smooth learning experience, your development machine should meet the following minimum specifications:

-   **Operating System**: Ubuntu 22.04 LTS (native installation or highly performant virtual machine/WSL2)
-   **CPU**: Quad-core processor (Intel Core i5 8th gen / AMD Ryzen 5 2000 series or newer)
-   **RAM**: 16 GB DDR4 (32 GB recommended for NVIDIA Isaac Sim)
-   **GPU**: NVIDIA GPU with 8 GB VRAM (e.g., GeForce RTX 2060, Quadro P4000) for simulation and AI tasks. NVIDIA Isaac Sim and Isaac ROS are heavily optimized for NVIDIA GPUs.
-   **Storage**: 256 GB SSD (512 GB or 1 TB NVMe SSD recommended for faster loading times)
-   **Internet Connection**: Stable broadband connection for software downloads and updates

## Recommended Hardware Kits

For optimal performance, especially for modules involving NVIDIA Isaac Sim and Isaac ROS, an NVIDIA GPU is highly recommended.

### Budget-Friendly Workstation (Local Development)
-   **CPU**: Intel Core i7 (10th Gen or newer) or AMD Ryzen 7 (3000 series or newer)
-   **RAM**: 32 GB DDR4
-   **GPU**: NVIDIA GeForce RTX 3060 (12 GB VRAM) or RTX 4060 (12 GB VRAM)
-   **Storage**: 1 TB NVMe SSD
-   **Operating System**: Ubuntu 22.04 LTS (native installation recommended)

### High-Performance Workstation (Local Development)
-   **CPU**: Intel Core i9 (12th Gen or newer) or AMD Ryzen 9 (5000 series or newer)
-   **RAM**: 64 GB DDR4/DDR5
-   **GPU**: NVIDIA GeForce RTX 3080 (10 GB VRAM) / RTX 3090 (24 GB VRAM) / RTX 4080 (16 GB VRAM) or newer
-   **Storage**: 2 TB NVMe SSD
-   **Operating System**: Ubuntu 22.04 LTS (native installation recommended)

### Mini PC / NVIDIA Jetson (Edge Robotics)
For deploying to smaller, embedded platforms, consider:
-   **NVIDIA Jetson Orin Nano Developer Kit**: For small-scale AI and robotics projects.
-   **NVIDIA Jetson Orin NX Developer Kit**: For more demanding edge AI applications.
*(Note: Some Isaac ROS components are optimized for Jetson platforms.)*

## Robot Platforms

For advanced modules and the capstone project, specific robot platforms or components might be recommended:

### Mobile Robots
-   **TurtleBot 4**: A popular open-source mobile robot platform with ROS 2 support, suitable for navigation and basic manipulation. [Link to TurtleBot 4]
-   **Husky A200 / Jackal (Clearpath Robotics)**: Robust outdoor-ready mobile robot platforms for research and development. [Link to Clearpath Robotics]

### Manipulator Arms
-   **UR5e / UR10e (Universal Robots)**: Collaborative robot arms widely used in industry and research.
-   **Franka Emika Panda**: A highly precise and sensitive collaborative robot arm.

### Humanoid Robots (Simulation Focus)
-   **NVIDIA Digit (Agility Robotics)**: A bipedal humanoid robot. This book primarily focuses on simulating such robots in Isaac Sim.
-   **Unitree Go1 / Go2**: Quadruped robots that offer dynamic locomotion.

*(These are general recommendations. The book focuses on simulation, so physical hardware is optional for most chapters.)*

## Cloud Alternatives

If you do not have access to the recommended hardware, cloud-based development environments can be utilized.

*(Refer to the [Cloud Setup Guide](./cloud-setup.md) for detailed instructions on setting up cloud instances with GPU support.)*
