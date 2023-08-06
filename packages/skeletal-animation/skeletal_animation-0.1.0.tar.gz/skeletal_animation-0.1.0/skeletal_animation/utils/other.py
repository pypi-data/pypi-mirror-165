import numpy as np

from skeletal_animation.core.math.constants import VERY_HIGH_R_TOL


def are_skeletons_similar(first_skeleton, second_skeleton):
    """Checks if the skeletons are similar.

    Similarity is defined as:
    - The skeletons have the same number of joints.
    - The local bind transforms of the joints are within a tolerance of each other.
      The tolerance used in this case does not need to be tight. Since if the joints
      of the first skeleton start at similar positions to those of the second skeleton,
      the animation will look correct.
      Tolerance values are defined in skeletal_animation/core/math/constants.py. file
      Very high tolerance values are used here.

    Parameters
    ----------
    first_skeleton : Skeleton
        First skeleton.
    second_skeleton : Skeleton
        Skeleton to compare to the first.
    
    Returns
    -------
    bool
        True if the skeletons are similar, False otherwise.

    Warnings
    --------
    This function may return false positives.
    For two skeletons to be similar, the joint hierarchy of both must be the same.
    However, this check is not implemented yet.    
    """
    first_joint_list = first_skeleton.as_joint_list()
    second_joint_list = second_skeleton.as_joint_list()

    if len(first_joint_list) != len(second_joint_list):
        return False
    for i in range(len(first_joint_list)):
        if not np.allclose(
            first_joint_list[i].local_bind_transform.as_matrix(),
            second_joint_list[i].local_bind_transform.as_matrix(),
            rtol=VERY_HIGH_R_TOL
        ):
            return False
    return True