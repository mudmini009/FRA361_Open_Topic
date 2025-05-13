#not used in main code
#to upload my train model to online
import sys
import roboflow
from pathlib import Path

# Add YOLOv5 directory to Python path to access models
sys.path.append(str(Path('C:/Users/mudno/yolov5').resolve()))

# Replace with your actual Roboflow API key and project ID
api_key = "mHg9O9jSYIMK0Jt3O4F5"
project_id = "fra361_opentopic_aimbot"
version_id = 1  # The specific version ID you want to deploy

# Set up Roboflow API connection
rf = roboflow.Roboflow(api_key=api_key)

# Access the project and version
project = rf.workspace().project(project_id)
version = project.version(version_id)

# Specify the model path for best.pt
model_path = "C:/Users/mudno/yolov5/runs/train/exp3"  # Full path to the model weights

# Deploy the YOLOv5 model (with your custom weights)
version.deploy("yolov5", model_path)  # Deploying with weights passed directly

# Alternatively, you can deploy without specifying the weights (will default to "weights/best.pt")
# version.deploy("yolov5")
