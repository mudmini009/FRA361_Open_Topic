#annotate_and_collect
# annotator.py
import cv2
import math
from distance import get_center
from config import CENTER_BOX_SIZE, CHEST_Y_FACTOR

def annotate_and_collect(frame, boxes, mode, log):
    """
    Draw central aim-box, pick nearest target by bbox-center,
    recompute to chest-point, draw line+marker, detect overlap,
    then append [dist,ang,on_target,mode] to log.
    """
    frame = frame.copy()
    h, w = frame.shape[:2]
    cx, cy = get_center(w, h)
    half = CENTER_BOX_SIZE // 2
    left, top = cx - half, cy - half
    right, bottom = cx + half, cy + half

    # draw central “aim” box
    cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)

    dist, ang, on_target = 0.0, 0.0, 0
    if boxes.size:
        # pick closest by bbox center
        best = min(
            ((math.hypot((b[0]+b[2])/2 - cx, (b[1]+b[3])/2 - cy), b) 
             for b in boxes),
            key=lambda x: x[0]
        )[1]
        x1,y1,x2,y2 = best[:4]

        # chest‐point
        tx = (x1 + x2) / 2
        ty = y1 + (y2 - y1) * CHEST_Y_FACTOR

        # recompute distance & angle
        dx, dy = tx - cx, cy - ty
        dist = math.hypot(dx, dy)
        ang  = math.degrees(math.atan2(dx, dy)) % 360

        # draw marker & line
        cv2.circle(frame, (int(tx), int(ty)), 5, (0,0,255), -1)
        cv2.line(frame, (cx, cy), (int(tx), int(ty)), (255,0,0), 2)

        # on_target if bbox overlaps central box
        if not (x2 < left or x1 > right or y2 < top or y1 > bottom):
            on_target = 1

    log.append([round(dist,1), round(ang,1), on_target, mode])

    # overlay stats
    cv2.putText(frame, f"Mode: {mode}",         (10,  30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)
    cv2.putText(frame, f"Dist: {dist:.1f}px",   (10,  70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    cv2.putText(frame, f"Ang: {ang:.1f}°",      (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    cv2.putText(frame, f"OnTarget: {on_target}",(10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

    return frame


