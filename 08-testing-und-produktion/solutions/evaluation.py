"""Aufgabe 9.1 – Loesung: einfache Evaluierung des Wissens-Assistenten.

Eval-Muster: keine Identitaet pruefen, sondern EIGENSCHAFTEN der Antwort.
Offline ist alles deterministisch -> die Quote ist reproduzierbar.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from lernakademie.mock_llm import is_offline_mode

# Testfragen mit erwarteten Eigenschaften (Kriterien):
EVAL_Faelle = [
    {
        "frage": "Wie viele Urlaubstage gibt es?",
        "erwartung": lambda ergebnis: (
            "mitarbeiter-handbuch.md" in str(ergebnis["quellen"])
        ),
        "beschreibung": "Quelle Mitarbeiter-Handbuch genannt",
    },
    {
        "frage": "Wie richte ich VPN ein?",
        "erwartung": lambda ergebnis: (
            "it-handbuch.md" in str(ergebnis["quellen"])
        ),
        "beschreibung": "Quelle IT-Handbuch genannt",
    },
    {
        "frage": "Was gilt fuer Passwoerter?",
        "erwartung": lambda ergebnis: ergebnis["gefundene_stellen"] >= 1,
        "beschreibung": "mind. 1 Stelle gefunden",
    },
    {
        "frage": "Wie hoch ist das Weihnachtsgeld?",
        "erwartung": lambda ergebnis: (
            ergebnis["quellen"] == []
            and "leider nicht" in ergebnis["antwort"]
        ),
        "beschreibung": "ehrliches 'nicht gefunden' ohne Quellen",
    },
]


def bewerte() -> tuple[int, int, list[str]]:
    """Fuehrt die Eval aus: liefert (treffer, gesamt, details)."""
    import importlib.util

    loesung = PROJEKT / "08-real-world-projects" / "solutions" / "knowledge_assistant.py"
    spec = importlib.util.spec_from_file_location("knowledge_assistant", loesung)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)

    retriever = modul.baue_index()
    treffer, details = 0, []
    for fall in EVAL_Faelle:
        ergebnis = modul.beantworte(fall["frage"], retriever)
        bestanden = bool(fall["erwartung"](ergebnis))
        treffer += int(bestanden)
        details.append(f"{'PASS' if bestanden else 'FAIL'} | {fall['frage']} "
                       f"({fall['beschreibung']})")
    return treffer, len(EVAL_Faelle), details


PROJEKT = Path(__file__).resolve().parents[2]


def main() -> None:
    if is_offline_mode():
        print("OFFLINE-Eval: deterministisch und reproduzierbar.\n")

    treffer, gesamt, details = bewerte()
    for zeile in details:
        print(" ", zeile)
    quote = 100 * treffer / gesamt
    print(f"\nErfolgsquote: {treffer}/{gesamt} = {quote:.0f}%")


if __name__ == "__main__":
    main()
