from pathlib import Path

from detector import FoodDetector


def main():
    model_path = Path(__file__).resolve().parent.parent / "runs" / "food-v6-local" / "weights" / "best.pt"
    if not model_path.exists():
        raise FileNotFoundError(f"Modelo nao encontrado: {model_path}")

    detector = FoodDetector(str(model_path), conf=0.7)
    detector.predict_webcam(camera_id=0)


if __name__ == "__main__":
    main()
