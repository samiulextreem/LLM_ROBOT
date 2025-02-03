import math
import numpy as np
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




sim_context = SimulationContext()
articulation_root_path = "/panda"
stage = get_current_stage()
articulation_root_prim = get_prim_at_path(articulation_root_path)
robot = Articulation(articulation_root_path)

# Initialize the articulation view (optional: in simulation loop)
robot.initialize()

robot_handle =  KinematicsSolver(robot)
current_joint_positions = robot.get_joint_positions()
# Modify the last two elements of the current_joint_positions array
current_joint_positions[-2:] = [0, 0]

print("Modified joint positions:", current_joint_positions)


action = ArticulationAction(joint_positions=current_joint_positions)
robot.apply_action(action)


