import unittest
import numpy as np
import quaternion

from skeletal_animation.core.model.joint import Joint
from skeletal_animation.core.math.transform import Transform, identity
from skeletal_animation.core.math.constants import HIGH_R_TOL, HIGH_A_TOL

class TestJointDefaultConstructor(unittest.TestCase):
    def setUp(self): 
        self.root = Joint(name="root")
        self.back = Joint(name="back", local_bind_transform=Transform(pos=[1,0,1]))
        self.root.add_child(self.back)
        self.arm = Joint(name="arm", local_bind_transform=Transform(pos=[0.25,0,0], orient=np.quaternion(1,0,0,0)))
        self.back.add_child(self.arm)
        with self.assertWarnsRegex(UserWarning, "Transform built with non unit quaternion."):
            self.hand = Joint(name="hand", local_bind_transform=Transform(orient=quaternion.from_float_array([.2,.8,.2,0])))
        self.arm.add_child(self.hand)
        # root -> back -> arm -> hand
        
    def test_default_constructor_with_default_parameters(self):
        j = Joint()
        self.assertIsNone(j.parent)
        self.assertEqual(j.name, "new joint")
        self.assertEqual(j.local_bind_transform, identity)

    def test_default_constructor_with_no_parent(self):
        t = Transform([1,0,2], np.quaternion(0, 2/3, 1/3, 2/3))
        j = Joint(name="root", local_bind_transform=t)
        self.assertIsNone(j.parent)
        self.assertEqual(j.name, "root")
        self.assertEqual(j.local_bind_transform, t)
    
    def test_default_constructor_with_root_parent(self):          
        j = self.back
        self.assertEqual(j.parent, self.root)
    
    def test_default_constructor_with_non_root_parent(self):  
        j = self.hand
        self.assertEqual(j.parent.parent.parent, self.root)


class TestJointIsCyclic(unittest.TestCase):
    def setUp(self): 
        self.root = Joint(name="root")
        self.back = Joint(name="back", local_bind_transform=Transform(pos=[1,0,1]))
        self.root.add_child(self.back)
        # root -> back
    
    def test_is_cyclic_simple(self):
        self.assertFalse(self.root.is_cyclic())
        with self.assertWarns(UserWarning):
            self.back.add_child(self.root)
        # root -> back -> root  =>  CYCLE!
        self.assertTrue(self.root.is_cyclic())
        self.back.remove_child(self.root)
        self.assertFalse(self.root.is_cyclic())

    def test_is_cyclic_intermediate(self):
        r = Joint(name="r")
        c1 = Joint(name="c1")
        c2 = Joint(name="c2")
        c3 = Joint(name="c3")
        r.add_children([c1, c2])
        c1.add_child(c3)
        self.assertFalse(r.is_cyclic())
        with self.assertWarns(UserWarning):
            c3.add_child(c1)
        self.assertFalse(r.is_cyclic())
        self.assertTrue(c1.is_cyclic())
        c3.remove_child(c1)
        self.assertFalse(c1.is_cyclic())
        c3.add_child(r)
        self.assertFalse(c1.is_cyclic())

    def test_is_cyclic_complex(self):
        arm = Joint(name="arm", local_bind_transform=identity)
        self.back.add_child(arm)
        forearm = Joint(name="forearm", local_bind_transform=identity)
        arm.add_child(forearm)
        hand = Joint(name="hand", local_bind_transform=identity)
        forearm.add_child(hand)
        finger = Joint(name="finger", local_bind_transform=identity)
        hand.add_child(finger)
        fingertip = Joint(name="fingertip", local_bind_transform=identity)
        finger.add_child(fingertip)
        head = Joint(name="head", local_bind_transform=identity)
        self.back.add_child(head)
        nose = Joint(name="nose", local_bind_transform=identity)
        head.add_child(nose)
        # root -> back -> arm -> forearm -> hand -> finger -> fingertip
        #              -> head -> nose
        
        self.assertFalse(self.root.is_cyclic())
        self.assertFalse(arm.is_cyclic())
        with self.assertWarns(UserWarning):
            finger.add_child(self.back)
        # root -> 
        # back -> arm -> forearm -> hand -> finger -> fingertip
        #      -> head -> nose -> arm              -> back -> arm -> forearm -> hand -> finger -> fingertip
        #                                                  -> head -> nose -> arm 
        # => CYCLE!  
        self.assertFalse(self.root.is_cyclic())      
        self.assertTrue(arm.is_cyclic())


