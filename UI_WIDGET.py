import math
import numpy as np
import omni
from omni.isaac.core import SimulationContext
from omni.isaac.core.utils.nucleus import get_assets_root_path
from omni.isaac.core.utils.stage import get_current_stage
from omni.isaac.core.utils.prims import get_prim_at_path
from omni.isaac.core.articulations import Articulation
from omni.isaac.core.articulations import ArticulationView
from omni.isaac.franka.controllers.rmpflow_controller import RMPFlowController
from omni.isaac.core.utils.types import ArticulationAction
from omni.isaac.core.simulation_context import SimulationContext       
from omni.isaac.franka import KinematicsSolver



from omni.ui import Window, Label, Button
from pydantic import BaseModel, Field
from typing import List



import omni.ui as ui
import asyncio
import carb

import omni.ui as ui
import carb

def on_submit(user_name):
    carb.log_info(f"Submit button clicked by user: {user_name}")

# Build the UI
window = ui.Window("Button Argument Example", width=300, height=150)
with window.frame:
    with ui.VStack():
        ui.Label("Click the button with an argument:", height=20)
        ui.Button(
            "Submit", 
            clicked_fn=lambda: on_submit("Alice")
        )



# for i in range(1, parsed_data["steps"] + 1):
#     window_name = f"window_{i}"
#     locals()[window_name] = ui.Window(f"User Input Example {i}", width=300, height=200)


#     with window_name.frame:
#         with ui.VStack():
#             ui.Label(f"the {i}th task is:")
#             input_field = ui.StringField()
#             ui.Button("Submit", clicked_fn=on_submit)












# # Callback for button click
# def on_button_click():
#     carb.log_info("Button clicked: User triggered an action.")
#     user_name = "Bob"
#     action = "selected an option"

#     carb.log_warn("User Action: {} has {}.".format(user_name, action))
  
#     sim_context = SimulationContext()
#     articulation_root_path = "/panda"
#     stage = get_current_stage()
#     articulation_root_prim = get_prim_at_path(articulation_root_path)
#     robot = Articulation(articulation_root_path)

#     # Initialize the articulation view (optional: in simulation loop)
#     robot.initialize()

#     robot_handle =  KinematicsSolver(robot)
#     current_joint_positions = robot.get_joint_positions()
#     # Modify the last two elements of the current_joint_positions array
#     current_joint_positions[-2:] = [0, 0]

#     print("Modified joint positions:", current_joint_positions)


#     action = ArticulationAction(joint_positions=current_joint_positions)
#     robot.apply_action(action)
#     window.destroy()





# # Callback for text input
# def on_text_submit():
#     user_text = text_field.model.get_value_as_string()

    



# # UI Layout
# with window.frame:
#     with ui.VStack():
#         ui.Label("Enter some text and click the button:", height=20)
        
#         # Text Field for user input
#         text_field = ui.StringField()
#         ui.Button("Submit", clicked_fn=on_text_submit)
        
#         # Button for logging
#         ui.Button("Log Info Button", clicked_fn=on_button_click)
