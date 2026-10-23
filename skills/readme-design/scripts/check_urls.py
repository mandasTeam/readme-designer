"""Confere links e imagens de um README: status HTTP e content-type, uma linha por URL.

Saída enxuta de propósito (só o que falhou, salvo --all): link morto e widget fora do ar
são o achado; listar 40 URLs OK só gasta contexto.

    python check_urls.py README.md
    python check_urls.py --url "https://github-readme-stats.vercel.app/api?username=x"
"""
from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 readme-design-check"}
URL_RE = re.compile(r"""(?:src|href|srcset)\s*=\s*["']([^"']+)["']|\]\((https?://[^)\s]+)\)""")
IMG_RE = re.compile(r"""<img[^>]+src\s*=\s*["']([^"']+)["']|!\[[^\]]*\]\((https?://[^)\s]+)\)|srcset\s*=\s*["']([^"']+)["']""")


def extract(text: str) -> tuple[list[str], set[str]]:
    """Todas as URLs http(s) em ordem, sem repetição, e o subconjunto usado como imagem."""
    seen, urls = set(), []
    for m in URL_RE.finditer(text):
        u = (m.group(1) or m.group(2)).strip()
        if u.startswith("http") and u not in seen:
            seen.add(u)
            urls.append(u)
    imgs = {next(g for g in m.groups() if g).strip() for m in IMG_RE.finditer(text)}
    return urls, imgs


def probe(url: str) -> tuple[int, str]:
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Content-Type", "") if e.headers else ""
    except Exception as e:  # DNS, timeout, TLS
        return 0, type(e).__name__


def verdict(url: str, status: int, ctype: str, is_img: bool) -> str:
    if status != 200:
        return "FALHA"
    if is_img and not ctype.startswith("image/"):
        return "NÃO-IMAGEM"
    return "ok"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("readme", nargs="?")
    ap.add_argument("--url", action="append", default=[])
    ap.add_argument("--all", action="store_true", help="mostra também as URLs ok")
    a = ap.parse_args()
    urls, imgs = extract(Path(a.readme).read_text(encoding="utf-8")) if a.readme else ([], set())
    urls += a.url
    imgs |= set(a.url)
    # mailto e âncoras não são checáveis por HTTP; LinkedIn responde 999 a robôs
    urls = [u for u in urls if "linkedin.com" not in u]
    with ThreadPoolExecutor(8) as ex:
        results = list(ex.map(probe, urls))
    bad = 0
    for u, (st, ct) in zip(urls, results):
        v = verdict(u, st, ct, u in imgs)
        bad += v != "ok"
        if v != "ok" or a.all:
            print(f"{v:<10} {st:>3} {ct.split(';')[0]:<22} {u[:110]}")
    print(f"{len(urls)} urls, {bad} com problema")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
