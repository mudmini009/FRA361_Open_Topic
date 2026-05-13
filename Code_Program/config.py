# config.py — Central configuration for Virtual Aimbot
import os
import sys


# ─── Model Selection ──────────────────────────────────────
# Change this to use a different YOLO model:
#   "model1(y5s)"  → YOLOv5s  ~15ms  (fast, less accurate)
#   "model2(y5s)"  → YOLOv5s  ~15ms  (alternate training)
#   "model3(y5m)"  → YOLOv5m  ~25ms  (recommended)
#   "model4(y5l)"  → YOLOv5l  ~40ms  (slow, most accurate)
MODEL_CHOICE = "model3(y5m)"

# Weight filenames per model folder
_WEIGHT_NAMES = {
    "model1(y5s)": "yolov5s_best.pt",
    "model2(y5s)": "yolov5s_best.pt",
    "model3(y5m)": "yolov5m_best.pt",
    "model4(y5l)": "yolov5l_best.pt",
}


def _get_model_path() -> str:
    """
    Resolve YOLO weight file path.
    - PyInstaller bundle  → sys._MEIPASS root
    - Development         → ../models/<MODEL_CHOICE>/
    """
    weight = _WEIGHT_NAMES.get(MODEL_CHOICE, "yolov5m_best.pt")
    if getattr(sys, "_MEIPASS", None):
        return os.path.join(sys._MEIPASS, weight)
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "models", MODEL_CHOICE, weight,
    )


MODEL_PATH  = _get_model_path()
CONFIDENCE  = 0.23
IMGSZ       = 640

# ─── Aim Point ────────────────────────────────────────────
CENTER_BOX_SIZE = 15      # central aim-box overlay size (px)
CHEST_Y_FACTOR  = 0.25    # aim 25 % down from bbox top (≈ chest)

# ─── Mouse / Sensitivity ─────────────────────────────────
MOUSE_DPI   = 800         # physical mouse DPI
CM_PER_360  = 33.0        # in-game sens: 33 cm pad = full 360°
GAME_FOV    = 103.0       # horizontal FOV (Overwatch / KovaaK default)

# Derived: raw sensor counts for one full 360° rotation
#   counts = cm × DPI / 2.54
COUNTS_PER_360 = CM_PER_360 * MOUSE_DPI / 2.54   # ≈ 10 394

# ─── Aim Behaviour ───────────────────────────────────────
AIM_SPEED      = 1.0      # lerp factor: 1.0 = instant, < 1.0 = smooth
PIXEL_DEADZONE = 5        # ignore sub-pixel jitter (px)
