# clicker.py - Mouse click handling (Windows only, win32api)
import time
import win32api
import win32con

click_held = False
last_click_time = 0
click_toggle = False


def _press():
    """Send left mouse button down."""
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)


def _release():
    """Send left mouse button up."""
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def handle_mouse_click(mode, on_target):
    """
    Mode 0 / 1 : no clicking.
    Mode 2     : pulse-click (~70 ms press, ~72 ms gap) while on-target.
    """
    global click_held, last_click_time, click_toggle

    # Only mode 2 fires
    if mode != 2:
        if click_held:
            _release()
            click_held = False
        click_toggle = False
        return

    # Mode 2: pulse click when on target
    now = time.time()
    if on_target:
        if not click_toggle or (now - last_click_time > 0.142):
            _press()
            time.sleep(0.07)
            _release()
            last_click_time = time.time()
            click_toggle = True
    else:
        click_toggle = False
