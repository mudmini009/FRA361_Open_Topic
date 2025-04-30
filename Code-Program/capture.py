import pygetwindow as gw
import mss
import numpy as np
import cv2

def find_game_window(target="KovaaK"):
    """Find visible game window with fuzzy name matching"""
    windows = [w for w in gw.getAllWindows() if target.lower() in w.title.lower() and w.visible]
    if not windows:
        raise RuntimeError(f"No visible window containing '{target}' found!")
    return windows[0]

def get_game_capture(window):
    """Generator yielding game frames"""
    with mss.mss() as sct:
        monitor = {
            "top": window.top,
            "left": window.left,
            "width": window.width,
            "height": window.height,
            "mon": 0
        }
        
        while True:
            frame = np.array(sct.grab(monitor))
            yield cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

if __name__ == "__main__":
    # Test capture directly
    win = find_game_window()
    cv2.namedWindow("Capture Test", cv2.WINDOW_NORMAL)
    
    try:
        for frame in get_game_capture(win):
            cv2.imshow("Capture Test", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cv2.destroyAllWindows()