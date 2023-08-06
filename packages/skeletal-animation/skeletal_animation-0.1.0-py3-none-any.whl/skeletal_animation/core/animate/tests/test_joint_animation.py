import unittest
import numpy as np
import quaternion

from skeletal_animation.core.math.transform import Transform, identity
from skeletal_animation.core.math.constants import HIGH_R_TOL, HIGH_A_TOL
from skeletal_animation.core.model.joint import Joint
from skeletal_animation.core.animate.key import Key
from skeletal_animation.core.animate.curve import Curve
from skeletal_animation.core.animate.jointanimation import JointAnimation

# TODO might want to rewrite the tests about timekeys here 

class TestJointAnimationConstructor(unittest.TestCase):
    def setUp(self):
        self.t = Transform(pos=[0., 1., 0.], orient=quaternion.one)
        self.root_joint = Joint("root", local_bind_transform=self.t)
        self.child_joint = Joint("child", local_bind_transform=identity)
        self.root_joint.add_child(self.child_joint)

        self.translation_curve = Curve([Key(0., [0., 0., 0.]), Key(1., [1., 2., 3.])])
        self.rotation_curve = Curve([Key(0., np.quaternion(1., 0., 0., 0.)), Key(1., np.quaternion(4/5, 3/5, 0., 0.))])
        
    def test_joint_animation_constructor_with_translation_curve(self):
        joint_animation = JointAnimation(joint=self.root_joint, translation_curve=self.translation_curve)
        self.assertEqual(joint_animation.translation_curve, self.translation_curve)
        self.assertEqual(joint_animation.rotation_curve, Curve())

class TestJointAnimationGetLocalTransformWithConstantInterpolation(unittest.TestCase):
    def setUp(self):
        self.t = Transform(pos=[1., 2., 3.], orient=quaternion.one)
        self.root_joint = Joint("root", local_bind_transform=self.t)
        self.child_joint = Joint("child", local_bind_transform=identity)
        self.root_joint.add_child(self.child_joint)
        
        self.child_joint.transform = self.t

        self.translation_curve = Curve([Key(0., [1., 0., 0.]), Key(1., [1., 2., 3.])])
        self.rotation_curve = Curve([Key(0., np.quaternion(1., 0., 0., 0.)), Key(1., np.quaternion(4/5, 3/5, 0., 0.))])

        self.empty_curve = Curve()

    def test_joint_animation_get_local_transform_on_root(self):
        ja = JointAnimation(joint=self.root_joint, translation_curve=self.translation_curve, rotation_curve=self.rotation_curve)
        self.assertEqual(
            ja.get_local_transform(0, "constant"),
            Transform(pos=[1., 0., 0.], orient=np.quaternion(1, 0, 0., 0.))
            )
        self.assertEqual(
            ja.get_local_transform(0.5, "constant"),
            Transform(pos=[1., 0., 0.], orient=np.quaternion(1, 0, 0., 0.))
            )
        self.assertEqual(
            ja.get_local_transform(1, "constant"),
            Transform(pos=[1., 2., 3.], orient=np.quaternion(4/5, 3/5, 0., 0.))
            )
    
    def test_joint_animation_get_local_transform_on_child(self):
        ja = JointAnimation(joint=self.child_joint, translation_curve=self.translation_curve, rotation_curve=self.rotation_curve)
        self.assertEqual(
            ja.get_local_transform(0, "constant"),
            Transform(pos=[1., 0., 0.], orient=np.quaternion(1, 0, 0., 0.))
            )
        self.assertEqual(
            ja.get_local_transform(0.5, "constant"),
            Transform(pos=[1., 0., 0.], orient=np.quaternion(1, 0, 0., 0.))
            )
        self.assertEqual(
            ja.get_local_transform(1, "constant"),
            Transform(pos=[1., 2., 3.], orient=np.quaternion(4/5, 3/5, 0., 0.))
            )

    def test_joint_animation_get_local_transform_on_root_with_no_animation_curve(self):
        ja = JointAnimation(joint=self.root_joint, translation_curve=self.empty_curve, rotation_curve=self.empty_curve)
        self.assertEqual(ja.get_local_transform(0, "constant"), self.t)
        self.assertEqual(ja.get_local_transform(0.5, "constant"), self.t)
        self.assertEqual(ja.get_local_transform(1, "constant"), self.t)
    
    def test_joint_animation_get_local_transform_on_root_with_translation_curve(self):
        ja = JointAnimation(joint=self.root_joint, translation_curve=self.translation_curve, rotation_curve=self.empty_curve)
        self.assertEqual(
            ja.get_local_transform(0, "constant"),
            Transform(pos=[1., 0., 0.], orient=quaternion.one)
            )
        self.assertEqual(
            ja.get_local_transform(0.5, "constant"),
            Transform(pos=[1., 0., 0.], orient=quaternion.one)
            )
        self.assertEqual(
            ja.get_local_transform(1, "constant"),
            Transform(pos=[1., 2., 3.], orient=quaternion.one)
            )
    
    def test_joint_animation_get_local_transform_on_child_with_rotation_curve(self):
        ja = JointAnimation(joint=self.child_joint, translation_curve=self.empty_curve, rotation_curve=self.rotation_curve)
        self.assertEqual(
            ja.get_local_transform(0, "constant"),
            Transform(pos=[0., 0., 0.], orient=np.quaternion(1, 0, 0., 0.))
            )
        self.assertEqual(
            ja.get_local_transform(0.5, "constant"),
            Transform(pos=[0., 0., 0.], orient=np.quaternion(1, 0, 0., 0.))
            )
        self.assertEqual(
            ja.get_local_transform(1, "constant"),
            Transform(pos=[0., 0., 0.], orient=np.quaternion(4/5, 3/5, 0., 0.))
            )

