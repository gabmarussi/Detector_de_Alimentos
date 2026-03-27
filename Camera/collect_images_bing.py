import argparse
import hashlib
import logging
import shutil
import tempfile
from pathlib import Path

from icrawler.builtin import BingImageCrawler
from PIL import Image, UnidentifiedImageError


DEFAULT_QUERIES = {
    "rice_package": [
        "arroz pacote 1kg mercado -mockup -maquete -psd -template -vector",
        "saco de arroz marca embalagem fechada supermercado -mockup -maquete -psd",
        "pacote de arroz supermercado prateleira marca -mockup -maquete -template",
        "rice bag 1kg supermarket brand package photo -mockup -template -vector",
        "arroz agulhinha tipo 1 pacote marca -mockup -maquete -psd -template",
        "arroz parboilizado pacote 1kg marca supermercado -mockup -maquete -psd",
        "arroz integral pacote 1kg marca supermercado -mockup -maquete -psd",
        "arroz branco tipo 1 pacote 5kg marca -mockup -maquete -psd",
        "arroz camil pacote 1kg supermercado -mockup -maquete -psd",
        "arroz tio joao pacote 1kg supermercado -mockup -maquete -psd",
        "arroz urbano pacote 1kg supermercado -mockup -maquete -psd",
        "arroz tio joao pacote 5kg supermercado -mockup -maquete -psd",
        "arroz prato fino pacote 1kg supermercado -mockup -maquete -psd",
        "arroz namorado pacote 1kg supermercado -mockup -maquete -psd",
        "arroz karpil pacote 1kg supermercado -mockup -maquete -psd",
        "arroz kicaldo pacote 1kg supermercado -mockup -maquete -psd",
        "arroz pacote 2kg 5kg marca supermercado foto -mockup -maquete -psd",
    ],
    "beans_package": [
        "feijao pacote 1kg mercado -mockup -maquete -psd -template -vector",
        "saco de feijao marca embalagem fechada supermercado -mockup -maquete -psd",
        "pacote de feijao supermercado prateleira marca -mockup -maquete -template",
        "bean bag 1kg supermarket brand package photo -mockup -template -vector",
        "feijao carioca pacote 1kg marca supermercado -mockup -maquete -psd",
        "feijao preto pacote 1kg marca supermercado -mockup -maquete -psd",
        "feijao fradinho pacote 1kg marca supermercado -mockup -maquete -psd",
        "feijao vermelho pacote 1kg marca supermercado -mockup -maquete -psd",
        "feijao jalo pacote 1kg marca supermercado -mockup -maquete -psd",
        "feijao branco pacote 500g 1kg marca supermercado -mockup -maquete -psd",
        "feijao kicaldo pacote 1kg supermercado -mockup -maquete -psd",
        "feijao camil pacote 1kg supermercado -mockup -maquete -psd",
        "feijao namorado pacote 1kg supermercado -mockup -maquete -psd",
        "feijao da casa pacote 1kg supermercado -mockup -maquete -psd",
        "feijao broto legal pacote 1kg supermercado -mockup -maquete -psd",
        "feijao urbano pacote 1kg supermercado -mockup -maquete -psd",
        "feijao pacote 2kg marca supermercado foto -mockup -maquete -psd",
    ],
    "pasta_package": [
        "macarrao espaguete pacote marca supermercado -mockup -maquete -psd -template -vector",
        "macarrao parafuso fusilli pacote marca mercado -mockup -maquete -psd -template -vector",
        "macarrao penne pacote marca supermercado -mockup -maquete -psd -template -vector",
        "macarrao talharim pacote marca supermercado -mockup -maquete -psd -template -vector",
        "macarrao fettuccine pacote marca supermercado -mockup -maquete -psd -template -vector",
        "macarrao gravatinha farfalle pacote marca supermercado -mockup -maquete -psd -template -vector",
        "macarrao padre nosso pacote marca supermercado -mockup -maquete -psd -template -vector",
        "macarrao argolinha pacote marca supermercado -mockup -maquete -psd -template -vector",
        "macarrao ave maria pacote marca supermercado -mockup -maquete -psd -template -vector",
        "macarrao lasanha folhas pacote marca supermercado -mockup -maquete -psd -template -vector",
        "macarrao ninho pacote marca supermercado -mockup -maquete -psd -template -vector",
        "macarrao rigatoni pacote marca supermercado -mockup -maquete -psd -template -vector",
        "macarrao conchinha shell pacote marca supermercado -mockup -maquete -psd -template -vector",
        "macarrao canelone pacote marca supermercado -mockup -maquete -psd -template -vector",
    ],
}


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def file_hash(raw: bytes) -> str:
    return hashlib.sha1(raw).hexdigest()


