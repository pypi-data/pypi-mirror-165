import numpy as np
import quaternion

from skeletal_animation.core.math import *
from skeletal_animation.core.model import *
from skeletal_animation.core.animate import *
from skeletal_animation.utils.loader import *
from skeletal_animation.algo.motionblending import *

"""
This program demonstrates the creation of a new skeletal animation
based on existing ones.

The starting animations are a walk and a death animation.
The goal is to create a new animation of a character walking and
then suddenly dying. The resulting animation through the uss of
blending, cropping, merging and translating existing animations.
"""

# Set up variables with the path to where our animations are stored
DATA_DIR = "D:/He-Arc/TB/tb-animation-squelettale/skeletal_animation/animated_models/"
# Folder for FBX files
FBX_DATA_DIR = DATA_DIR + "fbx/"
# Folder for serialized .pkl files
SERIALIZED_DATA_DIR = DATA_DIR + "serialized/"

# Load the walk animation from a FBX file
walk_animator = load_fbx(FBX_DATA_DIR + "walk.fbx")
# Load the death animation from a FBX file
death_animator = load_fbx(FBX_DATA_DIR + "death.fbx")

# We crop the walk animation into 2 halfs, one to be played at the beginning
# of the new animation and the other to be blended with the death animation
walk_start = walk_animator.crop(0.0, 0.5)
walk_end_for_blend = walk_animator.crop(0.5, 1.0)

# Similarly, we crop the death animation into 2 parts. The first part is
# blended with the walk animation and the second part is played at the end of
# the new animation
death_start_for_blend = death_animator.crop(0.0, 0.2)
death_end = death_animator.crop(0.2, 1.0)

# We define a blend curve for the blending between the walk and death animation
# The curve starts slowly and speeds up over time
blend_curve = Curve([Key(0.0, 0.0), Key(0.4, 0.5), Key(0.7, 0.9), Key(1.0, 1.0)])

# Before we blend the animations, we need to align them. We do this by translating the death
# animation to be aligned with the end of the first half of the walk animation.
# Here is how we do it:

# We get the position of the root bone at the end of the first half of the walk animation
walk_last_root_position = walk_start.animation.joint_animations[0].translation_curve.keys[-1].value
print(walk_last_root_position) # [4.16174078  102.57474518  96.60121155]

# We get the position of the root bone at the beginning of the death animation
death_first_root_position = death_start_for_blend.animation.joint_animations[0].translation_curve.keys[0].value
print(death_first_root_position) # [-0.40051448  101.26885986   1.7320683]

# We compute the translation vector that we need to apply to the death animation
translation_vector = walk_last_root_position - death_first_root_position
print(translation_vector) # [ 4.56225526  1.30588532 94.86914325]

# We translate both parts of the death animation
death_start_for_blend.translate(
    translation_vector[0],
    translation_vector[1],
    translation_vector[2]
    )

death_end.translate(
    translation_vector[0],
    translation_vector[1],
    translation_vector[2]
    )

# We are now ready to blend the walk and death animations
blend_animator = generate_blend_animator(walk_end_for_blend, death_start_for_blend, blend_curve)

# We finish by merging the 3 animations into a single one
# Walk start -> Walk end blended with death start -> Death end
clipped_animator = walk_start.clip(blend_animator).clip(death_end)

# We save the resulting animation to a file
serialize(clipped_animator, "walk_then_suddenly_die", SERIALIZED_DATA_DIR)

# It is now ready to be used in the GUI
# Result is shown in the video Features_deno.mp4