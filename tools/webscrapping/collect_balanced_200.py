"""Coleta balanceada com erro handling melhorado."""
import hashlib, time, sys, random
from pathlib import Path
import requests
from PIL import Image, UnidentifiedImageError

try:
    from ddgs import DDGS
except:
    from duckduckgo_search import DDGS

# 40 categorias x 5 = 200
PRODUCTS = {
    "agua": 5,          "suco": 5,          "vinho": 5,         "cerveja": 5,
    "refrigerante": 5,  "leite": 5,         "iogurte": 5,       "queijo": 5,
    "manteiga": 5,      "chocolate": 5,     "biscoito": 5,      "chips": 5,
    "sorvete": 5,       "pao": 5,           "maca": 5,          "banana": 5,
    "laranja": 5,       "shampoo": 5,       "sabonete": 5,      "detergente": 5,
    "papel": 5,         "desodorante": 5,   "pasta": 5,         "sacola": 5,
    "carrinho": 5,      "mao": 5,           "doce": 5,          "cafe": 5,
    "achocolatado": 5,  "pó": 5,            "oleo": 5,          "sal": 5,
    "tempero": 5,       "conserva": 5,      "soja": 5,          "azeite": 5,
    "vinagre": 5,       "caldo": 5,         "brinquedo": 5,     "livro": 5,
}

QUERIES = {
    "agua": ["water bottle supermarket"], "suco": ["juice box drink"],
    "vinho": ["wine bottle red white"], "cerveja": ["beer bottle drink"],
    "refrigerante": ["soda drink bottle"], "leite": ["milk carton"],
    "iogurte": ["yogurt container"], "queijo": ["cheese slice"],
    "manteiga": ["butter package"], "chocolate": ["chocolate bar wrapper"],
    "biscoito": ["cookie package"], "chips": ["potato chips bag"],
    "sorvete": ["ice cream popsicle"], "pao": ["bread loaf bakery"],
    "maca": ["red apple fruit"], "banana": ["yellow banana"],
    "laranja": ["orange fruit citrus"], "shampoo": ["shampoo bottle"],
    "sabonete": ["soap bar"], "detergente": ["cleaning detergent"],
    "papel": ["toilet paper roll"], "desodorante": ["deodorant spray"],
    "pasta": ["toothpaste tube"], "sacola": ["shopping bag"],
    "carrinho": ["shopping cart"], "mao": ["hand holding food"],
    "doce": ["candies lollipop"], "cafe": ["coffee bag"],
    "achocolatado": ["chocolate drink"], "pó": ["powdered milk"],
    "oleo": ["cooking oil bottle"], "sal": ["salt container"],
    "tempero": ["spice jar"], "conserva": ["canned food"],
    "soja": ["soy sauce bottle"], "azeite": ["olive oil bottle"],
    "vinagre": ["vinegar bottle"], "caldo": ["broth cube"],
    "brinquedo": ["toy box"], "livro": ["book cover"],
}

def file_hash(raw): 
    return hashlib.sha1(raw).hexdigest()

def save_img(raw, path):
    tmp = path.with_suffix(".tmp")
    tmp.write_bytes(raw)
    try:
        img = Image.open(tmp)
        w, h = img.size
        if w < 200 or h < 200:
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

print(f"Alvo: {sum(PRODUCTS.values())} imagens\n")

for cat in list(PRODUCTS.keys()):
    target = PRODUCTS[cat]
    if cat not in QUERIES:
        continue
    
    collected = 0
    queries = QUERIES[cat]
    
    for q in queries:
        if collected >= target:
            break
        
        try:
            with DDGS(timeout=12) as d:
                results = []
                try:
                    results = list(d.images(query=q, max_results=12))
                except Exception as e:
                    try:
                        results = list(d.images(query=q.split()[0], max_results=8))
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
                print(f"[{cat:15}] {collected}/{target}", end="\r", flush=True)
            
            time.sleep(0.03)
    
    if collected > 0:
        print(f"[{cat:15}] ✓ {collected:2}/{target}  ")
    else:
        print(f"[{cat:15}] × 0/{target}  ")

print(f"\n✓ {total} imagens coletadas")
