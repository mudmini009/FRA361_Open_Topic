#part of main code (but not main)
#to detect the screen using yolo model
# detect.py
import yolov5

def load_model(model_path: str, confidence: float):
    """Load YOLOv5 model once and set its confidence threshold."""
    model = yolov5.load(model_path)
    model.conf = confidence
    return model

def detect_objects(model, frame, imgsz: int):
    """
    Run inference on a single frame.
    Returns:
      - raw bounding‐boxes array (xyxy, conf, cls)
      - annotated BGR image
    """
    results   = model(frame, size=imgsz)
    boxes_np  = results.xyxy[0].cpu().numpy()
    annotated = results.render()[0]
    return boxes_np, annotated
