#!/usr/bin/env python3
"""Build / refresh the Golden Rabbit book catalog used by every promo variant.

Discovers books from goldenrabbit.co.kr (home page cards + JSON-LD lists on / and /books),
optionally adds explicit ISBNs, reads each detail page's Book JSON-LD, downloads covers
as JPG and writes shared/books/books.json.

Usage:
  python3 fetch_books.py                    # discover + fetch missing
  python3 fetch_books.py --refresh          # re-fetch every detail page and cover
  python3 fetch_books.py --isbn 979112451... --isbn ...   # add specific books
  python3 fetch_books.py --list             # print the catalog table and exit
"""
import argparse, html, io, json, re, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "shared" / "books"
COVERS = OUT / "covers"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/128 Safari/537.36"}
SITE = "https://goldenrabbit.co.kr"
BADGES = ["Coming Soon", "BEST", "NEW", "찜하기"]


def get(url, binary=False, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                data = r.read()
                return data if binary else data.decode("utf-8", "ignore")
        except Exception as e:  # noqa: BLE001
            if i == tries - 1:
                raise
            time.sleep(1.5 * (i + 1))


def drive_id(url):
    m = re.search(r"/d/([A-Za-z0-9_-]{20,})", url or "") or re.search(r"[?&]id=([A-Za-z0-9_-]{20,})", url or "")
    return m.group(1) if m else None


def ld_blocks(page):
    out = []
    for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S):
        try:
            out.append(json.loads(raw))
        except Exception:  # noqa: BLE001
            pass
    return out


def walk(o, fn):
    if isinstance(o, dict):
        fn(o)
        for v in o.values():
            walk(v, fn)
    elif isinstance(o, list):
        for v in o:
            walk(v, fn)


def discover():
    """isbn -> partial info from list pages (title, cover id, badges, series label, author)."""
    found = {}
    home = get(SITE)
    # rich home-page cards: <a href="/books/ISBN"> ... alt="title" ... text with badges/series/author
    for href, inner in re.findall(r'<a[^>]+href="/books/([0-9a-z_]+)"[^>]*>(.*?)</a>', home, re.S):
        alt = re.findall(r'alt="([^"]*)"', inner)
        src = re.findall(r'(?:src|srcSet|srcset)="([^"]+)"', inner)
        text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", inner))).strip()
        if not alt or not text:
            continue
        title = html.unescape(alt[0])
        badges = [b for b in BADGES if re.search(r"(^|\s)" + re.escape(b) + r"(\s|$)", text) and b != "찜하기"]
        rest = text
        for b in BADGES:
            rest = re.sub(r"(^|\s)" + re.escape(b) + r"(?=\s|$)", " ", rest)
        rest = re.sub(r"\s+", " ", rest).strip()
        series, author = "", ""
        if title in rest:
            pre, post = rest.split(title, 1)
            series, author = pre.strip(), post.strip()
        d = found.setdefault(href, {})
        d.update({"isbn": href, "title": title, "badges": badges, "series_label": series, "author_card": author})
        if src:
            d["cover_id"] = drive_id(src[0])
    # JSON-LD ItemLists on / and /books
    for page in (home, get(SITE + "/books")):
        def take(o):
            if o.get("@type") == "ListItem" and "/books/" in str(o.get("url", "")):
                isbn = o["url"].rstrip("/").split("/")[-1]
                d = found.setdefault(isbn, {"isbn": isbn})
                d.setdefault("title", o.get("name", ""))
                d.setdefault("cover_id", drive_id(o.get("image", "")))
        for blk in ld_blocks(page):
            walk(blk, take)
    return found


def detail(isbn):
    page = get(f"{SITE}/books/{isbn}")
    info = {}
    def take(o):
        if o.get("@type") == "Book":
            info["title_full"] = o.get("name", "")
            a = o.get("author")
            names = [x.get("name", "") for x in (a if isinstance(a, list) else [a]) if isinstance(x, dict)]
            info["authors"] = [n for n in names if n]
            info["published"] = o.get("datePublished", "")
            info["cover_id"] = drive_id(o.get("image", "")) or info.get("cover_id")
            offers = o.get("offers") or {}
            if isinstance(offers, dict):
                info["price"] = offers.get("price")
                info["availability"] = str(offers.get("availability", "")).split("/")[-1]
    for blk in ld_blocks(page):
        walk(blk, take)
    m = re.search(r'<meta property="og:description" content="([^"]*)"', page)
    if m:
        info["description"] = html.unescape(m.group(1))
    return info


def download_cover(cover_id, dest):
    from PIL import Image  # type: ignore
    data = get(f"https://lh3.googleusercontent.com/d/{cover_id}=w1080-rw", binary=True)
    im = Image.open(io.BytesIO(data)).convert("RGB")
    im.save(dest, "JPEG", quality=92)
    return im.size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--isbn", action="append", default=[])
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    COVERS.mkdir(parents=True, exist_ok=True)
    cat_path = OUT / "books.json"
    catalog = {b["isbn"]: b for b in json.loads(cat_path.read_text())} if cat_path.exists() else {}

    if a.list:
        for b in sorted(catalog.values(), key=lambda b: b.get("published", ""), reverse=True):
            print(f'{b["isbn"]}  {b.get("published",""):10s}  {",".join(b.get("badges",[])):12s}  {b.get("series_label",""):10s}  {b.get("title","")[:40]}  — {", ".join(b.get("authors",[]))}')
        return

    found = discover()
    for i in a.isbn:
        found.setdefault(i, {"isbn": i})
    print(f"discovered {len(found)} books")
    for isbn, d in found.items():
        if not re.fullmatch(r"[0-9a-z_]+", isbn):
            continue
        cur = catalog.get(isbn, {})
        merged = {**cur, **{k: v for k, v in d.items() if v}}
        if a.refresh or "authors" not in cur:
            try:
                merged.update({k: v for k, v in detail(isbn).items() if v})
            except Exception as e:  # noqa: BLE001
                print(f"  ⚠ detail {isbn}: {e}")
        cover = COVERS / f"{isbn}.jpg"
        if merged.get("cover_id") and (a.refresh or not cover.exists()):
            try:
                w, h = download_cover(merged["cover_id"], cover)
                merged["cover_size"] = [w, h]
            except Exception as e:  # noqa: BLE001
                print(f"  ⚠ cover {isbn}: {e}")
        if cover.exists():
            merged["cover"] = str(cover.relative_to(ROOT))
        merged.setdefault("badges", [])
        if not merged.get("title") and merged.get("title_full"):
            merged["title"] = merged["title_full"].split(" - ")[0]
        catalog[isbn] = merged
        print(f'  ✓ {isbn} {merged.get("title","")[:38]}')
    cat_path.write_text(json.dumps(sorted(catalog.values(), key=lambda b: b["isbn"]), ensure_ascii=False, indent=2))
    print(f"wrote {cat_path.relative_to(ROOT)} ({len(catalog)} books)")


if __name__ == "__main__":
    sys.exit(main())
