# How To Run the Detector

Project structure at a glance:

- camera/ for real-time inference
- detector/ for dataset and trained model

## Option 1: VS Code (Play/Debug)

1. Open a file inside camera/.
2. Open Run and Debug.
3. Choose a launch configuration:
   - Detector - RUN.PY
   - Webcam MacBook
   - Continuity Camera (iPhone)
   - Current Model Test (RUN.PY)
4. Run and stop with q.

Note: configurations point to ../detector/runs/train/weights/best.pt.

## Option 2: Terminal (Windows PowerShell)

From project root:

```powershell
.\.venv\Scripts\Activate.ps1
python .\camera\run.py --camera-id 0 --mode conveyor
```

Using iPhone or a second camera:

```powershell
python .\camera\run.py --camera-id 1 --mode conveyor
```

Live mode (without line-based counting):

```powershell
python .\camera\run.py --camera-id 0 --mode live
```

Forcing a specific model weight:

```powershell
python .\camera\run.py --model .\detector\runs\train\weights\best.pt --camera-id 0 --mode conveyor
```

## Arguments (camera/run.py)

| Argument            | Description                             | Default  |
| ------------------- | --------------------------------------- | -------- |
| `--model`           | Path to custom `.pt` model              | Auto     |
| `--camera-id`       | Camera ID (0, 1, 2, ...)                | 0        |
| `--mode`            | Mode (`conveyor` / `live`)              | conveyor |
| `--conf`            | Minimum confidence (0.0-1.0)            | 0.7      |
| `--line-y`          | Line position (0.0-1.0)                 | 0.6      |
| `--min-label-votes` | Frames required to stabilize detection  | 3        |

## Training Summary Without Reading CSV Manually

From project root:

```powershell
python .\detector\summarize_results.py --csv .\detector\runs\train\results.csv
```

Additional options:

```powershell
# Sort by best mAP50-95 epochs
python .\detector\summarize_results.py --metric "metrics/mAP50-95(B)"

# Show top 10 epochs
python .\detector\summarize_results.py --top-k 10
```

## Quick Troubleshooting

- Camera error:
  - Close apps currently using the webcam.
  - Try camera-id 0, 1, and 2.
- Module not found:
  - Activate .venv before running.
- Model not found:
  - Check if detector/runs/train/weights/best.pt exists.
