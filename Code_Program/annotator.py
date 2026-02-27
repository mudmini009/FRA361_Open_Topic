#annotate_and_collect
# annotator.py
import cv2
import math
from distance import get_center
from config import CENTER_BOX_SIZE, CHEST_Y_FACTOR

def annotate_and_collect(frame, boxes, mode, logger):
    """
    Draw aim-box + marker/line, compute dx, dy, on_target,
    log them (dx,dy,mode), and return (dx,dy,on_target), annotated frame.
    """
    frame = frame.copy()
    h, w = frame.shape[:2]
    cx, cy = get_center(w, h)
    half = CENTER_BOX_SIZE // 2
    left, top   = cx - half, cy - half
    right, bottom = cx + half, cy + half

    # draw central “aim” box
    cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)

    dx, dy, on_target = 0.0, 0.0, 0
    if boxes.size:
        # pick closest box
        best = min(
            ((math.hypot((b[0]+b[2])/2 - cx, (b[1]+b[3])/2 - cy), b)
             for b in boxes),
            key=lambda x: x[0]
        )[1]
        x1, y1, x2, y2 = best[:4]

        # chest point
        tx = (x1 + x2) / 2
        ty = y1 + (y2 - y1) * CHEST_Y_FACTOR

        # pixel error: +right, +up
        dx = tx - cx
        dy = cy - ty

        # on_target if overlapping
        if not (x2 < left or x1 > right or y2 < top or y1 > bottom):
            on_target = 1

        # draw marker + line
        cv2.circle(frame, (int(tx), int(ty)), 5, (0,0,255), -1)
        cv2.line(frame, (cx, cy), (int(tx), int(ty)), (255,0,0), 2)

    # log dx, dy, mode
    logger.log(round(dx,1), round(dy,1), mode)

    # overlay
    cv2.putText(frame, f"Mode: {mode}",         (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)
    cv2.putText(frame, f"dx: {dx:.1f}px",       (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    cv2.putText(frame, f"dy: {dy:.1f}px",       (10,110),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    cv2.putText(frame, f"OnT: {on_target}",      (10,150),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

    return (dx, dy, on_target), frame
