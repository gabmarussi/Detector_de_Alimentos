import argparse
import hashlib
import time
from pathlib import Path

import requests
from PIL import Image, UnidentifiedImageError

try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS

try:
    from ddgs.exceptions import DDGSException
except ImportError:
    DDGSException = Exception


DEFAULT_QUERIES = {
    "rice_package": [
        "rice package",
        "saco de arroz",
        "embalagem de arroz",
        "arroz pacote mercado",
    ],
    "beans_package": [
        "beans package",
        "saco de feijao",
        "embalagem de feijao",
        "feijao pacote mercado",
    ],
    "pasta_package": [
        "pasta package",
        "macarrao pacote",
        "embalagem de macarrao",
        "massa pacote mercado",
    ],
}


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def file_hash(raw: bytes) -> str:
    return hashlib.sha1(raw).hexdigest()


def save_valid_image(raw: bytes, out_path: Path) -> bool:
    tmp_path = out_path.with_suffix(".tmp")
    with open(tmp_path, "wb") as f:
        f.write(raw)

    try:
        with Image.open(tmp_path) as img:
            img = img.convert("RGB")
            img.save(out_path, format="JPEG", quality=92)
    except (UnidentifiedImageError, OSError):
        tmp_path.unlink(missing_ok=True)
        return False

    tmp_path.unlink(missing_ok=True)
    return True


def download_image(url: str, timeout: int = 12) -> bytes | None:
    try:
        response = requests.get(
            url,
            timeout=timeout,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        if response.status_code == 200 and response.content:
            return response.content
    except requests.RequestException:
        return None
    return None


def collect_for_class(
    class_name: str,
    queries: list[str],
    out_root: Path,
    target_count: int,
    max_results_per_query: int,
    delay_seconds: float,
) -> None:
    class_dir = out_root / class_name
    ensure_dir(class_dir)

    existing_hashes = set()
    existing_files = sorted(class_dir.glob("*.jpg"))
    for img_path in existing_files:
        raw = img_path.read_bytes()
        existing_hashes.add(file_hash(raw))

    next_idx = len(existing_files) + 1
    print(f"\n[{class_name}] imagens atuais: {len(existing_files)}")

    with DDGS() as ddgs:
        for query in queries:
            if len(list(class_dir.glob("*.jpg"))) >= target_count:
                break

            print(f"[{class_name}] buscando: {query}")
            try:
                # ddgs package API
                results = ddgs.images(
                    query=query,
                    max_results=max_results_per_query,
                    safesearch="moderate",
                    size="Medium",
                    color="color",
                )
            except TypeError:
                # duckduckgo_search legacy API
                results = ddgs.images(
                    keywords=query,
                    max_results=max_results_per_query,
                    safesearch="moderate",
                    size="Medium",
                    color="color",
                )
            except DDGSException:
                # Some queries return no results with strict filters.
                try:
                    results = ddgs.images(query=query, max_results=max_results_per_query)
                except Exception:
                    print(f"[{class_name}] sem resultados para: {query}")
                    continue
            except Exception:
                print(f"[{class_name}] erro na busca: {query}")
                continue

            for item in results:
                if len(list(class_dir.glob("*.jpg"))) >= target_count:
                    break

                url = item.get("image")
                if not url:
                    continue

                raw = download_image(url)
                if not raw:
                    continue

                h = file_hash(raw)
                if h in existing_hashes:
                    continue

                out_path = class_dir / f"{class_name}_{next_idx:04d}.jpg"
                ok = save_valid_image(raw, out_path)
                if ok:
                    existing_hashes.add(h)
                    next_idx += 1

                time.sleep(delay_seconds)

    total = len(list(class_dir.glob("*.jpg")))
    print(f"[{class_name}] total final: {total}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Coleta automatica de imagens para dataset de produtos"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="../Alimentos",
        help="Pasta de saida com subpastas por classe",
    )
    parser.add_argument("--target", type=int, default=220, help="Quantidade alvo por classe")
    parser.add_argument(
        "--max-results-per-query",
        type=int,
        default=140,
        help="Maximo de resultados por busca",
    )
    parser.add_argument("--delay", type=float, default=0.2, help="Pausa entre downloads")
    parser.add_argument(
        "--only",
        type=str,
        default="",
        help="Coletar apenas uma classe (rice_package, beans_package, pasta_package)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    out_root = Path(args.output).resolve()
    ensure_dir(out_root)

    class_map = DEFAULT_QUERIES
    if args.only:
        if args.only not in DEFAULT_QUERIES:
            raise ValueError("Classe invalida em --only")
        class_map = {args.only: DEFAULT_QUERIES[args.only]}

    print(f"Saida: {out_root}")
    print(f"Alvo por classe: {args.target}")

    for class_name, queries in class_map.items():
        collect_for_class(
            class_name=class_name,
            queries=queries,
            out_root=out_root,
            target_count=args.target,
            max_results_per_query=args.max_results_per_query,
            delay_seconds=args.delay,
        )

    print("\nColeta finalizada.")


if __name__ == "__main__":
    main()
