"""
Coleta automatica de imagens negativas usando Bing (mais estável que DuckDuckGo).
"""

import argparse
import hashlib
import logging
import shutil
import tempfile
from pathlib import Path

from icrawler.builtin import BingImageCrawler
from PIL import Image, UnidentifiedImageError

logging.basicConfig(level=logging.WARNING)

# Diversas categorias de imagens negativas
NEGATIVE_QUERIES = {
    "plantas": ["planta verde", "flores coloridas", "árvore floresta"],
    "animais": ["gato", "cachorro", "pássaro", "borboleta"],
    "objetos": ["livro", "caneca", "prato", "panela"],
    "frutas": ["maçã", "banana", "laranja", "morango"],
    "rostos": ["rosto pessoa", "retrato humano", "criança"],
    "natureza": ["pedra rocha", "madeira tronco", "areia praia"],
    "outros_alimentos": ["pizza", "bolo", "salada", "pão"],
}


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def file_hash(raw: bytes) -> str:
    return hashlib.sha1(raw).hexdigest()


def is_valid_image(img_path: Path) -> bool:
    """Valida se a imagem tem tamanho mínimo."""
    try:
        with Image.open(img_path) as img:
            width, height = img.size
            if width < 200 or height < 200:
                return False
            return True
    except (UnidentifiedImageError, OSError):
        return False


def normalize_to_jpg(src_path: Path, dst_path: Path) -> bool:
    """Converte para JPG padrão."""
    try:
        with Image.open(src_path) as img:
            img = img.convert("RGB")
            img.save(dst_path, format="JPEG", quality=92)
        return True
    except (UnidentifiedImageError, OSError):
        return False


def collect_negative_images_bing(
    out_root: Path,
    target_count: int,
) -> None:
    """Coleta imagens negativas usando Bing."""
    out_dir = out_root / "negative_samples"
    ensure_dir(out_dir)

    existing_hashes = set()
    existing_files = sorted(out_dir.glob("*.jpg"))
    for img_path in existing_files:
        raw = img_path.read_bytes()
        existing_hashes.add(file_hash(raw))

    next_idx = len(existing_files) + 1
    current_total = len(existing_files)
    
    print(f"\n[negative_samples] imagens atuais: {current_total}")
    print(f"[negative_samples] alvo: {target_count} imagens")

    for category, queries in NEGATIVE_QUERIES.items():
        if current_total >= target_count:
            print(f"\n✓ Meta atingida: {current_total} imagens coletadas")
            break

        for query in queries:
            if current_total >= target_count:
                break

            print(f"[negative_samples/{category}] buscando: {query}")
            
            # Quantas imagens baixar dessa query
            remaining = target_count - current_total
            images_per_query = min(15, remaining)
            
            try:
                bing_crawler = BingImageCrawler(storage={"root_dir": "temp_download"})
                
                # Baixar imagens
                bing_crawler.crawl(keyword=query, arg1=images_per_query)
                
                # Processar imagens baixadas
                temp_dir = Path("temp_download") / query
                if not temp_dir.exists():
                    print(f"  ✗ nenhuma imagem baixada para: {query}")
                    continue
                
                for img_file in sorted(temp_dir.glob("*.jpg")) + sorted(temp_dir.glob("*.png")):
                    if current_total >= target_count:
                        break
                    
                    # Validar tamanho
                    if not is_valid_image(img_file):
                        img_file.unlink(missing_ok=True)
                        continue
                    
                    # Converter para JPG se necessário
                    out_path = out_dir / f"negative_{next_idx:04d}.jpg"
                    
                    if img_file.suffix.lower() == ".jpg":
                        raw = img_file.read_bytes()
                        h = file_hash(raw)
                        if h not in existing_hashes:
                            shutil.copy(img_file, out_path)
                            existing_hashes.add(h)
                            current_total += 1
                            next_idx += 1
                            print(f"  ✓ salvo: {out_path.name} ({current_total}/{target_count})")
                    else:
                        # Converter PNG ou outros para JPG
                        if normalize_to_jpg(img_file, out_path):
                            raw = out_path.read_bytes()
                            h = file_hash(raw)
                            if h not in existing_hashes:
                                existing_hashes.add(h)
                                current_total += 1
                                next_idx += 1
                                print(f"  ✓ salvo: {out_path.name} ({current_total}/{target_count})")
                            else:
                                out_path.unlink(missing_ok=True)
                    
                    img_file.unlink(missing_ok=True)
                
                # Limpar diretório temporário
                if temp_dir.exists():
                    shutil.rmtree(temp_dir)
                    
            except Exception as e:
                print(f"  ! erro ao coletar de {query}: {e}")
                continue

    # Limpar diretório temporário
    temp_root = Path("temp_download")
    if temp_root.exists():
        shutil.rmtree(temp_root, ignore_errors=True)

    total = len(list(out_dir.glob("*.jpg")))
    print(f"\n[negative_samples] total final: {total} imagens")
    print(f"[negative_samples] pasta: {out_dir}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Coleta automatica de imagens negativas usando Bing"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=".",
        help="Pasta de saida (default: pasta atual)",
    )
    parser.add_argument(
        "--target",
        type=int,
        default=100,
        help="Quantidade alvo de imagens (default: 100)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    out_root = Path(args.output).resolve()
    ensure_dir(out_root)

    print("=" * 60)
    print("COLETA DE IMAGENS NEGATIVAS COM BING (validação)")
    print("=" * 60)
    print(f"Saída: {out_root}")
    print(f"Alvo: {args.target} imagens")
    print("=" * 60)

    collect_negative_images_bing(
        out_root=out_root,
        target_count=args.target,
    )


if __name__ == "__main__":
    main()
