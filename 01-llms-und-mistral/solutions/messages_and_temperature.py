"""Aufgabe 2.3 – Referenzloesung: System-Nachrichten & Temperature.

Zwei Experimente:
A) Gleiche Frage, zwei verschiedene System-Rollen (Persona).
B) Gleiche Frage, dreimal temperature=0.0 vs. dreimal 0.9.

Hinweis: Im OFFLINE-Modus sind alle Antworten identisch (Simulation ist
deterministisch) – der CODE-Ablauf ist aber exakt derselbe. Mit Key
siehst du die Verhaltensunterschiede.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from lernakademie.mock_llm import get_mistral_client, is_offline_mode

MODELL = "mistral-small-latest"


def frage(client, prompt: str, system: str, temperature: float) -> str:
    """Eine wiederverwendbare Funktion fuer ALLE Aufrufe (Experiment A und B)."""
    antwort = client.chat.complete(
        model=MODELL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
    )
    return antwort.choices[0].message.content


def drucke_block(titel: str, antworten: list[str]) -> None:
    """Gibt mehrere Antworten uebersichtlich aus."""
    print(f"\n=== {titel} ===")
    for nummer, text in enumerate(antworten, start=1):
        print(f"{nummer}. {text}")


def main() -> None:
    offline = is_offline_mode()
    if offline:
        print("OFFLINE-Modus: Antworten sind simuliert und daher identisch.")
        print("Mit MISTRAL_API_KEY siehst du echte Verhaltensunterschiede.\n")

    client = get_mistral_client()

    # Experiment A: die ROLLE aendern
    prompt = "Erkläre, was Regenbogen sind – in maximal 3 Saetzen."
    antwort_prof = frage(client, prompt, "Du bist ein Physik-Professor.", 0.3)
    antwort_kind = frage(client, prompt, "Du bist ein 6-jaehriges Kind.", 0.3)
    drucke_block("Experiment A: Rolle = Physik-Professor", [antwort_prof])
    drucke_block("Experiment A: Rolle = 6-jaehriges Kind", [antwort_kind])

    # Experiment B: TEMPERATURE aendern
    kreativ_prompt = "Nenne ein kreatives Geschenk fuer eine Person, die Kaffee liebt."
    antworten_genau = [frage(client, kreativ_prompt, "Du bist ein Geschenkberater.", 0.0)
                       for _ in range(3)]
    antworten_wild = [frage(client, kreativ_prompt, "Du bist ein Geschenkberater.", 0.9)
                      for _ in range(3)]
    drucke_block("Experiment B: temperature=0.0", antworten_genau)
    drucke_block("Experiment B: temperature=0.9", antworten_wild)

    # Auswertung: wie viele UNTERSCHIEDLICHE Antworten pro Temperatur?
    print("\n=== Auswertung ===")
    print(f"Einzigartige Antworten bei 0.0: {len(set(antworten_genau))} von 3")
    print(f"Einzigartige Antworten bei 0.9: {len(set(antworten_wild))} von 3")
    # Faustregel (fuer eigene Anwendungen):
    print("\nFaustregel: Fakten/Struktur -> temperature 0.0-0.2; Ideen/Kreativitaet -> 0.7+")


if __name__ == "__main__":
    main()
