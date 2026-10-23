"""Gera a arte do README deste repositório com o próprio template da skill (dogfooding).

    python tools/build_banner.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills" / "readme-design" / "scripts"))
sys.path.insert(0, str(ROOT / "skills" / "readme-design" / "templates"))
import build_assets as tpl  # noqa: E402
from svgkit import Font, Theme, heading  # noqa: E402

FONTS = ROOT / "tools" / "fonts"
CONFIG = {
    **tpl.CONFIG,
    "theme": Theme(),
    "title": "README DESIGN",
    "chip": "SKILL PARA AGENTES",
    "subtitle": "README de perfil e de projeto com cara de design, não de template",
    "place": "fatos conferidos · arte em SVG próprio · poucos tokens",
}
HEADINGS = {"h-fluxo.svg": "COMO FUNCIONA", "h-instalar.svg": "INSTALAÇÃO", "h-estrutura.svg": "ESTRUTURA"}


def main() -> None:
    display = Font(FONTS / "Bangers-Regular.ttf")
    body = Font(FONTS / "BarlowCondensed-SemiBold.ttf")
    out = ROOT / "assets"
    out.mkdir(exist_ok=True)
    files = {"banner.svg": tpl.banner(CONFIG, display, body)}
    files.update({n: heading(t, display, CONFIG["theme"]) for n, t in HEADINGS.items()})
    for name, content in files.items():
        (out / name).write_text(content, encoding="utf-8")
        print(f"{name}: {len(content) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
