"""Aufgabe 2.2 – Referenzloesung: erster API-Call an Mistral.

Ablauf:
1. Hilfs-Paket der Akademie importierbar machen (Skript liegt in einem
   Unterordner; deshalb legen wir den Projektordner in sys.path).
2. Client holen: echt (mit Key) oder simuliert (offline) – gleicher Code!
3. Nachricht senden, Antwort ausgeben, Fehler freundlich uebersetzen.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from lernakademie.mock_llm import get_mistral_client, is_offline_mode

SYSTEM_NACHRICHT = "Du bist ein freundlicher Erklaerbaer fuer Technik-Anfaenger."
USER_NACHRICHT = "Erkläre in zwei Saetzen, was eine API ist."


def sende_nachricht(client) -> str:
    """Sendet die Nachrichten und liefert die Antwort als Text zurueck."""
    antwort = client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {"role": "system", "content": SYSTEM_NACHRICHT},
            {"role": "user", "content": USER_NACHRICHT},
        ],
    )
    return antwort.choices[0].message.content


def main() -> None:
    if is_offline_mode():
        print("Hinweis: Kein MISTRAL_API_KEY gesetzt -> OFFLINE-Modus.\n")

    client = get_mistral_client()
    try:
        inhalt = sende_nachricht(client)
    except Exception as fehler:  # Netz, Key, Rate-Limit ... alles abfangen
        text = str(fehler)
        if "401" in text:
            print("Fehler 401: API-Key fehlt oder ist ungueltig (.env pruefen).")
        elif "429" in text:
            print("Fehler 429: Rate-Limit erreicht. Kurz warten und erneut versuchen.")
        elif "connection" in text.lower():
            print("Netzwerkproblem: Kein Internet oder Server nicht erreichbar.")
        else:
            print(f"Unerwarteter Fehler: {fehler}")
        return

    print("Modell-Antwort:")
    print(inhalt)


if __name__ == "__main__":
    main()
