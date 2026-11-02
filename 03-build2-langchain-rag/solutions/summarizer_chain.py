"""Aufgabe 3.2 – Referenzloesung: Prompt-Templates & Chains.

Muster:
    chain = prompt | model | parser   (links: Dict rein, rechts: String raus)

Fabrikfunktion statt Duplikat-Code: baue_chain() erstellt das
Fließband einmal; alle Aufrufe unten nutzen dasselbe Muster.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from lernakademie.llm_client import get_chat_model, is_offline_mode

BEISPIELTEXT = (
    "Python ist eine Programmiersprache, die 1991 von Guido van Rossum "
    "veroeffentlicht wurde. Sie ist bekannt fuer ihre gut lesbare Syntax "
    "und wird in Bereichen von Webentwicklung bis Data Science eingesetzt. "
    "Viele Einsteiger beginnen mit Python, weil Fehlermeldungen verstaendlich "
    "sind und die Sprache kaum Boilerplate-Code verlangt."
)


def baue_summarizer(modell) -> object:
    """Fabrik: erzeugt die Zusammenfassungs-Chain (Runnable)."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Du fasst Texte praegnant und korrekt zusammen."),
        ("human", "Stil: {stil}. Zusammenfassen: {text}"),
    ])
    return prompt | modell | StrOutputParser()


def baue_translator(modell) -> object:
    """Fabrik: erzeugt die Uebersetzungs-Chain (Bonus)."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Du uebersetzt sauber und natuerlich."),
        ("human", "Uebersetze nach {zielsprache}: {text}"),
    ])
    return prompt | modell | StrOutputParser()


def main() -> None:
    if is_offline_mode():
        print("OFFLINE-Modus: simulierte Antworten.\n")

    modell = get_chat_model(temperature=0.0)
    summarizer = baue_summarizer(modell)
    translator = baue_translator(modell)

    for stil in ("kurz", "als Bullet Points"):
        # dieselbe Chain, nur die Eingabe aendert sich:
        ergebnis = summarizer.invoke({"stil": stil, "text": BEISPIELTEXT})
        print(f"--- Stil: {stil} ---")
        print(ergebnis, "\n")

    kurzfassung = summarizer.invoke({"stil": "ein Satz", "text": BEISPIELTEXT})
    uebersetzung = translator.invoke({"zielsprache": "Englisch", "text": kurzfassung})
    print("--- Uebersetzung der Zusammenfassung ---")
    print(uebersetzung)


if __name__ == "__main__":
    main()
