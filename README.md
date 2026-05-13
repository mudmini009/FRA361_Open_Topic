
# 🎯 Virtual Aimbot — Software-Only FPS Aim Assistant

A software-based aimbot that uses real-time **YOLOv5** object detection to move your mouse cursor onto targets automatically. Originally built as a physical robot aimbot for a university thesis, now refactored into a clean Windows executable.

Tested in **KovaaK's Aim Trainer** (103° FOV, 800 DPI, 33 cm/360°).

> 💡 Looking for the original **hardware robot** version? Switch to the [`main`](https://github.com/mudmini009/FRA361_Open_Topic/tree/main) branch.

---

## ✨ Features

- **YOLOv5m** real-time target detection at 640px inference
- **Perspective-correct** DPI/sensitivity math — no overshoot at screen edges
- **Three modes:** Idle, Track (aim only), Flick + Click (aim & auto-fire)
- **Pulse-click** system with configurable timing
- **On-screen display (OSD)** showing current mode + hotkeys
- **Post-session plots** for dx/dy error analysis
- **Single `.exe`** build via PyInstaller (GitHub Actions CI)

---

## ⌨️ Hotkeys

| Key | Action |
|-----|--------|
| `X` | Mode 0 — **IDLE** (no aim, no click) |
| `C` | Mode 1 — **TRACK** (aim follows target, no click) |
| `V` | Mode 2 — **FLICK + CLICK** (aim & auto-fire) |
| `F9` | **Pause / Resume** |
| `Z` | **Quit** and save logs |

---

## 📁 Project Structure

```text
📦 FRA361_Open_Topic (software-only branch)
 ┣ 📂 Code_Program/         # Main source code
 ┃  ┣ main.py               # Entry point
 ┃  ┣ config.py              # DPI, sensitivity, FOV, model settings
 ┃  ┣ capture.py             # Window selection + MSS screen capture
 ┃  ┣ detect.py              # YOLOv5 model loading + inference
 ┃  ┣ annotator.py           # Aim overlay + OSD rendering
 ┃  ┣ mouse_mover.py         # Pixel error → raw mouse counts (win32api)
 ┃  ┣ clicker.py             # Pulse-click logic (win32api)
 ┃  ┣ control.py             # Hotkey / mode / pause logic
 ┃  ┣ distance.py            # Geometric helpers
 ┃  ┣ logger.py              # Per-frame CSV logging
 ┃  ┗ plotter.py             # Matplotlib session plots
 ┣ 📂 models/                # Trained YOLOv5 weights (.pt)
 ┣ 📂 archive/               # Old hardware robot code, CAD, docs, presentations
 ┣ 📂 .github/workflows/     # GitHub Actions: auto-build Windows .exe
 ┗ 📜 requirements.txt       # Python dependencies
```

---

## 🚀 Quick Start

### Option A: Download the `.exe` (no install needed)

1. Go to [**Actions → Build Windows EXE**](https://github.com/mudmini009/FRA361_Open_Topic/actions)
2. Click the latest green ✅ run
3. Download the **VirtualAimbot** artifact at the bottom
4. Unzip → run `VirtualAimbot.exe` on your gaming PC

### Option B: Run from source

```bash
# 1. Create environment
conda create -n aimbot python=3.10 -y
conda activate aimbot

# 2. Install PyTorch (with CUDA for GPU)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
cd Code_Program
python main.py
```

---

## ⚙️ Configuration

Edit `Code_Program/config.py` to match your setup:

```python
MOUSE_DPI      = 800       # your mouse DPI
CM_PER_360     = 33.0      # cm of mousepad for a full 360°
GAME_FOV       = 103.0     # horizontal FOV (103 = Overwatch/KovaaK default)
AIM_SPEED      = 1.0       # 1.0 = instant snap, 0.3 = smooth tracking
PIXEL_DEADZONE = 5         # ignore tiny movements (px)
CONFIDENCE     = 0.23      # YOLO detection threshold
```

### Common FOV values

| Game | FOV |
|------|-----|
| Overwatch / KovaaK's | 103° |
| Valorant | 103° |
| CS2 | 106.26° (at 16:9) |
| Apex Legends | 110° (max) |

---

## 🧠 AI Models

Custom-trained YOLOv5 weights in `models/`:

| Model | File | Speed | Use case |
|-------|------|-------|----------|
| YOLOv5s | `model1(y5s)/` | ~15ms | Fast tracking |
| **YOLOv5m** | `model3(y5m)/` | ~25ms | **Recommended** — best accuracy/speed balance |
| YOLOv5l | `model4(y5l)/` | ~40ms | High precision, slower |

---

## 🎓 Origin

Originally built as a **physical Mecanum-wheeled robot** that moved a real mouse for the **FRA361 — Open Topics** course at FIBO, KMUTT. The original hardware code and demo are on the [`main`](https://github.com/mudmini009/FRA361_Open_Topic/tree/main) branch. Old files kept here in `archive/` for reference.

**Author:** Pollapaat Suttimala

---
