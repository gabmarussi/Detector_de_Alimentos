import argparse
from pathlib import Path

from detector import FoodDetector


def parse_args():
    parser = argparse.ArgumentParser(description="Executa detector com YOLOv11")
    parser.add_argument("--camera-id", type=int, default=0)
    parser.add_argument("--conf", type=float, default=0.7)
    parser.add_argument("--mode", choices=["conveyor", "live"], default="conveyor")
    parser.add_argument("--line-y", type=float, default=0.6)
    parser.add_argument("--min-label-votes", type=int, default=3)
    return parser.parse_args()


def resolve_model_path() -> Path:
    root = Path(__file__).resolve().parent.parent
    candidates = [
        root / "detectors" / "versions" / "v8" / "best.pt",
        root / "detectors" / "runs" / "food-v8-local" / "weights" / "best.pt",
    ]

    for path in candidates:
        if path.exists():
            return path

    searched = "\n".join(str(p) for p in candidates)
    raise FileNotFoundError(
        f"Modelo YOLOv11 nao encontrado. Caminhos verificados:\n{searched}"
    )


def main():
    args = parse_args()
    model_path = resolve_model_path()

    detector = FoodDetector(str(model_path), conf=args.conf)
    detector.predict_webcam(
        camera_id=args.camera_id,
        mode=args.mode,
        line_y_ratio=args.line_y,
        min_label_votes=args.min_label_votes,
    )


if __name__ == "__main__":
    main()
