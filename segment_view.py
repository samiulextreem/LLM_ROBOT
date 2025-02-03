import omni.replicator.core as rep
from omni.kit.viewport.utility import get_active_viewport
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import omni
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


omni.kit.pipapi.install(
    package="open3d",
    version="0.18.0",
    module="open3d", # sometimes module is different from package name, module is used for import check
    ignore_import_check=False,
    ignore_cache=False,
    use_online_index=True,
    surpress_output=False,
    extra_args=[]
)

import open3d as o3d

viewport_api = get_active_viewport()
active_cam = viewport_api.get_active_camera()
resolution = viewport_api.get_texture_resolution()

rp = rep.create.render_product(active_cam, resolution)

ldr = rep.AnnotatorRegistry.get_annotator("instance_segmentation")
ldr.attach([rp])

output = ldr.get_data()


print("output data",output['data'])
print("output info",output['info']) 


def segmented_view(output):
    segmentation_data = np.array(output['data'])

    info = output['info']

    label_colors = {
        0: [0, 0, 0],         # BACKGROUND -> black
        1: [0.5, 0.5, 0.5],   # UNLABELLED -> gray
        2: [0, 1, 0],         # /World/Cube_2 -> green
        3: [1, 0, 0],         # Example label -> red
        5: [1, 1, 1],         # New label -> white
    }
    # Convert segmentation data to an RGB image

    # Create a color image based on the data
    height, width = segmentation_data.shape
    segmented_image = np.zeros((height, width, 3))  # RGB image

    for label, color in label_colors.items():
        segmented_image[segmentation_data == label] = color


    segmentation_image = Image.fromarray((segmented_image * 255).astype(np.uint8))
    return segmentation_image




segmentation_image = segmented_view(output)
segmentation_image.show()

