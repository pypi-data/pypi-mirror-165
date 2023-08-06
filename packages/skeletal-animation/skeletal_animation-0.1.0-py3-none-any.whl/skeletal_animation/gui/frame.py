import gh_utils
import gh_camera
import gh_renderer
import gh_gpu_program
import gh_object
import gh_imgui

from inspect import getmembers, isfunction

from skeletal_animation.core.math import *
from skeletal_animation.gui.init import SERIALIZED_ANIMATION_PATH
from skeletal_animation.utils.loader import *
from skeletal_animation.algo.motionblending import *

elapsed_time = gh_utils.get_elapsed_time()
dt = elapsed_time - last_time
last_time = elapsed_time

if (elapsed_time - g_fps_last_time) > 1.0:
    g_fps_last_time = elapsed_time
    g_fps = g_frames
    g_frames = 0

g_frames = g_frames + 1

# Background
#
gh_renderer.set_depth_test_state(0)

gh_camera.bind(camera_ortho)

gh_renderer.clear_color_depth_buffers(0, 0, 0, 0, 1.0)

gh_gpu_program.bind(color_prog)

gh_mesh.set_vertex_color(fullscreen_quad, 0, bkg_color_bottom.r, bkg_color_bottom.g, bkg_color_bottom.b, bkg_color_bottom.a) # bottom-left
gh_mesh.set_vertex_color(fullscreen_quad, 1, bkg_color_top.r, bkg_color_top.g, bkg_color_top.b, bkg_color_top.a) # top-left
gh_mesh.set_vertex_color(fullscreen_quad, 2, bkg_color_top.r, bkg_color_top.g, bkg_color_top.b, bkg_color_top.a) # top-right
gh_mesh.set_vertex_color(fullscreen_quad, 3, bkg_color_bottom.r, bkg_color_bottom.g, bkg_color_bottom.b, bkg_color_bottom.a) # bottom-right

gh_object.render(fullscreen_quad)


# Main rendering
#
gh_renderer.set_depth_test_state(1)

# Apply 3D camera settings
#
if not imgui_window_hovered:
  gh_camera.set_fov(camera, camera_fov)
  gx_camera.set_keyboard_speed(keyboard_speed)
  gx_camera.update(camera, dt)

gh_utils.tripod_visualizer_camera_render(camera, 0, 0, 100, 100)
gh_camera.bind(camera)

# The lighting shader
#
prog = lighting_prog
gh_gpu_program.bind(prog)
gh_gpu_program.uniform1i(prog, "tex0", 0)

cx, cy, cz = gh_camera.get_position(camera)

light0_pos = {"x":-160.0, "y":80.0, "z":-160.0}
light1_pos = {"x":160.0, "y":160.0, "z":80.0}

gh_gpu_program.uniform4f(prog, "light_ambient", 0.2, 0.2, 0.2, 1.0)
gh_gpu_program.uniform4f(prog, "light_specular", 0.6, 0.6, 0.6, 1.0)

gh_gpu_program.uniform4f(prog, "light0_position", light0_pos["x"], light0_pos["y"], light0_pos["z"], 1.0)
gh_gpu_program.uniform4f(prog, "light0_diffuse", 1.0, 1.0, 1.0, 1.0)

gh_gpu_program.uniform4f(prog, "light1_position", light1_pos["x"], light1_pos["y"], light1_pos["z"], 1.0)
gh_gpu_program.uniform4f(prog, "light1_diffuse", 1.0, 1.0, 1.0, 1.0)

gh_gpu_program.uniform4f(prog, "uv_tiling", 1.0, 1.0, 0.0, 1.0)

gh_gpu_program.uniform4f(prog, "material_diffuse", 1.0, 1.0, 1.0, 1.0)
gh_gpu_program.uniform4f(prog, "material_ambient", 1.0, 1.0, 1.0, 1.0)
gh_gpu_program.uniform4f(prog, "material_specular", 0.1, 0.1, 0.1, 1.0)
gh_gpu_program.uniform1f(prog, "material_shininess", 24.0)

gh_renderer.solid()

gh_object.render(grid)

LEFT_BUTTON = 1
mouse_left_button = gh_input.mouse_get_button_state(LEFT_BUTTON)
RIGHT_BUTTON = 2
mouse_right_button = gh_input.mouse_get_button_state(RIGHT_BUTTON)
mouse_x, mouse_y = gh_input.mouse_get_position()
IMGUI_WIDGET_SEPARATOR = 1
IMGUI_WIDGET_SAME_LINE = 2
IMGUI_WIDGET_BULLET = 3
IMGUI_WIDGET_VERTICAL_SPACING = 4

##_______________________________ANIMATION__________________________________##
# TODO better way than using global?
def load_animator_1():
    global animation_render_dict, SERIALIZED_ANIMATION_PATH, animated_model, anim_1, file_not_found_message
    #gh_utils.trace("Loading animator 1")
    try:
        file_not_found_message = None
        animator = load_serialized(animated_models[anim_1], SERIALIZED_ANIMATION_PATH)
        joint_list = animator.skeleton.as_joint_list()
        animator.skeleton.compute_bind_pose()
        animation_render_dict['anim1'] = [JointWrapper(joint) for joint in joint_list]
        return animator

    except FileNotFoundError:
        file_not_found_message = "File not found: " + SERIALIZED_ANIMATION_PATH + animated_models[anim_1] + ".pkl. Element removed from list."
        animated_models.pop(anim_1)
        anim_1 = 0
        return None

