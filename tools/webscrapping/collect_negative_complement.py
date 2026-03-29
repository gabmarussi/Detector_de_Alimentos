"""
Completa a coleta de imagens negativas usando DuckDuckGo com melhor tratamento de erros.
"""

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


NEGATIVE_QUERIES = [
    "planta verde vaso interior",
    "flores buquê decoração",
    "árvore paisagem floresta",
    "gato marom casa",
    "cachorro golden animal",
    "pássaro pousado natureza",
    "maçã fruta vermelha",
    "banana amarela madura",
    "laranja fruta cítrus",
    "morango fruta vermelha",
    "livro reading mesa",
    "caneca café quente",
    "prato louça branco",
    "panela metal cozinha",
    "salada legumes frescos",
]


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
            width, height = img.size
            if width < 200 or height < 200:
                tmp_path.unlink(missing_ok=True)
                return False
            
            img = img.convert("RGB")
            img.save(out_path, format="JPEG", quality=92)
    except (UnidentifiedImageError, OSError):
        tmp_path.unlink(missing_ok=True)
        return False

    tmp_path.unlink(missing_ok=True)
    return True


def download_image(url: str, timeout: int = 10) -> bytes | None:
    try:
        response = requests.get(
            url,
            timeout=timeout,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        if response.status_code == 200 and response.content:
            return response.content
    except Exception:
        return None
    return None


def collect_more_images(
    out_dir: Path,
    current_total: int,
    target_count: int,
) -> int:
    """Coleta mais imagens para atingir a meta."""
    
    existing_hashes = set()
    for img_path in out_dir.glob("*.jpg"):
        raw = img_path.read_bytes()
        existing_hashes.add(file_hash(raw))

    # Encontrar próximo índice
    existing_files = sorted(out_dir.glob("negative_*.jpg"))
    next_idx = len(existing_files) + 1
    
    print(f"\n[negative_samples] imagens atuais: {current_total}")
    print(f"[negative_samples] alvo: {target_count}")
    
    for query in NEGATIVE_QUERIES:
        if current_total >= target_count:
            print(f"\n✓ Meta atingida: {current_total} imagens")
            break
        
        print(f"[negative_samples] buscando: {query}")
        
        try:
            with DDGS(timeout=15) as ddgs:
                results = list(ddgs.images(
                    query=query,
                    max_results=30,
                ))
                
        except Exception as e:
            print(f"  ✗ erro na busca: {e}")
            continue
        
        if not results:
            print(f"  ✗ sem resultados")
            continue
        
        for item in results:
            if current_total >= target_count:
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
            
            out_path = out_dir / f"negative_{next_idx:04d}.jpg"
            if save_valid_image(raw, out_path):
                existing_hashes.add(h)
                next_idx += 1
                current_total += 1
                print(f"  ✓ salvo: negative_{next_idx-1:04d}.jpg ({current_total}/{target_count})")
            
            time.sleep(0.15)
    
    return current_total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, default=".")
    parser.add_argument("--target", type=int, default=100)
    args = parser.parse_args()
    
    out_root = Path(args.output).resolve()
    out_dir = out_root / "negative_samples"
    ensure_dir(out_dir)
    
    print("=" * 60)
    print("COLETA COMPLEMENTAR DE IMAGENS NEGATIVAS")
    print("=" * 60)
    
    current_count = len(list(out_dir.glob("*.jpg")))
    
    final_count = collect_more_images(
        out_dir=out_dir,
        current_total=current_count,
        target_count=args.target,
    )
    
    print(f"\n[negative_samples] total final: {final_count} imagens")
    print(f"[negative_samples] pasta: {out_dir}")


if __name__ == "__main__":
    main()
