
---
# 🤖 MechAim-CV: Hardware-Based Physical Aimbot Using Computer Vision

A hardware-based robotic aimbot that uses real-time object detection (YOLOv5) to physically move a computer mouse. Built as an end-to-end exploration of Computer Vision, PID Control, and Inverse Kinematics.

Tested primarily in **Kovaak's Aim Trainer** to evaluate latency, tracking accuracy, and mechanical constraints without interfering with competitive multiplayer environments.

## 📺 Project Showcase

![Physical Aimbot Showcase](https://github.com/mudmini009/FRA361_Open_Topic/raw/main/final_show_robot.gif)

---

## 🚀 System Architecture

Unlike software-based aimbots, this system physically moves the mouse using a custom-built Mecanum-wheeled robot, bypassing traditional software anti-cheat mechanisms.

* **Vision System (PC):** Captures the screen, runs YOLOv5 object detection to find targets, and calculates pixel error `(dx, dy)` from the screen center.
* **Control System (PC):** A dual-axis PID controller processes the pixel error and computes the required linear velocities `(vx, vy)`. Inverse Kinematics (IK) then translates these velocities into specific speed commands for four Mecanum wheels.
* **Hardware Execution (ESP32):** The PC sends wheel speed data via Serial to an ESP32 microcontroller, which generates PWM signals for the DRV8833 motor drivers to move the physical mouse.
* **Clicking Mechanism (PC):** A Python script utilizes `pynput` to simulate realistic "pulse clicks" when the target is centered, reducing latency and simulating human input.

---

## 📁 Repository Structure

```text
📦 FRA361_Open_Topic
 ┣ 📂 archive/              # Legacy test scripts, early prototypes, and V1 learning logs
 ┣ 📂 CAD/                  # SolidWorks design files for the 3D-printed chassis
 ┣ 📂 Code_Program/         # MAIN WORKSPACE: Contains the Python vision loop & ESP32 firmware
 ┣ 📂 DATASET/              # (Ignored via .gitignore) Contains the custom 38k+ image training dataset
 ┣ 📂 documentation/        # Detailed academic reports, research papers, and reflection logs
 ┣ 📂 model_evaluation/     # Training results, confusion matrices, and metrics from Tesla V100 GPU runs
 ┣ 📂 models/               # Trained YOLOv5 weights (.pt) - Includes Small, Medium, and Large
 ┣ 📂 research_testing/     # Scripts for unit testing hardware, PWM deadzones, and software isolation
 ┣ 📜 .gitignore            # Keeps the repo clean of heavy datasets and __pycache__
 ┣ 📜 final show robot.mp4  # Showcase demonstration video
 ┣ 📜 hardware_bom.xlsx     # Bill of Materials (BOM) for the robotic chassis
 ┣ 📜 Presentation.pdf      # High-level slide deck summarizing the project engineering
 ┗ 📜 requirements.txt      # Python dependencies for the vision and control loop

```

---

## 🛠️ Getting Started

### 1. Prerequisites

* **Python 3.9+** (Tested on PyTorch 2.1 with CUDA 12.1 for RTX 3060).
* **PlatformIO** (For flashing the microcontroller).
* A generic ESP32 development board and 4x Yellow TT Motors with Mecanum wheels.

### 2. Software Installation

Clone the repository and install the required Python libraries using the provided requirements file:

```bash
git clone https://github.com/mudmini009/FRA361_Open_Topic.git
cd FRA361_Open_Topic
pip install -r requirements.txt

```

### 3. Hardware Setup (ESP32)

1. Navigate to `Code_Program/esp32/`.
2. Open the  `.cpp` firmware file in PlatformIO.
3. Connect your ESP32 via USB and upload the code.
4. Refer to `hardware_bom.xlsx` and the `CAD/` folder for assembly and wiring instructions.

### 4. Running the Aimbot

Ensure your Kovaak Aim Trainer window is open. Run the main execution loop:

```bash
cd Code_Program
python main.py

```

*Note: The script will prompt you to enter the name of the game window to bind the screen capture.*

---

## ⌨️ Controls & Modes

The system uses global keyboard hooks to allow mode switching even while the game is fully focused.

* **`Z`** : Quit application.
* **`X`** : Mode 0 (Idle / System Pause).
* **`C`** : Mode 1 (Aim Only - Tracks target but does not shoot).
* **`V`** : Mode 2 (Aim + Pulse Click - Tracks and automatically fires).

---

## 🧠 AI Models

The `models/` folder contains custom-trained YOLOv5 weights evaluated on a Tesla V100 server.

* **YOLOv5s (Small):** Best for high-speed tracking (~15ms inference).
* **YOLOv5m (Medium):** The recommended balance of accuracy and latency for PID tracking.
* **YOLOv5l (Large):** High precision, but introduces latency.
* *(Note: The YOLOv5x (X-Large) model was omitted from this repository due to file size limits and significant latency impacts >30ms that bottlenecked physical robot control)*.

---

🎓 Engineering & Academic Context

This system was originally developed and engineered as part of the **FRA361 - Open Topics** coursework within the Institute of Field Robotics (FIBO). Extensive research documentation regarding the physical prototyping iterations, empirical PWM deadzone calibrations, and dataset augmentation metrics can be found inside the `documentation/` folder and the accompanying `Presentation.pdf`.

* **Lead Engineer:** Pollapaat Suttimala
---

