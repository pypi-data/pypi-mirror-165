
SERIALIZED_ANIMATION_PATH = "D:/He-Arc/TB/tb-animation-squelettale/skeletal_animation/animated_models/serialized/"
FBX_ANIMATION_PATH = "D:/He-Arc/TB/tb-animation-squelettale/skeletal_animation/animated_models/fbx/"


import gh_utils
import gh_window
import gh_camera
import gh_node
import gh_renderer
import gh_object
import gh_imgui
import gh_mesh

import sys
import os
import numpy as np
import quaternion

from skeletal_animation.core.math import *
from skeletal_animation.core.model import *
from skeletal_animation.core.animate import *
from skeletal_animation.utils.loader import *

demo_dir = gh_utils.get_demo_dir() 		
sys.path.append(demo_dir)

lib_dir = gh_utils.get_lib_dir() 		
sys.path.append(lib_dir + "/python/")

class Color():
    """Class representing a color.

    Attributes:
        r : int
            Red component. Must be between 0 and 255. By default 255.
        g : int
            Green component. Must be between 0 and 255. By default 255.
        b : int
            Blue component. Must be between 0 and 255. By default 255.
        a : float
            Alpha component. Must be between 0 and 1. By default 1.
    """
    def __init__(self, r=255, g=255, b=255, a=1.0):
        self.r = r/255
        self.g = g/255
        self.b = b/255
        self.a = a

##______________________CAMERA______________________##
from gxcamera_v1 import *

gx_camera = gxcamera()

winW, winH = gh_window.getsize(0)

# A fly mode camera managed by the Python gx_camera library.
#
keyboard_speed = 100.0
camera_fov = 60.0
camera_lookat_x = 0
camera_lookat_y = 100
camera_lookat_z = 20
camera_znear = 3
camera_zfar = 3000.0

camera = gx_camera.create_perspective(camera_fov, 1, 0, 0, winW, winH, camera_znear, camera_zfar)

gh_camera.set_position(camera, -150, 200, 250)
gx_camera.set_orbit_lookat(camera, camera_lookat_x,
                           camera_lookat_y, camera_lookat_z)
gx_camera.set_mode_fly()
gx_camera.set_keyboard_speed(keyboard_speed)

camera_ortho = gh_camera.create_ortho(-winW/2, winW/2, -winH/2, winH/2, 1.0, 10.0)
gh_camera.set_viewport(camera_ortho, 0, 0, winW, winH)
gh_camera.set_position(camera_ortho, 0, 0, 4)

# The fullscreen quad for the background
#
fullscreen_quad = gh_mesh.create_quad(winW, winH)

bkg_color_top = Color(125, 152, 196, 1.0)
bkg_color_bottom = Color(35, 35, 30, 1.0)

gh_mesh.set_vertex_color(fullscreen_quad, 0, bkg_color_bottom.r, bkg_color_bottom.g, bkg_color_bottom.b, bkg_color_bottom.a) #bottom-left
gh_mesh.set_vertex_color(fullscreen_quad, 1, bkg_color_top.r, bkg_color_top.g, bkg_color_top.b, bkg_color_top.a) #top-left
gh_mesh.set_vertex_color(fullscreen_quad, 2, bkg_color_top.r, bkg_color_top.g, bkg_color_top.b, bkg_color_top.a) #top-right
gh_mesh.set_vertex_color(fullscreen_quad, 3, bkg_color_bottom.r, bkg_color_bottom.g, bkg_color_bottom.b, bkg_color_bottom.a) #bottom-right

# The GLGL shaders
#
lighting_prog = gh_node.getid("lighting_prog")
color_prog = gh_node.getid("color_prog")

