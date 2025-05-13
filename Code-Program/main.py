#the main one
# main.py
# main.py
from capture       import select_game_window, get_game_capture
from detect        import load_model, detect_objects
from distance      import calculate_distance_and_angle, get_center
from config        import MODEL_PATH, CONFIDENCE, IMGSZ, CENTER_BOX_SIZE
import cv2

def annotate(frame, boxes):
    h, w = frame.shape[:2]
    cx, cy = get_center(w, h)
    half = CENTER_BOX_SIZE // 2
    cv2.rectangle(frame,
                  (cx-half, cy-half),
                  (cx+half, cy+half),
                  (0,255,0), 2)

    if boxes.size:
        # pick closest
        dist, ang, ox, oy = min(
            (calculate_distance_and_angle(b[:4], w, h) + (b,) for b in boxes), 
            key=lambda x: x[0]
        )[:4]

        cv2.circle(frame, (int(ox),int(oy)), 5, (0,0,255), -1)
        status = "Yes" if (cx-half <= ox <= cx+half and cy-half <= oy <= cy+half) else "No"
        cv2.putText(frame, f"Dist: {dist:.1f}px",  (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.putText(frame, f"Angle: {ang:.1f}°",  (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.putText(frame, f"In box: {status}",   (10,110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

def main():
    window = select_game_window()
    model  = load_model(MODEL_PATH, CONFIDENCE)
    cv2.namedWindow("Aimbot View", cv2.WINDOW_NORMAL)

    for frame in get_game_capture(window):
        boxes, annotated = detect_objects(model, frame, IMGSZ)
        annotate(annotated, boxes)
        cv2.imshow("Aimbot View", annotated)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()