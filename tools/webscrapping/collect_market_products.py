"""
Coleta imagens negativas com foco em produtos de mercado divergentes.
Não vai usar: arroz, feijão, macarrão, açúcar, fubá, óleo, leite em pó, enlatados.
Vai coletar: refrigerante, cerveja, chocolate, snacks, cosméticos, higiene, frutas, pessoas com compras, etc.
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


QUERIES = {
    "refrigerantes": [
        "refrigerante garrafa mercado",
        "coca cola fanta sprite garrafa",
        "bebida carbonatada supermercado",
    ],
    "cerveja": [
        "cerveja garrafa mercado",
        "pack cerveja supermercado",
    ],
    "chocolate": [
        "chocolate barra mercado",
        "chocolate pudim doce",
    ],
    "snacks": [
        "batata chips salgadinhos mercado",
        "biscoito pacote supermercado",
        "pipoca alimento",
    ],
    "cosmeticos": [
        "shampoo garrafa higiene",
        "sabonete espuma higiene",
        "creme rosto cosmético",
    ],
    "frutas_frescas": [
        "maçã banana laranja frescas",
        "abacaxi melancia fruta",
        "morango uva fruta mercado",
    ],
    "personas_compras": [
        "pessoa segurando compras sacola",
        "pessoa com produtos mercado",
        "mão segurando garrafa comida",
    ],
    "leite_bebidas": [
        "leite caixa garrafa",
        "suco natural bebida",
        "água mineral garrafa",
    ],
    "congelados": [
        "sorvete picolé gelado",
        "alimento congelado embalagem",
    ],
    "diversos": [
        "brinquedo supermercado",
        "caixa cereal matinal",
        "manteiga queijo alimento",
        "limpeza detergente produto",
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
    next_idx = len(existing_files) + 1
    current = len(existing_files)
    
    print(f"Atual: {current} | Alvo: {target}")
    
    for category, query_list in QUERIES.items():
        if current >= target:
            break
        
        for query in query_list:
            if current >= target:
                break
            
            print(f"[{category}] {query}")
            
            try:
                with DDGS(timeout=15) as ddgs:
                    results = list(ddgs.images(query=query, max_results=20))
            except Exception:
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
                    print(f"  ✓ {current}/{target}")
                
                time.sleep(0.1)
    
    print(f"Final: {current} imagens")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, default=".")
    parser.add_argument("--target", type=int, default=150)
    args = parser.parse_args()
    
    out_root = Path(args.output).resolve()
    out_dir = out_root / "negative_samples"
    ensure_dir(out_dir)
    
    print("=" * 50)
    print("COLETA: Produtos de Mercado Diversos")
    print("=" * 50)
    collect(out_dir=out_dir, target=args.target)


if __name__ == "__main__":
    main()
