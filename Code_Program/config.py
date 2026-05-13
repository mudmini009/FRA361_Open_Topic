# config.py — Central configuration for Virtual Aimbot
import os
import sys


# ─── Available Models ─────────────────────────────────────
# Maps display name → (folder, weight filename)
MODELS = {
    "S":    ("model1(y5s)", "yolov5s_best.pt"),
    "S v2": ("model2(y5s)", "yolov5s_best.pt"),
    "M":    ("model3(y5m)", "yolov5m_best.pt"),
    "L":    ("model4(y5l)", "yolov5l_best.pt"),
}

DEFAULT_MODEL = "M"


def get_model_path(choice: str) -> str:
    """
    Resolve YOLO weight path for the chosen model.
    - PyInstaller bundle  → sys._MEIPASS root
    - Development         → ../models/<folder>/
    """
    folder, weight = MODELS[choice]
    if getattr(sys, "_MEIPASS", None):
        return os.path.join(sys._MEIPASS, weight)
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "models", folder, weight,
    )


# ─── Inference ────────────────────────────────────────────
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
