import math
import numpy as np
import omni
from omni.isaac.core import SimulationContext
from omni.isaac.core.utils.nucleus import get_assets_root_path
from omni.isaac.core.utils.stage import get_current_stage
from omni.isaac.core.utils.prims import get_prim_at_path
from omni.isaac.core.articulations import Articulation
import omni.replicator.core as rep
from omni.isaac.core.articulations import ArticulationView
from omni.isaac.franka.controllers.rmpflow_controller import RMPFlowController
from omni.isaac.core.utils.types import ArticulationAction
from omni.isaac.core.simulation_context import SimulationContext       
from omni.isaac.franka import KinematicsSolver
from omni.kit.viewport.utility import get_active_viewport

import omni.ui as ui
from omni.ui import Window, Label, Button 
from pydantic import BaseModel, Field
from typing import List
import carb
from PIL import Image
import open3d as o3d
from dotenv import load_dotenv
import os
from openai import OpenAI
# from robot_controller import RobotController

omni.kit.pipapi.install(
    package="openai",
    version="1.58.1",
    module="openai", # sometimes module is different from package name, module is used for import check
    ignore_import_check=False,
    ignore_cache=False,
    use_online_index=True,
    surpress_output=False,
    extra_args=[]
)

class AIClients:
    # Model constants
    GROK2 = "grok-2-vision-1212"
    LALMA70B = "meta/llama-3.3-70b-instruct"
    GPT4TURBO = "gpt-4-turbo-2024-04-09"
    GPT4O = "gpt-4o"

    def __init__(self, api_keys_path):
        self.api_keys = self._load_api_keys(api_keys_path)
        self.lalmar = self._init_nvidia_client()
        self.grokker = self._init_grok_client()
        self.openaiar = self._init_openai_client()
        print("finished creating agents")

    def _load_api_keys(self, api_keys_path):
        api_keys = {}
        with open(api_keys_path, 'r') as file:
            for line in file:
                if '=' in line:
                    key, value = line.strip().split('=')
                    api_keys[key] = value
        return api_keys

    def _init_nvidia_client(self):
        return OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=self.api_keys.get('NVIDIA_API_KEY')
        )

    def _init_grok_client(self):
        return OpenAI(
            base_url="https://api.x.ai/v1",
            api_key=self.api_keys.get('GROK_API_KEY')
        )

    def _init_openai_client(self):
        return OpenAI(
            api_key=self.api_keys.get('OPENAI_API_KEY')
        )

# Initialize AI clients
ai_clients = AIClients('C:\\Users\\GHOSTFISH\\AppData\\Local\\ov\\pkg\\isaac-sim-4.2.0\\api_keys.txt')
lalmar = ai_clients.lalmar
grokker = ai_clients.grokker
openaiar = ai_clients.openaiar

# Access model constants through the class
GROK2 = AIClients.GROK2
LALMA70B = AIClients.LALMA70B
GPT4TURBO = AIClients.GPT4TURBO
GPT4O = AIClients.GPT4O




def clip_ply_file(input_file, output_file):
    # Read all lines from the file
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    # Find where vertex data begins (after header)
    header_end = 10
    for i, line in enumerate(lines):
        if "end_header" in line:
            header_end = i + 1
            break
    
    # Keep header lines and filter vertex data
    header = lines[:header_end]
    filtered_lines = []
    
    for line in lines[header_end:]:
        try:
            # Split line into values and convert first value (x coordinate) to float
            values = line.split()
            x = float(values[0])
            y =  float(values[1])
            z = float(values[2])
            # Only keep lines where x <= 1
            if x <= 1 and 0 < y <= .5  and .1 < z < 1:
                filtered_lines.append(line)
        except (ValueError, IndexError):
            continue
    
    # Update vertex count in header
    for i, line in enumerate(lines):
        if "element vertex" in line:
            header[i] = f"element vertex {len(filtered_lines)}\n"
            break
    
    # Write updated file
    with open(output_file, 'w') as f:
        f.writelines(header + filtered_lines)


