"""Regenerate a doodle avatar as a layered paper-cut illustration via the OpenAI image edit API.

usage: gen_paper.py [<input.png> …] --out <output.png> --prompt <prompt-file-or-text> [--size 1024x1024] [--bg transparent|opaque]
The API key is read from ROOT/.env and never printed.
"""
import base64, os, sys, time, argparse, requests

ROOT = "/Users/canine89/Documents/dev/oh-my-motiongraphic"

def env():
    d = {}
    for line in open(os.path.join(ROOT, ".env"), encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            d[k.strip()] = v.strip().strip('"').strip("'")
    return d

ap = argparse.ArgumentParser()
ap.add_argument("inp", nargs="*")
ap.add_argument("--out", required=True)
ap.add_argument("--prompt", required=True)
ap.add_argument("--size", default="1024x1024")
ap.add_argument("--bg", default="transparent")
ap.add_argument("--quality", default="high")
ap.add_argument("--model", default=None)
a = ap.parse_args()

e = env()
key = e["OPENAI_API_KEY"]
model = a.model or e.get("OPENAI_IMAGE_MODEL", "gpt-image-1")
prompt = open(a.prompt, encoding="utf-8").read() if os.path.exists(a.prompt) else a.prompt

GEN = not a.inp
files = [("image[]", (os.path.basename(p), open(p, "rb"), "image/png")) for p in a.inp]
data = {"model": model, "prompt": prompt, "size": a.size, "quality": a.quality, "n": 1}
if a.bg:
    data["background"] = a.bg
t = time.time()
r = None
for attempt in range(4):
    try:
        if GEN:
            r = requests.post("https://api.openai.com/v1/images/generations",
                              headers={"Authorization": f"Bearer {key}"}, json=data, timeout=150)
        else:
            r = requests.post("https://api.openai.com/v1/images/edits",
                              headers={"Authorization": f"Bearer {key}"}, data=data, files=files, timeout=150)
    except requests.exceptions.RequestException as ex:
        print("retry after", type(ex).__name__, file=sys.stderr)
        r = None
        for _, (n, fh, _) in files:
            fh.seek(0)
        continue
    if r.status_code == 200:
        break
    print("HTTP", r.status_code, r.text[:600], file=sys.stderr)
    if r.status_code in (400, 401, 403, 404):
        sys.exit(1)
    time.sleep(5)
    for _, (n, fh, _) in files:
        fh.seek(0)
if r is None or r.status_code != 200:
    sys.exit(1)
j = r.json()
b64 = j["data"][0].get("b64_json")
if not b64:
    url = j["data"][0]["url"]
    img = requests.get(url, timeout=120).content
else:
    img = base64.b64decode(b64)
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
open(a.out, "wb").write(img)
print(f"ok {a.out} model={model} {time.time()-t:.1f}s usage={j.get('usage')}")
