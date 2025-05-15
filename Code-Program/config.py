# config.py
MODEL_PATH      = r"model\model4(y5l)\yolov5l_best.pt"
CONFIDENCE      = 0.25
IMGSZ           = 640
CENTER_BOX_SIZE = 20 #30
CHEST_Y_FACTOR  = 0.3    # aim 30% down from top of bbox

# ─── Serial settings ───────────────────────────────
# set SERIAL_PORT to whatever your ESP32 enumerates as:
SERIAL_PORT     = 'COM5'
SERIAL_BAUD     = 115200