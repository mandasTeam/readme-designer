import xml.etree.ElementTree as ET

import pytest
from svgkit import MissingGlyph, Theme, card_frame, heading, num, rich_lines, rich_paths, svg

NS = "{http://www.w3.org/2000/svg}"


def test_num_arredonda_e_corta_zero():
    assert num(3.0) == "3"
    assert num(3.14159) == "3.1"
    assert num(-0.04) == "-0"


def test_path_ancora_no_meio_desloca_metade_da_largura(fonts):
    body = fonts["body"]
    w = body.width("Protheus", 30)
    start = body.path("Protheus", 30, 100, 50)
    middle = body.path("Protheus", 30, 100 + w / 2, 50, "middle")
    assert start and start == middle


def test_acentos_viram_path_e_glifo_ausente_falha(fonts):
    assert fonts["body"].path("Implantação", 20, 0, 20)
    with pytest.raises(MissingGlyph):
        fonts["body"].path("🦇", 20, 0, 20)


def test_fit_encolhe_ate_caber(fonts):
    body = fonts["body"]
    size = body.fit("Consultor de Implantação", 40, 200)
    assert size < 40
    assert body.width("Consultor de Implantação", size) <= 200


def test_rich_lines_quebra_so_nos_espacos(fonts):
    r, b = fonts["body"], fonts["bold"]
    segs = [("Sou o ", r, 27, "#000"), ("Igor", b, 27, "#f00"), (". No crachá, consultor.", r, 27, "#000")]
    lines = rich_lines(segs, 60)  # estreito: força uma palavra por linha
    words = ["".join(t for t, *_ in w) for line in lines for _, w in line]
    assert "Igor." in words  # negrito + pontuação ficam juntos
    assert len(rich_paths(lines, 0, 40, 30)) == sum(len(w) for line in lines for _, w in line)


def test_heading_e_svg_validos(fonts):
    root = ET.fromstring(heading("MISSÕES", fonts["display"], Theme()))
    assert root.find(f"{NS}title").text == "MISSÕES"
    assert root.get("width") == "1200"
    ET.fromstring(svg(10, 10, "a & <b>", ""))  # escapa o título


def test_card_frame_usa_as_cores_da_faixa():
    theme = Theme(stripes=["#111111", "#222222", "#333333"])
    body = "".join(card_frame(600, 150, theme))
    for c in theme.stripes:
        assert c in body
