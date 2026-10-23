"""Gerador inicial dos SVGs de um README. Copie para <repo>/tools/build_assets.py e ajuste o CONFIG.

    python tools/build_assets.py            # escreve assets/*.svg

Mantenha o desenho em código: mudar texto/cor é editar o CONFIG e rodar de novo,
nunca editar SVG à mão (cada card tem 50-250 KB de paths; ler isso custa caro).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# aponte para a pasta scripts/ da skill ou copie svgkit.py para tools/
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / "skills" / "readme-design" / "scripts"))
from svgkit import Font, Theme, balloon, card_frame, chip, halftone, heading, num, rich_lines, rich_paths, svg  # noqa: E402

FONTS = ROOT / "tools" / "fonts"
CONFIG = {
    "theme": Theme(),  # troque as cores pelo plano de design (4-6 hex nomeados)
    "display": "Bangers-Regular.ttf",
    "body": "BarlowCondensed-SemiBold.ttf",
    "bold": "BarlowCondensed-Bold.ttf",
    "title": "SEU NOME",
    "chip": "CARGO @ EMPRESA",
    "subtitle": "O que você faz, numa linha",
    "place": "Cidade · Estado · País",
    "headings": {"h-sobre.svg": "QUEM É ESSE AÍ?", "h-contato.svg": "CONTATO"},
    "about": [  # (texto, estilo) — estilo: "r" regular, "b" negrito, "a" negrito em destaque
        ("E aí! Sou ", "r"), ("Fulano", "b"), (". Trabalho com ", "r"), ("o que importa", "a"), (".", "r"),
    ],
}


def banner(c: dict, display: Font, body: Font) -> str:
    t: Theme = c["theme"]
    w, h = 1200, 360
    d = ["<defs>", halftone("dots", 12, 1.8, "#FFFFFF", 0.07), "</defs>",
         f'<rect width="{w}" height="{h}" rx="20" fill="{t.card}"/>',
         f'<rect width="{w}" height="{h}" rx="20" fill="url(#dots)"/>',
         '<g transform="skewX(-12)">',
         f'<rect x="-60" y="0" width="300" height="{h}" fill="{t.stripes[0]}"/>',
         f'<rect x="252" y="0" width="14" height="{h}" fill="{t.stripes[1]}"/>',
         f'<rect x="278" y="0" width="24" height="{h}" fill="{t.stripes[2]}"/>',
         "</g>"]
    tx = 360
    size = display.fit(c["title"], 92, w - tx - 40, 2)
    d += [f'<path d="{display.path(c["title"], size, tx + 6, 160, tracking=2)}" fill="{t.ink}" opacity=".6"/>',
          f'<path d="{display.path(c["title"], size, tx, 154, tracking=2)}" fill="{t.text}" stroke="{t.ink}" '
          'stroke-width="6" stroke-linejoin="round" paint-order="stroke"/>']
    d += chip(tx, 184, c["chip"], display, 28, t.accent, t.ink)
    d += [f'<path d="{body.path(c["subtitle"], 28, tx, 276)}" fill="{t.soft}"/>',
          f'<path d="{body.path(c["place"], 22, tx, 310, tracking=.6)}" fill="{t.muted}"/>']
    return svg(w, h, f'{c["title"]} — {c["chip"]}. {c["subtitle"]}', "".join(d))


def about(c: dict, body: Font, bold: Font) -> str:
    t: Theme = c["theme"]
    w = 1200
    style = {"r": (body, t.ink), "b": (bold, t.ink), "a": (bold, t.stripes[0])}
    segs = [(txt, style[s][0], 27, style[s][1]) for txt, s in c["about"]]
    x1, x2, y1 = 60, 1192, 10
    lines = rich_lines(segs, x2 - x1 - 84)
    first, lh = y1 + 56, 37
    y2 = first + (len(lines) - 1) * lh + 34
    shape = balloon(x1, y1, x2, y2, 34, (y1 + y2) / 2, tail_dx=40)
    d = [f'<path d="{shape}" fill="{t.ink}" opacity=".5" transform="translate(6,7)"/>',
         f'<path d="{shape}" fill="{t.text}" stroke="{t.ink}" stroke-width="5" stroke-linejoin="round"/>']
    d += rich_paths(lines, x1 + 42, first, lh)
    plain = "".join(txt for txt, _ in c["about"])
    return svg(w, int(y2 + 14), plain, "".join(d))


def main() -> None:
    c = CONFIG
    display, body, bold = (Font(FONTS / c[k]) for k in ("display", "body", "bold"))
    out = ROOT / "assets"
    out.mkdir(exist_ok=True)
    files = {"banner.svg": banner(c, display, body), "about.svg": about(c, body, bold)}
    files.update({name: heading(text, display, c["theme"]) for name, text in c["headings"].items()})
    for name, content in files.items():
        (out / name).write_text(content, encoding="utf-8")
        print(f"{name}: {len(content) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
