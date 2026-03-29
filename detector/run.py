import argparse
from pathlib import Path

from detector import FoodDetector


def parse_args():
    parser = argparse.ArgumentParser(description="Executa detector com modelo v6 ou v7")
    parser.add_argument("--version", choices=["v6", "v7"], default="v7")
    parser.add_argument("--camera-id", type=int, default=0)
    parser.add_argument("--conf", type=float, default=0.7)
    parser.add_argument("--mode", choices=["conveyor", "live"], default="conveyor")
    parser.add_argument("--line-y", type=float, default=0.6)
    parser.add_argument("--min-label-votes", type=int, default=3)
    return parser.parse_args()


def resolve_model_path(version: str) -> Path:
    root = Path(__file__).resolve().parent.parent
    candidates = {
        "v6": [
            root / "runs" / "food-v6-local" / "weights" / "best.pt",
            root / "versions" / "v6" / "best.pt",
            root / "detectors" / "runs" / "food-v6-local" / "weights" / "best.pt",
            root / "detectors" / "versions" / "v6" / "best.pt",
        ],
        "v7": [
            root / "runs" / "food-v7-local" / "weights" / "best.pt",
            root / "versions" / "v7" / "best.pt",
            root / "detectors" / "runs" / "food-v7-local" / "weights" / "best.pt",
            root / "detectors" / "versions" / "v7" / "best.pt",
        ],
    }

    for path in candidates[version]:
        if path.exists():
            return path

    searched = "\n".join(str(p) for p in candidates[version])
    raise FileNotFoundError(
        f"Modelo {version} nao encontrado. Caminhos verificados:\n{searched}"
    )


def main():
    args = parse_args()
    model_path = resolve_model_path(args.version)

    detector = FoodDetector(str(model_path), conf=args.conf)
    detector.predict_webcam(
        camera_id=args.camera_id,
        mode=args.mode,
        line_y_ratio=args.line_y,
        min_label_votes=args.min_label_votes,
    )


if __name__ == "__main__":
    main()
