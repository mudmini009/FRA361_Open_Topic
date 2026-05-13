# clicker.py — Mouse click handling (win32api, Windows only)
import time

import win32api
import win32con

# ─── Timing constants ─────────────────────────────────────
_CLICK_HOLD_MS  = 0.070   # pulse press duration        (s)
_CLICK_COOLDOWN = 0.142   # minimum gap between pulses  (s)

# ─── Internal state ───────────────────────────────────────
_click_held     = False
_last_click_at  = 0.0
_click_armed    = False


def _press() -> None:
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)


def _release() -> None:
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def handle_mouse_click(mode: int, on_target: bool) -> None:
    """
    Mode 0 → no clicking.
    Mode 1 → hold click while on target (release when off).
    Mode 2 → pulse click while on target.
    """
    global _click_held, _last_click_at, _click_armed

    # Mode 0: no clicking
    if mode == 0:
        if _click_held:
            _release()
            _click_held = False
        _click_armed = False
        return

    # Mode 1: hold click while on target
    if mode == 1:
        if on_target:
            if not _click_held:
                _press()
                _click_held = True
        else:
            if _click_held:
                _release()
                _click_held = False
        return

    # Mode 2: pulse click while on target
    if mode == 2:
        now = time.time()
        if on_target:
            if not _click_armed or (now - _last_click_at > _CLICK_COOLDOWN):
                _press()
                time.sleep(_CLICK_HOLD_MS)
                _release()
                _last_click_at = time.time()
                _click_armed = True
        else:
            _click_armed = False
