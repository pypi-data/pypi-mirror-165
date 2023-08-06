import json
import copy
import warnings

from skeletal_animation.core.math import Transform, identity

class Joint:
    """A class to represent a joint.

    A joint is considered a root if it has no parent.
    
    Attributes
    ----------
    id : int
        Unique id of the joint.
    name : str
        Name given to the joint. Not necessarily unique.    
    parent : Joint
        Parent of the joint.
    children : (Joint) list
        List of children joints.
    local_bind_transform : Transform
        Initial transform of the joint in the parent's local coordinate system.
    model_transform : Transform
        Current transform of the joint in the model (or world) coordinate system.

    Static Attributes
    ------------------
    LAST_ID : int
        Auto incrementing ID for the next joint.
    """
    LAST_ID = 0

    
    def __init__(self, name="new joint", local_bind_transform=identity):
        """**Default constructor for the Joint class.**

        Parameters
        ----------
        name : str, optional
            Name of the joint, by default "new joint".
        local_bind_transform : Transform, optional
            Initial transform relative to the parent, by default identity transform.
        """
        self.id = Joint.LAST_ID
        Joint.LAST_ID += 1
        self.name = name
        self.parent = None   
        self.children = []
        self.local_bind_transform = local_bind_transform
        self.model_transform = None 
    
    
    def add_child(self, joint):
        """Makes the given joint a child of the current joint.

        Note
        ----
        The joint's parent is updated automatically.

        Parameters
        ----------
        joint : Joint
            The joint to be added as a child.

        Raises
        --------
        If the addition of the joint makes the tree cyclic, an error is raised.        
        """
        if joint.parent is None:
            joint.parent = self
            self.children.append(joint)
        elif joint.parent != self:
            old_parent = joint.parent
            old_parent.children.remove(joint)
            joint.parent = self
            self.children.append(joint)
        if self.is_cyclic():              
            warnings.warn("The addition of the joint makes the tree cyclic.", UserWarning)

       
    def add_children(self, joints):
        """Makes the given joints children of the current joint.

        Note
        ----
        The joints' parents are updated automatically.

        Parameters
        ----------
        joints : (Joint) list
            The joints to be added as children.
        """
        for joint in joints:
            self.add_child(joint)

    
    def remove_child(self, joint):
        """Removes the given joint from the children of the current joint.

        Note
        ----
        If the joint is not a child of the current joint, then nothing happens.
        The joint's parent is updated automatically.
        
        Parameters
        ----------
        joint : Joint
            The joint to be removed.
        """
        if joint in self.children:
            self.children.remove(joint)
            joint.parent = None

    
    def remove_children(self, joints):
        """Removes the given joints from the children of the current joint.

        Note
        ----
        The joints' parents are updated automatically.

        Parameters
        ----------
        joints : (Joint) list
            The joints to be removed.
        """
        for joint in joints:
            self.remove_child(joint)

    
    def remove_all_children(self):
        """Removes all the children of the current joint.

        Note
        ----
        The removed joints' parents are updated automatically.
        """
        self.remove_children(copy.copy(self.children))


    def forward_kinematics(self, current_pose_dict, parent_model_transform=identity):
        """Computes the model transform of the current joint and all its children recursively using forward kinematics.

        The formula used to compute the model transform of the current joint is:
        model_transform = parent_model_transform x local_bind_transform x local_anim_transform.

        This formula is valid for transform matrices in column-major order, as is the case in this module.

        Parameters
        ----------
        current_pose_dict : Dict[int, Transform]
            Dictionary with joint id as keys and their respective transform as values.
            Dictionary containing the local transforms to be applied to each joint in the skeleton for it 
            to be in the current pose, also known as the local animation transforms.
            It is obtained from the animation data stored in curves. 
            See generate_pose() method in the Animator class.
        parent_model_transform : Transform, optional
            Model transform of the parent joint, by default identity transform. 
            This parameter is optional only because the parent model transform for the root joint 
            does not exist. In that case, it is set to identity.
        """
        # If current_pose_dict is None (i.e. when compute_bind_pose() is called),
        # then the root's transform is its local bind transform
        # and the delta for other joints is null (identity transform).

        current_local_transform = Transform()

        if current_pose_dict == None:
            if self.parent is None: # root
                current_local_transform = self.local_bind_transform
            else:
                # current_local_transform = Transform()
                pass
        else:
            if self.id in current_pose_dict:
                current_local_transform = current_pose_dict[self.id]   

        # Assumes that the actual transform is given for the root joint
        # And that, for other joints, the delta transform is given instead.

        if self.parent is None: # root
            current_model_transform = current_local_transform
        else:
            current_model_transform = parent_model_transform @ self.local_bind_transform @ current_local_transform
        
        self.model_transform = current_model_transform  

        # Recursively compute the model transforms of the children
        for child_joint in self.children:
            child_joint.forward_kinematics(current_pose_dict, current_model_transform)        

    
    def is_cyclic(self):
        """Checks for cyclicity in the joint hierarchy for the current joint.

        Note: The joint hierarchy is considered cyclic only if a joint is the parent of one of its ancestors.

        Examples
        -------
        >>> root = Joint()
        >>> child1 = Joint()
        >>> child2 = Joint()
        >>> child3 = Joint()
        >>> root.add_children([child1, child2])
        >>> child1.add_child(child3)
        # The joint hierarchy is now:
        #   root -> child1 -> child3
        #        -> child2
        >>> root.is_cyclic()
        False
        >>> child3.add_child(child1)
        # The joint hierarchies are now:
        # root -> child2  and  ... -> child1 -> child3 -> child1 -> child3 -> child1 -> ...
        >>> root.is_cyclic()
        False
        >>> child1.is_cyclic()
        True
        
        Returns
        -------
        bool
            True if the joint hierarchy is cyclic, False otherwise.
        """

        # List of visited nodes.
        visited = []
        # Stack to keep track of the current node.
        stack = []
        stack.append(self)

        # Run till stack is empty or cycle is found.
        while stack:
            node = stack.pop()
            for child in node.children:
                if child in visited:
                    return True
                else:
                    stack.append(child)
                    visited.append(node)

        # If we reach here, then there is no cycle
        return False

    
    def __repr__(self):
        dict = {}
        dict["id"] = self.id
        dict["name"] = self.name
        if self.parent is None:
            dict["parent"] = None
        else:
            dict["parent"] = self.parent.name
        dict["children"] = [child.name for child in self.children]
        dict["local_bind_transform"] = self.local_bind_transform.__repr__()
        if self.model_transform is None:
            dict["model_transform"] = None
        else:
            dict["model_transform"] = self.model_transform.__repr__()
        return json.dumps(dict, indent=4)

    def __eq__(self, other):
        """Equality operator for joint objects.

        Note
        ----
        Two joints are considered equal if:
        - They are of the same type (i.e. have the same class)
        - They have the same id, name, parent and children
        - Their local bind transforms are equal. (See Transform.__eq__())

        Model transforms are not necessarily equal, since the model transform
        of a same joint changes over the course of the animation.

        Parameters
        ----------
        other : Joint
            Joint object to compare to.

        Returns
        -------
        bool
            True if the two joints are equal, False otherwise.
        """
        if type(self) != type(other):
            return False

        if self.id != other.id or self.name != other.name or self.local_bind_transform != other.local_bind_transform:
            return False

        self_p_id = None
        other_p_id = None
        if self.parent is not None:
            self_p_id = self.parent.id
        if other.parent is not None:
            other_p_id = other.parent.id
        if self_p_id != other_p_id:
            return False

        if self.children != other.children:
            return False

        return True
