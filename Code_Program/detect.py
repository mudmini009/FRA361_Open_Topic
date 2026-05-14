# detect.py — YOLOv5 model loading and inference
import numpy as np
import yolov5


def load_model(model_path: str, confidence: float):
    """Load a YOLOv5 model and set its confidence threshold."""
    # -- Monkeypatch PyInstaller crash --
    # YOLOv5's file_date checks __file__.stat(), which crashes in PyInstaller
    # because .pyc files inside the zip don't exist as standard files.
    # By mocking Path.stat, we globally bypass this check.
    import pathlib
    original_stat = pathlib.Path.stat
    
    def safe_stat(self, *args, **kwargs):
        try:
            return original_stat(self, *args, **kwargs)
        except FileNotFoundError:
            class DummyStat:
                st_mtime = 0
            return DummyStat()
            
    pathlib.Path.stat = safe_stat
    
    model = yolov5.load(model_path)
    model.conf = confidence
    return model


def detect_objects(model, frame: np.ndarray, imgsz: int):
    """
    Run inference on a single BGR frame.

    Returns
    -------
    boxes : np.ndarray
        Shape (N, 6) — each row is [x1, y1, x2, y2, conf, cls].
    annotated : np.ndarray
        The frame with YOLO-drawn bounding boxes.
    """
    results   = model(frame, size=imgsz)
    boxes     = results.xyxy[0].cpu().numpy()
    annotated = results.render()[0]
    return boxes, annotated
