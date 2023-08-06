# Low tolerance are used for comparison that require high precision.
# e.g. verifying that a transform is exactly equal to another transform.

LOW_R_TOL = 1e-10 # Low relative tolerance for high-precision floating point comparisons
LOW_A_TOL  = 1e-14 # Low absolute tolerance for high-precision floating point comparisons

# High tolerance are used for comparisons that do not require high precision.
# e.g. verifying that a test result for transform multiplication is close to
# its expected result given by an external tool.

HIGH_R_TOL = 1e-5 # High relative tolerance for low-precision floating point comparisons
HIGH_A_TOL = 1e-7 # High absolute tolerance for low-precision floating point comparisons

# Very high tolerance are used for comparisons that require low precision.
# e.g. verifying that a key exist at a given time before adding a new one.
# If a user wants to add a key at time 0.10000 and a key exist at time 0.10001,
# the user should be prevented from adding the key. The keys are so close that
# a human would not be able to tell the difference in the animation. Therefore,
# adding the key would be irrelevent.

VERY_HIGH_R_TOL = 1e-3 # Very high relative tolerance for very low-precision floating point comparisons
VERY_HIGH_A_TOL = 1e-4 # Very high absolute tolerance for very low-precision floating point comparisons