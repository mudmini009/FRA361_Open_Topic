import math

def get_center(w: int, h: int):
    """Return the pixel‐center (cx,cy) of a frame."""
    return w // 2, h // 2

def calculate_distance_and_angle(box, frame_w: int, frame_h: int):
    """
    box = (x1,y1,x2,y2)
    returns (distance_px, angle_deg, (obj_cx,obj_cy))
    0°=up (12), 90°=right, 180°=down, 270°=left
    """
    x1,y1,x2,y2 = box
    ox = (x1+x2)/2
    oy = (y1+y2)/2

    cx, cy = get_center(frame_w, frame_h)
    dx = ox - cx
    dy = cy - oy   # invert y so positive=up

    dist = math.hypot(dx, dy)
    ang  = math.degrees(math.atan2(dx, dy))
    if ang < 0:
        ang += 360
    return dist, ang, (ox, oy)
