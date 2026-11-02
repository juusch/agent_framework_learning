"""Aufgabe 2.4 – Referenzloesung: Kommandozeilen-Chatbot mit Gespraechsverlauf.

Kernidee: LLMs haben KEIN Gedchtnis. Das "Gedaechtnis" ist unsere Liste
`messages`, die wir bei jedem Aufruf komplett mitschicken und um jeden
Gespraechszug (user + assistant) erweitern.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from lernakademie.llm_client import get_api_client, is_offline_mode

MODELL = "mistral-small-latest"
MAX_NACHRICHTEN = 20  # Budget-Kontrolle fuer das Kontextfenster

PERSONA = (
    "Du bist ein freundlicher Lern-Coach. Du beantwortest Fragen zu Python "
    "und KI geduldig, kurz und ohne Fachchinesisch."
)


def sende_und_merke(client, messages: list[dict], eingabe: str) -> str:
    """Sendet die gesamte Historie und haengt Frage + Antwort an sie an.

    Genau hier entsteht das "Gedaechtnis": append vor dem Call (User-Frage)
    und append nach dem Call (Modell-Antwort).
    """
    messages.append({"role": "user", "content": eingabe})
    antwort = client.chat.complete(model=MODELL, messages=messages)
    text = antwort.choices[0].message.content
    messages.append({"role": "assistant", "content": text})
    return text


def kuerze_historie(messages: list[dict]) -> list[dict]:
    """Laesst die System-Nachricht (Index 0) IMMER am Anfang stehen."""
    if len(messages) <= MAX_NACHRICHTEN:
        return messages
    return [messages[0]] + messages[-(MAX_NACHRICHTEN - 1):]


def main() -> None:
    if is_offline_mode():
        print("OFFLINE-Modus: Der Chatbot spiegelt deine Eingaben simuliert.\n")

    client = get_api_client()
    messages = [{"role": "system", "content": PERSONA}]

    print("Chatbot gestartet. Tippe 'exit' oder 'fertig' zum Beenden.")
    print("Tipp: Nenne zuerst deinen Namen und frage spaeter 'Wie heisse ich?'.\n")

    while True:
        eingabe = input("Du: ").strip()
        if not eingabe:
            continue  # leere Eingabe -> einfach weiterfragen
        if eingabe.lower() in ("exit", "fertig"):
            print("Chatbot: Auf Wiedersehen – bis zum naechsten Mal!")
            break
        try:
            antwort = sende_und_merke(client, messages, eingabe)
        except Exception as fehler:
            print(f"Chatbot: Entschuldigung, technisches Problem ({fehler}).")
            continue
        messages = kuerze_historie(messages)
        print(f"Chatbot: {antwort}")


if __name__ == "__main__":
    main()
