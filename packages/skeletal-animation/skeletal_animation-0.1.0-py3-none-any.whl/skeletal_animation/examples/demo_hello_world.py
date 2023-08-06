import numpy as np

from skeletal_animation.core.math import Transform
from skeletal_animation.core.model import Joint, Skeleton
from skeletal_animation.core.animate import *
from skeletal_animation.utils.loader import serialize

# CREATING A SKELETON
# ------------------
# Create a root joint with name "root" and default parameters
root = Joint(name="root")

# Create a skeleton with the root joint as root
skeleton = Skeleton(root)

# Create a joint with name "back" and default parameters
back = Joint(name="back")
root.add_child(back) # Add the joint as a child of the root joint

# We only need set position of the back joint, not its orientation
back.local_bind_transform.pos = [0,50,0]

# CREATING MOTION
# ---------------
# Create a translation curve for the root joint
root_translation_curve = Curve()

# Create a key at time 0 with a position of (0,0,0)
key0 = Key(time=0., value=[0.,0.,0.]) # all values must be given as floats
# Create a key at time 1 with a position of (0,0,100)
key1 = Key(time=1., value=[0.,0.,100.])
# Add the keys to the translation curve
root_translation_curve.add_key(key0)
root_translation_curve.add_key(key1)

# Create a joint animation for the root joint and give it our translation curve
root_joint_animation = JointAnimation(root, translation_curve=root_translation_curve)

# Create an animation and give it our joint animation
animation = Animation(joint_animations=[root_joint_animation])

# Create an animator object and give it our animation and skeleton
animator = Animator(animation, skeleton, kps=1.)

# NEXT STEPS
# ----------
# The head joint is located 15 units above its parent
head = Joint(name="head", local_bind_transform=Transform(pos=[0.,15.,0.]))
# The right arm joint is located 30 units to the right of its parent
right_arm = Joint("right_arm", Transform(pos=[-30.,0.,0.]))
# The left arm joint is located 30 units to the left of its parent
left_arm = Joint("left_arm", Transform(pos=[30.,0.,0.]))
# The right forearm joint is located 20 units to the right of its parent
left_forearm = Joint("left_forearm", Transform(pos=[-20.,0.,0.]))
# The left forearm joint is located 20 units to the left of its parent
right_forearm = Joint("right_forearm", Transform(pos=[20.,0.,0.]))

# Add the head joint as a child of the back joint
back.add_child(head)
# Add the right arm joint as a child of the back joint
back.add_child(right_arm)
# Add the left arm joint as a child of the back joint
back.add_child(left_arm)
# Add the right forearm joint as a child of the right arm joint
right_arm.add_child(left_forearm)
# Add the left forearm joint as a child of the left arm joint
left_arm.add_child(right_forearm)

# Create a key at time 1 with no rotation
key0 = Key(1., np.quaternion(1, 0, 0, 0))
# Create a key at time 3 with a rotation of ~53 degrees around the z axis
key1 = Key(3., np.quaternion(0.5, 0, 0, -1).normalized())
# Do not forget to normalize the quaternions when necessary
# Create a key at time 4 with a rotation of ~127 degrees around the z axis
key2 = Key(4., np.quaternion(2, 0, 0, -1).normalized())
# Create a key at time 5 with a rotation of ~53 degrees around the z axis
key3 = Key(5., np.quaternion(0.5, 0, 0, -1).normalized())
# Create a key at time 7 with no rotation
key4 = Key(7., np.quaternion(1, 0, 0, 0))

# Create a rotation curve for the right arm joint
right_arm_rotation_curve = Curve(keys=[key0, key1, key2, key3, key4])

# First we get the maximum time of the curve
max_time = right_arm_rotation_curve.get_max_key_time()
# Then we normalize the curve by this maximum time
right_arm_rotation_curve.normalize_times(max_time)
# This effectively divides all the key times by the maximum time

# Create a joint animation for the right arm joint
right_arm_animation = JointAnimation(
    joint=right_arm,
    rotation_curve=right_arm_rotation_curve
    )
# Add the joint animation to the animation
animation.joint_animations.append(right_arm_animation)

# Remove the key at time 1 of the root's translation curve
root_joint_animation.translation_curve.remove_key_at(1.)

# Replace default path with the path where you want to save the serialized animation
serialize(
    animator,
    "demo_hello_world",
    "D:/He-Arc/TB/tb-animation-squelettale/skeletal_animation/animated_models/serialized/"
    )

