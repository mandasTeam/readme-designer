import xml.etree.ElementTree as ET

from svgkit import Theme
from visits import card, next_state, parse_count

KOMAREV = """<svg><g><text x="40" y="15">Profile views</text><text x="40" y="14">Profile views</text>
<text x="86" y="15">1,234</text><text x="86" y="14">1,234</text></g></svg>"""


def test_le_o_numero_do_selo():
    assert parse_count(KOMAREV) == 1234


def test_desconta_as_leituras_do_proprio_workflow():
    s1 = next_state({}, 10)
    assert s1 == {"raw": 10, "bot_hits": 1, "shown": 9}
    s2 = next_state(s1, 12)  # 1 visita real + 1 leitura do bot
    assert s2["shown"] == 10
    assert next_state({"bot_hits": 50}, 3)["shown"] == 0


def test_card_valido_com_zeros_a_esquerda(fonts):
    root = ET.fromstring(card(42, fonts["display"], fonts["bold"], Theme()))
    assert root.find("{http://www.w3.org/2000/svg}title").text == "Visitas: 42"