def load_animator_2():    
    global animation_render_dict, SERIALIZED_ANIMATION_PATH, animated_models, anim_2, file_not_found_message
    #gh_utils.trace("Loading animator 2")
    try:
        file_not_found_message = None
        animator = load_serialized(animated_models[anim_2], SERIALIZED_ANIMATION_PATH)
        joint_list = animator.skeleton.as_joint_list()
        animator.skeleton.compute_bind_pose()
        animation_render_dict['anim2'] = [JointWrapper(joint) for joint in joint_list]
        return animator

    except FileNotFoundError:
        file_not_found_message = "File not found: " + SERIALIZED_ANIMATION_PATH + animated_models[anim_2] + ".pkl. Element removed from list."
        animated_models.pop(anim_2)
        anim_2 = 0
        return None

def load_blend_animator():
    #gh_utils.trace("Loading blend animator")
    global animation_render_dict, weight, blend_error_message
    ba = generate_blend_animator(animator_1, animator_2, Curve([Key(0.0, weight)]))
    if ba is None:
        blend_error_message = "Cannot generate blend animation: incompatible skeletons"
    else:
        blend_error_message = None

        animator_2.duration = animator_1.duration
        ba.duration = animator_1.duration
        animator_2.anim_time = animator_1.anim_time
        ba.anim_time = animator_1.anim_time   

        joint_list = ba.skeleton.as_joint_list()
        ba.skeleton.compute_bind_pose()    
        animation_render_dict['blend'] = [JointWrapper(joint, Color(90, 180, 90)) for joint in joint_list]

    return ba

def update_animation(dt, stepping=False):
    # start = time.time()
    if is_playing or stepping:

        if animator_1 is not None:        
            animator_1.kps = anim_speed * 30
            if render_anim_1:
                animator_1.step(dt)
            else:
                animator_1.update(dt)
        
        if animator_2 is not None:
            animator_2.kps = anim_speed * 30
            if render_anim_2:
                animator_2.step(dt)
            else:
                animator_2.update(dt)

        if blend_animator is not None:
            blend_animator.kps = anim_speed * 30
            if render_blend:
                blend_animator.step(dt)
            else:
                blend_animator.update(dt)
    # end = time.time()
    # gh_utils.trace("update_animation : " + str(end - start))

def render_animation():
    global animation_render_dict, render_anim_1, render_anim_2, render_blend
    if render_anim_1:
        for joint_wrapper in animation_render_dict['anim1']:
            joint_wrapper.apply_transform()
            gh_object.render(joint_wrapper.get_id())
    if render_anim_2:
        for joint_wrapper in animation_render_dict['anim2']:
            joint_wrapper.apply_transform()
            gh_object.render(joint_wrapper.get_id())
    if render_blend:
        for joint_wrapper in animation_render_dict['blend']:
            joint_wrapper.apply_transform()
            gh_object.render(joint_wrapper.get_id())

def any_active_animation():
    global animator_1, animator_2, blend_animator
    return animator_1 is not None or animator_2 is not None or blend_animator is not None

def play():
    global is_playing
    is_playing = True

def pause():
    global is_playing
    is_playing = False


##_________________________________GUI______________________________________##
##
gh_imgui.frame_begin(winW, winH, mouse_x, mouse_y,
                     mouse_left_button, mouse_right_button, dt)


# Flags for window style, window position and window size.
##
window_default = 0
window_no_resize = 2
window_no_move = 4
window_no_collapse = 32
window_show_border = 128
window_no_save_settings = 256
pos_size_flag_always = 1  # Always set the pos and/or size
# Set the pos and/or size once per runtime session (only the first call with succeed)
pos_size_flag_once = 2
# Set the pos and/or size if the window has no saved data (if doesn't exist in the .ini file)
pos_size_flag_first_use_ever = 4
# Set the pos and/or size if the window is appearing after being hidden/inactive (or the first time)
pos_size_flag_appearing = 8


# Beginning of the window with caption "Menu"

window_flags = 0  # default flag

IMGUI_WINDOW_BG_COLOR = 1
gh_imgui.set_color(IMGUI_WINDOW_BG_COLOR, 0.1, 0.1, 0.1, 0.8)

is_open = gh_imgui.window_begin("Menu", 300, 200, 50, 20, window_flags,
                                pos_size_flag_first_use_ever, pos_size_flag_first_use_ever)

# The following test is important because without it, if we move the window, we will move the camera too...
##
if gh_imgui.is_window_hovered() or gh_imgui.is_any_item_hovered():
    imgui_window_hovered = True
else:
    imgui_window_hovered = False

