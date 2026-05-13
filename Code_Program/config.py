# config.py — Central configuration for Virtual Aimbot
import os
import sys


# ─── Model ────────────────────────────────────────────────
def _get_model_path() -> str:
    """
    Resolve YOLO weight path.
    - PyInstaller  → sys._MEIPASS root
    - Development  → ../models/model3(y5m)/
    """
    if getattr(sys, "_MEIPASS", None):
        return os.path.join(sys._MEIPASS, "yolov5m_best.pt")
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "models", "model3(y5m)", "yolov5m_best.pt",
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
COUNTS_PER_360 = CM_PER_360 * MOUSE_DPI / 2.54   # ≈ 10 394

# ─── Aim Behaviour ───────────────────────────────────────
AIM_SPEED      = 1.0      # lerp factor: 1.0 = instant, < 1.0 = smooth
PIXEL_DEADZONE = 5        # ignore sub-pixel jitter (px)
