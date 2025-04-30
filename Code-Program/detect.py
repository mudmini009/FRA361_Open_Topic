import yolov5
import cv2
from capture import find_game_window, get_game_capture

# Configuration
MODEL_PATH = r'model\model1(y5s)\weights\best.pt'  # RAW string for Windows paths
CONFIDENCE = 0.25  # Minimum detection confidence
IMGSZ = 640  # Inference size (match training size)

def main():
    # Load YOLOv5 model
    model = yolov5.load(MODEL_PATH)
    model.conf = CONFIDENCE
    
    # Setup game capture
    window = find_game_window()
    
    try:
        cv2.namedWindow("Aimbot View", cv2.WINDOW_NORMAL)
        for frame in get_game_capture(window):
            # Perform detection
            results = model(frame, size=IMGSZ)
            
            # Display results
            cv2.imshow("Aimbot View", results.render()[0])
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()