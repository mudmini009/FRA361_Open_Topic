# main.py — Virtual Aimbot entry point (Windows only)
import cv2
import keyboard

from capture      import select_game_window, get_game_capture
from clicker      import handle_mouse_click
from config       import CONFIDENCE, IMGSZ, MODEL_PATH
from control      import (
    PAUSE_KEY, get_mode, is_paused, should_quit, toggle_pause,
)
from detect       import load_model, detect_objects
from annotator    import annotate_and_collect
from logger       import DataLogger
from mouse_mover  import compute_mouse_delta, move_mouse_relative
from plotter      import plot_log


# ─── Startup banner ──────────────────────────────────────

def _print_banner() -> None:
    """Print hotkey cheat-sheet to the console."""
    print("=" * 55)
    print("       VIRTUAL AIMBOT — HOTKEY REFERENCE")
    print("=" * 55)
    print("  [X]   Mode 0 — IDLE (no aim, no click)")
    print("  [C]   Mode 1 — TRACK (aim follows target)")
    print("  [V]   Mode 2 — FLICK + CLICK (aim & auto-fire)")
    print("  [F9]  PAUSE / RESUME")
    print("  [Z]   QUIT and save logs")
    print("=" * 55)
    print()


# ─── Pause edge-detection ────────────────────────────────

class _PauseToggle:
    """Detect key-down edges so holding F9 doesn't spam on/off."""

    def __init__(self) -> None:
        self._was_pressed = False

    def update(self) -> None:
        pressed = keyboard.is_pressed(PAUSE_KEY)
        if pressed and not self._was_pressed:
            toggle_pause()
            state = "PAUSED" if is_paused() else "ACTIVE"
            print(f">> Aimbot {state}")
        self._was_pressed = pressed


# ─── Main loop ───────────────────────────────────────────

def main() -> None:
    _print_banner()

    # Initialise
    window   = select_game_window()
    capture  = get_game_capture(window)
    model    = load_model(MODEL_PATH, CONFIDENCE)
    logger   = DataLogger()
    pause    = _PauseToggle()
    mode     = 0
    screen_w = window.width
    screen_h = window.height

    cv2.namedWindow("Aimbot", cv2.WINDOW_NORMAL)

    try:
        while True:
            pause.update()

            # ── Capture → detect → annotate ──
            frame = next(capture)
            boxes, annotated = detect_objects(model, frame, IMGSZ)
            (dx, dy, on_target), display = annotate_and_collect(
                annotated, boxes, mode, logger,
            )
            cv2.imshow("Aimbot", display)

            # ── Act (only when unpaused + aiming) ──
            if not is_paused() and mode > 0:
                mouse_dx, mouse_dy = compute_mouse_delta(
                    dx, -dy, screen_w, screen_h,
                )
                move_mouse_relative(mouse_dx, mouse_dy)
                handle_mouse_click(mode, on_target)

            # ── Input ──
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
