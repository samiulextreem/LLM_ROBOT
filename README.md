# LLM driven Robotics manipulation

![Robot Arm Demo](robot_arm.gif)

A Python-based control system for managing and operating robotic joints through a secure API interface of grok.

## Overview

This project provides a robust interface for controlling robotic joints with secure API integration. It features:
- Automated joint control management
- API integration with security measures
- Real-time control feedback
- Environment configuration management

## Usages

1. Download and install [NVIDIA Omniverse Isaac Sim](https://developer.nvidia.com/isaac-sim) from the official NVIDIA developer portal.
2. Launch Isaac Sim and load the provided environment file`franka_arm.usd`, which contains the simulated Franka arm setup.Create an `api_keys.txt` file and place it in the installation directory.This environment enables the robot to perceive and interact with its surroundings.
3. Open VS Code and install the Omniverse Isaac Sim extension. Run the `cyberdyne.py` file, which will connect to the simulator over TCP protocol and execute commands.
4. The user instruction has to be given inside the `cyberdyne.py`  file taskmessage variable which will call the grok 2 model and receive necessary function order to execute the desired task.
5. Based on used command the robot should be able to call necessary predefined function to move the enf effector and execute desired task, like picking up blocks, moving to a certain position and stacking them etc.
