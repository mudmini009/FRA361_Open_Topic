# detect.py — YOLOv5 model loading and inference
import numpy as np
import yolov5


def load_model(model_path: str, confidence: float):
    """Load a YOLOv5 model and set its confidence threshold."""
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