def robot_operator_function(num1, num2, num3):
    # Define the target coordinate
    target_position = np.array([num1, num2, num3])  # x, y, z in meters
    target_orientation = np.array([0.707, 0, 0.707, 0])  # Quaternion (x, y, z, w)

    action, is_solvalbe = robot_handle.compute_inverse_kinematics(target_position, target_orientation)
    if is_solvalbe:
        # print("Solution found. joint_positions:", action.joint_positions)
        robot.apply_action(action)
    else:
        carb.log_warn("No solution found")

    return {"num1": num1, "num2": num2, "num3": num3}



def gripping_status(image_path):
    base64_image = base64.b64encode(open(image_path, "rb").read()).decode("utf-8")
    img_messages_grip_confirm=[
        {"role": "system", "content": """based on available info, provide definitative answer to the user's request.
                                        check if the green object is completely inside the space of robot fingers"""},
                                        
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": " in the given images, is the green object is positioned completely  inside the  enclosed space formed by the two open fingers  two open fingers?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ]

    parse_response =  openaiar.beta.chat.completions.parse(
        model=GPT4O,
        messages=img_messages_grip_confirm,
        response_format= GripDetermination

    )
    is_gripping = json.loads(parse_response.choices[0].message.content)

    return is_gripping.get('is_gripping')




def robot_gripper_control(grip):
    if grip:
        current_joint_positions = robot.get_joint_positions()
        # Modify the last two elements of the current_joint_positions array
        current_joint_positions[-2:] = [0, 0]


        action = ArticulationAction(joint_positions=current_joint_positions)
        robot.apply_action(action)
    else:
        current_joint_positions = robot.get_joint_positions()
        # Modify the last two elements of the current_joint_positions array
        current_joint_positions[-2:] = [1, 1]

       

        action = ArticulationAction(joint_positions=current_joint_positions)
        robot.apply_action(action)

    return {"grip": grip}


def robot_end_effector_position():
    position, orientation = robot_handle.compute_end_effector_pose()
    return position, orientation
























viewport_api = get_active_viewport()
active_cam = viewport_api.get_active_camera()
resolution = viewport_api.get_texture_resolution()
render_product = rep.create.render_product(active_cam, resolution)





pointcloud_anno = rep.annotators.get("pointcloud")
pointcloud_anno.attach([render_product])


depth_data = pointcloud_anno.get_data()
print(depth_data.keys())
print(depth_data['data'])
print(depth_data['pointRgb'])
print("\n\ndepth instance\n ",depth_data['pointInstance'])
print("\n\ndepth info \n",depth_data['info'])


pointcloud = depth_data['data']
pointrgb = depth_data['pointRgb']
pointcloudinfo = depth_data['info']




combined_data = np.hstack((pointcloud, pointrgb))



output_file = "C:\\Users\\GHOSTFISH\\AppData\\Local\\ov\\pkg\\isaac-sim-4.2.0\\output.ply"
with open(output_file, 'w') as f:
    # Write the header
    f.write("ply\n")
    f.write("format ascii 1.0\n")
    f.write(f"element vertex {combined_data.shape[0]}\n")
    f.write("property float x\n")
    f.write("property float y\n")
    f.write("property float z\n")
    f.write("property uchar red\n")
    f.write("property uchar green\n")
    f.write("property uchar blue\n")
    f.write("end_header\n")
    
    # Write the points
    for point in combined_data:
        f.write(f"{' '.join(map(str, point[:3]))} {int(point[3])} {int(point[4])} {int(point[5])}\n")

print(f"Saved to {output_file}")






# Example usage
input_ply = output_file  # Replace with your input PLY file path
output_ply = output_file  # Replace with desired output file path
clip_ply_file(input_ply, output_ply)


# Load the point cloud
ply_file = output_file
pcd = o3d.io.read_point_cloud(ply_file)