def normalize_to_jpg(src_path: Path, dst_path: Path) -> bool:
    try:
        with Image.open(src_path) as img:
            img = img.convert("RGB")
            img.save(dst_path, format="JPEG", quality=92)
        return True
    except (UnidentifiedImageError, OSError):
        return False


def is_useful_package_image(img_path: Path) -> bool:
    try:
        with Image.open(img_path) as img:
            width, height = img.size
    except (UnidentifiedImageError, OSError):
        return False

    if width < 320 or height < 320:
        return False

    ratio = width / max(height, 1)
    if ratio < 0.4 or ratio > 2.3:
        return False

    return True


def normalize_class_dir(class_dir: Path, class_name: str, target_count: int) -> None:
    existing_hashes = set()
    final_images = sorted(class_dir.glob(f"{class_name}_*.jpg"))

    for img_path in final_images:
        existing_hashes.add(file_hash(img_path.read_bytes()))

    next_idx = len(final_images) + 1

    for src in list(class_dir.iterdir()):
        if len(list(class_dir.glob(f"{class_name}_*.jpg"))) >= target_count:
            break

        if not src.is_file():
            continue

        if src.suffix.lower() == ".jpg" and src.name.startswith(f"{class_name}_"):
            continue

        try:
            raw = src.read_bytes()
        except OSError:
            continue

        if not is_useful_package_image(src):
            src.unlink(missing_ok=True)
            continue

        h = file_hash(raw)
        if h in existing_hashes:
            src.unlink(missing_ok=True)
            continue

        dst = class_dir / f"{class_name}_{next_idx:04d}.jpg"
        if normalize_to_jpg(src, dst):
            existing_hashes.add(h)
            next_idx += 1

        src.unlink(missing_ok=True)


def collect_for_class(
    class_name: str,
    queries: list[str],
    output_root: Path,
    target_count: int,
    per_query_limit: int,
) -> None:
    class_dir = output_root / class_name
    ensure_dir(class_dir)

    print(f"\n[{class_name}] imagens atuais: {len(list(class_dir.glob(f'{class_name}_*.jpg')))}")
    logging.getLogger("icrawler").setLevel(logging.ERROR)

    for query in queries:
        current_count = len(list(class_dir.glob("*.jpg")))
        if current_count >= target_count:
            break

        remaining = target_count - current_count
        max_to_download = min(per_query_limit, max(remaining * 2, 20))

        print(f"[{class_name}] buscando no Bing: {query} (max {max_to_download})")
        crawler = BingImageCrawler(storage={"root_dir": str(class_dir)})
        crawler.crawl(keyword=query, max_num=max_to_download)
        normalize_class_dir(class_dir, class_name, target_count)

    print(f"[{class_name}] total final: {len(list(class_dir.glob(f'{class_name}_*.jpg')))}")


def parse_args():
    parser = argparse.ArgumentParser(description="Coleta imagens via Bing para dataset")
    parser.add_argument("--output", type=str, default="../Alimentos")
    parser.add_argument("--target", type=int, default=120)
    parser.add_argument("--per-query", type=int, default=50)
    parser.add_argument("--only", type=str, default="")
    parser.add_argument("--clean-existing", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    output_root = Path(args.output).resolve()
    ensure_dir(output_root)

    class_map = DEFAULT_QUERIES
    if args.only:
        if args.only not in DEFAULT_QUERIES:
            raise ValueError("Classe invalida em --only")
        class_map = {args.only: DEFAULT_QUERIES[args.only]}

    if args.clean_existing:
        for class_name in class_map:
            class_dir = output_root / class_name
            if class_dir.exists():
                shutil.rmtree(class_dir)

    print(f"Saida: {output_root}")
    print(f"Alvo por classe: {args.target}")

    for class_name, queries in class_map.items():
        collect_for_class(
            class_name=class_name,
            queries=queries,
            output_root=output_root,
            target_count=args.target,
            per_query_limit=args.per_query,
        )

    print("\nColeta Bing finalizada.")


if __name__ == "__main__":
    main()
