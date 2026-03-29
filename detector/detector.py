import argparse
from collections import Counter
from collections import defaultdict
from collections import deque

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

    def _draw_conveyor_overlay(self, frame, totals: Counter, line_y: int):
        h, w = frame.shape[:2]
        cv2.line(frame, (0, line_y), (w, line_y), (0, 255, 255), 2)
        cv2.putText(
            frame,
            "Linha de contagem",
            (20, max(20, line_y - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )

        y = 30
        for name in ["Feijao", "Macarrao", "Arroz"]:
            cv2.putText(
                frame,
                f"Total {name}: {totals.get(name, 0)}",
                (20, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 200, 0),
                2,
                cv2.LINE_AA,
            )
            y += 30

        cv2.putText(
            frame,
            f"Qtd total: {sum(totals.values())}",
            (20, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 200, 0),
            2,
            cv2.LINE_AA,
        )
        return frame

    def _stable_label(self, labels: deque, min_votes: int) -> str | None:
        if not labels:
            return None
        voted = Counter(labels).most_common(1)[0]
        if voted[1] >= min_votes:
            return voted[0]
        return None

    def predict_image(self, image_path: str):
        result = self.model.predict(source=image_path, conf=self.conf, verbose=False)[0]
        counts = self._count(result)
        frame = self._draw_counts(result.plot(), counts)
        print(dict(counts))
        cv2.imshow("Deteccao", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def predict_webcam(
        self,
        camera_id: int = 0,
        mode: str = "conveyor",
        line_y_ratio: float = 0.6,
        min_label_votes: int = 3,
    ):
        cap = cv2.VideoCapture(camera_id)
        if not cap.isOpened():
            raise RuntimeError(f"Nao foi possivel abrir camera {camera_id}")

        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        totals = Counter()
        track_labels = defaultdict(lambda: deque(maxlen=10))
        track_last_y = {}
        counted_ids = set()

        while True:
            ok, frame = cap.read()
            if not ok:
                continue

            if mode == "conveyor":
                result = self.model.track(
                    source=frame,
                    conf=self.conf,
                    persist=True,
                    verbose=False,
                    tracker="bytetrack.yaml",
                )[0]
            else:
                result = self.model.predict(source=frame, conf=self.conf, verbose=False)[0]

            counts = self._count(result)
            shown = result.plot()

            if mode == "conveyor":
                h = shown.shape[0]
                line_y = int(h * line_y_ratio)

                if result.boxes is not None and result.boxes.id is not None:
                    for box, track_id_tensor in zip(result.boxes, result.boxes.id):
                        track_id = int(track_id_tensor.item())
                        class_id = int(box.cls[0])
                        label = self._label(class_id)
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        cy = int((y1 + y2) / 2)

                        track_labels[track_id].append(label)
                        stable = self._stable_label(track_labels[track_id], min_label_votes)
                        prev_y = track_last_y.get(track_id)
                        track_last_y[track_id] = cy

                        # Conta apenas quando o centro cruza a linha de cima para baixo.
                        if (
                            stable is not None
                            and prev_y is not None
                            and track_id not in counted_ids
                            and prev_y < line_y <= cy
                        ):
                            totals[stable] += 1
                            counted_ids.add(track_id)

                shown = self._draw_conveyor_overlay(shown, totals, line_y)
            else:
                shown = self._draw_counts(shown, counts)

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
    parser.add_argument("--mode", choices=["conveyor", "live"], default="conveyor")
    parser.add_argument("--line-y", type=float, default=0.6)
    parser.add_argument("--min-label-votes", type=int, default=3)
    return parser.parse_args()


def main():
    args = parse_args()
    detector = FoodDetector(args.model, args.conf)
    if args.source.lower() == "webcam":
        detector.predict_webcam(
            camera_id=args.camera_id,
            mode=args.mode,
            line_y_ratio=args.line_y,
            min_label_votes=args.min_label_votes,
        )
    else:
        detector.predict_image(args.source)


if __name__ == "__main__":
    main()
