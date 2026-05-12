# distance.py — Geometric helpers (screen-centre, distance, angle)
import math
from typing import Tuple


def get_center(w: int, h: int) -> Tuple[int, int]:
    """Return the pixel-centre (cx, cy) of a frame."""
    return w // 2, h // 2


def calculate_distance_and_angle(
    box: Tuple[float, float, float, float],
    frame_w: int,
    frame_h: int,
) -> Tuple[float, float, Tuple[float, float]]:
    """
    Compute distance and compass-angle from screen centre to a bbox centre.

    Parameters
    ----------
    box : (x1, y1, x2, y2)
    frame_w, frame_h : capture dimensions

    Returns
    -------
    (distance_px, angle_deg, (obj_cx, obj_cy))
        angle: 0° = up, 90° = right, 180° = down, 270° = left.
    """
    x1, y1, x2, y2 = box
    obj_cx = (x1 + x2) / 2
    obj_cy = (y1 + y2) / 2

    cx, cy = get_center(frame_w, frame_h)
    dx = obj_cx - cx
    dy = cy - obj_cy   # positive = up

    dist  = math.hypot(dx, dy)
    angle = math.degrees(math.atan2(dx, dy))
    if angle < 0:
        angle += 360

    return dist, angle, (obj_cx, obj_cy)
