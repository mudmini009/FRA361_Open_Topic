# main.py
from capture       import select_game_window, get_game_capture
from detect        import load_model, detect_objects
from distance      import get_center
from config        import MODEL_PATH, CONFIDENCE, IMGSZ, CENTER_BOX_SIZE

import cv2
import math
import pathlib as _pl
_pl.PosixPath = _pl.WindowsPath

from pynput.mouse import Button, Controller
import time

import keyboard

mouse = Controller()
click_held = False
last_click_time = 0
click_toggle = False  # for pulse click tracking

# fraction down from the top of the bbox to aim at chest (0=top, 1=center)
CHEST_Y_FACTOR = 0.3

def annotate_and_collect(frame, boxes, mode, log):
    """
    Draw central aim-box, pick nearest target by bbox-center,
    then re-calc distance/angle to its chest-point, draw them,
    detect overlap for on_target, and log [dist,ang,on,mode].
    """
    frame = frame.copy()
    h, w = frame.shape[:2]
    cx, cy = get_center(w, h)
    half = CENTER_BOX_SIZE // 2

    # draw central “aim” box
    left, top = cx - half, cy - half
    right, bottom = cx + half, cy + half
    cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)

    dist, ang, on_target = 0.0, 0.0, 0

    if boxes.size:
        # 1) choose closest by geometric center
        candidates = []
        for b in boxes:
            x1,y1,x2,y2 = b[:4]
            ox = (x1 + x2) / 2
            oy = (y1 + y2) / 2
            d = math.hypot(ox - cx, oy - cy)
            candidates.append((d, (x1,y1,x2,y2)))
        _, (bx1,by1,bx2,by2) = min(candidates, key=lambda x: x[0])

        # 2) compute chest-point
        tx = (bx1 + bx2) / 2
        ty = by1 + (by2 - by1) * CHEST_Y_FACTOR

        # 3) recompute dist & angle to chest-point
        dx = tx - cx
        dy = cy - ty   # invert so +dy = up
        dist = math.hypot(dx, dy)
        ang  = math.degrees(math.atan2(dx, dy))
        if ang < 0:
            ang += 360

        # 4) draw marker & line
        cv2.circle(frame, (int(tx), int(ty)), 5, (0,0,255), -1)
        cv2.line(frame, (cx, cy), (int(tx), int(ty)), (255,0,0), 2)

        # 5) on_target if bbox overlaps central box
        if not (bx2 < left or bx1 > right or by2 < top or by1 > bottom):
            on_target = 1

    # log [distance, angle, on_target, mode]
    log.append([round(dist,1), round(ang,1), on_target, mode])

    # overlay stats
    cv2.putText(frame, f"Mode: {mode}",        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)
    cv2.putText(frame, f"Dist: {dist:.1f}px",  (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    cv2.putText(frame, f"Ang: {ang:.1f}°",     (10,110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    cv2.putText(frame, f"OnTarget: {on_target}",(10,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

    return frame

def handle_mouse_click(mode, on_target):
    global click_held, last_click_time, click_toggle

    # always release if not in a clicky mode
    if mode not in (1, 2):
        if click_held:
            mouse.release(Button.left)
            click_held = False
        click_toggle = False
        return
       
    if mode == 1:
        if on_target and not click_held:
            mouse.press(Button.left)
            click_held = True
        elif not on_target and click_held:
            mouse.release(Button.left)
            click_held = False

    elif mode == 2:
        now = time.time()
        if on_target:
            if not click_toggle or (now - last_click_time > 0.07 + 0.072):
                # click pulse: press then release with delay
                mouse.press(Button.left)
                time.sleep(0.026)
                mouse.release(Button.left)
                time.sleep(0.027)
                last_click_time = time.time()
                click_toggle = True
        else:
            click_toggle = False

def main():
    window     = select_game_window()
    capture_gen= get_game_capture(window)
    model      = load_model(MODEL_PATH, CONFIDENCE)
    mode, log  = 0, []

    cv2.namedWindow("Aimbot", cv2.WINDOW_NORMAL)
    while True:
        frame = next(capture_gen)
        boxes, annotated = detect_objects(model, frame, IMGSZ)
        out = annotate_and_collect(annotated, boxes, mode, log)
        cv2.imshow("Aimbot", out)
        
        # 🔫 Trigger click logic (after logging updated)
        last_log = log[-1] if log else [0, 0, 0, mode]
        on_target = last_log[2]
        handle_mouse_click(mode, on_target)

        # keep window responsive
        cv2.waitKey(1)

        # **global** hot-keys (works even when Kovaak is focused)
        if keyboard.is_pressed('z'):        # Z → quit
            break
        elif keyboard.is_pressed('x'):      # X → mode 0
            mode = 0
        elif keyboard.is_pressed('c'):      # C → mode 1
            mode = 1
        elif keyboard.is_pressed('v'):      # V → mode 2
            mode = 2

    cv2.destroyAllWindows()
    # `log` now has your [dist,angle,on,mode] history ready for PySerial.

if __name__ == "__main__":
    main()
