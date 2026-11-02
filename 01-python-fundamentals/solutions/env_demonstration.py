"""Aufgabe 1.4 – Referenzloesung: .env laden und API-Keys sicher pruefen.

Regeln, die du hier lernst und die fuer ALLE folgenden Stufen gelten:
1. load_dotenv() aufrufen, BEVOR man Umgebungsvariablen liest.
2. os.environ.get(...) statt os.environ[...] – kein Absturz ohne Key.
3. Keys niemals ausgeben/loggen; existence reicht als Info.
"""

import os

from dotenv import load_dotenv

load_dotenv()


def lese_name() -> str:
    """Liest BEISPIEL_NAME aus .env (oder per Eingabe, falls nicht gesetzt)."""
    name = os.environ.get("BEISPIEL_NAME", "").strip()
    if not name:
        name = input("Kein BEISPIEL_NAME gefunden. Wie heisst du? ")
    return name


def pruefe_mistral_key() -> None:
    """Prueft, ob ein Mistral-Key existiert – ohne ihn preiszugeben."""
    key = os.environ.get("MISTRAL_API_KEY", "").strip()
    if key:
        # Nur ein kurzer Hinweis, nie der komplette Key!
        print(f"Mistral-Key gefunden (beginnt mit {key[:4]}...). Online-Modus moeglich.")
    else:
        print("Kein Mistral-Key gesetzt. Alle Aufgaben laufen im OFFLINE-Modus.")


def main() -> None:
    name = lese_name()
    print(f"Hallo {name}! Deine .env funktioniert. 🔑")
    pruefe_mistral_key()


if __name__ == "__main__":
    main()
