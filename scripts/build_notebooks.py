"""Erzeugt ALLE Lern- und Loesungs-Notebooks aus den Specs.

Aufruf im Projektordner:
    python scripts/build_notebooks.py            # baut + fuehrt Loesungen aus
    python scripts/build_notebooks.py --schnell  # nur schreiben (keine Ausfuehrung)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from nbkit import schreibe_notebooks  # noqa: E402
from specs_a import SPECS_A  # noqa: E402
from specs_b import SPECS_B  # noqa: E402
from specs_c import SPECS_C  # noqa: E402
from specs_d import SPECS_D  # noqa: E402
from specs_e import SPECS_E  # noqa: E402
from specs_f import SPECS_F  # noqa: E402
from specs_g import SPECS_G  # noqa: E402

ALLE_SPECS = SPECS_A + SPECS_B + SPECS_C + SPECS_D + SPECS_E + SPECS_F + SPECS_G


def main() -> None:
    projekt = Path(__file__).resolve().parents[1]
    mit_ausfuehrung = "--schnell" not in sys.argv
    if not mit_ausfuehrung:
        print("Modus: nur schreiben (Loesungen ohne Ausfuehrung).")
    for spec in ALLE_SPECS:
        schreibe_notebooks(spec, projekt, mit_ausfuehrung=mit_ausfuehrung)
    print(f"\n{len(ALLE_SPECS)} Notebooks erzeugt "
          "(Start_HERE + 20 Lektionen). Loesungen in solutions/.")


if __name__ == "__main__":
    main()
