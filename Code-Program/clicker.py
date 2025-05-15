#handle mouse click
# clicker.py
from pynput.mouse import Button, Controller
import time

mouse = Controller()
click_held = False
last_click_time = 0
click_toggle = False

def handle_mouse_click(mode, on_target):
    """
    mode 1: hold mouse while on_target
    mode 2: pulse‐click at ~70ms on, ~72ms off while on_target
    """
    global click_held, last_click_time, click_toggle

    # if neither clicky mode → reset any held click
    if mode not in (1, 2):
        if click_held:
            mouse.release(Button.left)
            click_held = False
        click_toggle = False
        return

    if mode == 1:
        if on_target and not click_held:
            mouse.press(Button.left); click_held = True
        elif not on_target and click_held:
            mouse.release(Button.left); click_held = False

    elif mode == 2:
        now = time.time()
        if on_target:
            # ensure a full cycle (0.07 + 0.072s) before next pulse
            if not click_toggle or (now - last_click_time > 0.142):
                mouse.press(Button.left)
                time.sleep(0.07)
                mouse.release(Button.left)
                last_click_time = time.time()
                click_toggle = True
        else:
            click_toggle = False
