import numpy as np
import quaternion

from skeletal_animation.core.animate import Curve
from skeletal_animation.core.math import Transform

class JointAnimation:
    """Class to store a joint's animation curves.

    It contains the animation curves for the position and orientation of the joint.
    As well as the time warp curve.

    The time warp curve is a curve that can be used to control the speed of the animation
    as a function of time.
    It contains keys with a single float as value called timekeys.
    - The time of the timekey is the real time of the animation.
    - The value of the timekey is the time at which the translation and rotation curves are evaluated.

    let :math:`R(t)` the result of evaluating the rotation curve at time :math:`t` and
    :math:`f(t)` the result of evaluating the time warp curve at time :math:`t`.

    Then the effective rotation of the joint at time :math:`t` is:
    :math:`R(f(t))`
    in other words, the rotation of the joint at time :math:`t` is the result of evaluating the rotation curve at :math:`f(t)` 
    This works similarly for translations.

    The logic for time warping is applied in the get_local_transform method.

    Examples
    -------
    # A translation curve that goes from [0,0,0] to [1,1,1] at time 0 and 1 respectively.
    >>> translation_curve = Curve(
    >>>     [Key(time=0., value=[0,0,0]),
    >>>     Key(time=1., value=[1,1,1])]
    >>> )

    # A default time warp curve. The value of the key at time 0 is 0 and the value of the key at time 1 is 1.
    >>> timewarp_curve = Curve(
    >>>    [Key(time=0., value=0.),
    >>>    Key(time=1., value=1.)]
    >>> )
        
    # A JointAnimation object with the above curves.
    >>> joint_animation = JointAnimation(
    >>>     joint=Joint(),
    >>>     translation_curve=translation_curve,
    >>>     rotation_curve=Curve(),
    >>>     timewarp_curve=timewarp_curve
    >>> )
    # let us see the result of the get_local_transform method at different times using linear interpolation.
    >>> for t in [0., 0.25, 0.5, 0.75, 1.]: 
    >>>    print(joint_animation.get_local_transform(t, 'linear').pos)
    [0,0,0]
    [0.25,0.25,0.25]
    [0.5,0.5,0.5]
    [0.75,0.75,0.75]
    [1,1,1]

    # Now if we add a key to the time warp curve...
    # Adding a time key at time 0.5 with value 0.2.
    >>> joint_animation.timewarp_curve.set_key_at(time=0.5, value=0.2)
    >>> # or joint_animation.timewarp_curve.add_key(Key(time=0.5, value=0.2))
    # This means that at time 0.5 of the animation, the translation and rotation curves are evaluated at time 0.2.
    >>> for t in [0., 0.25, 0.5, 0.75, 1.]: 
    >>>    print(joint_animation.get_local_transform(t, 'linear').pos)
    [0,0,0]
    [0.1,0.1,0.1]
    [0.2,0.2,0.2]
    [0.6,0.6,0.6]
    [1,1,1]
    # As we can see, the addition of this timekey causes the animation to start slow and speed up from t = 0.5.
    # In other words, 20% of the animation is performed in the first half of the animation and
    # the other 80% of the animation is performed in the second half of the animation.

    Attributes:
    ----------
    joint : Joint
        The joint that is animated.
    translation_curve : AnimationCurve
        The animation curve on the position of the joint.
    rotation_curve : AnimationCurve
        The animation curve on the orientation of the joint.
    timewarp_curve : AnimationCurve
        The time warp curve to apply to the animation.        
    """
    def __init__(self, joint, translation_curve=Curve(), rotation_curve=Curve(), timewarp_curve=Curve()):
        """**Default constructor for the JointAnimation class.**

        Parameters:
        ----------
        joint : Joint
            The joint that is animated.
        translation_curve : Curve, optional
            The animation curve on the position of the joint. By default, an empty curve is used.         
        rotation_curve : Curve, optional
            The animation curve on the orientation of the joint. By default, an empty curve is used.
        timewarp_curve : Curve, optional
            The time warp curve to apply to the animation. By default, a curve with a start key
            at time 0 with value 0 and an end key at time 1 with value 1 is used.

        Notes
        ----
        A time warp curve must contain a start and end key. The start key must have time 0 and the end key must have time 1.
        If no start key is found, a start key is added with time 0 and value 0.
        Similarly, if no end key is found, a end key is added with time 1 and value 1.
        This is done by the init_timewarp_curve method.
        """
        self.joint = joint
        self.translation_curve = translation_curve
        self.rotation_curve = rotation_curve
        self.timewarp_curve = timewarp_curve

        self.init_timewarp_curve()
    
    def init_timewarp_curve(self):
        """Initializes the timewarp curve with a start key at time 0 with value 0
        and an end key at time 1 with value 1.
        """
        self.timewarp_curve.set_key_at(time=0., value=0.)
        self.timewarp_curve.set_key_at(time=1., value=1.)


    def get_local_transform(self, time, interpolation_algorithm):
        """Computes the local animation transform for joint at the given time.

        Parameters:
        ----------
        time : float
            The time at which to compute the transform.
        interpolation_algorithm : str
            The algorithm to use for interpolating the animation curves.
            Possible values: 'constant' and 'linear'.

        Raises:
        ----------
        ValueError
            If the interpolation algorithm is not valid. 
        
        Returns:
        ----------
        Transform
            The local animation transform for the joint at the given time.

        Notes
        -----
        If the translation curve is empty, the behavior of this method changes whether
        the joint is a root joint or not. If the joint is a root joint, the translation
        is set to its local bind transform's position and if the joint is not a root joint,
        the translation is set to [0,0,0].
        Similarly, if the rotation curve is empty, the behavior of this method changes whether
        the joint is a root joint or not. If the joint is a root joint, the rotation is set to its
        local bind transform's orientation and if the joint is not a root joint, the rotation is set
        to the identity quaternion (1,0,0,0).
        If the timewarp curve is empty, this method behaves the same way as with a default timewarp curve.
        """
        if self.timewarp_curve.is_empty():
            key_time = time
        else:
            key_time = self.timewarp_curve.get_lerp_value(time)
        
        if interpolation_algorithm == "constant":
            translation = self.translation_curve.get_previous_value(key_time)
            rotation = self.rotation_curve.get_previous_value(key_time)
        elif interpolation_algorithm == "linear":
            translation = self.translation_curve.get_lerp_value(key_time)
            rotation = self.rotation_curve.get_lerp_value(key_time)
        elif interpolation_algorithm == "spline":
            raise NotImplementedError("Spline interpolation not implemented yet.")
        else:
            raise ValueError("Invalid interpolation algorithm. Must be one of 'constant', 'linear', or 'spline'.")

        if translation is None:
            if self.joint.parent is None:
                translation = self.joint.local_bind_transform.pos
            else:
                translation = np.array([0,0,0])
        
        if rotation is None:
            if self.joint.parent is None:
                rotation = self.joint.local_bind_transform.orient
            else:
                rotation = quaternion.one

        return Transform(pos=translation, orient=rotation)

    def __repr__(self):
        return f"JointAnimation(joint={str(self.joint)},\
        translation_curve={str(self.translation_curve)}, \
        rotation_curve={str(self.rotation_curve)},\
        timewarp_curve={str(self.timewarp_curve)})" 

    def __eq__(self, other):
        """Equality operator for JointAnimation objects.

        Note:
        ----------
        Two JointAnimation objects are considered equal if:
        - Their joints are equal. (See Joint.__eq__)
        - Their translation curves are equal. (See Curve.__eq__)
        - Their rotation curves are equal. (See Curve.__eq__)
        - Their timewarp curves are equal. (See Curve.__eq__)

        Parameters
        ----------
        other : JointAnimation
            JointAnimation object to compare to.

        Returns
        -------
        bool
            True if the two JointAnimation objects are equal, False otherwise.
        """
        return (self.joint == other.joint
            and self.translation_curve == other.translation_curve
            and self.rotation_curve == other.rotation_curve
            and self.timewarp_curve == other.timewarp_curve)