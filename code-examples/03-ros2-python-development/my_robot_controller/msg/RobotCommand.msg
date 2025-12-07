# msg/RobotCommand.msg
string command_type  # e.g., "move", "stop", "turn"
float32 linear_velocity_x
float32 angular_velocity_z