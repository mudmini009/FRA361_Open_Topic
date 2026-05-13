import cv2

def main():
    # === EDIT THESE PATHS/PARAMETERS ===
    video_path = "RoboTS180.mp4"  # <-- Replace with your video file path
    skip_frames = 1  # Change to N to sample every Nth frame (e.g., 2 to see every other frame)
    # ====================================

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: cannot open video {video_path}")
        return

    frame_idx = 0
    counts = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % skip_frames != 0:
            frame_idx += 1
            continue

        cv2.imshow("Frame", frame)
        cv2.waitKey(1)  # Necessary to render the window

        # Prompt user for manual count input
        while True:
            val = input(f"Frame {frame_idx}: Enter detected robot count (or 'q' to quit): ")
            if val.lower() == 'q':
                cap.release()
                cv2.destroyAllWindows()
                summary(counts)
                return
            try:
                count = int(val)
                break
            except ValueError:
                print("Invalid input. Please enter an integer.")

        counts.append(count)
        frame_idx += 1

    cap.release()
    cv2.destroyAllWindows()
    summary(counts)


def summary(counts):
    total_frames = len(counts)
    total_detections = sum(counts)
    false_negatives = sum(1 for c in counts if c == 0)

    print("\n=== Summary ===")
    print(f"Frames counted: {total_frames}")
    print(f"Total detections: {total_detections}")
    print(f"Average detections per frame: {total_detections/total_frames if total_frames else 0:.2f}")
    print(f"False negatives (frames with zero detections): {false_negatives}")

if __name__ == "__main__":
    main()
