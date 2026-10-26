"""Baixa fontes OFL do repositório google/fonts (ttf + OFL.txt) para gerar SVG offline.

    python fetch_fonts.py tools/fonts "<familia>/<Arquivo>.ttf" ...
    python fetch_fonts.py tools/fonts "ibmplexsans/IBMPlexSans[wdth,wght].ttf"

O caminho é <família em minúsculas>/<Arquivo>.ttf, igual ao de
https://github.com/google/fonts/tree/main/ofl. A maioria das famílias hoje é variável
(Arquivo[wght].ttf): um arquivo cobre todos os pesos, escolhidos em svgkit.Font(..., wght=N).
Commite as fontes e as licenças.
"""
from __future__ import annotations

import sys
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://raw.githubusercontent.com/google/fonts/main/ofl/"


def fetch(rel: str, dest: Path) -> None:
    family, name = rel.split("/", 1)
    dest.mkdir(parents=True, exist_ok=True)
    targets = [(rel, dest / name), (f"{family}/OFL.txt", dest / f"OFL-{family}.txt")]
    for src, out in targets:
        if out.exists():
            continue
        with urllib.request.urlopen(BASE + urllib.parse.quote(src), timeout=30) as r:
            out.write_bytes(r.read())
        print(f"{out} ({out.stat().st_size // 1024} KB)")


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    dest = Path(sys.argv[1])
    for rel in sys.argv[2:]:
        fetch(rel, dest)


if __name__ == "__main__":
    main()
