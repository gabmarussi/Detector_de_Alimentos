# Project Documentation

## Folder Structure

```text
Detector de Alimentos/
|- camera/                       # real-time inference
|  |- detector.py                # FoodDetector class
|  |- run.py                     # main run script
|  |- requirements.txt
|  `- yolo11n.pt
|- detector/                     # dataset + trained model
|  |- data.yaml
|  |- train/                     # 551 images
|  |- valid/                     # 161 images
|  |- test/                      # 80 images
|  `- runs/train/
|     |- results.csv             # metrics per epoch
|     `- weights/
|        |- best.pt              # main model
|        `- last.pt              # latest checkpoint
|- common/
|  |- constants.py               # colors, names, settings
|  `- model_utils.py             # model path resolution
|- docs/
|- tools/webscrapping/           # image collection scripts
|- README.md
`- .vscode/launch.json
```

## Main Components

- camera/run.py: camera execution script
- camera/detector.py: main detection class
- detector/runs/train/weights/best.pt: default model used for inference

## Dataset and Model

- Framework: Ultralytics YOLOv11 nano
- Dataset: Roboflow v8 (981 images)
- Classes: beans package (283), pasta package (259), rice package (262)
- Negative samples: 191 images
- Split: 60% train (589) / 20% valid (196) / 20% test (196)

## Metrics

Roboflow (Test Set, Industry Standard off):
- Precision: 93.7%
- Recall: 69.8%
- mAP@50: 76.2%

Google Colab (Validation Set, epoch 200):
- Precision: 90.25%
- Recall: 70.44%
- mAP@50: 71.79%
- mAP@50-95: 62.73%

## Operating Modes

- conveyor: line-based counting with tracking
- live: instant frame-by-frame detection without cumulative counting

## Useful Commands

Show training metrics:
```powershell
python detector\summarize_results.py
```

Run detector:
```powershell
python camera\run.py --camera-id 0 --mode conveyor
```
