"""Coleta rápida com queries simples."""
import argparse, hashlib, time
from pathlib import Path
import requests
from PIL import Image, UnidentifiedImageError

try:
    from ddgs import DDGS
except:
    from duckduckgo_search import DDGS

QUERIES = ["shopping", "store", "bottle", "product", "package", "food", "drink", 
           "people shopping", "hand food", "person grocery", "supermarket"]

def file_hash(raw): return hashlib.sha1(raw).hexdigest()

def save_img(raw, path):
    tmp = path.with_suffix(".tmp")
    tmp.write_bytes(raw)
    try:
        img = Image.open(tmp)
        if img.size[0] < 200 or img.size[1] < 200:
            tmp.unlink(); return False
        img.convert("RGB").save(path, format="JPEG", quality=92)
        tmp.unlink(); return True
    except: 
        tmp.unlink(); return False

def dl(url):
    try: return requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"}).content
    except: return None

def collect(out_dir, target):
    hashes = {file_hash(p.read_bytes()) for p in out_dir.glob("*.jpg")}
    files = sorted(out_dir.glob("negative_*.jpg"))
    idx = max([int(f.stem.split('_')[1]) for f in files] + [0]) + 1
    cur = len(files)
    print(f"{cur}/{target}\n")
    
    for q in QUERIES:
        if cur >= target: break
        try:
            with DDGS(timeout=15) as d:
                res = list(d.images(query=q, max_results=20))
        except: continue
        if not res: continue
        
        for item in res:
            if cur >= target: break
            url = item.get("image")
            if not url: continue
            raw = dl(url)
            if not raw: continue
            h = file_hash(raw)
            if h in hashes: continue
            
            p = out_dir / f"negative_{idx:04d}.jpg"
            if save_img(raw, p):
                hashes.add(h); idx += 1; cur += 1
                if cur % 5 == 0: print(f"  {cur}/{target}")
            time.sleep(0.05)
    
    print(f"\n✓ {cur}")

Path("args").mkdir(exist_ok=True)
out = Path("c:/Users/gabri/Documents/GitHub/Detector de Alimentos/negative_samples")
out.mkdir(exist_ok=True)
collect(out, 200)
