"""Gerador dos SVGs de um README. Copie para <repo>/tools/build_assets.py e ajuste o CONFIG.

    python tools/build_assets.py            # escreve assets/*.svg

Este arquivo é um esqueleto ESTRUTURAL: banner, card de texto e títulos de seção com
peças neutras do svgkit. O estilo (cores, fontes, formas, motivo) vem do plano de design
do projeto. Preencha o CONFIG com os tokens do plano e desenhe o motivo em `motif()`.

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
from svgkit import Font, Theme, card_frame, heading, pill, rich_lines, rich_paths, svg  # noqa: E402

FONTS = ROOT / "tools" / "fonts"
CONFIG = {
    "theme": Theme(),  # troque pelos tokens do plano (4-6 hex nomeados; motivo em extra)
    # (arquivo, eixos) — eixos só para fonte variável, ex.: ("Familia[wght].ttf", {"wght": 700})
    "display": ("DISPLAY.ttf", {}),
    "body": ("CORPO.ttf", {}),
    "bold": ("CORPO-NEGRITO.ttf", {}),
    "radius": 16,
    "title": "Seu Nome",
    "tag": "Cargo @ Empresa",
    "subtitle": "O que você faz, numa linha",
    "place": "Cidade, Estado",
    "headings": {"h-sobre.svg": "Sobre", "h-contato.svg": "Contato"},
    "about": [  # (texto, estilo) — estilo: "r" regular, "b" negrito, "a" negrito no acento
        ("Sou ", "r"), ("Fulano", "b"), (". Trabalho com ", "r"), ("o que importa", "a"), (".", "r"),
    ],
}


def motif(w: int, h: int, t: Theme) -> list[str]:
    """O elemento do plano que se repete em todo card (forma, textura, faixa, ícone...).
    Vazio por padrão: o motivo é do projeto, não do template."""
    return []


def load_fonts(c: dict, base: Path = FONTS) -> dict[str, Font]:
    return {k: Font(base / c[k][0], **c[k][1]) for k in ("display", "body", "bold")}


def banner(c: dict, f: dict[str, Font]) -> str:
    t: Theme = c["theme"]
    w, h, x = 1200, 320, 64
    d = card_frame(w, h, t, c["radius"]) + motif(w, h, t)
    size = f["display"].fit(c["title"], 84, w - x * 2)
    d.append(f'<path d="{f["display"].path(c["title"], size, x, 140)}" fill="{t.text}"/>')
    d += pill(x, 168, c["tag"], f["bold"], 22, t.accent, t.on_accent)
    d += [f'<path d="{f["body"].path(c["subtitle"], 28, x, 254)}" fill="{t.soft}"/>',
          f'<path d="{f["body"].path(c["place"], 20, x, 288)}" fill="{t.muted}"/>']
    return svg(w, h, f'{c["title"]} — {c["tag"]}. {c["subtitle"]}', "".join(d))


def about(c: dict, f: dict[str, Font]) -> str:
    t: Theme = c["theme"]
    w, x, lh = 1200, 56, 38
    style = {"r": (f["body"], t.soft), "b": (f["bold"], t.text), "a": (f["bold"], t.accent)}
    segs = [(txt, style[s][0], 26, style[s][1]) for txt, s in c["about"]]
    lines = rich_lines(segs, w - x * 2)
    h = 56 + (len(lines) - 1) * lh + 40
    d = card_frame(w, h, t, c["radius"]) + motif(w, h, t) + rich_paths(lines, x, 64, lh)
    return svg(w, h, "".join(txt for txt, _ in c["about"]), "".join(d))


def main() -> None:
    c = CONFIG
    f = load_fonts(c)
    out = ROOT / "assets"
    out.mkdir(exist_ok=True)
    files = {"banner.svg": banner(c, f), "about.svg": about(c, f)}
    files.update({name: heading(text, f["display"], c["theme"]) for name, text in c["headings"].items()})
    for name, content in files.items():
        (out / name).write_text(content, encoding="utf-8")
        print(f"{name}: {len(content) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
