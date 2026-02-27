#yeah this is the main code
# main.py
import pathlib as _pl
_pl.PosixPath = _pl.WindowsPath

import cv2
import time
import os
print("cwd:", os.getcwd())

from capture        import select_game_window, get_game_capture
from detect         import load_model, detect_objects
from config         import MODEL_PATH, CONFIDENCE, IMGSZ
from annotator      import annotate_and_collect
from wheel_control  import pixel_error_to_wheels
from serial_sender  import SerialSender
from clicker        import handle_mouse_click
from control        import get_mode, should_quit

from logger         import DataLogger
from plotter        import plot_log

def main():
    window    = select_game_window()
    cap       = get_game_capture(window)
    model     = load_model(MODEL_PATH, CONFIDENCE)
    sender    = SerialSender()
    logger    = DataLogger()
    mode      = 0

    cv2.namedWindow("Aimbot", cv2.WINDOW_NORMAL)
    print("Press your quit key to exit and show plots.")

    try:
        while True:
            frame = next(cap)
            boxes, ann = detect_objects(model, frame, IMGSZ)

            # annotate + log
            (dx, dy, on_target), out = annotate_and_collect(ann, boxes, mode, logger)
            cv2.imshow("Aimbot", out)

            # wheel drive & clicks (unchanged)
            fl, fr, bl, br = pixel_error_to_wheels(dx, dy, mode)
            sender.send_wheels(fl, fr, bl, br)
            handle_mouse_click(mode, on_target)

            cv2.waitKey(1)
            if should_quit():
                break
            mode = get_mode(mode)

    finally:
        sender.close()
        cv2.destroyAllWindows()

        # at exit: plot & save
        plot_log(logger.entries)
        logger.save_csv()
        print("Done.")
        
if __name__ == "__main__":
    main()
