# Food Detector - YOLO

Real-time object detection system for food products (rice, beans, and pasta) using YOLO11 and OpenCV.

## 🎯 Features

- **Real-time detection** via webcam with YOLO11 nano
- **Two operating modes:**
  - 🎥 **Live:** frame-by-frame detection without cumulative counting
  - 📦 **Conveyor:** conveyor-style mode with tracking and object counting
- **Smart tracking** with ByteTrack for persistent IDs
- **Visual interface** with overlays and counters
- **Detection stabilization** through multi-frame label voting

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- An available webcam
- Windows (tested), Linux, or macOS

### Installation

1. **Clone the repository (if needed)**

   ```powershell
   cd "Detector de Alimentos"
   ```

2. **Create and activate a virtual environment:**

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r camera\requirements.txt
   ```

### Quick Run

**Main Menu (recommended):**

```powershell
python main.py
```

It opens an interactive menu with these options:

```
0️⃣  📹 Camera (real-time detection)
1️⃣  📷 Photo (capture from webcam)
2️⃣  🖼️  Saved File (image from disk)
q️  ❌ Exit
```

The script guides you through:

- Detection in **Conveyor** mode (line-based counting) or **Live** mode (simple)
- Selecting an available camera
- Analyzing images saved on disk

### Quick Test Script

For fast tests with command-line arguments:

```powershell
# Default test (conveyor mode)
python camera\run.py

# Live mode with a specific camera
python camera\run.py --mode live --camera-id 1

# Change confidence threshold
python camera\run.py --conf 0.5

# Show all arguments
python camera\run.py --help
```

**Available arguments for `camera/run.py`:**

| Argument            | Description                             | Default  |
| ------------------- | --------------------------------------- | -------- |
| `--model`           | Path to a custom `.pt` model            | Auto     |
| `--camera-id`       | Camera ID (0, 1, 2, ...)                | 0        |
| `--mode`            | Mode (`conveyor` / `live`)              | conveyor |
| `--conf`            | Minimum confidence (0.0-1.0)            | 0.7      |
| `--line-y`          | Counting line position (0.0-1.0)        | 0.6      |
| `--min-label-votes` | Frames required to stabilize detection  | 3        |

## 📁 Project Structure

```text
Detector de Alimentos/
├── main.py                    # 🍽️ Main interactive menu
│
├── camera/                    # Inference application
│   ├── detector.py            # FoodDetector class
│   ├── run.py                 # Quick test script (with args)
│   ├── requirements.txt       # Project dependencies
│   └── yolo11n.pt             # Base YOLO11 nano model
│
├── detector/                  # Dataset and trained model
│   ├── data.yaml              # Dataset configuration (updated paths)
│   ├── data/                  # Organized data (code separated from data)
│   │   ├── train/             # 551 training images
│   │   │   └── images/, labels/
│   │   ├── valid/             # 161 validation images
│   │   │   └── images/, labels/
│   │   └── test/              # 80 test images
│   │       └── images/, labels/
│   ├── runs/train/            # Training results
│   │   ├── results.csv        # Metrics per epoch
│   │   └── weights/
│   │       ├── best.pt        # Best model (default)
│   │       └── last.pt        # Last checkpoint
│   └── summarize_results.py   # Metrics analysis utility
│
├── common/                    # Shared code
│   ├── constants.py           # Constants and configuration
│   └── model_utils.py         # Model utilities
│
├── docs/                      # Full documentation
│   ├── HOW_TO_RUN.md          # Detailed run guide
│   ├── DOCUMENTATION.md       # General documentation
│   ├── ARCHITECTURE.md        # Technical architecture
│   ├── DEVELOPMENT.md         # Development guide
│   ├── FAQ.md                 # Frequently asked questions
│   └── README.md              # Documentation index
│
└── tools/                     # Helper tools
    └── webscrapping/          # Image collection scripts
```

**Structural Updates (v2025):**

- ✨ **[main.py](main.py)** - user-focused interactive menu (recommended)
- 🔧 **[camera/run.py](camera/run.py)** - quick argument-based test script (development)
- 📦 **`detector/data/`** - organized data split (train/valid/test)
- 🔒 **`.gitignore`** - updated to ignore `runs/` and `*.pt` models

## 📊 Model Metrics (v8)

**Dataset:**

- Classes: `beans package`, `pasta package`, `rice package`
- Total: 981 images (589 train / 196 valid / 196 test)
- Negative samples: 191 images (to reduce false positives)
- Source: Roboflow

**Performance (Google Colab, 200 epochs - Validation):**

- Precision: 90.25%
- Recall: 70.44%
- mAP50: 71.79%

**Performance (Roboflow - Test Set):**

- Precision: 93.7%
- Recall: 69.8%
- mAP50: 76.2%

**Analyze detailed metrics:**

```powershell
python detector\summarize_results.py --csv detector\runs\train\results.csv
```

## 🔧 Programmatic Usage

```python
from camera.detector import FoodDetector
from pathlib import Path

# Initialize detector
model_path = Path("detector/runs/train/weights/best.pt")
detector = FoodDetector(str(model_path), conf=0.7)

# Image detection
counts = detector.predict_image("test.jpg")
print(f"Detected: {dict(counts)}")

# Real-time webcam detection
detector.predict_webcam(camera_id=0, mode="conveyor")
```

## 🛠️ Technologies

- **[Ultralytics YOLO](https://github.com/ultralytics/ultralytics)** - object detection framework
- **[OpenCV](https://opencv.org/)** - image and video processing
- **[ByteTrack](https://github.com/ifzhang/ByteTrack)** - multi-object tracking algorithm
- **Python 3.8+** - programming language

## 📖 Documentation

- **[How To Run](docs/HOW_TO_RUN.md)** - complete execution guide
- **[Project Documentation](docs/DOCUMENTATION.md)** - folder and file organization
- **[Architecture](docs/ARCHITECTURE.md)** - system design and data flow
- **[Development Guide](docs/DEVELOPMENT.md)** - contribution and coding standards
- **[FAQ](docs/FAQ.md)** - common questions and troubleshooting
