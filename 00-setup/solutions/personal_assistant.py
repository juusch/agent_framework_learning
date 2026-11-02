"""Aufgabe 1.5 – Referenzloesung: regelbasierter persoenlicher Assistent.

Designidee (wichtig!):
- finde_antwort() ist REINE LOGIK: Eingabe rein, Antwort raus.
  Deshalb koennen wir sie in tests/ automatisch pruefen.
- main() macht nur Ein-/Ausgabe und die Gespraechsschleife.
- Ab Stufe 2 ersetzen wir die Regel-Logik durch ein LLM – und sehen
  genau, was sich aendert und was gleich bleibt (die Schleife!).
"""

from __future__ import annotations

import os
import random
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

WITZE = [
    "Warum koennen Geister so schlecht luegen? Weil man durch sie hindurchsieht.",
    "Treffen sich zwei Lampen. Sagt die eine: 'Gehst du an?'",
    "Was macht ein Pirat am Computer? Er drueckt die Enter-Taste.",
]

EINKAUF = ["Milch", "Brot", "Aepfel"]

BEFEHLE = ("zeit", "witz", "einkauf")


def begruesse(name: str) -> str:
    return f"Hallo {name}! Ich bin dein Assistent."


def finde_antwort(eingabe: str) -> str:
    """Reine Entscheidungslogik: Eingabe -> Antwort (testbar, ohne Terminal)."""
    text = eingabe.lower()  # Gross-/Kleinschreibung neutralisieren

    if text == "fertig":
        return "__ENDE__"  # Signalwert, den main() in break uebersetzt
    if "zeit" in text:
        return f"Es ist {datetime.now().strftime('%H:%M')} Uhr."
    if "witz" in text:
        return random.choice(WITZE)
    if "einkauf" in text:
        return "Auf der Liste stehen: " + ", ".join(EINKAUF)
    return (
        "Das habe ich leider nicht verstanden. "
        f"Ich kenne: {', '.join(BEFEHLE)} (und 'fertig' zum Beenden)."
    )


def main() -> None:
    name = os.environ.get("BEISPIEL_NAME", "").strip() or input("Wie heisst du? ")
    print(begruesse(name))

    while True:  # Gespraechsschleife: laeuft, bis 'fertig' getippt wird
        eingabe = input("\nDu: ")
        antwort = finde_antwort(eingabe)
        if antwort == "__ENDE__":
            print(f"Bis bald, {name}!")
            break
        print(f"Assistent: {antwort}")


if __name__ == "__main__":
    main()
