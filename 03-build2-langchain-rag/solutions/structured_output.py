"""Aufgabe 3.3 – Referenzloesung: strukturierte Ausgaben mit Pydantic.

Kernidee: with_structured_output(schema) macht aus dem Modell eine
Chain, die GEPRUEFTE Python-Objekte liefert statt Fließtext.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from pydantic import BaseModel, Field

from lernakademie.mock_llm import get_chat_model, is_offline_mode


class RezeptIdee(BaseModel):
    """Formular, das das Modell ausfuellen muss. Die descriptions liest das Modell mit!"""

    titel: str = Field(description="Kreativer, appetitlicher Rezeptname")
    zutaten: list[str] = Field(description="Liste der noetigen Zutaten")
    dauer_minuten: int = Field(description="Zubereitungszeit in Minuten", gt=0)
    schwierigkeit: str = Field(description="einfach, mittel oder schwer")


class Kurzanalyse(BaseModel):
    """Zweites Beispiel: Analyse eines freien Satzes."""

    thema: str = Field(description="Worum geht es in einem Wort?")
    stimmung: str = Field(description="positiv, neutral oder negativ")
    hat_fragezeichen: bool = Field(description="Endet der Satz mit '?'?")


def main() -> None:
    if is_offline_mode():
        print("OFFLINE-Modus: Das Formular wird mit Platzhaltern gefuellt.\n")

    modell = get_chat_model(temperature=0.0)

    rezept_chain = modell.with_structured_output(RezeptIdee)
    analyse_chain = modell.with_structured_output(Kurzanalyse)

    try:
        rezept = rezept_chain.invoke("Ich habe Nudeln, Tomaten und Knoblauch da.")
        print(f"Titel: {rezept.titel}")
        print(f"Zutaten ({len(rezept.zutaten)}): {', '.join(rezept.zutaten)}")
        print(f"Dauer: {rezept.dauer_minuten} Minuten ({rezept.schwierigkeit})")
        # Mit den Feldern normal weiterrechnen:
        print(f"Fuer {len(rezept.zutaten)} Zutaten also ca. "
              f"{rezept.dauer_minuten * 2 // 3} Minuten Vorbereitung.")

        analyse = analyse_chain.invoke("Ist der Kurs fuer Anfaenger wirklich geeignet?")
        print(f"\nThema: {analyse.thema} | Stimmung: {analyse.stimmung} "
              f"| Fragezeichen: {analyse.hat_fragezeichen}")
    except Exception as fehler:  # z. B. ValidationError, wenn das Modell
        # gegen das Schema verstoesst
        print(f"Strukturfehler: {fehler}")


if __name__ == "__main__":
    main()
