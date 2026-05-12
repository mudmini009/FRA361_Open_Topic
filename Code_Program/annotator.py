# annotator.py - Draw aim overlay + OSD with hotkey reference
import cv2
import math
from distance import get_center
from config   import CENTER_BOX_SIZE, CHEST_Y_FACTOR
from control  import MODE_NAMES, is_paused


def annotate_and_collect(frame, boxes, mode, logger):
    """
    Draw aim-box, target marker/line, compute (dx, dy, on_target),
    log them, render the OSD, and return ((dx, dy, on_target), frame).
    """
    frame = frame.copy()
    h, w = frame.shape[:2]
    cx, cy = get_center(w, h)
    half = CENTER_BOX_SIZE // 2
    left, top     = cx - half, cy - half
    right, bottom = cx + half, cy + half

    # Central aim box
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    dx, dy, on_target = 0.0, 0.0, 0

    if boxes.size:
        # Pick the bounding box closest to screen centre
        best = min(
            ((math.hypot((b[0]+b[2])/2 - cx, (b[1]+b[3])/2 - cy), b)
             for b in boxes),
            key=lambda x: x[0]
        )[1]
        x1, y1, x2, y2 = best[:4]

        # Chest point (aim slightly below head)
        tx = (x1 + x2) / 2
        ty = y1 + (y2 - y1) * CHEST_Y_FACTOR

        # Pixel error: +right, +up
        dx = tx - cx
        dy = cy - ty

        # On-target if bounding box overlaps the aim box
        if not (x2 < left or x1 > right or y2 < top or y1 > bottom):
            on_target = 1

        # Draw marker + line
        cv2.circle(frame, (int(tx), int(ty)), 5, (0, 0, 255), -1)
        cv2.line(frame, (cx, cy), (int(tx), int(ty)), (255, 0, 0), 2)

    # Log dx, dy, mode
    logger.log(round(dx, 1), round(dy, 1), mode)

    # --- OSD: Mode + Status ---
    mode_name = MODE_NAMES.get(mode, "Unknown({})".format(mode))
    paused    = is_paused()

    # Mode label - green when active, red when idle/paused
    if paused:
        mode_color = (0, 0, 255)
        mode_text  = "MODE: {}  [PAUSED]".format(mode_name)
    else:
        mode_color = (0, 255, 0) if mode > 0 else (0, 100, 255)
        mode_text  = "MODE: {}".format(mode_name)

    cv2.putText(frame, mode_text, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, mode_color, 2)

    # Pixel error readout
    cv2.putText(frame, "dx: {:.1f}px  dy: {:.1f}px  OnTarget: {}".format(dx, dy, on_target),
                (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    # --- Hotkey reference panel (bottom of frame) ---
    hotkey_lines = [
        "[F1] Idle   [F2] Track   [F3] Flick+Click",
        "[F9] Pause/Resume   [F10] Quit",
    ]
    y_start = h - 50
    for i, line in enumerate(hotkey_lines):
        cv2.putText(frame, line, (10, y_start + i * 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1)

    return (dx, dy, on_target), frame
