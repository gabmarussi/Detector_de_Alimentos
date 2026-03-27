import argparse
from collections import Counter

import cv2
from ultralytics import YOLO


DISPLAY_NAMES = {
    "beans package": "Feijao",
    "pasta package": "Macarrao",
    "rice package": "Arroz",
    "beans_package": "Feijao",
    "pasta_package": "Macarrao",
    "rice_package": "Arroz",
}


class FoodDetector:
    def __init__(self, model_path: str, conf: float = 0.7):
        self.model = YOLO(model_path)
        self.conf = conf

    def _label(self, class_id: int) -> str:
        raw = self.model.names.get(class_id, str(class_id))
        return DISPLAY_NAMES.get(raw, raw)

    def _count(self, result) -> Counter:
        counts = Counter()
        if result.boxes is None:
            return counts
        for box in result.boxes:
            class_id = int(box.cls[0])
            counts[self._label(class_id)] += 1
        return counts

    def _draw_counts(self, frame, counts: Counter):
        y = 30
        for name in ["Feijao", "Macarrao", "Arroz"]:
            cv2.putText(
                frame,
                f"{name}: {counts.get(name, 0)}",
                (20, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )
            y += 30
        return frame

    def predict_image(self, image_path: str):
        result = self.model.predict(source=image_path, conf=self.conf, verbose=False)[0]
        counts = self._count(result)
        frame = self._draw_counts(result.plot(), counts)
        print(dict(counts))
        cv2.imshow("Deteccao", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def predict_webcam(self, camera_id: int = 0):
        cap = cv2.VideoCapture(camera_id)
        if not cap.isOpened():
            raise RuntimeError(f"Nao foi possivel abrir camera {camera_id}")

        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        while True:
            ok, frame = cap.read()
            if not ok:
                continue

            result = self.model.predict(source=frame, conf=self.conf, verbose=False)[0]
            counts = self._count(result)
            shown = self._draw_counts(result.plot(), counts)

            cv2.imshow("Detector", shown)
            if (cv2.waitKey(1) & 0xFF) == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--source", default="webcam")
    parser.add_argument("--camera-id", type=int, default=0)
    parser.add_argument("--conf", type=float, default=0.7)
    return parser.parse_args()


def main():
    args = parse_args()
    detector = FoodDetector(args.model, args.conf)
    if args.source.lower() == "webcam":
        detector.predict_webcam(args.camera_id)
    else:
        detector.predict_image(args.source)


if __name__ == "__main__":
    main()
