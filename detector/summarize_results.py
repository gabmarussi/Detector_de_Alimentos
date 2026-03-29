import argparse
import csv
from pathlib import Path


DEFAULT_METRIC = "metrics/mAP50(B)"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Resume um results.csv do Ultralytics YOLO"
    )
    parser.add_argument(
        "--csv",
        default="detector/runs/train/results.csv",
        help="Caminho para o arquivo results.csv",
    )
    parser.add_argument(
        "--metric",
        default=DEFAULT_METRIC,
        help="Metrica para ranking (ex.: metrics/mAP50(B), metrics/mAP50-95(B))",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Quantidade de epocas no ranking",
    )
    return parser.parse_args()


def _to_float(row: dict[str, str], key: str) -> float:
    try:
        return float(row[key])
    except (KeyError, TypeError, ValueError):
        return float("nan")


def _fmt(value: float) -> str:
    if value != value:
        return "n/a"
    return f"{value:.5f}"


def main() -> None:
    args = parse_args()
    csv_path = Path(args.csv)
    if not csv_path.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {csv_path}")

    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fields = reader.fieldnames or []

    if not rows:
        raise ValueError(f"Arquivo vazio: {csv_path}")

    if args.metric not in fields:
        available = ", ".join(fields)
        raise ValueError(
            f"Metrica invalida: {args.metric}. Colunas disponiveis: {available}"
        )

    ranked = sorted(rows, key=lambda r: _to_float(r, args.metric), reverse=True)
    best = ranked[0]
    final = rows[-1]

    print(f"Arquivo: {csv_path}")
    print(f"Total de epocas: {len(rows)}")
    print()
    print("Melhor epoca pela metrica escolhida")
    print(f"- metrica: {args.metric}")
    print(f"- epoca: {best.get('epoch', 'n/a')}")
    print(f"- valor: {_fmt(_to_float(best, args.metric))}")
    print(
        "- precision/recall/mAP50/mAP50-95: "
        f"{_fmt(_to_float(best, 'metrics/precision(B)'))} / "
        f"{_fmt(_to_float(best, 'metrics/recall(B)'))} / "
        f"{_fmt(_to_float(best, 'metrics/mAP50(B)'))} / "
        f"{_fmt(_to_float(best, 'metrics/mAP50-95(B)'))}"
    )
    print()
    print("Metricas finais (ultima epoca)")
    print(f"- epoca: {final.get('epoch', 'n/a')}")
    print(
        "- precision/recall/mAP50/mAP50-95: "
        f"{_fmt(_to_float(final, 'metrics/precision(B)'))} / "
        f"{_fmt(_to_float(final, 'metrics/recall(B)'))} / "
        f"{_fmt(_to_float(final, 'metrics/mAP50(B)'))} / "
        f"{_fmt(_to_float(final, 'metrics/mAP50-95(B)'))}"
    )
    print()
    print(f"Top {max(1, args.top_k)} epocas por {args.metric}")
    for idx, row in enumerate(ranked[: max(1, args.top_k)], start=1):
        print(
            f"{idx}. epoca {row.get('epoch', 'n/a')} -> "
            f"{_fmt(_to_float(row, args.metric))}"
        )


if __name__ == "__main__":
    main()
