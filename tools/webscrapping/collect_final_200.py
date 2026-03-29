"""
Coleta simples e direto com queries curtas que funcionam bem.
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


QUERIES = [
    "person holding shopping bag",
    "woman with groceries",
    "person at supermarket",
    "shopping cart full",
    "can beverage drink",
    "glass bottle",
    "chocolate bar",
    "snack chips",
    "cookies biscuit",
    "shampoo bottle",
    "detergent cleaning",
    "juice bottle",
    "water bottle",
    "yogurt container",
    "cheese package",
    "bread loaf",
    "toy in box",
    "book cover",
    "person shopping",
    "supermarket shelf product",
    "ice cream frozen",
    "beer bottle",
    "soda can",
    "milk carton",
    "egg carton",
    "person with products",
    "hand holding food",
    "shopping bag items",
    "supermarket cashier",
    "store shelves items",
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


def collect(out_dir: Path, target: int) -> None:
    existing_hashes = set()
    for img_path in out_dir.glob("*.jpg"):
        existing_hashes.add(file_hash(img_path.read_bytes()))

    existing_files = sorted(out_dir.glob("negative_*.jpg"))
    next_idx = max([int(f.stem.split('_')[1]) for f in existing_files] + [0]) + 1
    current = len(existing_files)
    
    print(f"Atual: {current} | Alvo: {target}\n")
    
    for query in QUERIES:
        if current >= target:
            break
        
        try:
            with DDGS(timeout=15) as ddgs:
                results = list(ddgs.images(query=query, max_results=15))
        except Exception as e:
            continue
        
        if not results:
            continue
        
        for item in results:
            if current >= target:
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
                current += 1
                if current % 10 == 0:
                    print(f"  {current}/{target}")
            
            time.sleep(0.08)
    
    print(f"\n✓ Total: {current}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, default=".")
    parser.add_argument("--target", type=int, default=200)
    args = parser.parse_args()
    
    out_root = Path(args.output).resolve()
    out_dir = out_root / "negative_samples"
    ensure_dir(out_dir)
    
    print("=" * 50)
    print("COLETA: Produtos + Pessoas")
    print("=" * 50)
    collect(out_dir=out_dir, target=args.target)


if __name__ == "__main__":
    main()
