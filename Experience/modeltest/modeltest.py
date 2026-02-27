import os
import pathlib
# ← Patch PosixPath → WindowsPath so torch.load can reconstruct paths on Windows
pathlib.PosixPath = pathlib.WindowsPath

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
    {"name": "small_old",
     "weights": r"model\model1(y5s)\weights\best.pt",
     "imgsz": 640},
    {"name": "small_new",
     "weights": r"model\model2(y5s)\yolov5s_best.pt",
     "imgsz": 640},
    {"name": "medium",
     "weights": r"model\model3(y5m)\yolov5m_best.pt",
     "imgsz": 640},
    {"name": "large",
     "weights": r"model\model4(y5l)\yolov5l_best.pt",
     "imgsz": 640},
    {"name": "x",
     "weights": r"model\model5(y5x)\yolov5x_best.pt",
     "imgsz": 640},
]

CONF_THRESHOLD = 0.25   # minimum confidence
SKIP_FRAMES    = 1      # process every Nth frame (1 = every frame)
# =====================================

def analyze_video(model, video_path, imgsz):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"  ✗ could not open {os.path.basename(video_path)}")
        return None

    total_frames = detected_frames = no_detection_frames = total_detections = 0
    sum_confidences = 0.0
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % SKIP_FRAMES != 0:
            frame_idx += 1
            continue

        total_frames += 1
        results = model(frame, size=imgsz)
        preds   = results.pred[0]

        nbox = preds.shape[0]
        if nbox > 0:
            detected_frames += 1
            total_detections += nbox
            sum_confidences += float(preds[:, 4].sum())
        else:
            no_detection_frames += 1

        frame_idx += 1

    cap.release()
    avg_conf = (sum_confidences / total_detections) if total_detections else 0.0
    return {
        "total_frames":        total_frames,
        "detected_frames":     detected_frames,
        "no_detection_frames": no_detection_frames,
        "total_detections":    total_detections,
        "avg_confidence":      avg_conf,
    }

def main():
    for cfg in MODEL_CONFIGS:
        print(f"\n=== Model: {cfg['name']} ===")
        model = yolov5.load(cfg["weights"])
        model.conf = CONF_THRESHOLD

        for vid in VIDEO_FILES:
            path = os.path.join(VIDEO_DIR, vid)
            stats = analyze_video(model, path, cfg["imgsz"])
            if stats is None:
                continue

            print(f"Video: {vid}")
            print(f"  • Total frames       : {stats['total_frames']}")
            print(f"  • Detected frames    : {stats['detected_frames']}")
            print(f"  • No-detect frames   : {stats['no_detection_frames']}")
            print(f"  • Total detections   : {stats['total_detections']}")
            print(f"  • Avg. confidence    : {stats['avg_confidence']:.2f}")

if __name__ == "__main__":
    main()
