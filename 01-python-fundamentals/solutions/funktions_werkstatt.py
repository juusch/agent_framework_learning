"""Aufgabe 1.2 – Referenzloesung: Funktionen & Imports.

Wichtig fuer spaetere Stufen: Diese Funktionen machen KEINE Ein-/Ausgabe
(kein input/print), sondern rechnen nur. Reine Funktionen sind leicht
zu testen – genau so bauen wir spaeter LangChain-Bausteine.
"""

from __future__ import annotations

import random
from datetime import datetime


def begruessung(name: str, stil: str = "hoeflich") -> str:
    """Liefert je nach Stil eine passende Begruessung (return, nicht print!)."""
    if stil == "locker":
        return f"Na, {name}! Was geht?"
    return f"Guten Tag, {name}. Schoen, Sie zu sehen."


def durchschnitt(zahlen: list[float]) -> float:
    """Mittelwert einer Liste; leere Liste -> 0 (kein Absturz)."""
    if not zahlen:  # leere Liste ist "falsy" -> True, wenn nichts drin ist
        return 0.0
    return sum(zahlen) / len(zahlen)


def ist_arbeitszeit(stunde: int) -> bool:
    """True, wenn die Stunde zwischen 9 und 17 (inklusive) liegt."""
    return 9 <= stunde <= 17


def main() -> None:
    # Eigene Funktionen testen
    print(begruessung("Anna"))
    print(begruessung("Ben", stil="locker"))
    print(f"Durchschnitt [2, 4, 9]: {durchschnitt([2, 4, 9])}")
    print(f"Durchschnitt []: {durchschnitt([])}")

    # Standardbibliothek nutzen
    stunde = datetime.now().hour
    print(f"Aktuelle Stunde: {stunde} -> Arbeitszeit: {ist_arbeitszeit(stunde)}")
    print(f"Wuerfelwurf: {random.randint(1, 6)}")


if __name__ == "__main__":
    main()
