# capture.py — Window selection + MSS screen capture
import difflib

import cv2
import mss
import numpy as np
import pygetwindow as gw


def select_game_window():
    """List visible windows and let the user pick one by partial title."""
    windows = [w for w in gw.getAllWindows() if w.visible and w.title.strip()]
    if not windows:
        raise RuntimeError("No visible windows found!")

    titles = [w.title for w in windows]
    print("Available windows:")
    for title in titles:
        print(f"  • {title}")

    query   = input("\nType part of the window title to select: ")
    matches = difflib.get_close_matches(query, titles, n=1, cutoff=0)
    if not matches:
        raise RuntimeError(f"No window matching '{query}'.")

    selected = matches[0]
    print(f"\n→ Selected: '{selected}'\n")
    return next(w for w in windows if w.title == selected)


def get_game_capture(window):
    """Generator that yields BGR frames of the selected window region."""
    with mss.mss() as sct:
        region = {
            "top":    window.top,
            "left":   window.left,
            "width":  window.width,
            "height": window.height,
            "mon":    0,
        }
        while True:
            raw = np.array(sct.grab(region))
            yield cv2.cvtColor(raw, cv2.COLOR_BGRA2BGR)
