# Development and Contribution

## Development Environment Setup

### 1. Clone the Repository

```powershell
git clone <repository-url>
cd "Detector de Alimentos"
```

### 2. Create a Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r camera\requirements.txt
```

### 4. Verify Installation

**Option A: Interactive Menu (Recommended)**

```powershell
python main.py
```

**Option B: Quick Test**

```powershell
python camera\run.py --camera-id 0 --mode live
```

## Commit Structure

Follow semantic commit conventions:

- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation updates
- `refactor:` code refactoring
- `test:` adding or updating tests
- `chore:` maintenance tasks

**Examples:**

```
feat: add batch detection mode
fix: avoid duplicate counting in conveyor mode
docs: update API documentation
refactor: extract overlay logic into helper method
```

## Testing Changes

### Basic Manual Testing

1. **Live mode (instant detection):**

   ```powershell
   python camera\run.py --camera-id 0 --mode live
   ```

2. **Conveyor mode (with counting):**

   ```powershell
   python camera\run.py --camera-id 0 --mode conveyor --line-y 0.6
   ```

3. **Static image test:**
   ```powershell
   # In the interactive menu, choose option 2
   python camera\run.py
   ```

### Model Validation

Check training metrics:

```powershell
python detector\summarize_results.py --csv detector\runs\train\results.csv
```

## Style Guide

### Python

Use PEP 8 with lightweight adaptations:

- **Indentation:** 4 spaces
- **Max line length:** 100 characters (preferred)
- **Imports:** grouped as stdlib, third-party, local
- **Docstrings:** Google style for public classes/functions

### Naming

- **Variables and functions:** `snake_case`
- **Classes:** `PascalCase`
- **Constants:** `UPPER_SNAKE_CASE`
- **Files:** `snake_case.py`

## Adding New Features

### 1. Add a New Food Class

**Step 1:** Prepare dataset

- Collect images for the new class
- Annotate with Roboflow or a similar tool
- Export in YOLO format

**Step 2:** Retrain model

```powershell
# Update detector/data.yaml with the new class
# Train with Ultralytics
```

**Step 3:** Update constants

```python
# common/constants.py
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
    "NewClass": (200, 100, 255),  # Add BGR color
}
```

**Step 4:** Update overlays (if needed)

```python
# camera/detector.py
# Update _draw_counts() and _draw_conveyor_overlay()
# to include the new class in the UI
```

### 2. Add a New Operating Mode

**Example: Snapshot mode (periodic capture)**

**Step 1:** Implement in FoodDetector

```python
# camera/detector.py
def predict_snapshot(self, camera_id: int = 0, interval: int = 5):
    """Capture and analyze every N seconds."""
    cap = cv2.VideoCapture(camera_id)
    last_capture = 0

    while True:
        current_time = time.time()
        if current_time - last_capture >= interval:
            ok, frame = cap.read()
            if ok:
                result = self.model.predict(frame, conf=self.conf)
                counts = self._count(result)
                print(f"Snapshot: {dict(counts)}")
                last_capture = current_time

        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

    cap.release()
```

**Step 2:** Add parser arguments

```python
# camera/run.py
parser.add_argument("--mode", choices=["conveyor", "live", "snapshot"], default="conveyor")
parser.add_argument("--snapshot-interval", type=int, default=5)
```

**Step 3:** Document it

```markdown
# docs/HOW_TO_RUN.md

## Snapshot Mode

python camera\run.py --mode snapshot --snapshot-interval 10
```

## Debugging

### Common Issues

**1. Model not found:**

```
FileNotFoundError: Trained model not found
```

**Solution:** Check whether detector/runs/train/weights/best.pt exists.

**2. Camera does not open:**

```
RuntimeError: Could not open camera 0
```

**Solution:**

- Close other apps using the webcam
- Try another camera-id (1, 2, etc.)
- Check camera permissions in your OS

**3. Unstable tracking:**

```
# IDs frequently change between frames
```

**Solution:** increase `--min-label-votes` to stabilize labels:

```powershell
python camera\run.py --min-label-votes 5
```

### Debug Tools

**1. YOLO verbose output:**

```python
# Temporarily remove verbose=False
result = self.model.predict(source=frame, conf=self.conf, verbose=True)[0]
```

**2. Save problematic frames:**

```python
# Add in camera/detector.py
cv2.imwrite(f"debug_frame_{time.time()}.jpg", frame)
```

**3. Tracking logs:**

```python
# Add debug prints in tracking loop
print(f"Track ID: {track_id}, Label: {label}, Y: {cy}, Line: {line_y}")
```

## Performance

### Existing Optimizations

1. **Minimal camera buffer:** `cv2.CAP_PROP_BUFFERSIZE = 1`
2. **Optimized resolution:** 1280x720
3. **Nano model:** `yolo11n` for fast inference
4. **Limited deque:** `maxlen=10` for label history

### Benchmarking

To measure FPS:

```python
import time

frame_count = 0
start_time = time.time()

while True:
    # ... inference loop ...
    frame_count += 1

    if frame_count % 30 == 0:
        elapsed = time.time() - start_time
        fps = frame_count / elapsed
        print(f"FPS: {fps:.2f}")
```

### When to Optimize

- FPS < 15: reduce resolution or use a smaller model
- FPS > 30: already excellent for most scenarios
- High latency: inspect tracking and post-processing steps

## Contributing

1. Fork the repository
2. Create a branch for your feature (`git checkout -b feat/new-feature`)
3. Commit your changes (`git commit -m 'feat: add new feature'`)
4. Push your branch (`git push origin feat/new-feature`)
5. Open a Pull Request

### PR Checklist

- [ ] Code tested manually
- [ ] Documentation updated (if applicable)
- [ ] Commits follow semantic convention
- [ ] No hardcoded local paths
- [ ] Constants extracted into common/constants.py when needed

## Additional Resources

- [Ultralytics YOLO Docs](https://docs.ultralytics.com/)
- [OpenCV Python Tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [Roboflow Documentation](https://docs.roboflow.com/)
- [ByteTrack Paper](https://arxiv.org/abs/2110.06864)