class TestJointAddChild(unittest.TestCase):
    def setUp(self): 
        self.root = Joint(name="root")
        self.back = Joint(name="back")
        self.arm = Joint(name="arm")
        # wanted hierarchy
        # root -> back -> arm
    
    def test_parent_update(self):
        self.assertIsNone(self.back.parent)
        self.root.add_child(self.back)
        self.assertEqual(self.back.parent, self.root)
        self.assertEqual(self.root.children, [self.back])
    
    def test_cyclicity_warning(self):
        self.root.add_child(self.back)
        self.back.add_child(self.arm)
        with self.assertWarns(UserWarning):
            self.arm.add_child(self.root)

class TestJointAddChildre(unittest.TestCase):
    def setUp(self): 
        self.root = Joint(name="root")
        self.back = Joint(name="back")
        self.leftarm = Joint(name="leftarm")
        self.rightarm = Joint(name="rightarm")
        # wanted hierarchy
        # root -> back -> leftarm
        #              -> rightarm

    def test_joint_add_children(self):
        self.root.add_children([self.back])
        self.back.add_children([self.rightarm, self.leftarm])
        self.assertIsNone(self.root.parent)
        self.assertEqual(self.back.parent, self.root)
        self.assertEqual(self.leftarm.parent, self.back)
        self.assertEqual(self.rightarm.parent, self.back)

class TestJointRemoveChild(unittest.TestCase):
    def setUp(self): 
        self.root = Joint(name="root")
        self.back = Joint(name="back")
        self.arm = Joint(name="arm")

    def test_parent_update(self):
        self.root.add_child(self.back)
        self.back.add_child(self.arm)
        self.root.remove_child(self.back)
        self.assertIsNone(self.back.parent)
        self.assertEqual(self.root.children, [])

class TestJointRemoveAllChildren(unittest.TestCase):
    def setUp(self): 
        self.root = Joint(name="root")
        self.back = Joint(name="back")
        self.leftarm = Joint(name="leftarm")
        self.rightarm = Joint(name="rightarm")

    def test_parent_update(self):
        self.root.add_child(self.back)
        self.back.add_child(self.leftarm)
        self.back.add_child(self.rightarm)        
        self.root.remove_all_children()
        self.assertIsNone(self.back.parent)        
        self.back.remove_all_children()
        self.assertEqual(self.back.children, [])

