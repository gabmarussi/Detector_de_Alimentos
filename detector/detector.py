"""
Detector de Alimentos - YOLOv8

Sistema de detecção e contagem de embalagens de alimentos (arroz, feijão e macarrão)
usando visão computacional com modelo YOLO treinado.

Autores: Gabriel Marussi
Data: Março 2026
"""

import argparse
from collections import Counter
from typing import Dict, Tuple

import cv2
from ultralytics import YOLO


# ==================== Configurações ====================
CLASS_NAMES: Dict[int, str] = {
    0: "beans_package",
    1: "pasta_package",
    2: "rice_package",
}

# Nomes para exibição amigável
DISPLAY_NAMES: Dict[str, str] = {
    "beans_package": "Feijão",
    "pasta_package": "Macarrão",
    "rice_package": "Arroz",
}

# Constantes de visualização
CONFIDENCE_THRESHOLD = 0.6  # Aumentado para reduzir falsos positivos
TEXT_FONT = cv2.FONT_HERSHEY_SIMPLEX
TEXT_SCALE = 0.8
TEXT_THICKNESS = 2
TEXT_COLOR = (0, 255, 0)  # Verde em BGR
TEXT_Y_START = 30
TEXT_Y_OFFSET = 30


# ==================== Classe Principal ====================
class FoodDetector:
    """Detector de embalagens de alimentos usando YOLO."""

    def __init__(self, model_path: str, confidence: float = CONFIDENCE_THRESHOLD):
        """
        Inicializa o detector com um modelo YOLO.

        Args:
            model_path: Caminho para o arquivo de pesos do modelo (.pt)
            confidence: Threshold de confiança para detecções (0-1)
        """
        self.model = YOLO(model_path)
        self.confidence = confidence
        self.class_names = CLASS_NAMES

    def detect(self, source) -> Tuple[object, Counter]:
        """
        Realiza detecção em uma imagem ou frame.

        Args:
            source: Imagem (numpy array) ou caminho da imagem

        Returns:
            Tupla com (resultado YOLO, contagem de classes)
        """
        result = self.model.predict(
            source=source, 
            conf=self.confidence, 
            verbose=False
        )[0]
        
        counts = self._count_detections(result)
        return result, counts

    def _count_detections(self, result: object) -> Counter:
        """
        Conta as detecções por classe.

        Args:
            result: Resultado do modelo YOLO

        Returns:
            Counter com contagem por classe
        """
        counts = Counter()
        
        if result.boxes is not None and len(result.boxes) > 0:
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = self.class_names.get(class_id, f"class_{class_id}")
                counts[class_name] += 1
        
        return counts

    def annotate_frame(self, frame: object, counts: Counter) -> object:
        """
        Adiciona anotações de contagem ao frame.

        Args:
            frame: Frame com detecções já desenhadas
            counts: Contagem de classes

        Returns:
            Frame anotado
        """
        y = TEXT_Y_START
        
        for class_id in sorted(self.class_names.keys()):
            class_name = self.class_names[class_id]
            count = counts.get(class_name, 0)
            display_name = DISPLAY_NAMES.get(class_name, class_name)
            
            text = f"{display_name}: {count}"
            cv2.putText(
                frame,
                text,
                (20, y),
                TEXT_FONT,
                TEXT_SCALE,
                TEXT_COLOR,
                TEXT_THICKNESS,
                cv2.LINE_AA,
            )
            y += TEXT_Y_OFFSET
        
        return frame

    def detect_from_image(self, image_path: str) -> None:
        """
        Detecta em uma imagem estática e exibe o resultado.

        Args:
            image_path: Caminho da imagem
        """
        result, counts = self.detect(image_path)
        
        print("\n" + "="*50)
        print("Detecção em Imagem")
        print("="*50)
        for class_name in sorted(self.class_names.values()):
            count = counts.get(class_name, 0)
            display_name = DISPLAY_NAMES.get(class_name, class_name)
            print(f"  {display_name}: {count}")
        print("="*50 + "\n")
        
        plotted = result.plot()
        plotted = self.annotate_frame(plotted, counts)
        
        cv2.imshow("Deteccao", plotted)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def detect_from_webcam(self, camera_id: int = 0) -> None:
        """
        Detecta em stream de webcam em tempo real.

        Args:
            camera_id: ID da câmera (0=interna, 1=continuity camera, etc)
        """
        cap = cv2.VideoCapture(camera_id)
        
        if not cap.isOpened():
            raise RuntimeError(f"Não foi possível abrir a câmera {camera_id}.")
        
        # Ajustes para câmera mais responsiva
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduz delay
        cap.set(cv2.CAP_PROP_FPS, 30)         # Define FPS
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        camera_name = "MacBook" if camera_id == 0 else "iPhone"
        print(f"\n📷 Câmera {camera_id} ({camera_name}) inicializada.")
        print("Pressione 'q' para fechar.\n")

        try:
            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("⚠️  Aviso: Perda de frame. Reconectando câmera...")
                    continue

                frame_count += 1
                
                result, counts = self.detect(frame)
                plotted = result.plot()
                plotted = self.annotate_frame(plotted, counts)

                # Mostra FPS
                cv2.putText(
                    plotted,
                    f"FPS: {frame_count}",
                    (10, plotted.shape[0] - 10),
                    TEXT_FONT,
                    0.5,
                    (0, 255, 255),
                    1,
                )

                cv2.imshow("YOLOv8 - Contagem de Alimentos", plotted)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()
            print(f"\n✅ Detector finalizado. Total de frames: {frame_count}\n")


# ==================== Interface de Linha de Comando ====================
def parse_args() -> argparse.Namespace:
    """Analisa argumentos de linha de comando."""
    parser = argparse.ArgumentParser(
        description="Detector de Alimentos - Contar embalagens com YOLO",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Webcam interna (MacBook)
  python detector.py --model ../runs/food-v6/weights/best.pt --source webcam --camera-id 0
  
  # Continuity Camera (iPhone)
  python detector.py --model ../runs/food-v6/weights/best.pt --source webcam --camera-id 1
  
  # Imagem estática
  python detector.py --model ../runs/food-v6/weights/best.pt --source /caminho/imagem.jpg
        """
    )
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Caminho do modelo treinado (ex.: runs/food-v6/weights/best.pt)",
    )
    parser.add_argument(
        "--source",
        type=str,
        default="webcam",
        help="'webcam' para câmera ao vivo ou caminho para imagem",
    )
    parser.add_argument(
        "--camera-id",
        type=int,
        default=0,
        help="ID da câmera (0=interna, 1=continuity/externa)",
    )
    parser.add_argument(
        "--confidence",
        type=float,
        default=CONFIDENCE_THRESHOLD,
        help="Threshold de confiança para detecções (0-1)",
    )
    
    return parser.parse_args()


def main():
    """Função principal."""
    args = parse_args()
    
    try:
        detector = FoodDetector(args.model, args.confidence)
        
        if args.source.lower() == "webcam":
            detector.detect_from_webcam(args.camera_id)
        else:
            detector.detect_from_image(args.source)
    
    except FileNotFoundError:
        print(f"❌ Erro: Modelo não encontrado em '{args.model}'")
        exit(1)
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
