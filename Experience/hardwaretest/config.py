# config.py
MODEL_PATH      = r"model\model3(y5m)\yolov5m_best.pt"
CONFIDENCE      = 0.23
IMGSZ           = 640
CENTER_BOX_SIZE = 20 #30
CHEST_Y_FACTOR  = 0.25    # aim 30% down from top of bbox

# ─── Serial settings ───────────────────────────────
# set SERIAL_PORT to whatever your ESP32 enumerates as:
SERIAL_PORT     = 'COM5'
SERIAL_BAUD     = 115200

# ------------------------------------------------------
# Flip these to match your wiring / wheel orientation:
FL_DIR = +1
FR_DIR = -1
BL_DIR = -1
BR_DIR = +1

# Your PID gains…
KP_X = 0.6; KI_X = 7; KD_X = 3 #deadzone at 75 100cm/360 working good
KP_Y = 0.2; KI_Y = 3; KD_Y = 1.7 
# KP_X = 0.15; KI_X = 0.002; KD_X = 60 #deadzone at 140
# KP_Y = 0.05; KI_Y = 0.03; KD_Y = 22
# KP_X = 0.2; KI_X = 6; KD_X = 2.1 #deadzone at 135 65cm/360 
# KP_Y = 0.15; KI_Y = 6; KD_Y = 2.5 

MAX_WHEEL_PERCENT = 100
