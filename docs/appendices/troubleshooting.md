# Troubleshooting Guide

This guide provides solutions to common issues encountered while setting up the development environment, running simulations, or implementing the code examples in this book.

## General Issues

### Issue: `command not found` or `permission denied`
- **Cause**: The command is either not installed, not in your system's PATH, or you lack execution permissions.
- **Solution**:
    1.  Ensure the software is installed correctly.
    2.  Check your `.bashrc` or `.zshrc` file for correct PATH configuration.
    3.  For permission denied, try `chmod +x <script_name>` for scripts or use `sudo` for administrative commands.

### Issue: Slow simulation performance in Gazebo/Isaac Sim
- **Cause**: Insufficient hardware resources (CPU, GPU, RAM), high-fidelity models, or unoptimized simulation settings.
- **Solution**:
    1.  Verify your system meets the [Minimum Hardware Requirements](./hardware-guide.md).
    2.  In simulation settings, reduce physics update rates, decrease sensor refresh rates, and simplify visual models.
    3.  Ensure you are using a dedicated NVIDIA GPU and its drivers are up to date.
    4.  Run simulations in "headless" mode if visual rendering is not critical.

## ROS 2 Issues

### Issue: `ros2 topic list` shows no topics
- **Cause**: ROS 2 domain ID mismatch or nodes are not running.
- **Solution**:
    1.  Ensure all ROS 2 terminals have the same `ROS_DOMAIN_ID` environment variable set.
    2.  Verify your ROS 2 nodes are correctly launched and not crashing. Check terminal output for errors.
    3.  Source your ROS 2 setup files (`source /opt/ros/humble/setup.bash` and your workspace `install/setup.bash`).

### Issue: Package build fails with `colcon build`
- **Cause**: Missing dependencies, syntax errors in code, or incorrect `package.xml` / `CMakeLists.txt`.
- **Solution**:
    1.  Read the build output carefully for specific error messages.
    2.  Install missing dependencies (`rosdep install --from-paths src --ignore-src -r -y`).
    3.  Check `package.xml` for correct dependencies and `CMakeLists.txt` for valid build commands.
    4.  Clean your build space (`colcon build --packages-select <package_name> --cmake-args -DCMAKE_BUILD_TYPE=Release --event-handlers console_direct+ --base-paths src --continue-on-error --parallel-workers 1 --force-cmake-config -DFORCE_COLOR_OUTPUT=ON`) and try again.

## NVIDIA Isaac Sim Issues

### Issue: Isaac Sim fails to launch or crashes
- **Cause**: GPU driver issues, insufficient VRAM, or conflicts with other NVIDIA software.
- **Solution**:
    1.  Update your NVIDIA GPU drivers to the latest version.
    2.  Ensure your GPU meets the minimum VRAM requirements (8GB+ recommended).
    3.  Check for conflicts with other NVIDIA Omniverse applications.
    4.  Try launching Isaac Sim with `--allow-root` if running as root (not recommended for production).

### Issue: Robot models do not load or behave unexpectedly
- **Cause**: Incorrect USD/URDF file paths, malformed model descriptions, or physics properties.
- **Solution**:
    1.  Verify all paths to meshes and textures in your USD/URDF files are correct and absolute.
    2.  Check the USD/URDF syntax for errors using a validator.
    3.  Adjust physics materials and joint properties to ensure stable behavior.

*(More specific troubleshooting steps for individual chapters and modules will be added here as content is generated.)*
