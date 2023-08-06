import copy

from skeletal_animation.core.animate import *
from skeletal_animation.utils.other import are_skeletons_similar
from skeletal_animation.core.model import *

class Animator:
    """Controller class to animate a skeleton.

    Attributes:
    ----------
    animation : Animation
        Animation to be played.
    skeleton : Skeleton
        Skeleton to be animated.
    anim_time : float
        Time since the beginning of the animation.
    kps : int
        Keys per second of the animation. Corresponds to the speed at which the animation is played.
    duration : float
        Duration of the animation in seconds.
    interpolation_algo : str
        Algorithm to be used to interpolate between the keys of the animation.
    is_playing : bool
        Boolean to determine whether the animation is playing or paused.
        Only used when the animator is played by the gui script (frame.py).
    """

    def __init__(self, animation, skeleton, kps=30, interpolation_algo = "linear"):
        """**Default constructor for the Animator class.**

        Parameters:
        ----------
        animation : Animation
            Animation to be played.
        skeleton : Skeleton
            Skeleton to be animated.    
        kps : int, optional
            Keys per second of the animation, by default 30.
        interpolation_algo : str, optional
            Interpolation algorithm to be used, by default "linear".
            Possible values: "constant" and "linear".
        """
        self.animation = animation 
        self.skeleton = skeleton
        self.anim_time = 0
        self.kps = kps
        self.duration = self.compute_animation_duration()
        self.interpolation_algo = interpolation_algo
        self.is_playing = True

    def compute_animation_duration(self):
        """Computes the duration of the animation in seconds.

        Called by the constructor.

        Returns:
        ----------        
        float
            The duration of the animation in seconds.
        """
        return self.animation.max_key_time / self.kps


    def generate_pose(self):
        """Generates a pose dictionary.

        The pose dictionary is of the form:
        {int: Transform}
        The integer key is the id of a joint in the skeleton and
        the transform value is the local animation transform of the joint.

        The local animation transform is the transform that must be applied to the joint's local bind transform
        to obtain the model transform of the joint at a specific time in the animation.

        Returns:
        ----------
        dict (int: Transform)
            Pose dictionary generated.
            Where the integer key is the id of a joint in the skeleton and 
            the transform value is the local animation transform of the joint.

        See Also:
        ----------
        joint.forward_kinematics: method that computes the model transform of the joints
        using the pose dictionary.
        jointanimation.get_local_transform: method used to compute the local animation
        transform contained in the pose dictionary.
        """
        time = (self.anim_time / self.duration) % 1.0
        pose_dict = {}

        for joint_animation in self.animation.joint_animations:
            
            joint = joint_animation.joint                        
            
            local_transform = joint_animation.get_local_transform(time, self.interpolation_algo)

            pose_dict[joint.id] = local_transform      

        return pose_dict  
        
    def update(self, time, verbose=False):
        """Updates the animation time.

        Parameters:
        ----------
        time : float
            Time to be added to the animation time.
            Is affected by the speed of the animation in kps.
        verbose : bool, optional
            If set to true the effective time added to the animation time 
            will be printed. by default False.
        """
        if verbose:
            print("_dt:", time * (self.kps / 30))
        self.anim_time += time * (self.kps / 30)
    

    def play(self, play_duration = 1., fps=30., verbose=False):
        """Plays the animation for a given duration.

        This method is used to simulate the animation without rendering it.
        The animation is played for a simulated duration in seconds.
        The amount of step to compute per second is given by the fps parameter.

        Parameters:
        ----------
        play_duration : float, optional
            The length of time the animation is left running in seconds, by default 1.
        fps : float, optional
            The amount of steps to compute per second, by default 30.
        verbose : bool, optional
            If set to true the model transform of each joint will be printed at every step,
            by default False.    
        """
        while self.anim_time <= play_duration:
            self.step(1/fps, verbose)


    def step(self, time, verbose=False):
        """Steps the animation for a given time.

        Calls the update method to update the animation time.
        Calls the generate_pose method to generate the pose dictionary.
        Then calls the compute_pose method of the skeleton to update the model transform
        of every joint using forward kinematics.

        Parameters:
        ----------
        time : float
            Time to step the animation for.
            Negative values step the animation backwards.
        verbose : bool, optional
            If set to true the current time of the animation and the model transform
            of each joint will be printed, by default False.        
        """
        self.update(time, verbose)
        pose_dict = self.generate_pose()
        self.skeleton.compute_pose(pose_dict)
        if verbose:
            print("_Time:", self.anim_time)
            for joint in self.skeleton.as_joint_list():
                print("Joint:", joint.name, "Transform:", joint.model_transform)

    def translate(self, x, y, z):
        """Translates the animation by a given vector.

        The translation is only applied to the root joint of the skeleton.
        Every key in the translation curve for the root is translated by the given vector.

        Parameters:
        ----------
        x : float
            Amount of the translation in the x direction.
        y : floatthe 
            Amount of the translation in the y direction.
        z : floatthe 
            Amount of the translation in the z direction.
        """
        animation = self.animation
        root_animation = animation.joint_animations[0]
        for key in root_animation.translation_curve.keys:
            key.value = [key.value[0] + x, key.value[1] + y, key.value[2] + z]

    def clip(self, other):
        """Clips the other animation at the end of the current animation.

        Join the two animations together appending the keys of the other animation
        to the end of the current animation.
        This creates a new animation that is the concatenation of the two.
        The duration of the new animation is the sum of the duration of the two animations.
        Curves are normalized to keep the time values between 0 and 1.
        
        Parameters:
        ----------
        other : Animation
            Animation to be clipped to the current animation.
        
        Returns:
        ----------
        Animator
            New animator containing the concatenated animation.

        Notes
        -----
        The initial animator objects self and other are not modified.
        """
        if not are_skeletons_similar(self.skeleton, other.skeleton):
            raise ValueError("Cannot generate blend between the two given animators. Skeletons are not identical.")

        self_animation = copy.deepcopy(self.animation)
        other_animation = copy.deepcopy(other.animation)

        total_duration = self_animation.max_key_time + other_animation.max_key_time
        self_duration_ratio = self_animation.max_key_time / total_duration

        new_joint_animations = []
        
        for ja_id in range(len(self.animation.joint_animations)):
            self_joint_animation = self_animation.joint_animations[ja_id]
            other_joint_animation = other_animation.joint_animations[ja_id]
            new_joint_animation = JointAnimation(self_joint_animation.joint,
                                                rotation_curve=Curve(),
                                                translation_curve=Curve(),
                                                timewarp_curve=Curve())

            # translation
            self_translation_curve = self_joint_animation.translation_curve
            other_translation_curve = other_joint_animation.translation_curve
            if self_translation_curve is not None:
                self_translation_curve.normalize_times(total_duration / self_animation.max_key_time)
            if other_translation_curve is not None:
                other_translation_curve.normalize_times(total_duration / other_animation.max_key_time)
            for key in self_translation_curve.keys:
                new_joint_animation.translation_curve.set_key_at(key.time, key.value)
            for key in other_translation_curve.keys:
                new_joint_animation.translation_curve.set_key_at(key.time + self_duration_ratio, key.value)

            # rotation
            self_rotation_curve = self_joint_animation.rotation_curve
            other_rotation_curve = other_joint_animation.rotation_curve
            if self_rotation_curve is not None:
                self_rotation_curve.normalize_times(total_duration / self_animation.max_key_time)
            if other_rotation_curve is not None:
                other_rotation_curve.normalize_times(total_duration / other_animation.max_key_time)
            for key in self_rotation_curve.keys:
                new_joint_animation.rotation_curve.set_key_at(key.time, key.value)
            for key in other_rotation_curve.keys:
                new_joint_animation.rotation_curve.set_key_at(key.time + self_duration_ratio, key.value)

            # timewarp
            self_timewarp_curve = self_joint_animation.timewarp_curve
            other_timewarp_curve = other_joint_animation.timewarp_curve
            if self_timewarp_curve is not None:
                self_timewarp_curve.normalize_times(total_duration / self_animation.max_key_time)
                self_timewarp_curve.normalize_values(total_duration / self_animation.max_key_time)
            if other_timewarp_curve is not None:
                other_timewarp_curve.normalize_times(total_duration / other_animation.max_key_time)
                other_timewarp_curve.normalize_values(total_duration / other_animation.max_key_time)
            for key in self_timewarp_curve.keys:
                new_joint_animation.timewarp_curve.set_key_at(key.time, key.value)
            for key in other_timewarp_curve.keys:
                new_joint_animation.timewarp_curve.set_key_at(key.time + self_duration_ratio, key.value + self_duration_ratio)        

            new_joint_animations.append(new_joint_animation)    

        new_animation = Animation(new_joint_animations, total_duration)
        new_skeleton = copy.deepcopy(self.skeleton)

        new_animator = Animator(new_animation, new_skeleton, self.kps, self.interpolation_algo)

        return new_animator       

    def crop(self, start_time, end_time):
        """Crops the animation to be between the given start and end times.

        The resulting animation contains all the keys that are between the given start and end times.
        The duration of the resulting animation is the difference between the given start and end times.
        Curves are normalized to keep the time values between 0 and 1.

        Parameters:
        ----------
        start_time : float
            Start time of the cropped animation.
        end_time : float
            End time of the cropped animation.
        
        Returns:
        ----------
        Animator
            New animator containing the cropped animation.

        Raises:
        ----------
        ValueError
            If the start time is greater or equal to the end time.
        
        Notes
        -----
        The initial animator object is not modified.
        """
        if start_time >= end_time:
            raise ValueError("Start time must be strictly less than end time.")

        self_animation = copy.deepcopy(self.animation)

        new_joint_animations = []

        for ja in self_animation.joint_animations:
            new_joint_animation = JointAnimation(ja.joint,
                                                rotation_curve=Curve(),
                                                translation_curve=Curve(),
                                                timewarp_curve=Curve()) 
            new_joint_animation.timewarp_curve.remove_key_at(0.0)           
            new_joint_animation.timewarp_curve.remove_key_at(1.0)

            # translation
            self_translation_curve = ja.translation_curve
            if self_translation_curve is not None:
                for key in self_translation_curve.keys:
                    start_translation_value = self_translation_curve.get_lerp_value(start_time)
                    end_translation_value = self_translation_curve.get_lerp_value(end_time)
                    new_joint_animation.translation_curve.set_key_at(0., start_translation_value)
                    new_joint_animation.translation_curve.set_key_at(end_time - start_time, end_translation_value)
                
                    if key.time <= end_time and key.time >= start_time:
                        new_joint_animation.translation_curve.set_key_at(key.time - start_time, key.value)

            # rotation
            self_rotation_curve = ja.rotation_curve
            if self_rotation_curve is not None:
                for key in self_rotation_curve.keys:
                    start_rotation_value = self_rotation_curve.get_lerp_value(start_time)
                    end_rotation_value = self_rotation_curve.get_lerp_value(end_time)
                    new_joint_animation.rotation_curve.set_key_at(0., start_rotation_value)
                    new_joint_animation.rotation_curve.set_key_at(end_time - start_time, end_rotation_value)
                
                    if key.time <= end_time and key.time >= start_time:
                        new_joint_animation.rotation_curve.set_key_at(key.time - start_time, key.value)

            # timewarp
            self_timewarp_curve = ja.timewarp_curve
            if self_timewarp_curve is not None:
                for key in self_timewarp_curve.keys:
                    start_timewarp_value = self_timewarp_curve.get_lerp_value(start_time)
                    end_timewarp_value = self_timewarp_curve.get_lerp_value(end_time)
                    new_joint_animation.timewarp_curve.set_key_at(0., start_timewarp_value)
                    new_joint_animation.timewarp_curve.set_key_at(end_time - start_time, end_timewarp_value)
                
                    if key.time <= end_time and key.time >= start_time:
                        new_joint_animation.timewarp_curve.set_key_at(key.time - start_time, key.value)

            new_joint_animations.append(new_joint_animation)

        for new_ja in new_joint_animations:
            new_timewarp_curve = new_ja.timewarp_curve
            min_timewarp_value = 1.0
            max_timewarp_value = 0.0     

            for key in new_timewarp_curve.keys:
                if key.value < min_timewarp_value:
                    min_timewarp_value = key.value
                if key.value > max_timewarp_value:
                    max_timewarp_value = key.value

            for key in new_timewarp_curve.keys:
                key.value -= min_timewarp_value          

            new_ja.translation_curve.normalize_times(end_time - start_time)
            new_ja.rotation_curve.normalize_times(end_time - start_time)
            new_ja.timewarp_curve.normalize_times(end_time - start_time)
            new_ja.timewarp_curve.normalize_values(max_timewarp_value - min_timewarp_value)

        cropped_duration = (end_time - start_time) * self_animation.max_key_time

        new_animation = Animation(new_joint_animations, cropped_duration)
        new_skeleton = copy.deepcopy(self.skeleton)

        return Animator(new_animation, new_skeleton, self.kps, self.interpolation_algo)

    # Utility functions for live coding.
    def pause(self):
        """Pauses the animation.

        Sets the is_playing flag to False.
        """
        self.is_playing = False
    
    def resume(self):
        """Resumes the animation.

        Sets the is_playing flag to True.
        """
        self.is_playing = True

    def add_timekey(self, real_time, key_time):
        """Adds a timekey to the animation.

        The same timekey is added to the timewarp curve of every joint animation
        in the animator's animation.
        More information on timewarp curve and timekeys can be found in the documentation of the
        JointAnimation class.

        Parameters:
        ----------
        real_time : float
            The time of the timekey.
        key_time : float
            The value of the timekey.
        """
        for joint_animation in self.animation.joint_animations:
            joint_animation.timewarp_curve.set_key_at(real_time, key_time)

    def remove_timekey_at_time(self, time):
        """Removes a timekey from the animation at a given time.

        Remove the timekey from the timewarp curve of every joint animation in the animator's animation
        at the given time.
        More information on timewarp curve and timekeys can be found in the documentation of the
        JointAnimation class.

        Parameters:
        ----------
        time : float
            The time at which the timekeys are removed.
        """
        for joint_animation in self.animation.joint_animations:
            joint_animation.timewarp_curve.remove_key_at(time)
