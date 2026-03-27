import argparse
from collections import Counter

import cv2
from ultralytics import YOLO


CLASS_NAMES = {
	0: "beans_package",
	1: "pasta_package",
	2: "rice_package",
}


def draw_counts(frame, counts):
	y = 30
	for class_name in ["beans_package", "pasta_package", "rice_package"]:
		value = counts.get(class_name, 0)
		cv2.putText(
			frame,
			f"{class_name}: {value}",
			(20, y),
			cv2.FONT_HERSHEY_SIMPLEX,
			0.8,
			(0, 255, 0),
			2,
			cv2.LINE_AA,
		)
		y += 30


def predict_image(model, image_path):
	result = model.predict(source=image_path, conf=0.4, verbose=False)[0]
	counts = Counter()

	if result.boxes is not None and len(result.boxes) > 0:
		for box in result.boxes:
			class_id = int(box.cls[0])
			class_name = CLASS_NAMES.get(class_id, f"class_{class_id}")
			counts[class_name] += 1

	print("Contagem detectada:")
	for class_name in ["beans_package", "pasta_package", "rice_package"]:
		print(f"- {class_name}: {counts.get(class_name, 0)}")

	plotted = result.plot()
	draw_counts(plotted, counts)
	cv2.imshow("Deteccao", plotted)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


def predict_webcam(model, camera_id=0):
	cap = cv2.VideoCapture(camera_id)
	if not cap.isOpened():
		raise RuntimeError("Nao foi possivel abrir a webcam.")

	while True:
		ok, frame = cap.read()
		if not ok:
			break

		result = model.predict(source=frame, conf=0.4, verbose=False)[0]
		counts = Counter()

		if result.boxes is not None and len(result.boxes) > 0:
			for box in result.boxes:
				class_id = int(box.cls[0])
				class_name = CLASS_NAMES.get(class_id, f"class_{class_id}")
				counts[class_name] += 1

		plotted = result.plot()
		draw_counts(plotted, counts)

		cv2.imshow("YOLOv8 - Contagem", plotted)
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break

	cap.release()
	cv2.destroyAllWindows()


def parse_args():
	parser = argparse.ArgumentParser(description="Deteccao e contagem com YOLOv8")
	parser.add_argument(
		"--model",
		type=str,
		required=True,
		help="Caminho do modelo treinado (ex.: runs/detect/train/weights/best.pt)",
	)
	parser.add_argument(
		"--source",
		type=str,
		default="webcam",
		help="'webcam' para camera ao vivo ou caminho de imagem",
	)
	parser.add_argument("--camera-id", type=int, default=0)
	return parser.parse_args()


def main():
	args = parse_args()
	model = YOLO(args.model)

	if args.source.lower() == "webcam":
		predict_webcam(model, args.camera_id)
	else:
		predict_image(model, args.source)


if __name__ == "__main__":
	main()
