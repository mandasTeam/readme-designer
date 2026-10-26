"""Contador de visitas no visual do README (roda no GitHub Actions, publica na branch output).

O selo do komarev.com não aceita estilo. O README carrega um pixel dele para contar
e mostra o card gerado aqui. Cada leitura do workflow também soma +1 no komarev,
então descontamos essas leituras (bot_hits) guardadas em visits.json.

    python visits.py dist --user <user> --display fonts/<Display>.ttf --body "fonts/<Corpo>[wght].ttf@wght=600" \\
        --theme tools/theme.json
    python visits.py dist --count 42 ...      # teste local: sem rede, não infla o contador

--theme é um JSON com os campos de svgkit.Theme (tokens do plano de design do projeto).
Fonte variável: acrescente @eixo=valor[,eixo=valor] ao caminho.
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svgkit import Font, Theme, card_frame, svg  # noqa: E402


def parse_count(komarev_svg: str) -> int:
    """O último <text> do selo é o número (pode vir com separador de milhar)."""
    texts = re.findall(r"<text[^>]*>([^<]*)</text>", komarev_svg)
    return int(re.sub(r"\D", "", texts[-1]))


def next_state(prev: dict, raw: int) -> dict:
    bot = int(prev.get("bot_hits", 0)) + 1
    return {"raw": raw, "bot_hits": bot, "shown": max(raw - bot, 0)}


def previous_state() -> dict:
    try:
        subprocess.run(["git", "fetch", "--depth=1", "origin", "output"], check=True, capture_output=True)
        out = subprocess.run(["git", "show", "FETCH_HEAD:visits.json"], check=True, capture_output=True).stdout
        return json.loads(out)
    except Exception:
        return {"bot_hits": 0}


def card(n: int, display: Font, body: Font, theme: Theme, label: str = "Visitas", rx: float = 16) -> str:
    """Card neutro: rótulo, número em dígitos de largura fixa e o motivo do projeto por cima, se houver."""
    w, h = 600, 150
    d = card_frame(w, h, theme, rx)
    d.append(f'<path d="{body.path(label, 18, 40, 44)}" fill="{theme.muted}"/>')
    digits = str(max(n, 0)).rjust(6, "0")
    lead = len(digits) - len(str(max(n, 0)))
    x, bw, gap = 40, 54, 8
    for i, ch in enumerate(digits):
        color = theme.muted if i < lead else theme.text
        d += [f'<rect x="{x}" y="62" width="{bw}" height="64" rx="{min(rx, 10)}" fill="none" '
              f'stroke="{theme.line}" stroke-width="2"/>',
              f'<path d="{display.path(ch, 44, x + bw / 2, 94 + display.cap_height(44) / 2, "middle")}" fill="{color}"/>']
        x += bw + gap
    return svg(w, h, f"{label}: {n}", "".join(d))


def font_arg(arg: str) -> Font:
    """"arquivo.ttf" ou "arquivo.ttf@wght=600,wdth=90" (fonte variável)."""
    path, _, axes = arg.partition("@")
    return Font(path, **{k: float(v) for k, v in (a.split("=") for a in axes.split(",") if a)})


def load_theme(path: str | None) -> Theme:
    if not path:
        return Theme()
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    names = {f.name for f in dataclasses.fields(Theme)}
    return Theme(**{k: v for k, v in data.items() if k in names})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--user")
    ap.add_argument("--display", required=True)
    ap.add_argument("--body", required=True)
    ap.add_argument("--label", default="Visitas")
    ap.add_argument("--theme", help="JSON com os tokens de svgkit.Theme")
    ap.add_argument("--count", type=int)
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    if a.count is not None:
        state = {"raw": a.count, "bot_hits": 0, "shown": a.count}
    else:
        url = f"https://komarev.com/ghpvc/?username={a.user}&style=flat"
        req = urllib.request.Request(url, headers={"User-Agent": f"{a.user}-profile"})
        state = next_state(previous_state(), parse_count(urllib.request.urlopen(req, timeout=30).read().decode()))
    (out / "visits.svg").write_text(card(state["shown"], font_arg(a.display), font_arg(a.body),
                                         load_theme(a.theme), a.label),
                                    encoding="utf-8")
    (out / "visits.json").write_text(json.dumps(state), encoding="utf-8")
    print(state)


if __name__ == "__main__":
    main()
