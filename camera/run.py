import argparse
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from common.constants import (
    DEFAULT_CONFIDENCE,
    DEFAULT_LINE_Y_RATIO,
    DEFAULT_MIN_LABEL_VOTES,
)
from common.model_utils import resolve_best_model

from detector import FoodDetector


MENU_TEXT = """
Selecione o modo de teste:
    0 - Camera (tempo real)
    1 - Foto (captura da webcam)
    2 - Arquivo salvo (imagem no disco)
    q - Sair
""".strip()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Executa detector com o modelo treinado atual"
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Caminho opcional para um .pt especifico. Se omitido, usa detector/runs/train/weights/best.pt",
    )
    parser.add_argument("--camera-id", type=int, default=0)
    parser.add_argument("--conf", type=float, default=DEFAULT_CONFIDENCE)
    parser.add_argument("--mode", choices=["conveyor", "live"], default="conveyor")
    parser.add_argument("--line-y", type=float, default=DEFAULT_LINE_Y_RATIO)
    parser.add_argument("--min-label-votes", type=int, default=DEFAULT_MIN_LABEL_VOTES)
    return parser.parse_args()


def resolve_model_path(model_arg: str | None) -> Path:
    """
    Resolve o caminho do modelo. Usa utilitário compartilhado.
    Mantido por compatibilidade, mas delega para common.model_utils.
    """
    return resolve_best_model(model_arg)


def ask_mode() -> str:
    print("\n" + MENU_TEXT)
    return input("Modo: ").strip().lower()


def ask_image_path(project_root: Path) -> Path | None:
    raw = input("Informe o caminho da imagem (ou vazio para cancelar): ").strip()
    if not raw:
        return None

    candidate = Path(raw)
    if not candidate.is_absolute():
        candidate = project_root / candidate

    if not candidate.exists() or not candidate.is_file():
        print(f"Arquivo invalido: {candidate}")
        return None

    return candidate


def describe_counts(counts: dict) -> None:
    if not counts:
        print("Descricao: nenhum alimento detectado na imagem.")
        return

    top_label = max(counts, key=counts.get)
    print(f"Descricao: imagem mais provavel de conter {top_label}.")
    print(f"Contagem detectada: {counts}")


def run_saved_file_loop(detector: FoodDetector, project_root: Path) -> None:
    while True:
        image_path = ask_image_path(project_root)
        if image_path is None:
            back = input("Voltar ao menu inicial? [s/N]: ").strip().lower()
            if back in {"s", "sim", "y", "yes"}:
                return
            continue

        counts = detector.predict_image(str(image_path))
        describe_counts(dict(counts))

        action = input(
            "Digite 1 para analisar outra imagem, 0 para voltar ao menu inicial: "
        ).strip()
        if action == "0":
            return


def main():
    args = parse_args()
    project_root = Path(__file__).resolve().parent.parent
    model_path = resolve_model_path(args.model)

    detector = FoodDetector(str(model_path), conf=args.conf)

    while True:
        mode = ask_mode()

        if mode == "q":
            print("Encerrando.")
            return

        if mode == "0":
            detector.predict_webcam(
                camera_id=args.camera_id,
                mode=args.mode,
                line_y_ratio=args.line_y,
                min_label_votes=args.min_label_votes,
            )
            continue

        if mode == "1":
            detector.capture_and_predict_photo(camera_id=args.camera_id)
            continue

        if mode == "2":
            run_saved_file_loop(detector, project_root)
            continue

        print("Opcao invalida. Escolha 0, 1, 2 ou q.")


if __name__ == "__main__":
    main()