class TestJointAnimationGetLocalTransformWithLinearInterpolation(unittest.TestCase):
    def setUp(self):
        self.t = Transform(pos=[1., 2., 3.], orient=quaternion.one)
        self.root_joint = Joint("root", local_bind_transform=self.t)
        self.child_joint = Joint("child", local_bind_transform=identity)
        self.root_joint.add_child(self.child_joint)
        
        self.child_joint.transform = self.t

        self.translation_curve = Curve([Key(0., [1., 0., 0.]), Key(1., [1., 2., 3.])])

        self.rotation_curve = Curve([Key(0., np.quaternion(1., 0., 0., 0.)), Key(1., np.quaternion(4/5, 3/5, 0., 0.))])

        self.empty_curve = Curve()

    def test_joint_animation_get_local_transform_on_root(self):
        ja = JointAnimation(joint=self.root_joint, translation_curve=self.translation_curve, rotation_curve=self.rotation_curve)
        self.assertEqual(
            ja.get_local_transform(0, "linear"),
            Transform(pos=[1., 0., 0.], orient=np.quaternion(1, 0, 0., 0.))
            )
        self.assertEqual(
            ja.get_local_transform(0.5, "linear"),
            Transform(pos=[1., 1., 1.5], orient=quaternion.slerp(quaternion.one, np.quaternion(4/5, 3/5, 0., 0.), 0, 1, 0.5))
            )
        self.assertEqual(
            ja.get_local_transform(1, "linear"),
            Transform(pos=[1., 2., 3.], orient=np.quaternion(4/5, 3/5, 0., 0.))
            )
    
    def test_joint_animation_get_local_transform_on_root_with_no_animation_curve(self):
        ja = JointAnimation(joint=self.root_joint, translation_curve=self.empty_curve, rotation_curve=self.empty_curve)
        self.assertEqual(ja.get_local_transform(0, "linear"), self.t)
        self.assertEqual(ja.get_local_transform(0.5, "linear"), self.t)
        self.assertEqual(ja.get_local_transform(1, "linear"), self.t)
    
    def test_joint_animation_get_local_transform_on_root_with_translation_curve(self):
        ja = JointAnimation(joint=self.root_joint, translation_curve=self.translation_curve, rotation_curve=self.empty_curve)    
        self.assertEqual(
            ja.get_local_transform(0, "linear"),
            Transform(pos=[1., 0., 0.], orient=quaternion.one)
            )
        self.assertEqual(
            ja.get_local_transform(0.5, "linear"),
            Transform(pos=[1., 1., 1.5], orient=quaternion.one)
            )
        self.assertEqual(
            ja.get_local_transform(1, "linear"),
            Transform(pos=[1., 2., 3.], orient=quaternion.one)
            )
    
    def test_joint_animation_get_local_transform_on_child_with_rotation_curve(self):
        ja = JointAnimation(joint=self.child_joint, translation_curve=self.empty_curve, rotation_curve=self.rotation_curve)    
        self.assertEqual(
            ja.get_local_transform(0, "linear"),
            Transform(pos=[0., 0., 0.], orient=np.quaternion(1, 0, 0., 0.))
            )
        self.assertEqual(
            ja.get_local_transform(0.5, "linear"),
            Transform(pos=[0., 0., 0.], orient=quaternion.slerp(quaternion.one, np.quaternion(4/5, 3/5, 0., 0.), 0, 1, 0.5))
            )
        self.assertEqual(
            ja.get_local_transform(1, "linear"),
            Transform(pos=[0., 0., 0.], orient=np.quaternion(4/5, 3/5, 0., 0.))
            )

