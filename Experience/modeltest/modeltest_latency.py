import os
import pathlib
import time

# Monkey-patch to avoid PosixPath unpickle errors on Windows
import pathlib as _pl
_pl.PosixPath = _pl.WindowsPath

import yolov5
import cv2

# === EDIT THESE PATHS & PARAMETERS ===
VIDEO_DIR = r"D:\UNIVERSITY\YR3\FRA361_Open_Topic\Experience\modeltest"
VIDEO_FILES = [
    "[N] CLS Click Robots.mp4",
    "Cata IC Fast Strafes Robot.mp4",
    "Close Fast Colosseum Robots No Shooting.mp4",
    "Close Fast Strafes Invincivle OW Robot.mp4",
    "RoboTS180.mp4"
]

MODEL_CONFIGS = [
    {"name": "small_old",  "weights": r"model\model1(y5s)\weights\best.pt",        "imgsz": 640},
    {"name": "small_new",  "weights": r"model\model2(y5s)\yolov5s_best.pt",         "imgsz": 640},
    {"name": "medium",     "weights": r"model\model3(y5m)\yolov5m_best.pt",         "imgsz": 640},
    {"name": "large",      "weights": r"model\model4(y5l)\yolov5l_best.pt",         "imgsz": 640},
    {"name": "x",          "weights": r"model\model5(y5x)\yolov5x_best.pt",         "imgsz": 640},
]

CONF_THRESHOLD = 0.25   # minimum confidence
SKIP_FRAMES    = 1      # process every Nth frame (1 = every frame)
# =====================================

def analyze_video(model, video_path, imgsz):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"  ✗ could not open {os.path.basename(video_path)}")
        return None

    latencies = []
    frame_idx = 0

    # we only need timing, no need to count detections here
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % SKIP_FRAMES != 0:
            frame_idx += 1
            continue

        t0 = time.time()
        _ = model(frame, size=imgsz)  # inference
        t1 = time.time()

        latencies.append((t1 - t0) * 1000.0)  # ms
        frame_idx += 1

    cap.release()
    if not latencies:
        return None

    return {
        "frames": len(latencies),
        "mean_ms": sum(latencies) / len(latencies),
        "min_ms": min(latencies),
        "max_ms": max(latencies),
    }

def main():
    print(f"Running inference timing on {len(VIDEO_FILES)} videos × {len(MODEL_CONFIGS)} models...\n")
    for cfg in MODEL_CONFIGS:
        print(f"=== Model: {cfg['name']} ===")
        model = yolov5.load(cfg["weights"])
        model.conf = CONF_THRESHOLD

        for vid in VIDEO_FILES:
            path = os.path.join(VIDEO_DIR, vid)
            stats = analyze_video(model, path, cfg["imgsz"])
            if stats is None:
                continue

            print(f"{vid:40s}  frames: {stats['frames']:3d}  "
                  f"mean: {stats['mean_ms']:.1f} ms  "
                  f"min: {stats['min_ms']:.1f} ms  "
                  f"max: {stats['max_ms']:.1f} ms")
        print()

if __name__ == "__main__":
    main()
