import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills" / "readme-design" / "scripts"))
FONTS = ROOT / "tools" / "fonts"


@pytest.fixture(scope="session")
def fonts():
    from svgkit import Font
    return {
        "display": Font(FONTS / "Bangers-Regular.ttf"),
        "body": Font(FONTS / "BarlowCondensed-SemiBold.ttf"),
        "bold": Font(FONTS / "BarlowCondensed-Bold.ttf"),
    }