# Get the points and colors
points = np.asarray(pcd.points)
colors = np.asarray(pcd.colors)  # Colors are usually normalized [0, 1]



# Define the color range
lower_bound_green = np.array([0.0, 0.0, 0.0])  # RGB lower bounds
upper_bound_green = np.array([.4, .8, .4])  # RGB upper bounds
# Find indices of points within the color range
mask_green = np.all((colors >= lower_bound_green) & (colors <= upper_bound_green), axis=1)
# Filter points and colors
filtered_points_green = points[mask_green]
filtered_colors_green = colors[mask_green]






final_filter_points = np.vstack(filtered_points_green)
final_filter_colors = np.vstack(filtered_colors_green)

combined_data = np.hstack((final_filter_points, final_filter_colors* 255))  # Combine points and colors



output_file = "C:\\Users\\GHOSTFISH\\AppData\\Local\\ov\\pkg\\isaac-sim-4.2.0\\modified_output.ply"
with open(output_file, 'w') as f:
    # Write the header
    f.write("ply\n")
    f.write("format ascii 1.0\n")
    f.write(f"element vertex {combined_data.shape[0]}\n")
    f.write("property float x\n")
    f.write("property float y\n")
    f.write("property float z\n")
    f.write("property uchar red\n")
    f.write("property uchar green\n")
    f.write("property uchar blue\n")
    f.write("end_header\n")
    
    # Write the points
    for point in combined_data:
        f.write(f"{' '.join(map(str, point[:3]))} {int(point[3])} {int(point[4])} {int(point[5])}\n")





print(f"Saved to {output_file}")






# Step 1: Load the .ply point cloud file
point_cloud = o3d.io.read_point_cloud(output_file)

# Step 2: Convert Open3D point cloud to a NumPy array
points = np.asarray(point_cloud.points)

# Step 3: Compute the centroid of the point cloud
centroid = np.mean(points, axis=0)

print(f"Centroid of the point cloud: {centroid}")
centroid[0] += 0.01

print(f"Centroid of the point cloud: {centroid}")




class Numberofsteps(BaseModel):
    steps: float = Field(description="number of steps in the given instruction")


class GripDetermination(BaseModel):
    # summary: str = Field(description="The summary of the function")
    is_gripping: bool = Field(description="is the object is positioned  completely inside the space of  two open fingers")




robot_arm = "C:\\Users\\GHOSTFISH\\AppData\\Local\\ov\\pkg\\isaac-sim-4.2.0\\robot_arm.png"



sim_context = SimulationContext()
articulation_root_path = "/panda"
stage = get_current_stage()
articulation_root_prim = get_prim_at_path(articulation_root_path)
robot = Articulation(articulation_root_path)
robot_handle =  KinematicsSolver(robot)
robot.initialize() # Initialize the articulation view (optional: in simulation loop)



















robot_IK_operator = {
    "type": "function",
    "function": {
        "name": "robot_operator_function",
        "description": "move the robot get the robot's end effector to a given position",
        "parameters": {
            "type": "object",
            "properties": {
                "num1": {
                    "type": "number",
                    "description": "The x coordinate of the robot end effector"
                },
                "num2": {
                    "type": "number",
                    "description": "The y coordinate of the robot end effector"
                },
                "num3": {
                    "type": "number",
                    "description": "The z coordinate of the robot end effector"
                }
            },
            "required": ["num1", "num2", "num3"]
        }
    }
}


