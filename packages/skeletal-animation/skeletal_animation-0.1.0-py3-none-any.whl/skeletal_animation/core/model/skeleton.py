
class Skeleton:
    """A class to represent a skeleton (or rig).

    Attributes
    ----------
    name : str
        Name given to the skeleton. Not necessarily unique.
    root : Joint
        Root joint of the hierarchy for the skeleton.    
    """

    def __init__(self, root, name="new skeleton"):
        """**Default constructor for the Skeleton class.**
        
        Parameters
        ----------
        root : Joint
            Root joint of the hierarchy for the skeleton.
        name : str, optional
            Name of the skeleton, by default "new skeleton".        
        """
        self.name = name
        self.root = root
    
    
    def as_joint_list(self):
        """Returns the skeleton as a list of joints.

        Note
        ----
        The list is in depth-first order starting from the root.
        
        Returns
        -------
        (Joint) list
            List of joints in the skeleton.
        """
        adjacency_list = []

        plus_count = 1

        print("Hips")

        # Depth-first search
        def dfs(joint, plus_count):
            adjacency_list.append(joint)
            for child in joint.children:
                for i in range(plus_count):
                    print("+", end="")
                print((child.name).split(":")[-1])
                plus_count += 1
                dfs(child, plus_count)

        dfs(self.root, plus_count)
        return adjacency_list
    
    
    def get_joint_by_id(self, id):
        """Returns the joint with the given id.
        
        Parameters
        ----------
        id : int
            Id of the joint to return.
        
        Returns
        -------
        Joint
            Joint with the given id. None if not found.
        """
        for joint in self.as_joint_list():
            if joint.id == id:
                return joint
        return None

    
    def compute_bind_pose(self):
        """Computes the initial model transform (i.e. model bind transform) for each joint in the skeleton's joint hierarchy.
        """
        self.root.forward_kinematics(None)

    def compute_pose(self, pose_dict):
        """Computes the model transform for each joint in the skeleton's joint hierarchy.
        
        Parameters
        ----------
        pose_dict : Dict[int, Transform]
            Dictionary with joint id as keys and their respective transform as values.
            Dictionary containing the local transforms to be applied to each joint in the skeleton for it 
            to be in the current pose. It is obtained from the animation data stored in curves. 
            See generate_pose() method in the Animator class.
        """
        self.root.forward_kinematics(pose_dict)
    
    def __repr__(self):
        s = "Name: " + self.name + "\nJoints:\n(root)\n"
        s += ",\n".join(joint.__repr__() for joint in self.as_joint_list())        
        return s
