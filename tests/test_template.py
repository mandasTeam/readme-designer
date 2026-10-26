import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "readme-design" / "templates"))
import build_assets as tpl  # noqa: E402


def test_template_gera_banner_e_card_de_texto(fonts):
    c = dict(tpl.CONFIG)
    ET.fromstring(tpl.banner(c, fonts))
    root = ET.fromstring(tpl.about(c, fonts))
    assert "Fulano" in root.find("{http://www.w3.org/2000/svg}title").text
