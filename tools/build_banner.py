"""Gera a arte do README deste repositório: uma folha única na direção de arte do mandasTeam.

    python tools/build_banner.py                 # escreve assets/readme-designer.svg
    python tools/build_banner.py --readme        # e reescreve o alt do <img> no README.md

A direção de arte é a do BRAND.md em mandasTeam/team-docs (fonte única dos tokens). As peças
plate(), rays(), dither(), sparks(), terminal(), section_title() e Glyphs vêm do gerador de lá;
mudou a marca, mude aqui junto. Texto ou ordem = editar CONFIG e rodar de novo; nunca edite o SVG.

Plano de design desta peça:
  Cor:       mármore #FBF8F1 · pergaminho #F3ECDD · veio #E3D6B8 · ouro #C79A3A (só linha e ponto)
             · ouro velho #8A6417 (rótulo e link) · tinta #1A1712 · grafite #4B4438 · pó #6E6656
  Tipo:      Big Shoulders 800 (nome, títulos, numerais) · Geist Mono 400/600 (texto e comandos)
  Grade:     1200 px de largura, margem de 72 px, texto alinhado à esquerda
  Motivo:    a fagulha (sol da forja no herói, régua com fagulha nos títulos) · plinto · janela
  Movimento: só as fagulhas do martelo piscam; param com prefers-reduced-motion
  Princípio: prancha de catálogo de gravura; o fluxo da skill vira seis lâminas numeradas

Figura: Hendrick Goltzius, segundo Polidoro da Caravaggio, "Vulcan" (c. 1592), National Gallery
of Art, CC0. Recorte de mandasTeam/team-docs (tools/art/vulcan.png), reduzido para 1100 px.
"""
from __future__ import annotations

import argparse
import base64
import io
import math
import random
import re
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills" / "readme-design" / "scripts"))
from fontTools.pens.svgPathPen import SVGPathPen  # noqa: E402
from fontTools.pens.transformPen import TransformPen  # noqa: E402
from svgkit import REDUCED_MOTION, Font, MissingGlyph, Theme, num, svg  # noqa: E402

FONTS = ROOT / "tools" / "fonts"
ART = ROOT / "tools" / "art" / "vulcan.png"
OUT = ROOT / "assets" / "readme-designer.svg"
HEAD = (0.582, 0.107)     # centro da cabeça, relativo ao recorte
HAMMER = (0.055, 0.415)   # cabeça do martelo, relativo ao recorte

# ----------------------------------------------------------------------------- tokens (BRAND.md §2)
T = Theme(card="#FBF8F1", line="#E3D6B8", text="#1A1712", soft="#4B4438", muted="#6E6656",
          accent="#8A6417", on_accent="#FBF8F1",
          extra={"pergaminho": "#F3ECDD", "ouro": "#C79A3A", "brasa": "#E9CF8E", "bronze": "#7A5716"})
X = T.extra

