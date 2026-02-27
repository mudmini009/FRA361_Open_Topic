#to pull the screen out 
# capture.py
import pygetwindow as gw
import mss
import numpy as np
import cv2
import difflib

def select_game_window():
    """List visible windows and prompt user to type part of the title."""
    windows = [w for w in gw.getAllWindows() if w.visible]
    if not windows:
        raise RuntimeError("No visible windows found!")

    titles = [w.title for w in windows]
    print("Available windows:")
    for t in titles:
        print(f" - {t}")

    target = input("\nType part of the window title to select: ")
    matches = difflib.get_close_matches(target, titles, n=1, cutoff=0)
    if not matches:
        raise RuntimeError(f"No window matches '{target}' found.")
    selected = matches[0]
    print(f"\nSelected window: '{selected}'")

    return next(w for w in windows if w.title == selected)

def get_game_capture(window):
    """Generator yielding BGR frames of that window."""
    with mss.mss() as sct:
        mon = {
            "top":    window.top,
            "left":   window.left,
            "width":  window.width,
            "height": window.height,
            "mon":    0
        }
        while True:
            img = np.array(sct.grab(mon))
            yield cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
