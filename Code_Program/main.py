# main.py - Virtual Aimbot (Software-Only, Windows Target)
import cv2
import keyboard

from capture      import select_game_window, get_game_capture
from detect       import load_model, detect_objects
from config       import MODEL_PATH, CONFIDENCE, IMGSZ
from annotator    import annotate_and_collect
from mouse_mover  import compute_mouse_delta, move_mouse_relative
from clicker      import handle_mouse_click
from control      import (get_mode, should_quit, is_paused,
                          toggle_pause, QUIT_KEY, PAUSE_KEY)
from logger       import DataLogger
from plotter      import plot_log


def print_startup_banner():
    """Print hotkey reference to console at startup."""
    print("=" * 55)
    print("       VIRTUAL AIMBOT - HOTKEY REFERENCE")
    print("=" * 55)
    print("  [F1]  Mode 0 - IDLE (no aim, no click)")
    print("  [F2]  Mode 1 - TRACK (aim follows target)")
    print("  [F3]  Mode 2 - FLICK + CLICK (aim & auto-fire)")
    print("  [F9]  PAUSE / RESUME the aimbot")
    print("  [F10] QUIT and save logs")
    print("=" * 55)
    print()


def main():
    print_startup_banner()

    window   = select_game_window()
    cap      = get_game_capture(window)
    model    = load_model(MODEL_PATH, CONFIDENCE)
    logger   = DataLogger()
    mode     = 0
    screen_w = window.width
    screen_h = window.height

    cv2.namedWindow("Aimbot", cv2.WINDOW_NORMAL)

    pause_was_pressed = False

    try:
        while True:
            # -- Pause toggle (edge-detect, not hold) --
            if keyboard.is_pressed(PAUSE_KEY):
                if not pause_was_pressed:
                    toggle_pause()
                    state = "PAUSED" if is_paused() else "ACTIVE"
                    print(">> Aimbot {}".format(state))
                    pause_was_pressed = True
            else:
                pause_was_pressed = False

            # -- Capture and detect --
            frame = next(cap)
            boxes, ann = detect_objects(model, frame, IMGSZ)
            (dx, dy, on_target), out = annotate_and_collect(
                ann, boxes, mode, logger
            )
            cv2.imshow("Aimbot", out)

            # -- Move mouse and click (only when active + tracking) --
            if not is_paused() and mode > 0:
                # dy from annotator is +up; win32 mouse expects +down so negate
                mouse_dx, mouse_dy = compute_mouse_delta(
                    dx, -dy, screen_w, screen_h
                )
                move_mouse_relative(mouse_dx, mouse_dy)
                handle_mouse_click(mode, on_target)

            cv2.waitKey(1)
            if should_quit():
                break
            mode = get_mode(mode)

    finally:
        cv2.destroyAllWindows()
        plot_log(logger.entries)
        logger.save_csv()
        print("Done.")


if __name__ == "__main__":
    main()
