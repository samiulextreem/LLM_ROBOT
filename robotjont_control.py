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
import carb











sim_context = SimulationContext()
articulation_root_path = "/panda"
stage = get_current_stage()
articulation_root_prim = get_prim_at_path(articulation_root_path)
robot = Articulation(articulation_root_path)
robot_handle =  KinematicsSolver(robot)


# Initialize the articulation view (optional: in simulation loop)
robot.initialize()






def robot_operator_handle(num1,num2,num3):
    target_position = np.array([num1, num2, num3])  # x, y, z in meters
    target_orientation = np.array([0.707, 0, 0.707, 0])  # Quaternion (x, y, z, w)

    position , orientation = robot_handle.compute_end_effector_pose()
    print(position)
    
    action, is_solvalbe = robot_handle.compute_inverse_kinematics(target_position, target_orientation)
    if is_solvalbe:
        print("Solution found. joint_positions:", action.joint_positions)
        robot.apply_action(action)
    else:
        print("No solution found")






robot_operator_handle(0.59,0.009,0.2)
















































# import omni
# from omni.isaac.core.articulations import Articulation 
# from omni.isaac.core.utils.types import ArticulationAction
# from omni.isaac.core.utils.prims import get_prim_at_path
# from omni.isaac.core.utils.stage import get_current_stage
# from omni.isaac.franka import KinematicsSolver
# # from omni.isaac.motion_generation import KinematicsSolver
# from omni.isaac.core.simulation_context import SimulationContext  
# import numpy as np