class TestJointAnimationGetLocalTransformWithTimewarpCurve(unittest.TestCase):
    def setUp(self):
        # A translation curve that goes from [0,0,0] to [1,1,1] at time 0 and 1 respectively.
        self.translation_curve = Curve(
            [Key(time=0., value=[0,0,0]),
            Key(time=1., value=[1,1,1])]
        )

        # A default time warp curve. The value of the key at time 0 is 0 and the value of the key at time 1 is 1.
        self.timewarp_curve = Curve(
            [Key(time=0., value=0.),
            Key(time=1., value=1.)]
        )
            
        # A JointAnimation object with the above curves.
        self.joint_animation = JointAnimation(
            joint=Joint(),
            translation_curve=self.translation_curve,
            rotation_curve=Curve(),
            timewarp_curve=self.timewarp_curve
        )
        
        self.expected_default_result = [[0,0,0],
        [0.25,0.25,0.25],
        [0.5,0.5,0.5],
        [0.75,0.75,0.75],
        [1,1,1]]

        self.expected_timewarp_result = [[0,0,0],
        [0.1,0.1,0.1],
        [0.2,0.2,0.2],
        [0.6,0.6,0.6],
        [1,1,1]]

    def test_joint_animation_get_local_transform_with_timewarp_curve(self):
        # let us see the result of the get_local_transform method at different times using linear interpolation.
        effective_default_result = []        
        for t in [0., 0.25, 0.5, 0.75, 1.]: 
            effective_default_result.append(self.joint_animation.get_local_transform(t, 'linear').pos)
        self.assertTrue(np.allclose(effective_default_result, self.expected_default_result, rtol=HIGH_R_TOL, atol=HIGH_A_TOL))

        # Now if we add a key to the time warp curve...
        # Adding a time key at time 0.5 with value 0.2.
        self.joint_animation.timewarp_curve.set_key_at(time=0.5, value=0.2)
        # or joint_animation.timewarp_curve.add_key(Key(time=0.5, value=0.2))
        # This means that at time 0.5 of the animation, the translation and rotation curves are evaluated at time 0.2.
        effective_timewarp_result = []
        for t in [0., 0.25, 0.5, 0.75, 1.]: 
            effective_timewarp_result.append(self.joint_animation.get_local_transform(t, 'linear').pos)
        self.assertTrue(np.allclose(effective_timewarp_result, self.expected_timewarp_result, rtol=HIGH_R_TOL, atol=HIGH_A_TOL))
