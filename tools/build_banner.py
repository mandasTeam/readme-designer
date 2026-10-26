"""Gera a arte do README deste repositório com o próprio template da skill (dogfooding).

    python tools/build_banner.py

Plano de design deste repo (o de outro projeto será outro):
  Cor:       card #111418 · borda #262B33 · texto #EEF0F3 · apoio #B9BFC9 · acento #6CC6B5
  Tipo:      IBM Plex Sans 700 (títulos) e 450/600 (corpo) · IBM Plex Mono (marcas de markdown)
  Motivo:    a marca de markdown ("#", "##") em mono no acento, antes de cada título
  Movimento: nenhum
  Princípio: parece documentação bem diagramada, não pôster
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills" / "readme-design" / "scripts"))
sys.path.insert(0, str(ROOT / "skills" / "readme-design" / "templates"))
import build_assets as tpl  # noqa: E402
from svgkit import Font, Theme, card_frame, svg  # noqa: E402

FONTS = ROOT / "tools" / "fonts"
SANS = "IBMPlexSans[wdth,wght].ttf"
THEME = Theme(card="#111418", line="#262B33", text="#EEF0F3", soft="#B9BFC9", muted="#868E9B",
              accent="#6CC6B5", on_accent="#0B0E11")
CONFIG = {
    **tpl.CONFIG,
    "theme": THEME,
    "display": (SANS, {"wght": 700}),
    "body": (SANS, {"wght": 450}),
    "bold": (SANS, {"wght": 600}),
    "radius": 14,
    "title": "readme-design",
    "tag": "skill para agentes de código",
    "subtitle": "README de perfil e de projeto com design próprio, não de template",
    "place": "fatos conferidos · arte em SVG próprio · poucos tokens",
}
HEADINGS = {"h-fluxo.svg": "Como funciona", "h-instalar.svg": "Instalação", "h-estrutura.svg": "Estrutura"}


def heading(text: str, f: dict, mono: Font, t: Theme, w: int = 1200, h: int = 64) -> str:
    """Título com a marca "##" em mono no acento e régua fina até a borda, sobre fundo próprio."""
    base = h / 2 + f["display"].cap_height(30) / 2
    x = 28 + mono.width("##", 26) + 14
    d = card_frame(w, h, t, 12) + [
        f'<path d="{mono.path("##", 26, 28, base)}" fill="{t.accent}"/>',
        f'<path d="{f["display"].path(text, 30, x, base)}" fill="{t.text}"/>']
    rx = x + f["display"].width(text, 30) + 24
    d.append(f'<line x1="{rx:.0f}" y1="{h / 2:.0f}" x2="{w - 28}" y2="{h / 2:.0f}" stroke="{t.line}" stroke-width="2"/>')
    return svg(w, h, text, "".join(d))


def main() -> None:
    f = tpl.load_fonts(CONFIG, FONTS)
    mono = Font(FONTS / "IBMPlexMono-Medium.ttf")
    tpl.motif = lambda w, h, t: [f'<path d="{mono.path("#", 84, 1060, 140)}" fill="{t.accent}" opacity=".9"/>']
    out = ROOT / "assets"
    out.mkdir(exist_ok=True)
    files = {"banner.svg": tpl.banner(CONFIG, f)}
    files.update({n: heading(txt, f, mono, THEME) for n, txt in HEADINGS.items()})
    for name, content in files.items():
        (out / name).write_text(content, encoding="utf-8")
        print(f"{name}: {len(content) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
