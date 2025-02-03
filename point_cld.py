import matplotlib.pyplot as plt
from omni.syntheticdata import visualize
from omni.kit.viewport.utility import get_active_viewport
import omni.replicator.core as rep
from omni.isaac.core import World
from omni.isaac.core.utils.prims import create_prim
from omni.isaac.core.utils.viewports import set_camera_view
from omni.isaac.nucleus import get_assets_root_path
from omni.isaac.core.materials.omni_glass import OmniGlass
from omni.isaac.core.prims.xform_prim import XFormPrim
from omni.isaac.core.utils.extensions import get_extension_path_from_name
from omni.isaac.core.utils.semantics import add_update_semantics

import omni
import carb
import numpy as np
from PIL import Image
import base64
import json





import open3d as o3d


print("Open3D version:", o3d.__version__)





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



output_file = "C:\\Users\\GHOSTFISH\\Downloads\\pointcld\\output.ply"
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




