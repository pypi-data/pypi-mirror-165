import warnings
import numpy as np
import pickle

from skeletal_animation.core.math import *
from skeletal_animation.core.model import *
from skeletal_animation.core.animate import *


def serialize(animator, file_name, path):
    """Serialize the current animator to a file using pickle.

    Animator object is saved as a pickle file (.pkl).

    Parameters:
    -----------
    animator : Animator
        The animator to serialize
    file_name : str
        The name of the file to save. Extension .pkl is added automatically.
    path : str
        The path to where the file will be saved.
    """
    with open(path + file_name + ".pkl", 'wb') as f:
        pickle.dump(animator, f)


def load_serialized(file_name, path):
    """Load a serialized animator from a file using pickle.

    Animator object is loaded from a pickle file (.pkl).

    Parameters:
    -----------
    file_name : str
        The name of the file to load. Extension .pkl is added automatically.
    path : str
        The path to the file to load.

    Returns:
    --------
    animator : Animator
        The loaded Animator object.

    Raises:
    -------
    FileNotFoundError
        If the file cannot be found.
    """
    try:
        with open(path + file_name + ".pkl", 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("File not found: " + path + file_name + ".pkl")


def load_fbx(fbx_file_path):
    """Creates an Animator object from a fbx file.

    This method requires the installation of the fbx sdk for python.
    The fbx sdk is available at: https://www.autodesk.com/developer-network/platform-technologies/fbx-sdk-2020-2-1.

    Parameters:
    -----------
    fbx_file_path : str
        The path to the fbx file to load.

    Raises:
    -------
    ImportError
        If the FBX SDK is not installed.

    Returns:
    --------
    animator : Animator
        The generated Animator object.

    Warnings
    --------
    This loader does not support all fbx files.
    Fbx files must follow the following criteria:
    - Animation data contains only one animation stack with only one animation layer.
    - If a key contains a value for one axis, the values for all other axes must be specified.
    Fbx files exported from Mixamo follow these criteria.
    """
    # check if the fbx sdk is installed 
    try:
        import fbx
    except ImportError:
        warnings.warn("The FBX SDK is not installed.\
            To load animation files from fbx, the FBX SDK must be installed.\
            see https://www.autodesk.com/developer-network/platform-technologies/fbx-sdk-2020-0",
            stacklevel=2)

    sdk_manager = fbx.FbxManager.Create()

    ios = fbx.FbxIOSettings.Create(sdk_manager, fbx.IOSROOT)
    sdk_manager.SetIOSettings(ios)

    importer = fbx.FbxImporter.Create(sdk_manager, '')

    if not importer.Initialize(fbx_file_path, -1, sdk_manager.GetIOSettings()):
        print("Call to FbxImporter::Initialize() failed.")
        raise ImportError("Error importing file %s file not found or %s" % (
            fbx_file_path, importer.GetStatus().GetErrorString(),
            ))

    scene = fbx.FbxScene.Create(sdk_manager, "myScene")
    importer.Import(scene)
    importer.Destroy()

    # _____________LOADING FBX HIERARCHY_____________
    def load_skeleton_nodes(skeleton_node_list, root_node):
        for i in range(root_node.GetChildCount()):
            child_node = root_node.GetChild(i)
            for i in range(child_node.GetNodeAttributeCount()):
                attribute = child_node.GetNodeAttributeByIndex(i)
                if type(attribute) == fbx.FbxSkeleton:
                    skeleton_node_list.append(child_node)
            load_skeleton_nodes(skeleton_node_list, child_node)

    def get_anim_layer():
        nb_anim_stack = scene.GetSrcObjectCount(
            fbx.FbxCriteria.ObjectType(fbx.FbxAnimStack.ClassId)
            )

        if nb_anim_stack == 0:
            raise ValueError("No animation stack found in fbx file.")
        elif nb_anim_stack > 1:
            warnings.warn("Multiple anim stacks found in fbx file, only the first one is treated", stacklevel=2)

        anim_stack = scene.GetSrcObject(
            fbx.FbxCriteria.ObjectType(fbx.FbxAnimStack.ClassId)
            , 0)

        nb_anim_layers = anim_stack.GetSrcObjectCount(
            fbx.FbxCriteria.ObjectType(fbx.FbxAnimLayer.ClassId)
            )

        if nb_anim_layers == 0:
            raise ValueError("No animation layer found in anim stack.")
        elif nb_anim_layers > 1:
            warnings.warn("Multiple anim layers found in anim stack, only the first one is treated", stacklevel=2)

        anim_layer = anim_stack.GetSrcObject(
            fbx.FbxCriteria.ObjectType(fbx.FbxAnimLayer.ClassId)
            , 0)

        return anim_layer

    def load_curves(skeleton_node, anim_layer):
        # Assumes that when a change to the position/orientation of a joint is made,
        # the translation/rotation values for each axis are given in the keyframe.

        tX_curve = skeleton_node.LclTranslation.GetCurve(anim_layer, "X")
        tY_curve = skeleton_node.LclTranslation.GetCurve(anim_layer, "Y")
        tZ_curve = skeleton_node.LclTranslation.GetCurve(anim_layer, "Z")
        rX_curve = skeleton_node.LclRotation.GetCurve(anim_layer, "X")
        rY_curve = skeleton_node.LclRotation.GetCurve(anim_layer, "Y")
        rZ_curve = skeleton_node.LclRotation.GetCurve(anim_layer, "Z")

        translation_keys = []
        rotation_keys = []

        duration = 1.0

        if tX_curve is not None and tY_curve is not None and tZ_curve is not None:
            for key_id in range(tX_curve.KeyGetCount()):
                key_time = tX_curve.KeyGetTime(key_id).GetTimeString("")

                t = [tX_curve.KeyGetValue(key_id), tY_curve.KeyGetValue(key_id), tZ_curve.KeyGetValue(key_id)]

                if "*" in key_time:
                    # Keys whose time is marked with "*" are not used in the animation.
                    # They are probably used to improve interpolation quality in between keyframes.         
                    pass
                else:
                    key_time = float(key_time)
                    if key_time > duration:
                        duration = key_time

                    translation_keys.append(Key(key_time, t))

        if rX_curve is not None and rY_curve is not None and rZ_curve is not None:
            for key_id in range(rX_curve.KeyGetCount()):
                key_time = rX_curve.KeyGetTime(key_id).GetTimeString("")

                v = fbx.FbxVector4(rX_curve.KeyGetValue(key_id), rY_curve.KeyGetValue(key_id), rZ_curve.KeyGetValue(key_id))

                m = fbx.FbxAMatrix()
                m.SetR(v)
                q = m.GetQ()
                q = np.quaternion(q.GetAt(3), q.GetAt(0), q.GetAt(1), q.GetAt(2))

                if "*" in key_time:
                    # Keys whose time is marked with "*" are not used in the animation.
                    # They are probably used to improve interpolation quality in between keyframes.
                    pass
                else:
                    key_time = float(key_time)
                    if key_time > duration:
                        duration = key_time

                    rotation_keys.append(Key(key_time, q))

        for key in translation_keys:
            key.time /= duration
        for key in rotation_keys:
            key.time /= duration

        translation_curve = Curve(translation_keys)
        rotation_curve = Curve(rotation_keys)
        return translation_curve, rotation_curve, duration

    # Assumes that the animation data contains only one animation stack with only one animation layer.
    # Mixamo rigged animations have this structure.
    # Assumes the duration of the animation for each joint is the same.

    root_node = scene.GetRootNode()
    skeleton_node_list = []

    load_skeleton_nodes(skeleton_node_list, root_node)

    skeleton_root = None
    root_set = False

    anim_layer = get_anim_layer()
    joint_animations = []

    joint_hierarchy = []

    anim_duration = 1.0

    for skeleton_node in skeleton_node_list:
        # Creating joints
        joint_name = skeleton_node.GetName()

        pos = [float(val) for val in skeleton_node.LclTranslation.Get()]

        rotation = skeleton_node.PreRotation.Get()

        v = fbx.FbxVector4(rotation)

        m = fbx.FbxAMatrix()
        m.SetR(v)
        q = m.GetQ()        
        orient = np.quaternion(q.GetAt(3), q.GetAt(0), q.GetAt(1), q.GetAt(2))

        joint = Joint(name=joint_name, local_bind_transform=Transform(pos, orient))

        children = []
        for i in range(skeleton_node.GetChildCount()):
            child_node = skeleton_node.GetChild(i)
            children.append(child_node.GetName())

        joint_hierarchy.append((joint, children))

        if not root_set:
            skeleton_root = joint
            root_set = True

        # Creating joint animations
        if anim_layer:
            translation_curve, rotation_curve, duration = load_curves(skeleton_node, anim_layer)
            if duration > anim_duration:
                anim_duration = duration
            joint_animation = JointAnimation(joint, translation_curve, rotation_curve)
            joint_animations.append(joint_animation)

    # Building joint hierarchy
    joint_list = [relation[0] for relation in joint_hierarchy]

    for relation in joint_hierarchy:
        children = [joint for joint in joint_list if joint.name in relation[1]]
        relation[0].add_children(children)

    # Creating skeleton
    skeleton = Skeleton(skeleton_root)

    # Creating animation
    animation = Animation(joint_animations, anim_duration)

    animator = Animator(animation=animation, skeleton=skeleton)

    return animator
