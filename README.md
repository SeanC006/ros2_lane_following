# ROS2 Lane Following (Gazebo Simulation)

This project implements lane detection and autonomous steering using:

- ROS2 Humble
- Gazebo simulation (TurtleBot3 waffle_pi)
- OpenCV computer vision

## Pipeline
Camera (/camera/image_raw)
→ OpenCV lane detection
→ Steering angle output
→ (Next: /cmd_vel control)