if is_open == 1:
    window_w = gh_imgui.get_content_region_available_width()
    widget_width = window_w * 1.0

    gh_imgui.text("Press [ESC] to quit the demo")

    raw_fps_str = "Framerate: {fps:.0f} FPS"
    fps_str = raw_fps_str.format(fps = g_fps)
    gh_imgui.text(fps_str)


    import_button = gh_imgui.button("Import...", 200, 20)

    if import_button:
        gh_imgui.file_browser_open()
        is_file_browser_open = True

    if is_file_browser_open:
        gh_imgui.file_browser_display(600, 400)

        if gh_imgui.file_browser_has_selected():
            filename = gh_imgui.file_browser_get_selected()
            temp_animator = load_fbx(filename)
            anim_name = filename.split("\\")[-1].split(".")[0]
            serialize(temp_animator, anim_name, SERIALIZED_ANIMATION_PATH)
            animated_models.append(anim_name)
            gh_imgui.file_browser_close()
            is_file_browser_open = False

    anim_1_selector = gh_imgui.combo_box_create("Animation 1")
    for animated_model in animated_models:
        gh_imgui.combo_box_add_item(anim_1_selector, animated_model)

    anim_1 = gh_imgui.combo_box_draw(
        anim_1_selector,
        anim_1
    )

    anim_2_selector = gh_imgui.combo_box_create("Animation 2")
    for animated_model in animated_models:
        gh_imgui.combo_box_add_item(anim_2_selector, animated_model)

    anim_2 = gh_imgui.combo_box_draw(
        anim_2_selector,
        anim_2
    )

    anim_speed = gh_imgui.slider_1f(
        "Animation speed",
        anim_speed,
        0.1, 10.0,
        2.0
    )

    if anim_1 != previous_anim_1:
        if anim_1 != 0:
            animator_1 = load_animator_1()
            if anim_2 != 0:
                blend_animator = load_blend_animator()
        else:
            animator_1 = None

    if anim_2 != previous_anim_2:
        if anim_2 != 0:
            animator_2 = load_animator_2()
            if anim_1 != 0:
                blend_animator = load_blend_animator()
        else:
            animator_2 = None

    gh_imgui.begin_disabled(
        not any_active_animation()
    )

    play_pause_label = "Pause" if is_playing else "Play"
    play_pause_button = gh_imgui.button(play_pause_label, 200, 20)

    if play_pause_button:
        is_playing = not is_playing

    gh_imgui.begin_disabled(
        is_playing
    )

    stepping_rate = 30 # frames per second

    step_back_button = gh_imgui.button("Step back", 200, 20)
    if step_back_button:
        update_animation(-dt * g_fps / stepping_rate, stepping = True)
        render_animation()

    step_forward_button = gh_imgui.button("Step forward", 200, 20)
    if step_forward_button:
        update_animation(dt * g_fps / stepping_rate, stepping = True)
        render_animation()

    gh_imgui.end_disabled()

    if blend_error_message is not None:
        gh_imgui.text_rgba("(!) " + str(blend_error_message), 1.0, 0.0, 0.0, 1.0)
    if file_not_found_message is not None:
        gh_imgui.text_rgba("(!) " + str(file_not_found_message), 1.0, 0.0, 0.0, 1.0)

    gh_imgui.begin_disabled(anim_1 == 0 or anim_2 == 0)

    render_anim_1 = gh_imgui.checkbox("Anim 1", render_anim_1)
    render_anim_2 = gh_imgui.checkbox("Anim 2", render_anim_2)

    gh_imgui.begin_disabled(blend_error_message != None)

    render_blend = gh_imgui.checkbox("Blend", render_blend)

    weight = gh_imgui.slider_1f(
        "blending weight",
        weight,
        0.0, 1.0,
        1.0
    )

    gh_imgui.end_disabled()

    gh_imgui.end_disabled()

    gh_imgui.end_disabled()

if anim_1 != 0 and anim_2 == 0:
    render_anim_1 = True
    render_anim_2 = False
    render_blend = False
elif anim_1 == 0 and anim_2 != 0:
    render_anim_2 = True
    render_anim_1 = False
    render_blend = False
elif anim_1 != 0 and anim_2 != 0:
    if len(set(previous_weights)) > 1:
        blend_animator = load_blend_animator()
        blend_animator.step(0)
        previous_weights = [weight]

if is_playing:
    update_animation(dt)

render_animation()

# End of the window.
##
gh_imgui.window_end()

gh_imgui.frame_end()

previous_anim_1 = anim_1
previous_anim_2 = anim_2

previous_weights.append(weight)
if len(previous_weights) > 10:
    previous_weights.pop(0)

##_______________________________LIVE_CODING_______________________________##
# The live coding section must be empty when the program is loaded
# For things that will be executed every frame, just write them here.
# For things that will be executed only once, wrap them in a function.












































##_____________________________END_LIVE_CODING_____________________________##

if not function_list_loaded:
    previous_function_list = getmembers(sys.modules[__name__], isfunction)
    function_list_loaded = True

function_list = getmembers(sys.modules[__name__], isfunction)

function_buffer = [function for function in function_list if function[0] not in \
    [previous_function[0] for previous_function in previous_function_list]]

previous_function_list = function_list

for function in function_buffer:
    gh_utils.trace("Calling function: " + str(function))
    function[1]()
    del function