CONFIG = {
    "name": ("readme", "designer"),
    "repo": "mandasTeam/readme-designer",
    "tagline": "README do GitHub com design próprio.",
    "about": [
        ("Skill no formato ", "r"), ("SKILL.md", "a"),
        (" que ensina o agente a criar e redesenhar README de perfil e de projeto. Ele confere os fatos, "
         "planeja o design, gera a arte em SVG e confere o resultado renderizado antes de dizer que terminou.", "r"),
    ],
    "promises": ["fatos conferidos na API do GitHub",
                 "arte em SVG com texto em path",
                 "poucos tokens, sem cortar a conferência"],
    "terminal": ("~/readme-designer", "$ ls skills/readme-design", "SKILL.md  references/  scripts/"),
    "plinth": "HEFESTO",
    "steps": [
        ("I", "Auditoria", "audit_profile.py junta perfil, repos, fixados, links mortos e telefone exposto numa saída curta."),
        ("II", "Perguntas", "O que a auditoria não resolve vai num lote só, com até cinco perguntas."),
        ("III", "Plano", "Cores, fontes, grade, motivo e movimento tirados do assunto e revisados contra os clichês."),
        ("IV", "Arte", "svgkit molda o texto com HarfBuzz e desenha cada glifo como path, porque o GitHub não carrega fonte em <img>."),
        ("V", "README", "Esqueletos de perfil e de projeto. Stats, cobrinha e visitas no tema, por workflow."),
        ("VI", "Conferência", "Folha PNG em fundo claro e escuro, URLs checadas, imagens carregadas e workflow rodado."),
    ],
    "tokens": ["filtrar a saída antes de ela entrar no contexto",
               "nunca ler SVG gerado",
               "conferir tudo com uma imagem só",
               "fazer as perguntas em lote",
               "mandar relatório curto"],
    "tokens_note": "Nada disso corta a verificação.",
    "clone": "$ git clone https://github.com/mandasTeam/readme-designer.git",
    "agents": [
        ("Hermes Agent", "adicione <clone>/skills em skills.external_dirs no config.yaml"),
        ("Claude Code", "$ cp -r readme-designer/skills/readme-design ~/.claude/skills/"),
        ("Outros agentes", "copie skills/readme-design/ para a pasta de skills do agente"),
    ],
    "pip": "$ python -m pip install -r requirements-dev.txt",
    "tree": [
        ("skills/readme-design/", ""),
        ("├── SKILL.md", "fluxo, regras de tokens e de design, armadilhas"),
        ("├── references/", "carregadas só no passo que pede"),
        ("│   ├── auditoria.md", "o que conferir antes de desenhar"),
        ("│   ├── design.md", "plano, clichês, hierarquia, acessibilidade, copy"),
        ("│   ├── svg-pipeline.md", "texto em path, peças do svgkit, avatar"),
        ("│   ├── widgets.md", "stats, streak, cobrinha, visitas"),
        ("│   ├── readme-projeto.md", "README de projeto e revisão de docs"),
        ("│   ├── tokens.md", "onde o gasto aparece e o que trocar"),
        ("│   └── preferencias-igor.md", "gosto geral do dono"),
        ("├── scripts/", "svgkit, audit_profile, check_urls, contact_sheet, visits"),
        ("└── templates/", "build_assets.py, esqueletos de README, workflow"),
        ("tests/", "pytest sem rede"),
        ("tools/build_banner.py", "gera esta folha"),
    ],
    "dev": "$ python -m pytest -q && python tools/build_banner.py",
    "footer": ("MIT · fontes OFL em tools/fonts", "direção de arte: mandasTeam/team-docs"),
}


# ----------------------------------------------------------------------------- peças da marca (team-docs)
class Glyphs:
    """Texto em path com glifo reaproveitado: cada glifo vira um <path id> em <defs> e cada
    ocorrência um <use>. Corta o SVG a menos da metade frente a um path por letra."""

    def __init__(self) -> None:
        self.ids: dict[tuple[int, str], str] = {}
        self.paths: list[str] = []

    def _glyph(self, font: Font, name: str) -> str | None:
        key = (id(font), name)
        if key not in self.ids:
            pen = SVGPathPen(font.gs, ntos=lambda v: str(round(v)))
            font.gs[name].draw(TransformPen(pen, (1, 0, 0, -1, 0, 0)))
            d = pen.getCommands()
            self.ids[key] = f"g{len(self.ids)}" if d else ""
            if d:
                self.paths.append(f'<path id="{self.ids[key]}" d="{d}"/>')
        return self.ids[key] or None

    def text(self, font: Font, s: str, size: float, x: float, y: float, fill: str,
             anchor: str = "start", tracking: float = 0) -> str:
        x -= {"start": 0, "middle": font.width(s, size, tracking) / 2, "end": font.width(s, size, tracking)}[anchor]
        sc = size / font.upem
        infos, pos = font._shape(s)
        uses, cx = [], 0.0
        for info, p in zip(infos, pos):
            if info.codepoint == 0:
                raise MissingGlyph(f"{font.name} sem glifo em {s!r}")
            gid = self._glyph(font, font.order[info.codepoint])
            if gid:
                uses.append(f'<use href="#{gid}" x="{round(cx + p.x_offset)}" y="{round(-p.y_offset)}"/>')
            cx += p.x_advance + tracking / sc
        return f'<g transform="translate({num(x)},{num(y)}) scale({sc:.5f})" fill="{fill}">{"".join(uses)}</g>'

    def rich(self, segs: list[tuple[str, Font, float, str]], x: float, y: float, max_w: float,
             lh: float) -> tuple[list[str], float]:
        """Parágrafo com trechos de estilos diferentes. Devolve as peças e a linha de base final."""
        words: list[list[tuple[str, Font, float, str]]] = [[]]
        for t, f, sz, col in segs:
            for i, part in enumerate(t.split(" ")):
                if i:
                    words.append([])
                if part:
                    words[-1].append((part, f, sz, col))
        out, cx, cy = [], 0.0, y
        for w in (w for w in words if w):
            ww = sum(f.width(t, sz) for t, f, sz, _ in w)
            sp = w[0][1].width(" ", w[0][2])
            if cx and cx + sp + ww > max_w:
                cx, cy = 0.0, cy + lh
            elif cx:
                cx += sp
            for t, f, sz, col in w:
                out.append(self.text(f, t, sz, x + cx, cy, col))
                cx += f.width(t, sz)
        return out, cy

    def defs(self) -> str:
        return "".join(self.paths)


