# mouse_mover.py - Virtual mouse movement with DPI / sensitivity scaling
#                  Windows only (win32api).
import math
import win32api
import win32con

from config import COUNTS_PER_360, AIM_SPEED, PIXEL_DEADZONE, GAME_FOV


def move_mouse_relative(dx, dy):
    """Move the cursor by (dx, dy) raw mouse counts."""
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(dx), int(dy), 0, 0)


def compute_mouse_delta(pixel_dx, pixel_dy, screen_width, screen_height):
    """
    Convert a pixel offset (from screen centre to target) into raw mouse
    counts that produce the equivalent in-game rotation.

    Uses perspective-correct angle calculation:
        focal_length = screen_width / (2 * tan(HFOV / 2))
        angle        = atan2(pixel_offset, focal_length)
    This avoids overshoot for targets near the screen edges compared to a
    naive linear mapping.

    Parameters
    ----------
    pixel_dx, pixel_dy : float
        Pixel offset from screen centre to target.  +right / +down.
    screen_width, screen_height : int
        Capture resolution in pixels.

    Returns
    -------
    (mouse_dx, mouse_dy) : tuple[int, int]
        Raw counts to feed into win32api.mouse_event.
    """
    # Dead-zone filter
    if abs(pixel_dx) < PIXEL_DEADZONE:
        pixel_dx = 0
    if abs(pixel_dy) < PIXEL_DEADZONE:
        pixel_dy = 0

    if pixel_dx == 0 and pixel_dy == 0:
        return 0, 0

    # Perspective-correct: pixel offset -> angle in degrees
    focal_len = screen_width / (2.0 * math.tan(math.radians(GAME_FOV / 2.0)))

    angle_x_deg = math.degrees(math.atan2(pixel_dx, focal_len))
    angle_y_deg = math.degrees(math.atan2(pixel_dy, focal_len))

    # Angle -> raw mouse counts
    mouse_dx = angle_x_deg / 360.0 * COUNTS_PER_360
    mouse_dy = angle_y_deg / 360.0 * COUNTS_PER_360

    # Smoothing (lerp factor)
    mouse_dx *= AIM_SPEED
    mouse_dy *= AIM_SPEED

    return int(round(mouse_dx)), int(round(mouse_dy))
