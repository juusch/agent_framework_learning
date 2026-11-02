"""Aufgabe 1.1 – Referenzloesung: Einkaufslisten-Manager.

Struktur: reine Funktionen (Daten rein, Ergebnis zurueck) + main() als
Dirigent. So bleibt alles testbar und spaeter leicht erweiterbar.
"""

from __future__ import annotations


def zeige_liste(einkauf: list[str], preise: dict[str, float]) -> None:
    """Gibt jeden Artikel mit Preis aus (Ausgabe-Funktion)."""
    print("\n-- Einkaufsliste --")
    for artikel in einkauf:
        preis = preise.get(artikel)  # sicher: None, wenn der Artikel fehlt
        if preis is None:
            print(f"- {artikel}: Preis unbekannt")
        else:
            print(f"- {artikel}: {preis:.2f} Euro")


def berechne_summe(einkauf: list[str], preise: dict[str, float]) -> float:
    """Summiert die Preise aller gelisteten Artikel.

    Artikel ohne Preis werden uebersprungen (statt abzustuerzen).
    """
    return sum(preise[a] for a in einkauf if a in preise)


def ergaenze(einkauf: list[str], preise: dict[str, float],
             artikel: str, preis: float) -> None:
    """Fuegt Artikel und Preis hinzu. None = 'kein Preis bekannt'."""
    if artikel not in einkauf:
        einkauf.append(artikel)
    preise[artikel] = preis


def main() -> None:
    # Startdaten
    einkauf = ["Milch", "Brot", "Aepfel"]
    preise = {"Milch": 1.2, "Brot": 2.5, "Aepfel": 3.0}

    zeige_liste(einkauf, preise)
    print(f"Summe: {berechne_summe(einkauf, preise):.2f} Euro")

    # Neuer Artikel
    ergaenze(einkauf, preise, "Kaffee", 4.99)

    zeige_liste(einkauf, preise)
    print(f"Neue Summe: {berechne_summe(einkauf, preise):.2f} Euro")


if __name__ == "__main__":
    main()
