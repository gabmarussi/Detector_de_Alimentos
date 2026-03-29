"""Coleta ultra rápida para completar 200."""
from pathlib import Path
import requests
from PIL import Image
import hashlib
import time
try:
    from ddgs import DDGS
except:
    from duckduckgo_search import DDGS

out = Path("negative_samples")
out.mkdir(exist_ok=True)
nfiles = len(list(out.glob("*.jpg")))
idx = nfiles + 1
target = 200

while nfiles < target:
    try:
        with DDGS(timeout=10) as d:
            res = list(d.images(query="product", max_results=20))
            for item in res:
                if nfiles >= target:
                    break
                url = item.get("image")
                if not url:
                    continue
                try:
                    r = requests.get(url, timeout=5)
                    if r.status_code != 200:
                        continue
                    tmp = out / f"negative_{idx:04d}.tmp"
                    tmp.write_bytes(r.content)
                    try:
                        img = Image.open(tmp)
                        if img.size[0] > 140 and img.size[1] > 140:
                            p = out / f"negative_{idx:04d}.jpg"
                            img.convert("RGB").save(p, "JPEG", quality=90)
                            idx += 1
                            nfiles += 1
                    except:
                        pass
                    tmp.unlink(missing_ok=True)
                    time.sleep(0.01)
                except:
                    continue
    except:
        pass
print(nfiles)
