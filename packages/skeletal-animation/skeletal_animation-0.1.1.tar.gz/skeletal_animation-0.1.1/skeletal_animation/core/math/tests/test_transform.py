import unittest
import numpy as np
import quaternion

from skeletal_animation.core.math.transform import Transform, identity
from skeletal_animation.core.math.constants import HIGH_R_TOL, HIGH_A_TOL

class TestTransformDefaultConstructor(unittest.TestCase):
    def setUp(self):
        self.t1 = identity
        self.t2 = Transform([1,2,3], np.quaternion(2/3, 0, 2/3, 1/3)) # arbitrary values
        self.m2 = np.array([[-1/9, -4/9, 8/9, 1], # expected values for self.t2 as a matrix
                            [4/9, 7/9, 4/9, 2],
                            [-8/9, 4/9, 1/9, 3],
                            [0, 0, 0, 1]])

    def test_default_constructor_with_default_params(self):        
        self.assertTrue(np.array_equal(self.t1.pos, np.array([0,0,0])))
        self.assertEqual(self.t1.orient, quaternion.one)
        self.assertTrue(np.allclose(self.t1.as_matrix(), np.eye(4), rtol=HIGH_R_TOL, atol=HIGH_A_TOL))
    
    def test_default_constructor_with_unit_quaternion(self):
        self.assertTrue(np.array_equal(self.t2.pos, np.array([1,2,3])))
        self.assertEqual(self.t2.orient, np.quaternion(2/3, 0, 2/3, 1/3))
        self.assertTrue(np.allclose(self.t2.as_matrix(), self.m2, rtol=HIGH_R_TOL, atol=HIGH_A_TOL))
    
    def test_default_constructor_with_non_unit_quaternion(self):
        q = np.quaternion(1,2,3,4)

        with self.assertWarns(UserWarning):
            t = Transform([1,2,3], q)
        self.assertTrue(np.allclose(t.as_matrix()[0:3,0:3], quaternion.as_rotation_matrix(q), rtol=HIGH_R_TOL, atol=HIGH_A_TOL))

class TestTransformFromMatrixConstructor(unittest.TestCase):
    def setUp(self):
        self.t1 = identity
        self.t2 = Transform([1,2,3], np.quaternion(2/3, 0, 2/3, 1/3)) # arbitrary values
        self.m2 = np.array([[-1/9, -4/9, 8/9, 1], # expected values for self.t2 as a matrix
                            [4/9, 7/9, 4/9, 2],
                            [-8/9, 4/9, 1/9, 3],
                            [0, 0, 0, 1]])

    def test_from_identity_matrix(self):
        t = Transform.from_matrix(np.eye(4))
        self.assertEqual(self.t1, t)

    def test_from_matrix(self):
        t = Transform.from_matrix(self.m2)
        self.assertEqual(self.t2, t)
    
class TestTransformAsMatrix(unittest.TestCase):
    def setUp(self):
        self.t1 = identity
        self.t2 = Transform([1,2,3], np.quaternion(2/3, 0, 2/3, 1/3)) # arbitrary values
        self.m2 = np.array([[-1/9, -4/9, 8/9, 1], # expected values for self.t2 as a matrix
                            [4/9, 7/9, 4/9, 2],
                            [-8/9, 4/9, 1/9, 3],
                            [0, 0, 0, 1]])

    def test_as_identity_matrix(self):
        np.allclose(self.t1.as_matrix(), np.eye(4), rtol=HIGH_R_TOL, atol=HIGH_A_TOL)

    def test_as_matrix(self):
        np.allclose(self.t2.as_matrix(), self.m2, rtol=HIGH_R_TOL, atol=HIGH_A_TOL)

class TestTransformNormalizeQuaternion(unittest.TestCase):
    def test_normalize_quaternion(self):
        with self.assertWarnsRegex(UserWarning, "Transform built with non unit quaternion."):
            self.t2 = Transform(orient=np.quaternion(1, 1, 0, 0)) # arbitrary values, non unit quaternion
        self.t2.normalize_quaternion()
        self.assertTrue(np.allclose(quaternion.as_float_array(self.t2.orient), [np.sqrt(2)/2, np.sqrt(2)/2, 0, 0]))