class TestJointForwardsKinematics(unittest.TestCase):
    def setUp(self):
        
        # Init joints
        self.root = Joint(name="root", local_bind_transform=identity)

        self.back = Joint(name="back", local_bind_transform=Transform(pos=[0,3,0]))

        self.leftarm_q = np.quaternion(-1, 0, 1, 0)
        with self.assertWarnsRegex(UserWarning, "Transform built with non unit quaternion."):            
            self.leftarm_t = Transform(pos=[2, 0, 0], orient=self.leftarm_q)
        self.leftarm_t.normalize_quaternion()
        self.leftarm = Joint(name="leftarm", local_bind_transform=self.leftarm_t)

        rightarm_t = Transform(pos=[-2, 0, 0])
        self.rightarm = Joint(name="rightarm", local_bind_transform=rightarm_t) 

        self.lefthand_t = Transform(pos=[1, 0, 0])        
        self.lefthand = Joint(name="lefthand", local_bind_transform=self.lefthand_t)

        # Build hierarchy
        self.root.add_child(self.back)
        self.back.add_children([self.leftarm, self.rightarm])
        self.leftarm.add_child(self.lefthand)

    def test_joint_fk_with_no_pose_dict_and_root_at_identity(self):        
        self.assertEqual(self.root.local_bind_transform, identity)
        self.assertEqual(self.root.model_transform, None)
        self.assertEqual(self.leftarm.local_bind_transform, self.leftarm_t)
        self.assertEqual(self.leftarm.model_transform, None)
        self.assertEqual(self.lefthand.local_bind_transform, self.lefthand_t)
        self.assertEqual(self.lefthand.model_transform, None)

        self.root.forward_kinematics(current_pose_dict=None)

        self.assertEqual(self.root.local_bind_transform, identity)
        self.assertEqual(self.root.model_transform, identity)

        self.assertEqual(self.leftarm.local_bind_transform, self.leftarm_t)

        with self.assertWarnsRegex(UserWarning, "Transform built with non unit quaternion."):
            leftarm_t = Transform(pos=[2,3,0], orient=self.leftarm_q)
        leftarm_t.normalize_quaternion()
        self.assertEqual(self.leftarm.model_transform, leftarm_t)

        self.assertEqual(self.lefthand.local_bind_transform, self.lefthand_t)
        with self.assertWarnsRegex(UserWarning, "Transform built with non unit quaternion."):
            lefthand_t = Transform(pos=[2,3,1], orient=self.leftarm_q)
        lefthand_t.normalize_quaternion()
        self.assertEqual(self.lefthand.model_transform, lefthand_t)

    def test_joint_fk_with_no_pose_dict_and_root_translated(self):    
        new_root_t = Transform(pos=[0, -1, 1])
        self.root.local_bind_transform = new_root_t

        self.root.forward_kinematics(current_pose_dict=None)

        self.assertEqual(self.root.model_transform, new_root_t)

        with self.assertWarnsRegex(UserWarning, "Transform built with non unit quaternion."):
            leftarm_t = Transform(pos=[2,2,1], orient=self.leftarm_q)
        leftarm_t.normalize_quaternion()
        self.assertEqual(self.leftarm.model_transform, leftarm_t)

        with self.assertWarnsRegex(UserWarning, "Transform built with non unit quaternion."):
            lefthand_t = Transform(pos=[2,2,2], orient=self.leftarm_q)
        lefthand_t.normalize_quaternion()
        self.assertEqual(self.lefthand.model_transform, lefthand_t)
    
    def test_joint_fk_with_no_pose_dict_and_root_rotated(self):       
        new_q = np.quaternion(1, 0, 1+np.sqrt(2), 0) # right handed 135° rotation around the y-axis

        with self.assertWarnsRegex(UserWarning, "Transform built with non unit quaternion."):
            new_root_t = Transform(orient=new_q)
        new_root_t.normalize_quaternion()
        self.root.local_bind_transform = new_root_t

        self.root.forward_kinematics(current_pose_dict=None)

        self.assertEqual(self.root.model_transform, new_root_t)


        leftarm_q = np.quaternion(1+np.sqrt(2), 0, 1, 0)
        with self.assertWarnsRegex(UserWarning, "Transform built with non unit quaternion."):
            leftarm_t = Transform(pos=[-np.sqrt(2), 3, -np.sqrt(2)], orient=leftarm_q)
        leftarm_t.normalize_quaternion()
        self.assertEqual(self.leftarm.model_transform, leftarm_t)

        with self.assertWarnsRegex(UserWarning, "Transform built with non unit quaternion."):
            lefthand_t = Transform(pos=[-np.sqrt(2)/2, 3, -3*np.sqrt(2)/2], orient=leftarm_q)
        lefthand_t.normalize_quaternion()
        self.assertEqual(self.lefthand.model_transform, lefthand_t)

    def test_joint_fk_with_translation_only_pose_dict_and_static_root_at_identity(self):
        # place root at identity
        self.root.local_bind_transform = identity

        pose_dict = {}
        pose_dict[self.root.id] = self.root.local_bind_transform # root doesn't move
        pose_dict[self.back.id] = Transform(pos=[0,1,0]) # back is lifted up
        pose_dict[self.leftarm.id] = identity # left arm doesn't move
        pose_dict[self.rightarm.id] = Transform(pos=[-3,-1,0]) # right arm extends and moves down
        pose_dict[self.lefthand.id] = Transform(pos=[2,0,0]) # left hand extends

        self.root.forward_kinematics(current_pose_dict=pose_dict)

        self.assertEqual(self.root.model_transform, identity)
        self.assertEqual(self.back.model_transform, Transform(pos=[0,4,0]))        
        with self.assertWarnsRegex(UserWarning, "Transform built with non unit quaternion."):
            leftarm_t = Transform(pos=[2,4,0], orient=self.leftarm_q)
        leftarm_t.normalize_quaternion()
        self.assertEqual(self.leftarm.model_transform, leftarm_t)
        self.assertEqual(self.rightarm.model_transform, Transform(pos=[-5,3,0]))
        with self.assertWarnsRegex(UserWarning, "Transform built with non unit quaternion."):
            lefthand_t = Transform(pos=[2,4,3], orient=self.leftarm_q)
        lefthand_t.normalize_quaternion()
        self.assertEqual(self.lefthand.model_transform, lefthand_t)

    def test_joint_fk_with_pose_dict_and_static_root_rotated(self):    
        # rotate root
        self.root.local_bind_transform = Transform(orient=quaternion.y) # 180° rotation around the y-axis (quaternion.y == np.quaternion(0, 0, 1, 0))

        pose_dict = {}
        pose_dict[self.root.id] = self.root.local_bind_transform # root doesn't move
        pose_dict[self.back.id] = Transform(pos=[0,1,0]) # back is lifted up  
        pose_dict[self.leftarm.id] = Transform(orient=np.quaternion(np.sqrt(2)/2, 0, 0, np.sqrt(2)/2)) # left arm rotates up (left handed 90° rotation around the pre rotation x-axis which is now the z-axis)
        pose_dict[self.rightarm.id] = identity # right arm doesn't move
        pose_dict[self.lefthand.id] = Transform(pos=[-0.5,0,0]) # left hand shrinks

        self.root.forward_kinematics(current_pose_dict=pose_dict)

        self.assertEqual(self.root.model_transform, Transform(orient=quaternion.y))
        self.assertEqual(self.back.model_transform, Transform(pos=[0,4,0], orient=quaternion.y))        
        with self.assertWarnsRegex(UserWarning, "Transform built with non unit quaternion."):
            leftarm_t = Transform(pos=[-2,4,0], orient=np.quaternion(1, 1, 1, 1))
        leftarm_t.normalize_quaternion()
        self.assertEqual(self.leftarm.model_transform, leftarm_t)
        self.assertEqual(self.rightarm.model_transform, Transform(pos=[2,4,0], orient=quaternion.y))        
        with self.assertWarnsRegex(UserWarning, "Transform built with non unit quaternion."):       
            lefthand_t = Transform(pos=[-2,4.5,0], orient=np.quaternion(1, 1, 1, 1))
        lefthand_t.normalize_quaternion()
        self.assertEqual(self.lefthand.model_transform, lefthand_t)
    
    def test_joint_fk_with_pose_dict_and_animated_root(self):
        # place root at identity
        self.root.local_bind_transform = identity

        new_q = np.quaternion(1, 0, 1+np.sqrt(2), 0).normalized() # right handed 135° rotation around the y-axis

        pose_dict = {}        
        pose_dict[self.root.id] = Transform(pos=[0,0,1], orient=new_q) # root moves "towards us" and rotates along the y-axis
        pose_dict[self.back.id] = Transform(pos=[0,1,0]) # back is lifted up
        pose_dict[self.leftarm.id] = identity # left arm rotates up (left handed 90° rotation around the pre rotation x-axis which is now the z-axis)
        pose_dict[self.rightarm.id] = Transform(pos=[-3,0,0]) # right arm extends
        pose_dict[self.lefthand.id] = identity # left hand shrinks

        self.root.forward_kinematics(current_pose_dict=pose_dict)
        
        
        self.assertEqual(self.root.model_transform, Transform(pos=[0,0,1], orient=new_q))
        self.assertEqual(self.back.model_transform, Transform(pos=[0,4,1], orient=new_q))
        self.assertEqual(
            self.leftarm.model_transform,
            Transform(
                pos=[-np.sqrt(2), 4, -np.sqrt(2) + 1],
                orient=np.quaternion(1+np.sqrt(2), 0, 1, 0).normalized()
            )
        )
        self.assertEqual(self.rightarm.model_transform, Transform(pos=[5*np.sqrt(2)/2, 4, 5*np.sqrt(2)/2 + 1], orient=new_q))            
        self.assertEqual(
            self.lefthand.model_transform,
            Transform(
                pos=[-np.sqrt(2)/2, 4, -3*np.sqrt(2)/2 + 1],
                orient=np.quaternion(1+np.sqrt(2), 0, 1, 0).normalized()
            )
        )



    


    