class JointWrapper():
    """Wrapper class encapsulating a Joint object from the skeletal-animation module 
    and a renderable GeexLab object representing the joint.

    Attributes
    ----------
    color : Color
        The color in which to render the joint.
    joint : Joint
        The joint to render.    
    """

    RADIUS = 1 # radius of the joint sphere
    NB_SUBDIVISIONS = 8 # number of subdivisions along the X and Y axis for the sphere mesh
    DEFAULT_COLOR =  Color(165, 170, 175, 1.0) 

    def __init__(self, joint, color=DEFAULT_COLOR, show_bones=True):
        """Constructor for the JointWrapper class.

        Parameters
        ----------
        color : Color
            The color in which to render the joint.
        joint : Joint
            The joint to render.    
        """
        self.joint = joint
        if show_bones:
            bones = self.create_joint_bones(self.joint, 2*self.RADIUS)
        sphere = self.create_sphere_mesh(self.RADIUS, self.NB_SUBDIVISIONS, self.NB_SUBDIVISIONS)
        self.id = gh_object.create()
        if show_bones:
            gh_node.add_child(self.id, bones)
        gh_node.add_child(self.id, sphere)
        gh_object.set_vertices_color(self.id, color.r, color.g, color.b, color.a)
    
    def get_id(self):
        """Returns the id of the GeexLab object representing the joint.

        Returns
        -------
        int
            id of the GeexLab object representing the joint.
        """
        return self.id
    
    def get(self):
        """Returns the joint object wrapped by the wrapper.

        Returns
        -------
        Joint
            the joint object wrapped by the wrapper.
        """
        return self.joint
    
    def apply_transform(self):
        """Applies the current transform of the joint to the GeexLab object for rendering.

        Raises
        ------
        ValueError
            If the joint's model_transform is None.
        """
        if self.joint.model_transform is None:
            raise ValueError("In apply_transform(), joint transform is None. Make sure to compute the bind pose before playing the animation: skeleton.compute_bind_pose()")
        transform_matrix = self.joint.model_transform.as_matrix()
        transform_values = [value for transform_row in transform_matrix for value in transform_row]
        tv = transform_values
        gh_object.set_transform(self.id,
            tv[0], tv[4], tv[8], tv[12],
            tv[1], tv[5], tv[9], tv[13],
            tv[2], tv[6], tv[10], tv[14],
            tv[3], tv[7], tv[11], tv[15])

    def compute_shape_length_and_orientation(self, joint):
        """Compute the length and orientation of the shape representing a bone.

        Args:
            joint: The joint to compute the length and orientation of.
        
        Returns:
            A tuple containing the length and orientation of the cylinder ((float) length, (np.quaternion) orientation).
        """
        if joint is None:
            return (0.0, quaternion.one)
        else:
            if joint.parent is None:
                return (0.0, quaternion.one)
            else:
                v0 = joint.local_bind_transform.pos 
                v1 = np.array([0, 1, 0]) # unit y-axis vector
                v = np.cross(v0, v1)
                w = np.sqrt((np.linalg.norm(v0)**2) * (np.linalg.norm(v1)**2)) + np.dot(v0, v1)
                q = np.quaternion(w, -v[0], v[1], -v[2])
                return (np.linalg.norm(v0), q.normalized())

    def create_joint_bones(self, joint, radius):
        """Creates GeeXLab object containing the meshes of every bone attached to the given joint.

        Parameters:
        -----------
        joint : Joint
            The joint to create the bones for.
        radius : float
            The maximum "radius" of the bones.


        """

        meshes = [self.create_bone_mesh(child, radius) for child in joint.children]

        shape = gh_object.create()  

        for mesh in meshes:
            gh_node.add_child(shape, mesh)  

        return shape

    def create_bone_mesh(self, joint, radius):
        """Creates a mesh describing the shape of a bone.

        Parameters
        ----------
        joint : Joint
            The joint for which to create a bone mesh.
        radius : float
            The maximum "radius" of the bone.

        Returns
        -------
        int
            newly created mesh id
        """
        h, orient = self.compute_shape_length_and_orientation(joint)

        width = min(radius, h/4)

        mesh = gh_mesh.create_v2()
        gh_mesh.alloc_mesh_data(mesh, 6, 8)
        gh_mesh.set_vertex_position(mesh, 0, 0, 0, 0, 1)
        gh_mesh.set_vertex_position(mesh, 1, -width, min(radius * np.sqrt(2), h/2), -width, 1)
        gh_mesh.set_vertex_position(mesh, 2, width, min(radius * np.sqrt(2), h/2), -width, 1)
        gh_mesh.set_vertex_position(mesh, 3, width, min(radius * np.sqrt(2), h/2), width, 1)
        gh_mesh.set_vertex_position(mesh, 4, -width, min(radius * np.sqrt(2), h/2), width, 1)
        gh_mesh.set_vertex_position(mesh, 5, 0, h, 0, 1)

        gh_mesh.set_face_vertex_indices(mesh, 0, 0, 1, 2)
        gh_mesh.set_face_vertex_indices(mesh, 1, 0, 2, 3)
        gh_mesh.set_face_vertex_indices(mesh, 2, 0, 3, 4)
        gh_mesh.set_face_vertex_indices(mesh, 3, 0, 4, 1)
        gh_mesh.set_face_vertex_indices(mesh, 4, 5, 1, 2)
        gh_mesh.set_face_vertex_indices(mesh, 5, 5, 2, 3)
        gh_mesh.set_face_vertex_indices(mesh, 6, 5, 3, 4)
        gh_mesh.set_face_vertex_indices(mesh, 7, 5, 4, 1)

        gh_mesh.set_vertex_normal(mesh, 0, 0, -1, 0)
        gh_mesh.set_vertex_normal(mesh, 1, -1, 0, -1)
        gh_mesh.set_vertex_normal(mesh, 2, 1, 0, -1)
        gh_mesh.set_vertex_normal(mesh, 3, 1, 0, 1)
        gh_mesh.set_vertex_normal(mesh, 4, -1, 0, 1)
        gh_mesh.set_vertex_normal(mesh, 5, 0, 1, 0)

        gh_object.set_orientation(mesh, orient.x, orient.y, orient.z, orient.w)

        return mesh

    def create_sphere_mesh(self, radius, stacks, slices):
        """Creates sphere mesh describing the shape of a joint.

        Parameters
        ----------
        radius : float
            The radius of the sphere.
        stacks : int
            The number of subdivisions along the X axis.
        slices : int
            The number of subdivisions along the Y axis.

        Returns
        -------
        int
            newly created mesh id
        """    
        mesh = gh_mesh.create_sphere(radius, stacks, slices)
        sphere = gh_object.create()
        gh_node.add_child(sphere, mesh) 
        return sphere

