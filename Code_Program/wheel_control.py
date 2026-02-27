# converts pixel error → [FL,FR,BL,BR] %
# wheel_control.py
import time
from pid import PID
from kinematics import mecanum_inverse, normalise_to_percent
from config import (KP_X, KI_X, KD_X, KP_Y, KI_Y, KD_Y, 
                    MAX_WHEEL_PERCENT,
                    FL_DIR, FR_DIR, BL_DIR, BR_DIR)

pid_x = PID(KP_X, KI_X, KD_X)
pid_y = PID(KP_Y, KI_Y, KD_Y)
_last = time.time()

def pixel_error_to_wheels(dx_px, dy_px, mode):
    if mode == 0:
        return [0, 0, 0, 0]

    now = time.time()
    dt  = now - _last if (_last := now) else 1/60

    # --- Apply pixel deadzone ---
    if abs(dx_px) < 10:
        dx_px = 0
    if abs(dy_px) < 10:
        dy_px = 0
        
    # compute desired forward (vx) and strafe (vy)
    vx = pid_y.update(dy_px, dt)    # forward / backward
    vy = pid_x.update(dx_px, dt)    # strafe right+
    # vx = pid_y.update(-dy_px, dt)   # invert forward/back
    # vy = pid_x.update(-dx_px, dt)   # invert strafe

    # raw IK outputs
    fl, fr, bl, br = mecanum_inverse(vx, vy, 0.0)

    # normalize into -MAX…+MAX percent
    perc = normalise_to_percent(fl, fr, bl, br, limit=MAX_WHEEL_PERCENT)
    # apply wiring direction flips
    flp = FL_DIR * perc[0]
    frp = FR_DIR * perc[1]
    blp = BL_DIR * perc[2]
    brp = BR_DIR * perc[3]

    return [flp, frp, blp, brp]

