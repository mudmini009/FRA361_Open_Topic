# main.py
import pathlib as _pl
_pl.PosixPath = _pl.WindowsPath

import cv2
from capture     import select_game_window, get_game_capture
from detect      import load_model, detect_objects
from config      import MODEL_PATH, CONFIDENCE, IMGSZ
from annotator   import annotate_and_collect
from clicker     import handle_mouse_click
from control     import get_mode, should_quit
from serial_sender import SerialSender  # ← new

def main():
    window    = select_game_window()
    cap_gen   = get_game_capture(window)
    model     = load_model(MODEL_PATH, CONFIDENCE)
    mode, log = 0, []

    # 🔌 set up serial
    sender = SerialSender()

    cv2.namedWindow("Aimbot", cv2.WINDOW_NORMAL)
    try:
        while True:
            frame  = next(cap_gen)
            boxes, ann = detect_objects(model, frame, IMGSZ)
            out    = annotate_and_collect(ann, boxes, mode, log)
            cv2.imshow("Aimbot", out)

            # fire clicks
            on_tgt = log[-1][2] if log else 0
            handle_mouse_click(mode, on_tgt)

            # send latest [dist,ang,on,mode] over USB-Serial
            sender.send(log[-1])

            cv2.waitKey(1)
            if should_quit():
                break
            mode = get_mode(mode)

    finally:
        sender.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
