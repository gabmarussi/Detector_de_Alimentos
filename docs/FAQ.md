# Frequently Asked Questions (FAQ)

## Installation and Setup

### Q: What are the minimum system requirements?

**A:**

- Python 3.8+
- 4GB RAM (8GB recommended)
- Working webcam
- Windows, Linux, or macOS
- ~500MB free disk space for dependencies

### Q: How do I install dependencies?

**A:**

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r camera\requirements.txt
```

### Q: Can I run without a virtual environment?

**A:** Yes, but it is not recommended. A virtual environment avoids dependency conflicts.

## Running the Project

### Q: How do I start the detector?

**A:** The simplest way:

```powershell
python camera\run.py --camera-id 0 --mode conveyor
```

### Q: What is the difference between conveyor and live modes?

**A:**

- **Live:** instant frame-by-frame detection with current frame counts.
- **Conveyor:** objects are counted when crossing a horizontal line; count is cumulative.

### Q: How do I choose which camera to use?

**A:** Use `--camera-id` with different values:

```powershell
# Primary webcam
python camera\run.py --camera-id 0

# Second camera (iPhone Continuity Camera, external webcam)
python camera\run.py --camera-id 1

# Third camera
python camera\run.py --camera-id 2
```

### Q: How do I adjust detection sensitivity?

**A:** Use `--conf` (0.0 to 1.0):

```powershell
# More sensitive (more detections, possible false positives)
python camera\run.py --conf 0.5

# Less sensitive (fewer detections, usually more reliable)
python camera\run.py --conf 0.8

# Default (balanced)
python camera\run.py --conf 0.7
```

### Q: Can I change the counting line position in conveyor mode?

**A:** Yes, use `--line-y` between 0.0 (top) and 1.0 (bottom):

```powershell
# Line in the center
python camera\run.py --mode conveyor --line-y 0.5

# Line lower on the frame (default)
python camera\run.py --mode conveyor --line-y 0.6
```

## Common Problems

### Q: "Could not open camera X"

**A:** Try these steps:

1. Close apps that are using the webcam (Teams, Zoom, etc.)
2. Try another camera ID: `--camera-id 1` or `--camera-id 2`
3. Check OS camera permissions
4. Restart your computer

### Q: "Trained model not found"

**A:** Check whether `detector/runs/train/weights/best.pt` exists. If not:

1. Ensure you are in the project root
2. Provide model path manually with `--model`

### Q: "Module not found" or "ImportError"

**A:**

1. Activate environment: `.\.venv\Scripts\Activate.ps1`
2. Reinstall dependencies: `pip install -r camera\requirements.txt`
3. Verify Python version: `python --version`

### Q: Detection is too slow (< 10 FPS)

**A:** Possible optimizations:

1. Close heavy background applications
2. Keep using a lightweight model (nano)
3. Reduce camera resolution in `common/constants.py`
4. Increase confidence threshold: `--conf 0.8`

### Q: Objects are counted multiple times

**A:** In conveyor mode, this can happen when:

1. The object crosses the line multiple times
2. Tracking loses IDs (increase `--min-label-votes 5`)

### Q: Detections "flicker" between classes

**A:** Increase label vote stabilization:

```powershell
python camera\run.py --min-label-votes 5
```

This requires 5 consistent frames before confirming a label.

## Advanced Usage

### Q: How do I use the detector in my own Python script?

**A:** Basic example:

```python
from camera.detector import FoodDetector

detector = FoodDetector("detector/runs/train/weights/best.pt", conf=0.7)

# Static image
counts = detector.predict_image("my_photo.jpg")
print(counts)

# Real-time webcam
detector.predict_webcam(camera_id=0, mode="live")
```

See [DEVELOPMENT.md](DEVELOPMENT.md) and [ARCHITECTURE.md](ARCHITECTURE.md) for implementation details.

### Q: Can I save detections to a file?

**A:** Yes:

```python
from camera.detector import FoodDetector

detector = FoodDetector("detector/runs/train/weights/best.pt")
counts = detector.predict_image("image.jpg")

with open("results.txt", "w") as f:
    f.write(str(dict(counts)))
```

### Q: How do I train a new model with more data?

**A:**

1. Collect and annotate new images (Roboflow)
2. Export in YOLO format
3. Update `detector/data.yaml`
4. Train with Ultralytics CLI:

```powershell
yolo detect train data=detector/data.yaml model=yolo11n.pt epochs=100
```

5. New weights will be generated under training output folders

### Q: Can I add new food classes?

**A:** Yes. See [DEVELOPMENT.md](DEVELOPMENT.md#1-add-a-new-food-class) for the full guide.

### Q: How do I integrate with an external API or database?

**A:** Use FoodDetector programmatically:

```python
from camera.detector import FoodDetector
import requests

detector = FoodDetector("model.pt")
counts = detector.predict_image("photo.jpg")

requests.post("https://my-api.com/detections", json=dict(counts))
```

## Performance

### Q: How many FPS can I get?

**A:** Depends on hardware:

- **GPU:** 30-60 FPS
- **Modern CPU (i5/i7):** 15-30 FPS
- **Older CPU:** 5-15 FPS

### Q: Can I use GPU acceleration?

**A:** Yes, if CUDA is available. PyTorch will detect it automatically.

```powershell
python -c "import torch; print(torch.cuda.is_available())"
```

### Q: What is memory usage like?

**A:** Approximate values:

- Loaded model: ~50MB
- Active webcam pipeline: ~200MB
- Total: ~300-400MB RAM

## Development

### Q: How can I contribute?

**A:** See [DEVELOPMENT.md](DEVELOPMENT.md) for environment setup, standards, and PR flow.

### Q: Can I use this code commercially?

**A:** Check the project license in [LICENSE](../LICENSE).

### Q: Where do I report bugs or suggest features?

**A:** Open a GitHub issue with:

- Clear problem/feature description
- Steps to reproduce (for bugs)
- Python version and OS
- Error logs (if available)

## Model and Dataset

### Q: Which YOLO model is used?

**A:** YOLO11 nano (`yolo11n`) as baseline, trained on a custom food dataset.

### Q: Which classes are detected?

**A:**

- Beans (`beans package`)
- Pasta (`pasta package`)
- Rice (`rice package`)

### Q: How many images are in the dataset?

**A:** Current dataset in this repository has 981 images in total according to Roboflow export metadata.

### Q: How do I check detailed training metrics?

**A:**

```powershell
python detector\summarize_results.py --csv detector\runs\train\results.csv
```

## Other Questions

### Q: Is it truly real-time?

**A:** Yes, with suitable hardware you can achieve real-time performance.

### Q: Can I use recorded videos instead of webcam?

**A:** Yes. Replace camera input with a video file in OpenCV:

```python
cap = cv2.VideoCapture("path/to/video.mp4")
```

### Q: Does it run on Raspberry Pi?

**A:** Yes, but with limited performance. Consider lower resolution and model optimization.

### Q: Do I need internet access to run it?

**A:** No, not after dependencies and model files are already installed locally.

### Q: How long does training take?

**A:** Depends on hardware:

- **NVIDIA GPU:** around 1-2 hours for 100 epochs
- **CPU only:** many hours to days

GPU platforms like Google Colab or Kaggle are recommended for training.
