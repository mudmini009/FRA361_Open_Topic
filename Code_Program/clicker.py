# clicker.py — Pulse-click handling (win32api, Windows only)
import time

import win32api
import win32con

# ─── Timing constants ─────────────────────────────────────
_CLICK_HOLD_MS  = 0.070   # how long the button stays pressed (s)
_CLICK_COOLDOWN = 0.142   # minimum gap between clicks    (s)

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
    Mode 0 / 1 → no clicking.
    Mode 2     → pulse-click while crosshair overlaps target bbox.
    """
    global _click_held, _last_click_at, _click_armed

    # Only mode 2 fires
    if mode != 2:
        if _click_held:
            _release()
            _click_held = False
        _click_armed = False
        return

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