# A reference grid.
#
grid = gh_utils.grid_create()
gh_utils.grid_set_geometry_params(grid, 1000, 1000, 40, 40)
gh_utils.grid_set_lines_color(grid, 0.7, 0.7, 0.7, 1.0)
gh_utils.grid_set_main_lines_color(grid, 1.0, 1.0, 0.0, 1.0)
gh_utils.grid_set_main_x_axis_color(grid, 1.0, 0.0, 0.0, 1.0)
gh_utils.grid_set_main_z_axis_color(grid, 0.0, 0.0, 1.0, 1.0)
display_main_lines = 1
display_lines = 1
gh_utils.grid_set_display_lines_options(grid, display_main_lines, display_lines)

color_prog = gh_node.getid("color_prog")
# Some render states and global variables
#
gh_renderer.set_vsync(0)

last_time = gh_utils.get_elapsed_time()

# ImGui initialization. We will use ImGui functions in the FRAME script to control
# various parameters of the demo.
#
gh_imgui.init()

# This variable will help us to manage to mouse in the FRAME script+.
#
imgui_window_hovered = False

g_fps_last_time = gh_utils.get_elapsed_time()
g_fps_dt = 0
g_fps = 0
g_frames = 0

# GUI Initialization.
animator_1 = None
animator_2 = None
blend_animator = None

animation_render_dict = {}

previous_anim_1 = 0
anim_1 = 0
previous_anim_2 = 0
anim_2 = 0

animated_models = ["None"]

for file in os.listdir(SERIALIZED_ANIMATION_PATH):
    if file.endswith(".pkl"):
        animated_models.append(file.split(".pkl")[0])

is_file_browser_open = False
file_browser_flags = 0
filename = "None"

gh_imgui.file_browser_init(
    file_browser_flags
)

gh_imgui.file_browser_set_title("Import external .fbx file")
gh_imgui.file_browser_set_current_directory(FBX_ANIMATION_PATH)
gh_imgui.file_browser_clear_type_filters()
gh_imgui.file_browser_add_type_filter(".fbx")

anim_speed = 1

is_playing = True

anim_time = 0

previous_function_list = []
function_list_loaded = False

render_anim_1 = False
render_anim_2 = False
render_blend = False

blend_error_message = None
file_not_found_message = None

previous_weights = []
weight = 0.5

loaded_blends = {}

weight_slider_focused = False