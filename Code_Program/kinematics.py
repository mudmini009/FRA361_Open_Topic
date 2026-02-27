# mecanum inverse-kinematics
# kinematics.py
def mecanum_inverse(vx, vy, omega=0.0):
    """
    Normalised inverse kinematics (no wheel-radius or geometry scaling).
    vx, vy: translational speeds  (forward+, right+)
    omega : rotation (counter-clockwise +)
    Returns tuple (FL, FR, BL, BR)  in arbitrary units.
    """
    fl = vy + vx + omega
    fr = vy - vx - omega
    bl = vy - vx + omega
    br = vy + vx - omega
    return fl, fr, bl, br

def normalise_to_percent(*speeds, limit=100.0):
    mx = max(abs(s) for s in speeds) or 1.0
    scale = min(1.0, limit / mx)
    return [int(s * scale) for s in speeds]