robot_FK_operator = {
    "type": "function",
    "function": {
        "name": "robot_end_effector_position",
        "description": "get the robot end effector position",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
}

robot_gripper_controller = {
    "type": "function",
    "function": {
        "name": "robot_gripper_control",
        "description": "control the robot gripper to grip or release objects",
        "parameters": {
            "type": "object",
            "properties": {
                "grip": {
                    "type": "boolean",
                    "description": "true to close gripper (grip), false to open gripper (release)"
                }
            },
            "required": ["grip"]
        }
    }
}


system_instruction = """follow these instruction strictly without any extra modification to complete the task as robot operator.
A robot as shown in the picture which has root at [0 0 0]. At first , the robot has to reach parallal to the object in X-Y plane with a little bit offset of .1 redution of position in  X  plane away from target 
position of the target object to avoid collision and no change in the Z co ordinates, then move towards the target object and 
grip it. After that, the robot has to move  in the Z axis  to .5 unit and the move to the target position [.5 .5 .5] and release the 
object.



The robot can perform the following functions. provide a step by step list to the user's request based on the functions provided. each step should utilize one functions provided below.

1. "function name": "robot_operator_function",
"description of the function": "move the robot get the robot's end effector to a given position position",
2."function name": "robot_gripper_control",
"description of the function": "control the robot gripper to grip or release objects"


 """

img_messages=[
    {"role": "system", "content": system_instruction},
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": f"based on the image, i want the robot to pick up the target green objrct? the object in question located at {centroid}"
            }

        ]
    }
]





plan = grokker.chat.completions.create(
    model=GROK2,
    messages=img_messages

)



print("GROK 2 SAYING :: "+plan.choices[0].message.content)








plan_data = plan.choices[0].message.content


plan_system_steps_number = """You are a helpful robot control assistant.
    you have to count the steps provided to you by user and provide the number of steps as a response.

    """

plan_system_driscription = """You are a helpful robot control assistant.
    you have to driscribe about the specific the step of the overall plan provided to you.
    """



task_messages = [
    {"role": "system", "content": plan_system_steps_number},
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": plan_data
            }
        ]
    }
]

plan_steps = grokker.beta.chat.completions.parse(
    model=GROK2,
    messages=task_messages,
    response_format=Numberofsteps
)


parsed_data = json.loads(plan_steps.choices[0].message.content)




def execute_load(execution_step, window_name):
    stepsystem_instruction = f"given the user input, execute the {execution_step} th step of user's instruction"
    # carb.log_warn(stepsystem_instruction)
    execution_messages = [
        {"role": "system", "content": stepsystem_instruction},
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": plan_data
                }
            ]
        }
    ]

    execution_result = grokker.chat.completions.create(
        model=GROK2,
        messages=execution_messages,
        tools=[robot_IK_operator, robot_FK_operator, robot_gripper_controller],
        tool_choice="auto"
    )


    if execution_result.choices[0].message.tool_calls:
        for tool_call in execution_result.choices[0].message.tool_calls:
            if tool_call.function.name == "robot_end_effector_position":
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                result = robot_end_effector_position()
                carb.log_warn(result)

            if tool_call.function.name == "robot_operator_function":
                function_args = json.loads(tool_call.function.arguments)
                num1 = function_args["num1"]
                num2 = function_args["num2"]
                num3 = function_args["num3"]
                result = robot_operator_function(num1, num2, num3)
                carb.log_warn(result)

            if tool_call.function.name == "robot_gripper_control":
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                result = robot_gripper_control(function_args['grip'])

                carb.log_warn(result)

    # destroy_window(window_name)  #this line does not create a ny problem and works as expected but throws error in the log  







def on_submit(execution_step, window_name):
    execute_load(execution_step, window_name)
    


def create_submit_handler(step, window_name):
    return lambda: on_submit(step, window_name)





print(f'number of steps {parsed_data["steps"]}')










for i in range(1, parsed_data["steps"] + 1):
    window_name = f"window_{i}"
    locals()[window_name] = ui.Window(f" {i}st task", width=200, height=200)


    with locals()[window_name].frame:
        with ui.VStack():
            ui.Label(f"step: {i}")
            # ui.Label(f"objective: {task_list[i-1]}")
            input_field = ui.StringField()

                
            ui.Button("approve", clicked_fn=create_submit_handler(i,locals()[window_name]))






def destroy_window(window):
    carb.log_info("Destroying the window safely.")
    window.destroy()








