W = 1200
X0 = 72
RX = 6
INSET = 14
G = Glyphs()

DEFS_GRAIN = ('<filter id="grain" x="0" y="0" width="100%" height="100%">'
              '<feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="4" stitchTiles="stitch"/>'
              '<feColorMatrix values="0 0 0 0 .48 0 0 0 0 .34 0 0 0 0 .09 0 0 0 .55 -.22"/></filter>')


def fonts() -> dict[str, Font]:
    bs, gm = FONTS / "BigShoulders[opsz,wght].ttf", FONTS / "GeistMono[wght].ttf"
    return {"display": Font(bs, wght=800, opsz=72), "body": Font(gm, wght=400), "bold": Font(gm, wght=600)}


def plate(w: int, h: int) -> list[str]:
    """Placa: mármore com grão de papel, borda veio e filete em ouro (a marca da chapa)."""
    return [f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{RX}" fill="{T.card}" stroke="{T.line}" stroke-width="2"/>',
            f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{RX}" filter="url(#grain)"/>',
            f'<rect x="{INSET}" y="{INSET}" width="{w - 2 * INSET}" height="{h - 2 * INSET}" fill="none" '
            f'stroke="{X["ouro"]}" stroke-width="1"/>']


def rays(cx: float, cy: float, r0: float, r1: tuple[float, float], n: int, seed: int,
         a0: float = 0, a1: float = 360, width: float = 1.1, color: str | None = None) -> str:
    """Motivo: a fagulha. Raios finos em feixes saindo de um ponto."""
    rnd = random.Random(seed)
    d = []
    for i in range(n):
        a = math.radians(a0 + (a1 - a0) * i / n)
        bundle = 0.5 + 0.5 * math.sin(i * 0.9) * math.cos(i * 0.23)
        ln = r1[0] + (r1[1] - r1[0]) * max(0.0, min(1.0, bundle + rnd.uniform(-0.15, 0.15)))
        d.append(f"M{num(cx + r0 * math.cos(a))},{num(cy + r0 * math.sin(a))}"
                 f"L{num(cx + (r0 + ln) * math.cos(a))},{num(cy + (r0 + ln) * math.sin(a))}")
    return (f'<path d="{"".join(d)}" stroke="{color or X["ouro"]}" stroke-width="{width}" '
            f'stroke-linecap="round" fill="none"/>')


def dither(w: int, h: int, px: int = 1) -> str:
    """Estátua em ouro: dithering de 4 tons (transparente, brasa, ouro, bronze) sobre o recorte."""
    src = Image.open(ART).convert("LA").resize((w // px, h // px), Image.Resampling.LANCZOS)
    g, a = src.split()
    g = ImageOps.autocontrast(g, cutoff=1).point(lambda v: int(40 + v * 0.86))
    pal = Image.new("P", (1, 1))
    cols = [T.card, X["brasa"], X["ouro"], X["bronze"]]
    pal.putpalette([int(c[i:i + 2], 16) for c in cols for i in (1, 3, 5)] + [0] * (256 - 4) * 3)
    q = Image.merge("RGB", (g, g, g)).quantize(palette=pal, dither=Image.Dither.FLOYDSTEINBERG)
    q.paste(0, mask=a.point(lambda v: 255 if v < 128 else 0))   # fora da figura = transparente
    buf = io.BytesIO()
    q.save(buf, "PNG", optimize=True, transparency=0, bits=2)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def sparks(cx: float, cy: float, seed: int) -> list[str]:
    """Fagulhas do martelo: pontos quadrados (o pixel do dithering) que piscam em tempos diferentes."""
    rnd = random.Random(seed)
    out = []
    for i in range(16):
        a = math.radians(rnd.uniform(150, 290))
        r = rnd.uniform(14, 78)
        s = rnd.choice((3, 4, 4, 6))
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        col = X["ouro"] if i % 3 else X["bronze"]
        out.append(f'<rect class="sp" style="animation-delay:{i * 0.37 % 2.6:.2f}s" x="{num(x)}" y="{num(y)}" '
                   f'width="{s}" height="{s}" fill="{col}"/>')
    return out


def terminal(x: float, y: float, w: float, f: dict[str, Font], lines: tuple[str, str, str]) -> list[str]:
    """Janela flutuante: pergaminho, barra em tinta, sombra chapada em ouro deslocada 6 px."""
    title, cmd, out = lines
    bar, h = 28, 92
    return [f'<rect x="{num(x + 6)}" y="{num(y + 6)}" width="{num(w)}" height="{h}" fill="{X["ouro"]}"/>',
            f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{h}" fill="{X["pergaminho"]}" stroke="{T.text}" stroke-width="1.5"/>',
            f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{bar}" fill="{T.text}"/>',
            G.text(f["body"], title, 15, x + 14, y + 19, fill=X["brasa"]),
            G.text(f["bold"], cmd, 17, x + 14, y + bar + 26, fill=T.accent),
            G.text(f["bold"], out, 17, x + 14, y + bar + 52, fill=T.text)]


def section_title(text: str, y: float, f: dict[str, Font]) -> list[str]:
    """Título de seção: display em tinta, régua de ouro e fagulha pequena na ponta."""
    size, x_end = 56, W - X0
    tw = f["display"].width(text, size)
    mid = y - f["display"].cap_height(size) / 2
    return [G.text(f["display"], text, size, X0, y, fill=T.text),
            f'<line x1="{num(X0 + tw + 24)}" y1="{num(mid)}" x2="{num(x_end - 40)}" y2="{num(mid)}" stroke="{X["ouro"]}" stroke-width="1.5"/>',
            rays(x_end - 18, mid, 5, (8, 22), 26, 3, width=1.2)]


def cmd_box(x: float, y: float, w: float, cmd: str, f: dict[str, Font], h: float = 46) -> list[str]:
    """Caixa de comando em tinta, como o git clone das pranchas de skill."""
    cs = f["body"].fit(cmd, 17, w - 32, floor=13)
    return [f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{h}" fill="{T.text}"/>',
            G.text(f["body"], cmd, cs, x + 16, y + h / 2 + f["body"].cap_height(cs) / 2, fill=X["brasa"])]


# ----------------------------------------------------------------------------- seções
def hero(c: dict, f: dict[str, Font]) -> tuple[list[str], list[str], float]:
    fh = 700
    aw, ah = Image.open(ART).size
    fw = fh * aw / ah
    fx, fy = 708, 74
    hx, hy = fx + fw * HEAD[0], fy + fh * HEAD[1]
    mx, my = fx + fw * HAMMER[0], fy + fh * HAMMER[1]
    py = fy + fh - 6                                   # topo do plinto
    defs = [f'<radialGradient id="fade" cx="{num(hx)}" cy="{num(hy)}" r="640" gradientUnits="userSpaceOnUse">'
            '<stop offset=".15" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>',
            f'<mask id="m"><rect width="{W}" height="{num(py)}" fill="url(#fade)"/></mask>',
            f'<clipPath id="in"><rect x="{INSET}" y="76" width="{W - 2 * INSET}" height="{num(py - 76)}"/></clipPath>']
    d = []
    # cabeçalho
    owner, name = c["repo"].split("/")
    d.append(f'<line x1="{X0}" y1="76" x2="{W - X0}" y2="76" stroke="{X["ouro"]}" stroke-width="1"/>')
    d.append(G.text(f["bold"], owner, 15, X0, 52, fill=T.text))
    d.append(G.text(f["body"], "/ " + name, 15, X0 + f["bold"].width(owner, 15) + 10, 52, fill=T.muted))
    d.append(G.text(f["body"], "github.com/" + c["repo"], 15, W - X0, 52, anchor="end", fill=T.accent))
    # sol da forja
    d.append(f'<g clip-path="url(#in)" mask="url(#m)">'
             f'{rays(hx, hy, 104, (120, 620), 180, 7, width=1)}'
             f'<circle cx="{num(hx)}" cy="{num(hy)}" r="96" fill="none" stroke="{X["ouro"]}" stroke-width="1.5"/>'
             f'<circle cx="{num(hx)}" cy="{num(hy)}" r="104" fill="none" stroke="{X["ouro"]}" stroke-width=".8" stroke-dasharray="2 5"/>'
             f'</g>')
    # plinto
    pw = 380
    px = hx - pw / 2
    d.append(f'<rect x="{num(px)}" y="{num(py)}" width="{pw}" height="58" fill="{X["pergaminho"]}" stroke="{X["ouro"]}" stroke-width="1.5"/>')
    d.append(f'<rect x="{num(px - 16)}" y="{num(py + 58)}" width="{pw + 32}" height="12" fill="{X["ouro"]}"/>')
    d.append(G.text(f["display"], c["plinth"], 30, hx, py + 29 + f["display"].cap_height(30) / 2,
                    anchor="middle", tracking=16, fill=T.accent))
    # estátua
    d.append(f'<image x="{num(fx)}" y="{fy}" width="{num(fw)}" height="{fh}" href="{dither(int(fw), fh)}" '
             f'style="image-rendering:pixelated"/>')
    d += sparks(mx - 6, my - 4, 5)
    # nome e apresentação
    for i, part in enumerate(c["name"]):
        size = f["display"].fit(part, 196, 620)
        d.append(G.text(f["display"], part, size, X0 - 6, 286 + i * 170, fill=T.text))
    d.append(G.text(f["bold"], c["tagline"], 26, X0, 528, fill=T.text))
    st = {"r": (f["body"], T.soft), "a": (f["bold"], T.accent)}
    parts, last = G.rich([(t, st[s][0], 19, st[s][1]) for t, s in c["about"]], X0, 576, 580, 31)
    d += parts
    y = last + 58
    d.append(G.text(f["body"], "o que entrega", 15, X0, y, fill=T.accent))
    for i, ln in enumerate(c["promises"]):
        yy = y + 36 + i * 31
        d.append(G.text(f["bold"], str(i + 1), 17, X0, yy, fill=X["ouro"]))
        d.append(G.text(f["body"], ln, 17, X0 + 28, yy, fill=T.text))
    d += terminal(776, 604, 366, f, c["terminal"])
    return defs, d, max(py + 70, y + 36 + 2 * 31)


def steps(c: dict, f: dict[str, Font], y: float) -> tuple[list[str], float]:
    """O fluxo em seis lâminas numeradas, três por linha."""
    d = section_title("Como funciona", y, f)
    gap, cols, ph, p = 24, 3, 252, 26
    pw = (W - 2 * X0 - gap * (cols - 1)) / cols
    top = y + 40
    for i, (numeral, name, desc) in enumerate(c["steps"]):
        x = X0 + (i % cols) * (pw + gap)
        yy = top + (i // cols) * (ph + gap)
        d.append(f'<rect x="{num(x)}" y="{num(yy)}" width="{num(pw)}" height="{ph}" fill="{X["pergaminho"]}" stroke="{T.line}" stroke-width="1.5"/>')
        d.append(G.text(f["display"], "Pl. " + numeral, 24, x + p, yy + 46, fill=T.accent))
        d.append(G.text(f["display"], name, 44, x + p - 1, yy + 100, fill=T.text))
        for j, ln in enumerate(f["body"].wrap(desc, 16, pw - 2 * p)):
            d.append(G.text(f["body"], ln, 16, x + p, yy + 138 + j * 24, fill=T.soft))
    return d, top + 2 * ph + gap


def tokens(c: dict, f: dict[str, Font], y: float) -> tuple[list[str], float]:
    d = section_title("Poucos tokens", y, f)
    top = y + 48
    half = 600                                    # a 1ª coluna tem a frase mais longa
    for i, ln in enumerate(c["tokens"]):
        x = X0 + (i % 2) * half
        yy = top + 10 + (i // 2) * 34
        d.append(f'<rect x="{num(x)}" y="{num(yy - 9)}" width="6" height="6" fill="{X["ouro"]}"/>')
        d.append(G.text(f["body"], ln, 18, x + 22, yy, fill=T.text))
    rows = (len(c["tokens"]) + 1) // 2
    ny = top + 10 + rows * 34 + 12
    d.append(G.text(f["bold"], c["tokens_note"], 18, X0, ny, fill=T.accent))
    return d, ny


def install(c: dict, f: dict[str, Font], y: float) -> tuple[list[str], float]:
    d = section_title("Instalação", y, f)
    cw = W - 2 * X0
    yy = y + 40
    d += cmd_box(X0, yy, cw, c["clone"], f)
    yy += 46 + 52
    col = 230
    rule = lambda ry: f'<line x1="{X0}" y1="{num(ry)}" x2="{W - X0}" y2="{num(ry)}" stroke="{T.line}" stroke-width="1.5"/>'  # noqa: E731
    d.append(rule(yy - 30))
    for agent, how in c["agents"]:
        d.append(G.text(f["display"], agent, 28, X0, yy + 4, fill=T.text))
        cmd = how.startswith("$")
        fnt = f["bold"] if cmd else f["body"]
        d.append(G.text(fnt, how, fnt.fit(how, 17, cw - col), X0 + col, yy, fill=T.accent if cmd else T.soft))
        yy += 58
        d.append(rule(yy - 30))
    yy += 18
    d.append(G.text(f["body"], "os scripts pedem Python 3.11+", 15, X0, yy, fill=T.accent))
    d += cmd_box(X0, yy + 16, cw, c["pip"], f)
    return d, yy + 16 + 46


def tree(c: dict, f: dict[str, Font], y: float) -> tuple[list[str], float]:
    d = section_title("Estrutura", y, f)
    lh, p = 30, 30
    h = p * 2 + lh * (len(c["tree"]) - 1) + 12
    top = y + 40
    d.append(f'<rect x="{X0}" y="{num(top)}" width="{W - 2 * X0}" height="{num(h)}" fill="{X["pergaminho"]}" stroke="{T.line}" stroke-width="1.5"/>')
    note_x = X0 + p + 400
    for i, (path, note) in enumerate(c["tree"]):
        yy = top + p + 14 + i * lh
        lead, rest = re.match(r"^([│├└─ ]*)(.*)$", path).groups()
        if lead:
            d.append(G.text(f["body"], lead, 17, X0 + p, yy, fill=X["ouro"]))
        lx = X0 + p + (f["body"].width(lead, 17) if lead else 0)
        d.append(G.text(f["bold"] if rest.endswith("/") else f["body"], rest, 17, lx, yy, fill=T.text))
        if note:
            d.append(G.text(f["body"], note, 16, note_x, yy, fill=T.muted))
    yy = top + h + 44
    d.append(G.text(f["body"], "para desenvolver", 15, X0, yy, fill=T.accent))
    d += cmd_box(X0, yy + 16, W - 2 * X0, c["dev"], f)
    return d, yy + 16 + 46


# ----------------------------------------------------------------------------- a folha
def folio(c: dict, f: dict[str, Font]) -> str:
    global G
    G = Glyphs()
    defs, body, y = hero(c, f)
    for part in (steps, tokens, install, tree):
        pd, y = part(c, f, y + 110)
        body += pd
    y += 72
    body.append(f'<line x1="{X0}" y1="{num(y - 34)}" x2="{W - X0}" y2="{num(y - 34)}" stroke="{X["ouro"]}" stroke-width="1"/>')
    body.append(G.text(f["body"], c["footer"][0], 15, X0, y, fill=T.muted))
    body.append(G.text(f["body"], c["footer"][1], 15, W - X0, y, anchor="end", fill=T.accent))
    h = round(y + 44)

    head = [f'<defs>{DEFS_GRAIN}{"".join(defs)}</defs>'] + plate(W, h)
    style = ("@keyframes tw{0%,100%{opacity:0}45%{opacity:1}}"
             ".sp{opacity:0;animation:tw 2.6s ease-in-out infinite}" + REDUCED_MOTION
             + "@media (prefers-reduced-motion:reduce){.sp{opacity:.8}}")
    cmd = lambda s: s.removeprefix("$ ")  # noqa: E731
    about = "".join(t for t, _ in c["about"])
    title = " ".join([
        f'{"-".join(c["name"])}, {c["repo"]}. {c["tagline"]} {about}',
        "O que entrega: " + "; ".join(c["promises"]) + ".",
        "Como funciona: " + " ".join(f"{n}. {nm}: {ds}" for n, nm, ds in c["steps"]),
        "Poucos tokens: " + "; ".join(c["tokens"]) + ". " + c["tokens_note"],
        "Instalação: " + cmd(c["clone"]) + ". " + " ".join(f"{a}: {cmd(h_)}." for a, h_ in c["agents"])
        + " Os scripts pedem Python 3.11+: " + cmd(c["pip"]) + ".",
        "Estrutura: " + "; ".join(p.strip("│├└─ ") + (f" ({n})" if n else "") for p, n in c["tree"]) + ".",
        "Para desenvolver: " + cmd(c["dev"]) + ".",
        f'{c["footer"][0]}. {c["footer"][1]}.',
    ])
    return svg(W, h, title, "".join(head + body) + f"<defs>{G.defs()}</defs>", style)


def main() -> None:
    ap = argparse.ArgumentParser(description="Gera a folha do README deste repositório.")
    ap.add_argument("--readme", action="store_true", help="também atualiza o alt do <img> no README.md")
    args = ap.parse_args()
    content = folio(CONFIG, fonts())
    OUT.parent.mkdir(exist_ok=True)
    for old in OUT.parent.glob("*.svg"):
        old.unlink()
    OUT.write_text(content, encoding="utf-8", newline="\n")
    print(f"{OUT.name}: {len(content) / 1024:.0f} KB")
    if args.readme:
        alt = content.split('<title id="t">', 1)[1].split("</title>", 1)[0].replace('"', "&quot;")
        readme = ROOT / "README.md"
        txt = readme.read_text(encoding="utf-8").replace("\r\n", "\n")
        new = re.sub(r'(<img src="assets/readme-designer\.svg"[^>]*?alt=")[^"]*(")',
                     lambda m: m.group(1) + alt + m.group(2), txt)
        readme.write_text(new, encoding="utf-8", newline="\n")
        print("README.md: alt", "atualizado" if new != txt else "sem mudança")


if __name__ == "__main__":
    main()
