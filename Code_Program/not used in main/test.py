#not used in main code
#for test some shit
from ultralytics import YOLO
import cv2
import pygetwindow as gw
import mss
import numpy as np

# Load the trained YOLOv5 model (same as YOLOv8 but with YOLOv5 weights)
model_path = 'D:/UNIVERSITY/YR3/FRA361_Open_Topic/model/model1/weights/best.pt'
model = YOLO(model_path)  # Load your trained YOLOv5 model

# Capture the game window
window_title = "KovaaK's  "  # Replace with your actual window title
window = gw.getWindowsWithTitle(window_title)[0]  # Get the first matching window

# Ensure the window is not minimized
if window.isMinimized:
    window.restore()

# Set up mss to capture the window
with mss.mss() as sct:
    monitor = {"top": window.top, "left": window.left, "width": window.width, "height": window.height}

    while True:
        # Capture the region of the window
        screenshot = sct.grab(monitor)

        # Convert screenshot to a numpy array
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)  # Convert RGBA to BGR

        # Perform inference using YOLOv5
        results = model(img)  # This performs the inference directly

        # Plot the detection results on the image
        annotated_frame = results[0].plot()  # Annotated image with boxes and labels

        # Show the result
        cv2.imshow('Game Window Detection', annotated_frame)

        # Exit if you press 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
