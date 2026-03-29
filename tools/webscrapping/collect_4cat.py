"""Coleta simples: 4 categorias com melhor resultado x muitas imagens."""
import hashlib, time
from pathlib import Path
import requests
from PIL import Image, UnidentifiedImageError

try:
    from ddgs import DDGS
except:
    from duckduckgo_search import DDGS

CATEGORIES = {
    "bebidas": 50,          # suco, vinho, cerveja
    "leite_derivados": 50,  # leite, queijo, iogurte
    "alimentos": 50,        # chocolate, pão, frutas
    "outros": 50,           # higiene, limpeza, pessoas, brinquedos
}

QUERIES_PER_CAT = {
    "bebidas": [
        "juice bottle", "wine bottle", "beer bottle", "soda drink",
        "beverage drink", "soft drink"
    ],
    "leite_derivados": [
        "milk carton", "cheese slice", "yogurt container", "butter",
        "dairy product", "cream"
    ],
    "alimentos": [
        "chocolate bar", "bread loaf", "cookie", "chip snack",
        "candy sweet", "fruit", "ice cream"
    ],
    "outros": [
        "shampoo bottle", "soap bar", "detergent", "toilet paper",
        "shopping bag", "person shopping", "toy box", "book",
        "spice jar", "oil bottle"
    ],
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
        r = requests.get(url, timeout=7, headers={"User-Agent": "Mozilla/5.0"})
        return r.content if r.status_code == 200 else None
    except:
        return None

out = Path("c:/Users/gabri/Documents/GitHub/Detector de Alimentos/negative_samples")
out.mkdir(exist_ok=True)

hashes = {file_hash(p.read_bytes()) for p in out.glob("*.jpg")}
idx = 1
total = 0

for cat, target in CATEGORIES.items():
    if cat not in QUERIES_PER_CAT:
        continue
    
    collected = 0
    queries = QUERIES_PER_CAT[cat]
    
    for q in queries:
        if collected >= target:
            break
        
        try:
            with DDGS(timeout=15) as d:
                results = []
                try:
                    results = list(d.images(query=q, max_results=20))
                except:
                    pass
        except:
            continue
        
        if not results:
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
                if collected % 10 == 0:
                    print(f"[{cat:20}] {collected}/{target}", flush=True)
            
            time.sleep(0.02)
    
    print(f"[{cat:20}] ✓ {collected}/{target}")

print(f"\n✓ Total: {total}")
