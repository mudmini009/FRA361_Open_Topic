import pygetwindow as gw
import mss
import numpy as np
import cv2
import yolov5
import pathlib as _pl
_pl.PosixPath = _pl.WindowsPath

# === CONFIGURATION ===
MODEL_PATH    = r'model\model5(y5x)\yolov5x_best.pt'  # path to your .pt
CONFIDENCE    = 0.25                                 # min detection confidence
IMGSZ         = 640                                  # inference size
TARGET_WINDOW = "KovaaK"                             # window title substring
WINDOW_NAME   = "Aimbot View"
# =====================

def find_game_window(target=TARGET_WINDOW):
    """Find the first visible window whose title contains target."""
    windows = [w for w in gw.getAllWindows()
               if target.lower() in w.title.lower() and w.visible]
    if not windows:
        raise RuntimeError(f"No visible window containing '{target}' found!")
    return windows[0]

def get_game_capture(window):
    """Yields BGR frames captured from the given window."""
    with mss.mss() as sct:
        monitor = {
            "top": window.top,
            "left": window.left,
            "width": window.width,
            "height": window.height,
            "mon": 0
        }
        while True:
            img = np.array(sct.grab(monitor))
            yield cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

def main():
    # load model
    model = yolov5.load(MODEL_PATH)
    model.conf = CONFIDENCE

    # find game window & setup display
    window = find_game_window()
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

    try:
        for frame in get_game_capture(window):
            # inference + render
            results = model(frame, size=IMGSZ)
            out = results.render()[0]
            # show
            cv2.imshow(WINDOW_NAME, out)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
