from skeletal_animation.utils.loader import *

# Load the fbx file
# Replace default path with the path of the fbx file
walk_animator = load_fbx(
    "D:/He-Arc/TB/tb-animation-squelettale/skeletal_animation/animated_models/fbx/walk.fbx"
    )

# Replace default path with the path where you want to save the serialized animation
serialize(
    animator,
    "demo_hello_world",
    "D:/He-Arc/TB/tb-animation-squelettale/skeletal_animation/animated_models/serialized/"
    )