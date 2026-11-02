"""Aufgabe 0.2 – Referenzloesung: personalisierte Begruessung.

Muster: Eingabe -> Verarbeitung -> Ausgabe.
Das ist dasselbe Grundmuster, das spaeter jeder Chatbot verwendet
(nur mit einer KI als "Verarbeitung").
"""


def frage_name() -> str:
    """Fragt den Namen ab. input() liefert immer einen String."""
    return input("Wie heisst du? ")


def frage_alter() -> int | None:
    """Fragt das Alter ab und wandelt es in eine Zahl um.

    Gibt None zurueck, wenn die Eingabe keine Zahl war -
    so stuerzt das Programm nie ab (Fehlerbehandlung).
    """
    rohwert = input("Wie alt bist du? ")
    try:
        return int(rohwert)
    except ValueError:
        print(f'"{rohwert}" ist leider keine Zahl.')
        return None


def baue_begruessung(name: str, alter: int) -> str:
    """Erzeugt die personalisierte Nachricht (Verarbeitung)."""
    return f"Hallo {name}! Naechstes Jahr wirst du {alter + 1}."


def main() -> None:
    """Hauptablauf: Eingabe, Pruefung, Ausgabe."""
    name = frage_name()
    alter = frage_alter()

    if alter is None:
        print("Bitte starte das Programm erneut und gib eine Zahl ein.")
        return

    if alter < 0 or alter > 130:
        # Plausibilitaetspruefung: kein echtes Alter -> freundlicher Hinweis
        print("Das Alter sieht unplausibel aus. Bist du sicher? ;-)")
        return

    print(baue_begruessung(name, alter))
    print("Bis bald!")


if __name__ == "__main__":
    #Dieser Block sorgt dafuer, dass main() nur beim direkten Start laeuft,
    # nicht aber, wenn diese Datei woanders importiert wird (wichtig fuer Tests).
    main()
