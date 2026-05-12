# mouse_mover.py — Pixel-error → raw mouse counts (win32api, Windows only)
import math
from typing import Tuple

import win32api
import win32con

from config import AIM_SPEED, COUNTS_PER_360, GAME_FOV, PIXEL_DEADZONE


def move_mouse_relative(dx: int, dy: int) -> None:
    """Send a relative mouse movement of (dx, dy) raw counts."""
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(dx), int(dy), 0, 0)


def compute_mouse_delta(
    pixel_dx: float,
    pixel_dy: float,
    screen_width: int,
    screen_height: int,
) -> Tuple[int, int]:
    """
    Convert a pixel offset (screen-centre → target) into raw mouse counts.

    Uses perspective-correct conversion::

        focal_length = screen_width / (2 · tan(FOV/2))
        angle        = atan2(pixel_offset, focal_length)

    This prevents overshoot for targets near screen edges compared to a
    naive linear mapping.

    Parameters
    ----------
    pixel_dx, pixel_dy : float
        Pixel offset from centre.  +right / +down.
    screen_width, screen_height : int
        Capture resolution.

    Returns
    -------
    (mouse_dx, mouse_dy) : (int, int)
        Raw counts for ``win32api.mouse_event``.
    """
    # ── Dead-zone filter ──
    if abs(pixel_dx) < PIXEL_DEADZONE:
        pixel_dx = 0
    if abs(pixel_dy) < PIXEL_DEADZONE:
        pixel_dy = 0

    if pixel_dx == 0 and pixel_dy == 0:
        return 0, 0

    # ── Perspective-correct: pixels → angle (degrees) ──
    focal = screen_width / (2.0 * math.tan(math.radians(GAME_FOV / 2.0)))
    angle_x = math.degrees(math.atan2(pixel_dx, focal))
    angle_y = math.degrees(math.atan2(pixel_dy, focal))

    # ── Angle → raw mouse counts ──
    mouse_dx = angle_x / 360.0 * COUNTS_PER_360 * AIM_SPEED
    mouse_dy = angle_y / 360.0 * COUNTS_PER_360 * AIM_SPEED

    return int(round(mouse_dx)), int(round(mouse_dy))
