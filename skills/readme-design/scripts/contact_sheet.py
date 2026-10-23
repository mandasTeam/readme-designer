"""Monta uma folha de conferência PNG com SVGs sobre fundo escuro e claro do GitHub.

Uma imagem só para inspecionar com visão: mais barato que um screenshot por card.
Para texto pequeno, peça um recorte (region) da folha em vez de outra captura.

    python contact_sheet.py saida.png assets/            # todos os .svg da pasta
    python contact_sheet.py saida.png a.svg b.svg --pair mission-*.svg

Dependências: resvg-py, pillow (só para a conferência; não vão para o repo do usuário).
"""
from __future__ import annotations

import argparse
import fnmatch
import io
from pathlib import Path

import resvg_py
from PIL import Image

DARK, LIGHT = "#0d1117", "#ffffff"


def render(path: Path, width: int) -> Image.Image:
    png = resvg_py.svg_to_bytes(svg_path=str(path), width=width)
    return Image.open(io.BytesIO(bytes(png))).convert("RGBA")


def collect(inputs: list[str]) -> list[Path]:
    files: list[Path] = []
    for item in inputs:
        p = Path(item)
        files += sorted(p.glob("*.svg")) if p.is_dir() else [p]
    return files


def rows_for(files: list[Path], pair_globs: list[str]) -> list[list[Path]]:
    """Arquivos que casam com --pair saem lado a lado (cards de meia largura)."""
    rows, pending = [], []
    for f in files:
        if any(fnmatch.fnmatch(f.name, g) for g in pair_globs):
            pending.append(f)
            if len(pending) == 2:
                rows.append(pending)
                pending = []
        else:
            rows.append([f])
    if pending:
        rows.append(pending)
    return rows


def sheet(rows: list[list[Path]], width: int, bg: str) -> Image.Image:
    imgs = [[render(f, width if len(r) == 1 else (width - 20) // 2) for f in r] for r in rows]
    h = sum(max(i.height for i in r) + 24 for r in imgs) + 24
    canvas = Image.new("RGBA", (width + 48, h), bg)
    y = 24
    for r in imgs:
        x = 24
        for im in r:
            canvas.alpha_composite(im, (x, y))
            x += im.width + 20
        y += max(i.height for i in r) + 24
    return canvas


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--width", type=int, default=1200)
    ap.add_argument("--pair", action="append", default=[], help="glob de cards de meia largura")
    ap.add_argument("--only", choices=["dark", "light"], help="gera só um fundo (metade do custo de visão)")
    a = ap.parse_args()
    rows = rows_for(collect(a.inputs), a.pair)
    parts = [sheet(rows, a.width, bg) for name, bg in (("dark", DARK), ("light", LIGHT)) if a.only in (None, name)]
    final = Image.new("RGBA", (parts[0].width, sum(p.height for p in parts)))
    y = 0
    for p in parts:
        final.paste(p, (0, y))
        y += p.height
    final.convert("RGB").save(a.out)
    print(f"{a.out} {final.width}x{final.height} ({sum(len(r) for r in rows)} svg)")


if __name__ == "__main__":
    main()
