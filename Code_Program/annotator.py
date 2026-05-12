# annotator.py — Aim overlay + on-screen display (OSD)
import math
from typing import Tuple

import cv2

from config  import CENTER_BOX_SIZE, CHEST_Y_FACTOR
from control import MODE_NAMES, is_paused
from distance import get_center


# ─── Colours (BGR) ────────────────────────────────────────
_GREEN  = (0, 255, 0)
_RED    = (0, 0, 255)
_BLUE   = (255, 0, 0)
_ORANGE = (0, 100, 255)
_WHITE  = (255, 255, 255)
_GREY   = (200, 200, 200)


# ─── OSD helpers ──────────────────────────────────────────

def _draw_osd(frame, h: int, mode: int, dx: float, dy: float, on_target: int) -> None:
    """Render mode label, pixel-error readout, and hotkey panel."""
    paused    = is_paused()
    mode_name = MODE_NAMES.get(mode, f"Unknown({mode})")

    # ── Top-left: mode + pause badge ──
    if paused:
        label = f"MODE: {mode_name}  [PAUSED]"
        color = _RED
    else:
        label = f"MODE: {mode_name}"
        color = _GREEN if mode > 0 else _ORANGE

    cv2.putText(frame, label, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    # ── Second line: pixel error ──
    info = f"dx: {dx:.1f}px  dy: {dy:.1f}px  OnTarget: {on_target}"
    cv2.putText(frame, info, (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, _WHITE, 1)

    # ── Bottom: hotkey reference ──
    keys = [
        "[X] Idle   [C] Track   [V] Flick+Click",
        "[F9] Pause/Resume   [Z] Quit",
    ]
    y = h - 50
    for line in keys:
        cv2.putText(frame, line, (10, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, _GREY, 1)
        y += 25


# ─── Target selection ─────────────────────────────────────

def _pick_closest_box(boxes, cx: int, cy: int):
    """Return the bounding-box row whose centre is closest to (cx, cy)."""
    return min(
        boxes,
        key=lambda b: math.hypot((b[0] + b[2]) / 2 - cx,
                                 (b[1] + b[3]) / 2 - cy),
    )


# ─── Main entry point ────────────────────────────────────

def annotate_and_collect(frame, boxes, mode: int, logger) -> Tuple[Tuple[float, float, int], any]:
    """
    Draw aim-box, marker, line, OSD.  Compute pixel error and log it.

    Returns
    -------
    ((dx, dy, on_target), annotated_frame)
    """
    frame = frame.copy()
    h, w  = frame.shape[:2]
    cx, cy = get_center(w, h)
    half   = CENTER_BOX_SIZE // 2

    aim_tl = (cx - half, cy - half)
    aim_br = (cx + half, cy + half)

    # Central aim box
    cv2.rectangle(frame, aim_tl, aim_br, _GREEN, 2)

    dx, dy, on_target = 0.0, 0.0, 0

    if boxes.size:
        best = _pick_closest_box(boxes, cx, cy)
        x1, y1, x2, y2 = best[:4]

        # Aim point: chest height (fraction of bbox from top)
        tx = (x1 + x2) / 2
        ty = y1 + (y2 - y1) * CHEST_Y_FACTOR

        # Pixel error: +right, +up
        dx = tx - cx
        dy = cy - ty

        # On-target: bbox overlaps the aim box
        if not (x2 < aim_tl[0] or x1 > aim_br[0] or
                y2 < aim_tl[1] or y1 > aim_br[1]):
            on_target = 1

        # Marker + line
        cv2.circle(frame, (int(tx), int(ty)), 5, _RED, -1)
        cv2.line(frame, (cx, cy), (int(tx), int(ty)), _BLUE, 2)

    logger.log(round(dx, 1), round(dy, 1), mode)
    _draw_osd(frame, h, mode, dx, dy, on_target)

    return (dx, dy, on_target), frame
