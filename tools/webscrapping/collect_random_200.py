"""Scraping direto - versão ultra simples."""
import hashlib, time
from pathlib import Path
import requests
from PIL import Image, UnidentifiedImageError
import random

try:
    from ddgs import DDGS
except:
    from duckduckgo_search import DDGS

# Lista simples de queries muito genéricas
QUERIES = [
    "bottle", "jar", "bag", "box", "package", "product",
    "food", "drink", "grocery", "item", "object",
    "person", "hand", "shopping", "store", "seller",
    "apple", "juice", "milk", "cheese", "bread",
    "soap", "paper", "toy", "book", "candy",
]

def file_hash(raw): 
    return hashlib.sha1(raw).hexdigest()

def save_img(raw, path):
    tmp = path.with_suffix(".tmp")
    tmp.write_bytes(raw)
    try:
        img = Image.open(tmp)
        if img.size[0] < 140 or img.size[1] < 140:
            tmp.unlink()
            return False
        img.convert("RGB").save(path, format="JPEG", quality=90)
        tmp.unlink()
        return True
    except:
        tmp.unlink()
        return False

def dl(url):
    try:
        r = requests.get(url, timeout=6, headers={"User-Agent": "Mozilla"})
        return r.content if r.status_code == 200 else None
    except:
        return None

out = Path("negative_samples")
out.mkdir(exist_ok=True)

hashes = {file_hash(p.read_bytes()) for p in out.glob("*.jpg")}
idx = 1
total = 0
target = 200

while total < target:
    q = random.choice(QUERIES)
    
    try:
        with DDGS() as d:
            results = list(d.images(query=q, max_results=10))
    except:
        continue
    
    if not results:
        continue
    
    for item in results:
        if total >= target:
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
            total += 1
            if total % 20 == 0:
                print(f"{total}/{target}", flush=True)
        
        time.sleep(0.01)

print(f"✓ {total}")
