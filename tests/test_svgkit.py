import xml.etree.ElementTree as ET

import pytest
from svgkit import MissingGlyph, Theme, card_frame, heading, num, pill, rich_lines, rich_paths, svg

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
        fonts["body"].path("🙂", 20, 0, 20)


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
    root = ET.fromstring(heading("Projetos", fonts["display"], Theme()))
    assert root.find(f"{NS}title").text == "Projetos"
    assert root.get("width") == "1200"
    ET.fromstring(svg(10, 10, "a & <b>", ""))  # escapa o título


def test_card_frame_e_pill_usam_os_tokens_do_tema(fonts):
    theme = Theme(card="#111111", line="#222222", accent="#333333", on_accent="#444444")
    frame = "".join(card_frame(600, 150, theme))
    assert "#111111" in frame and "#222222" in frame
    tag = "".join(pill(0, 0, "Python", fonts["bold"], 20, theme.accent, theme.on_accent))
    assert "#333333" in tag and "#444444" in tag


def test_fonte_variavel_muda_com_o_eixo(fonts):
    assert fonts["display"].width("Projetos", 30) > fonts["body"].width("Projetos", 30)
