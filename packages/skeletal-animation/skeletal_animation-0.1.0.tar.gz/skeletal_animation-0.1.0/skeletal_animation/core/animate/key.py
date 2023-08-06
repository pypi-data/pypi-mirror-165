import numpy as np

from skeletal_animation.core.math.constants import LOW_A_TOL, LOW_R_TOL

class Key:
    """Class to represent a key in an animation curve.

    It is effectively a wrapper around a time and a value.
    The time is a float representing the time of the key.
    The value can be of any type, however this class is meant to be used in Curve objects.
    Curve objects have type restrictions on the values of the keys they contain.

    Attributes:
    ----------
    time : float
        The time of the key.
    value : any
        The value of the key at a given time.
    """

    def __init__(self, time, value):
        """**Default constructor for the Key class.**

        Parameters:
        ----------
        time : float
            The time of the key.
        value : any
            The values of the key at a given time.
        """
        if not isinstance(time, (float, np.float32, np.float64)):            
            raise ValueError("The time of the key must be a float.")

        self.time = time       
        self.value = value

    def get_type(self):
        """Returns the type of the key, which is the type of its value.

        Returns:
        ----------
        type
            The type of the value of the key.
        """
        return type(self.value)

    def __repr__(self):
        return f'Key(time={str(self.time)}, value={str(self.value)})'

    def __eq__(self, other):
        """Equality operator for Key objects.

        Note
        ----
        Equality for floating point values is defined as being within a tolerance.
        Tolerance values are defined in the constants.py file.        
        Lower tolerance values are used here for more accurate equality.

        Parameters:
        ----------
        other : Key
            Key object to compare to.

        Returns:
        ----------
        bool
            True if the time and values for both keys are "equal" to each other. False otherwise.
        """
        return (np.isclose(self.time, other.time, rtol=LOW_R_TOL, atol=LOW_A_TOL)
            and self.value == other.value)