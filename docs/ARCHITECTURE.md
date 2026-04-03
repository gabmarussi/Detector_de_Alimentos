# Project Architecture

## Overview

This project is a real-time food detector that uses YOLO (You Only Look Once) to identify three food product types: rice, beans, and pasta.

## Main Components

### 1. Camera (Inference)

Responsible for real-time model execution.

```
camera/
├── detector.py       # Main FoodDetector class
├── run.py            # Quick test script (with arguments)
├── requirements.txt  # Project dependencies
└── yolo11n.pt        # Base YOLO11 nano model
```

**FoodDetector** (`camera/detector.py`):

- Manages the loaded YOLO model
- Implements two operation modes:
  - **Live**: frame-by-frame detection without cumulative count
  - **Conveyor**: tracking with counting when objects cross the line
- Draws overlays with counters and status information
- Stabilizes detections using multi-frame label voting

### 2. Detector (Dataset and Training)

Contains the dataset and trained models.

```
detector/
├── data.yaml              # YOLO dataset configuration
├── data/                  # Organized data (separated from code)
│   ├── train/             # Training images (551 images)
│   ├── valid/             # Validation images (161 images)
│   └── test/              # Test images (80 images)
├── runs/train/            # Training outputs
│   ├── results.csv        # Metrics per epoch
│   ├── args.yaml          # Training arguments
│   └── weights/
│       ├── best.pt        # Best model by mAP
│       └── last.pt        # Latest checkpoint
└── summarize_results.py   # Training analysis utility
```

### 3. Common (Shared Code)

Utilities and constants used by multiple modules.

```
common/
├── __init__.py
├── constants.py      # Colors, names, default settings
└── model_utils.py    # Model path resolution helpers
```

### 4. Tools (Auxiliary Utilities)

Scripts for data collection and helper tasks.

```
tools/
└── webscrapping/
    ├── collect_images.py
    ├── collect_images_bing.py
    └── README.md
```

## Data Flow

### Conveyor Mode

```
┌──────────────┐
│   Webcam     │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│  FoodDetector.model  │
│   .track()           │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  ByteTrack           │
│  (tracking IDs)      │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Label Voting        │
│  (min_label_votes)   │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Crossing Detection  │
│  line_y              │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Cumulative Counter  │
│  + Overlay           │
└──────────────────────┘
```

**Characteristics:**

- Uses tracking (ByteTrack) to keep IDs consistent
- Stabilizes labels with multi-frame voting
- Counts only when an object crosses the line from top to bottom
- Prevents double counting with a set of already-counted IDs

### Live Mode

```
┌──────────────┐
│   Webcam     │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│  FoodDetector.model  │
│   .predict()         │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Per-Frame Count     │
│  (no tracking)       │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Instant Overlay     │
│  Counter             │
└──────────────────────┘
```

**Characteristics:**

- Does not use tracking
- Instant count per frame
- Simpler mode, ideal for demonstrations

## Technologies Used

### AI Framework

- **Ultralytics YOLO**: object detection framework
- **Model**: YOLO11 nano (`yolo11n.pt`) as baseline

### Image Processing

- **OpenCV (cv2)**: video capture and image processing
- **ByteTrack**: multi-object tracking algorithm

### Dataset

- **Roboflow**: dataset preparation platform
- **Format**: YOLO (`.txt` annotations)
- **Classes**: 3 (`beans package`, `pasta package`, `rice package`)

### Code Structure

- **Python 3.x**
- **Pathlib**: path handling
- **Collections**: `Counter`, `defaultdict`, `deque`
- **argparse**: CLI argument parsing

## Performance Optimizations

### Camera

```python
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)      # Minimal buffer
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Optimized resolution
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
```

### Model

- Uses nano model (`yolo11n`) for fast inference
- Configurable confidence threshold (default 0.7)
- `verbose=False` to reduce logs

### Tracking

- `persist=True` keeps IDs across frames
- `maxlen=10` in `deque` limits history memory
- Label voting avoids unstable class changes

## Extensibility

### Add a New Class

1. Train a new model with the additional class
2. Update `common/constants.py`:

   ```python
   DISPLAY_NAMES = {
       "beans package": "Beans",
       "pasta package": "Pasta",
       "rice package": "Rice",
       "new_class": "NewClass",  # Add here
   }

   CLASS_COLORS = {
       "Beans": (80, 180, 255),
       "Pasta": (110, 245, 140),
       "Rice": (255, 215, 120),
       "NewClass": (255, 100, 50),  # Add color
   }
   ```

3. Update overlays in `camera/detector.py` if needed

### Add a New Detection Mode

1. Implement a new method in `FoodDetector`
2. Add a CLI option in `camera/run.py` parser
3. Document it in `docs/HOW_TO_RUN.md`

### Integrate with External Systems

FoodDetector can be imported and used programmatically:

```python
from camera.detector import FoodDetector

detector = FoodDetector("model.pt", conf=0.7)
counts = detector.predict_image("image.jpg")

# Process counts as needed
# e.g., send to API, save to database, etc.
```
