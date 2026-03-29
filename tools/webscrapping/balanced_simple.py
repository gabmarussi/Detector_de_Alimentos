"""Coleta com queries genéricas mais simples."""
import hashlib, time
from pathlib import Path
import requests
from PIL import Image, UnidentifiedImageError

try:
    from ddgs import DDGS
except:
    from duckduckgo_search import DDGS

CATEGORIES = {
    "agua": 5, "suco": 5, "vinho": 5, "cerveja": 5, "refrigerante": 5,
    "leite": 5, "iogurte": 5, "queijo": 5, "manteiga": 5, "chocolate": 5,
    "biscoito": 5, "chips": 5, "sorvete": 5, "pao": 5, "fruta": 5,
    "shampoo": 5, "sabonete": 5, "detergente": 5, "papel": 5, "desodorante": 5,
    "pasta": 5, "sacola": 5, "carrinho": 5, "mao": 5, "doce": 5,
    "cafe": 5, "leite_po": 5, "oleo": 5, "sal": 5, "tempero": 5,
    "conserva": 5, "soja": 5, "azeite": 5, "vinagre": 5, "caldo": 5,
    "brinquedo": 5, "livro": 5, "pessoa": 5, "compras": 5,
}

QUERIES = {
    "agua": "water bottle", "suco": "juice", "vinho": "wine", "cerveja": "beer",
    "refrigerante": "soda", "leite": "milk", "iogurte": "yogurt", "queijo": "cheese",
    "manteiga": "butter", "chocolate": "chocolate", "biscoito": "cookie", "chips": "chips",
    "sorvete": "ice cream", "pao": "bread", "fruta": "fruit", "shampoo": "shampoo",
    "sabonete": "soap", "detergente": "detergent", "papel": "tissue", "desodorante": "deodorant",
    "pasta": "toothpaste", "sacola": "shopping bag", "carrinho": "cart", "mao": "hand",
    "doce": "candy", "cafe": "coffee", "leite_po": "milk powder", "oleo": "oil",
    "sal": "salt", "tempero": "spice", "conserva": "canned", "soja": "soy",
    "azeite": "olive oil", "vinagre": "vinegar", "caldo": "broth", "brinquedo": "toy",
    "livro": "book", "pessoa": "person", "compras": "shopping",
}

def file_hash(raw): return hashlib.sha1(raw).hexdigest()

def save_img(raw, path):
    tmp = path.with_suffix(".tmp")
    tmp.write_bytes(raw)
    try:
        img = Image.open(tmp)
        if img.size[0] < 150 or img.size[1] < 150:
            tmp.unlink()
            return False
        img.convert("RGB").save(path, format="JPEG", quality=92)
        tmp.unlink()
        return True
    except:
        tmp.unlink()
        return False

def dl(url):
    try:
        r = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        return r.content if r.status_code == 200 else None
    except:
        return None

out = Path("c:/Users/gabri/Documents/GitHub/Detector de Alimentos/negative_samples")
out.mkdir(exist_ok=True)

hashes = {file_hash(p.read_bytes()) for p in out.glob("*.jpg")}
idx = 1
total = 0

for cat, target in CATEGORIES.items():
    if cat not in QUERIES:
        continue
    
    q = QUERIES[cat]
    collected = 0
    
    try:
        with DDGS(timeout=20) as d:
            try:
                results = list(d.images(query=q, max_results=15))
            except:
                results = []
    except:
        results = []
    
    if not results:
        print(f"[{cat:15}] × sem resultado")
        continue
    
    for item in results:
        if collected >= target:
            break
        
        url = item.get("image")
        if not url:
            continue
        
        raw = dl(url)
        if not raw:
            continue
        
        h = file_hash(raw)
        if h in hashes:
            continue
        
        p = out / f"negative_{idx:04d}.jpg"
        if save_img(raw, p):
            hashes.add(h)
            idx += 1
            collected += 1
            total += 1
            print(f"[{cat:15}] {collected}/{target}", end="\r", flush=True)
        
        time.sleep(0.02)
    
    if collected > 0:
        print(f"[{cat:15}] ✓ {collected}/{target} ", flush=True)
    else:
        print(f"[{cat:15}] × {collected}/{target} ", flush=True)

print(f"\n✓ {total}")
