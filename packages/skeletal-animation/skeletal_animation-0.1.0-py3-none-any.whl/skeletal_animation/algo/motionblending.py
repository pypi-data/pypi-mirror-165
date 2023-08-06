import warnings
import copy 

from skeletal_animation.core.math import *
from skeletal_animation.core.model import *
from skeletal_animation.core.animate import *
from skeletal_animation.utils.other import are_skeletons_similar


def generate_blend_animator(first_animator, second_animator, blend_curve=Curve()):
    """Generates a new animator that is the blend of the two given animators according to a blend curve.

    The blend curve allows the weight to vary over time to allow for transitions between animations.
    The blend curve is a Curve object with keys that give the weight of the blend 
    at a given time. Weight values between keys are linearly interpolated.

    A weight of 0.0 means the resulting animator is the first animator.
    A weight of 1.0 means the resulting animator is the second animator.
    Any weight in between means the resulting animator is a blend of the two animators.
    The lower the weight, the closer the resulting animation is to the first animator's animation. 

    If the blend curve has no keys, the resulting animator is a constant  blend of the two animators
    with a weight of 0.5.

    Parameters:
    -----------
    first_animator : Animator
        The first animator to blend.
    second_animator : Animator
        The second animator to blend.
    blend_curve : Curve, optional
        Curve that describes the weight value of the blend over the course of the animation. 
        By default, a constant curve with weight 0.5.
    
    Returns:
    --------
    Animator
        The animator that is the blend of the two given animators. None if the two animators are not compatible.

    Warns:
    ------
    UserWarning
        If the two animators are not compatible.
    UserWarning
        If the blend curve is empty.
    """
    if not are_skeletons_similar(first_animator.skeleton, second_animator.skeleton):
        warnings.warn("Cannot generate blend between the two given animators. Skeletons are not identical. Returning None.")
        return None
    
    first_animation = copy.deepcopy(first_animator.animation)
    second_animation = copy.deepcopy(second_animator.animation)

    if blend_curve.is_empty():
        warnings.warn("Blend curve is empty. Using default curve with a constant weight of 0.5.", stacklevel=2)
        blend_curve.set_key_at(0, 0.5)

    new_joint_animations = []

    for ja_id in range(len(first_animation.joint_animations)):
        first_joint_animation = first_animation.joint_animations[ja_id]
        second_joint_animation = second_animation.joint_animations[ja_id]
        new_joint_animation = JointAnimation(joint=first_joint_animation.joint
            , translation_curve=Curve()
            , rotation_curve=Curve()
            , timewarp_curve=Curve())
            
        # Translation curve
        frame_times = [key.time for key in first_joint_animation.translation_curve.keys]
        for frame_time in frame_times:
            blend_factor = blend_curve.get_lerp_value(frame_time)

            first_translation_value = first_joint_animation.translation_curve.get_key_at(frame_time).value
            second_translation_value = second_joint_animation.translation_curve.get_lerp_value(frame_time)
            if first_translation_value is None:
                if second_translation_value is None:
                    new_translation_key_value = None
                else:
                    new_translation_key_value = second_translation_value
            else:
                if second_translation_value is None:
                    new_translation_key_value = first_translation_value
                else:
                    new_translation_key_value = Curve.lerp(first_translation_value,
                                                        second_translation_value,
                                                        blend_factor)

            if new_translation_key_value is not None:
                new_joint_animation.translation_curve.set_key_at(frame_time, new_translation_key_value)

        # Rotation curve
        frame_times = [key.time for key in first_joint_animation.rotation_curve.keys]
        for frame_time in frame_times:
            blend_factor = blend_curve.get_lerp_value(frame_time)

            first_rotation_value = first_joint_animation.rotation_curve.get_key_at(frame_time).value
            second_rotation_value = second_joint_animation.rotation_curve.get_lerp_value(frame_time)
            if first_rotation_value is None:
                if second_rotation_value is None:
                    new_rotation_key_value = None
                else:
                    new_rotation_key_value = second_rotation_value
            else:
                if second_rotation_value is None:
                    new_rotation_key_value = first_rotation_value
                else:
                    new_rotation_key_value = Curve.lerp(first_rotation_value,
                                                        second_rotation_value,
                                                        blend_factor)

            if new_rotation_key_value is not None:
                new_joint_animation.rotation_curve.set_key_at(frame_time, new_rotation_key_value)
            
        # Timewarp curve
        frame_times = [key.time for key in first_joint_animation.timewarp_curve.keys]
        for frame_time in frame_times:
            blend_factor = blend_curve.get_lerp_value(frame_time)

            first_timewarp_value = first_joint_animation.timewarp_curve.get_key_at(frame_time).value
            second_timewarp_value = second_joint_animation.timewarp_curve.get_lerp_value(frame_time)
            if first_timewarp_value is None:
                if second_timewarp_value is None:
                    new_timewarp_key_value = None
                else:
                    new_timewarp_key_value = second_timewarp_value
            else:
                if second_timewarp_value is None:
                    new_timewarp_key_value = first_timewarp_value
                else:
                    new_timewarp_key_value = Curve.lerp(first_timewarp_value,
                                                        second_timewarp_value,
                                                        blend_factor)

            if new_timewarp_key_value is not None:
                new_joint_animation.timewarp_curve.set_key_at(frame_time, new_timewarp_key_value)

        new_joint_animations.append(new_joint_animation)

    new_animation = Animation(joint_animations=new_joint_animations, max_key_time=first_animation.max_key_time)
    new_skeleton = copy.deepcopy(first_animator.skeleton)

    new_animator = Animator(
        new_animation,
        new_skeleton,
        first_animator.kps,
        first_animator.interpolation_algo)

    return new_animator
    

