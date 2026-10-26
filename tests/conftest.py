import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills" / "readme-design" / "scripts"))
FONTS = ROOT / "tools" / "fonts"
SANS = FONTS / "IBMPlexSans[wdth,wght].ttf"


@pytest.fixture(scope="session")
def fonts():
    from svgkit import Font
    return {
        "display": Font(SANS, wght=700),
        "body": Font(SANS, wght=450),
        "bold": Font(SANS, wght=600),
        "mono": Font(FONTS / "IBMPlexMono-Medium.ttf"),
    }
