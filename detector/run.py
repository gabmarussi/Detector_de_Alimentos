import argparse
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from camera.detector import FoodDetector
from common.constants import DEFAULT_CONFIDENCE, DEFAULT_LINE_Y_RATIO, DEFAULT_MIN_LABEL_VOTES
from common.model_utils import resolve_best_model


def parse_args():
    parser = argparse.ArgumentParser(
        description="Use 'python camera/run.py' como script principal."
    )
    parser.add_argument("--camera-id", type=int, default=0)
    parser.add_argument("--conf", type=float, default=DEFAULT_CONFIDENCE)
    parser.add_argument("--mode", choices=["conveyor", "live"], default="conveyor")
    parser.add_argument("--line-y", type=float, default=DEFAULT_LINE_Y_RATIO)
    parser.add_argument("--min-label-votes", type=int, default=DEFAULT_MIN_LABEL_VOTES)
    return parser.parse_args()


def main():
    print("NOTA: Use 'python camera/run.py' como script principal.")
    print("Continuando execucao...\n")
    
    args = parse_args()
    
    try:
        model_path = resolve_best_model()
        print(f"Usando modelo: {model_path}\n")
    except FileNotFoundError as e:
        print(f"Erro: {e}")
        return

    detector = FoodDetector(str(model_path), conf=args.conf)
    detector.predict_webcam(
        camera_id=args.camera_id,
        mode=args.mode,
        line_y_ratio=args.line_y,
        min_label_votes=args.min_label_votes,
    )


if __name__ == "__main__":
    main()
