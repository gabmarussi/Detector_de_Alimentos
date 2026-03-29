"""
Coleta automatica de imagens negativas (nao-produtos) para dataset de validacao.
Essas imagens ajudam o modelo a entender o que NÃO é arroz, feijão ou macarrão.
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

try:
    from ddgs.exceptions import DDGSException
except ImportError:
    DDGSException = Exception


# Diversas categorias de imagens negativas
NEGATIVE_QUERIES = {
    "plantas": [
        "planta verde interior casa foto",
        "flores coloridas buquê decoração",
        "árvore floresta natureza paisagem",
        "tomate cereja vermelho alimento",
        "batata legume fresco mercado",
        "cenoura cenoura laranja vegetal",
    ],
    "animais": [
        "gato marrom interior casa",
        "cachorro golden retriever animal",
        "pássaro passarinho natureza",
        "borboleta inseto colorido",
    ],
    "objetos_domesticos": [
        "livro leitura mesa escritório",
        "caneca xícara café quente",
        "prato cerâmica louça branco",
        "copo vidro transparente bebida",
        "garfo colher talheres cueca",
        "panela metal cozinha fogão",
    ],
    "frutas_soltas": [
        "maçã vermelha fruta fresca",
        "banana amarela fruta madura",
        "laranja citrus fruta saudável",
        "morango vermelho fruta doce",
        "melancia melão frutas verão",
        "uva roxinha fruta pequena",
    ],
    "pessoas_rostos": [
        "rosto mulher sorriso retrato",
        "rosto homem barba masculino",
        "criança criança sorrindo feliz",
        "mão mãos gesto corpo",
    ],
    "natureza": [
        "pedra rocha mineral textura",
        "madeira tronco árvore cacos",
        "água rio lago reflexo",
        "areia praia deserto textura",
        "nuvem céu azul nublado",
    ],
    "tecnologia": [
        "computador teclado mouse banco",
        "celular smartphone telefone screen",
        "câmera fotográfica digital equipamento",
        "controle videogame joystick",
    ],
    "alimentos_outros": [
        "pizza fatia comida deliciosa",
        "bolo chocolate doce sobremesa",
        "salada legumes frescos prato",
        "pão francês branco alimento",
        "frango assado carne alimento",
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
            # Validar tamanho mínimo
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


def collect_negative_images(
    out_root: Path,
    target_count: int,
    max_results_per_query: int,
    delay_seconds: float,
) -> None:
    """Coleta imagens negativas de várias categorias."""
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
            try:
                with DDGS() as ddgs:
                    try:
                        # Tentar com timeout
                        results = list(ddgs.images(
                            query=query,
                            max_results=max_results_per_query,
                            safesearch="moderate",
                            timeout=10,
                        ))
                    except TypeError:
                        # API legado
                        results = list(ddgs.images(
                            keywords=query,
                            max_results=max_results_per_query,
                            safesearch="moderate",
                        ))
                    except Exception:
                        # Tentar sem filtros de segurança
                        try:
                            results = list(ddgs.images(
                                query=query,
                                max_results=max_results_per_query // 2,
                                timeout=10,
                            ))
                        except Exception:
                            print(f"  ✗ timeout/erro: {query}")
                            continue

                if not results:
                    print(f"  ✗ sem resultados para: {query}")
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
                    ok = save_valid_image(raw, out_path)
                    if ok:
                        existing_hashes.add(h)
                        next_idx += 1
                        current_total += 1
                        print(f"  ✓ salvo: {out_path.name} ({current_total}/{target_count})")
                    
                    time.sleep(delay_seconds)

            except Exception as e:
                print(f"  ! erro na categoria {category}: {e}")
                continue

    total = len(list(out_dir.glob("*.jpg")))
    print(f"\n[negative_samples] total final: {total} imagens")
    print(f"[negative_samples] pasta: {out_dir}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Coleta automatica de imagens negativas para validacao"
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
    parser.add_argument(
        "--max-results-per-query",
        type=int,
        default=80,
        help="Maximo de resultados por busca (default: 80)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.3,
        help="Pausa entre downloads em segundos (default: 0.3)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    out_root = Path(args.output).resolve()
    ensure_dir(out_root)

    print("=" * 60)
    print("COLETA DE IMAGENS NEGATIVAS (validação)")
    print("=" * 60)
    print(f"Saída: {out_root}")
    print(f"Alvo: {args.target} imagens")
    print(f"Delay entre downloads: {args.delay}s")
    print("=" * 60)

    collect_negative_images(
        out_root=out_root,
        target_count=args.target,
        max_results_per_query=args.max_results_per_query,
        delay_seconds=args.delay,
    )


if __name__ == "__main__":
    main()
