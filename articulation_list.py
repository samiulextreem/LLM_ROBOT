from omni.isaac.core.utils.stage import get_current_stage
from omni.isaac.core.utils.prims import get_prim_at_path
from omni.isaac.core.articulations import Articulation
from omni.isaac.core.utils.types import ArticulationAction
import numpy as np




# Define the path to your articulation root
articulation_root_path = "/panda"

# Get the current USD stage
stage = get_current_stage()

# Get the articulation root prim
articulation_root_prim = get_prim_at_path(articulation_root_path)

if articulation_root_prim:
    # Create an ArticulationView for the root
    articulation_view = Articulation(articulation_root_path)
    
    # Initialize the articulation view (optional: in simulation loop)
    articulation_view.initialize()
    
    # Retrieve all joint names
    joint_names = articulation_view.dof_properties
    print("List of joint names:", joint_names)
else:
    print(f"Articulation root at {articulation_root_path} not found.")

    # Example: Set the position of the first joint
if joint_names.all():
        # Create a dictionary to set positions for each joint
    action = ArticulationAction(joint_positions=np.array([3.0, -1.0, 0.0, -2.2, 0.0, 2.4, 0.8, 0.0, 0.0]))
    print(action)
        # Apply the joint positions
    articulation_view.apply_action(action)
    print("Joint positions have been set.")
else:
    print("No joints found in the articulation.")