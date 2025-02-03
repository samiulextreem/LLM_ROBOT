import carb
import omni.log
import logging

# Configure file logging
logging.basicConfig(filename="robot_control.log", level=logging.DEBUG)
carb.log_info("Starhellot...")

carb.log_info("Starting robot control script...")
try:
    # Your code here
    carb.log_info("Gripper movement successful!")
except Exception as e:
    carb.log_error(f"Error: {str(e)}")