class TestTransformMultiplyBy(unittest.TestCase):
    def setUp(self):
        self.t1 = identity
        self.t2 = Transform([1,2,3], np.quaternion(2/3, 0, 2/3, 1/3)) # arbitrary values
        self.m2 = np.array([[-1/9, -4/9, 8/9, 1], # expected values for self.t2 as a matrix
                            [4/9, 7/9, 4/9, 2],
                            [-8/9, 4/9, 1/9, 3],
                            [0, 0, 0, 1]])

        self.p = [0,2,1]  # arbitrary values,
        self.q = np.quaternion(2/3, 0, 2/3, 1/3) # arbitrary values,

        self.t4 = Transform(pos=self.p)
        self.t5 = Transform(orient=self.q)
        self.t6 = Transform(self.p,self.q)

    def test_multiply_by_identity(self):
        self.assertTrue(np.allclose(self.t2.multiply_by(self.t1).as_matrix(), self.t2.as_matrix(), rtol=HIGH_R_TOL, atol=HIGH_A_TOL))
    
    def test_multiply_by_non_unit(self):

        with self.assertWarnsRegex(UserWarning, "Transform built with non unit quaternion."):
            t3 = Transform([-3, 0.5, -0.02], np.quaternion(-1/2, -5/16, -1/16, 1/8)) # arbitrary values, non unit quaternion

        """
        t3.as_matrix():
        [[ 0.89361702  0.44680851 -0.04255319  -3        ]
        [-0.23404255  0.38297872 -0.89361702  0.5        ]
        [-0.38297872  0.80851064  0.44680851  -0.02       ]
        [0            0           0           1        ]]
        """

        tm = np.array([[-0.33569739776548, 0.49881796999947, 0.79905437221380, 1.0933333333333322],
                        [0.0449172611270, 0.855791959964, -0.51536642882118, 1.0466666666666812],
                        [-0.94089834220898, -0.1371158400067, -0.30969267222359, 5.8866666666666678],
                        [0, 0, 0, 1]]) # Result given by online calculator : https://matrix.reshish.com/fr/multCalculation.php
                                                                    # and confirmed by WolframAlpha : https://www.wolframalpha.com/

        with self.assertWarnsRegex(UserWarning, "Transform multiplication attempted with non unit quaternions."):
            self.assertTrue(np.allclose((self.t2.multiply_by(t3)).as_matrix(), tm, rtol=HIGH_R_TOL, atol=HIGH_A_TOL))
    
    def test_multiply_combine_translation_and_rotation(self):
        self.assertEqual(self.t5.multiply_by(self.t4), self.t6)
    
    def test_multiply_by_translation(self):
        self.assertEqual(self.t6, self.t5.translate(self.p))

    def test_multiply_by_rotation(self):        
        self.assertEqual(self.t6, self.t4.rotate_quaternion(self.q))
        
"""
Data formated for easy import into online calculator https://matrix.reshish.com/fr/multCalculation.php:

-0.11111111111111 -0.44444444444444 0.88888888888889 1
0.44444444444444 0.77777777777778 0.44444444444444 2
-0.88888888888889 0.44444444444444 0.11111111111111 3
0 0 0 1

-0.111111	0.4444444	-0.8888883	-1.666666
-0.444444	0.7777777	0.4444444	-3.333333
0.8888888	0.4444444	0.1111111	-0.3333333
0 0 0 1
"""

class TestTransformLerp(unittest.TestCase):
    def setUp(self):
        self.t1 = identity
        self.p = [1,2,3] # arbitrary values
        self.q = np.quaternion(2/3, 0, 2/3, 1/3) # arbitrary values
    
    def test_lerp_pos(self):
        t2 = Transform(pos=self.p)
        t = Transform.lerp(self.t1, t2, 0.25) # arbitrary time
        self.assertTrue(np.allclose(t.pos, [0.25, 0.5, 0.75], rtol=HIGH_R_TOL, atol=HIGH_A_TOL))
    
    def test_lerp_orient(self):
        t2 = Transform(orient=self.q)
        t = Transform.lerp(self.t1, t2, 0.25) # arbitrary time
        self.assertTrue(np.allclose(quaternion.as_float_array(t.orient), [0.9779751860797075, 0, 0.1866859082252575, 0.09334295411262875], rtol=HIGH_R_TOL, atol=HIGH_A_TOL))
