# config.py - Configuration for Virtual Aimbot (Windows Target)
import os
import sys


def _get_model_path():
    """
    Resolve the YOLO model path.
    PyInstaller bundle: model sits at _MEIPASS root.
    Development: model is at ../models/model3(y5m)/ relative to this file.
    """
    if getattr(sys, "_MEIPASS", None):
        return os.path.join(sys._MEIPASS, "yolov5m_best.pt")
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "models", "model3(y5m)", "yolov5m_best.pt",
    )


# --- Model Settings ---
MODEL_PATH      = _get_model_path()
CONFIDENCE      = 0.23
IMGSZ           = 640

# --- Aim Point Settings ---
CENTER_BOX_SIZE = 15          # central aim box overlay size (px)
CHEST_Y_FACTOR  = 0.25        # aim 25% down from bbox top (chest height)

# --- Mouse / Sensitivity Settings ---
MOUSE_DPI       = 800         # physical mouse DPI
CM_PER_360      = 33.0        # in-game sens: 33 cm mousepad = full 360 deg
GAME_FOV        = 103.0       # horizontal FOV in degrees (OW / KovaaK default)

# Derived: raw sensor counts per full 360 deg rotation
#   counts = CM_PER_360 (cm) x DPI (counts/inch) / 2.54 (cm/inch)
COUNTS_PER_360  = CM_PER_360 * MOUSE_DPI / 2.54   # approx 10394 counts

# --- Aim Behaviour ---
AIM_SPEED       = 1.0         # lerp: 1.0 = instant snap, < 1.0 = smooth
PIXEL_DEADZONE  = 5           # ignore movements smaller than this (px)
