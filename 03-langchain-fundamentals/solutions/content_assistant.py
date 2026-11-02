"""Aufgabe 3.4 – Referenzloesung: Content-Assistant (Mini-Projekt).

Architektur:
- pruefe_eingabe(): pure Python-Logik, laeuft VOR jedem API-Call
  (spart Kosten und verhindert Frust).
- Drei Chains als Fabriken: summarizer, translator, analyser.
- verarbeite(): der Dirigent, der alles zu einem Ergebnis-Paket kombiniert.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from lernakademie.mock_llm import get_chat_model, is_offline_mode

ZIELSPRACHEN = ("Englisch", "Spanisch", "Franzoesisch")
MIN_LAENGE = 50


class Kurzanalyse(BaseModel):
    thema: str = Field(description="Thema des Texts in wenigen Worten")
    stichpunkte: list[str] = Field(description="3-5 Kernaussagen als Stichpunkte")
    schaetzwortzahl: int = Field(description="Geschaetzte Wortzahl des Originals")


def pruefe_eingabe(text: str, zielsprache: str) -> None:
    """Laeuft VOR jedem API-Call. Wirft ValueError bei ungueltiger Eingabe."""
    if not text or not text.strip():
        raise ValueError("Der Text darf nicht leer sein.")
    if len(text.strip()) < MIN_LAENGE:
        raise ValueError(
            f"Der Text ist zu kurz (mindestens {MIN_LAENGE} Zeichen)."
        )
    if zielsprache not in ZIELSPRACHEN:
        raise ValueError(f"Zielsprache muss eine von {ZIELSPRACHEN} sein.")


def baue_summarizer(modell):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Du fasst Texte in 2-3 Saetzen zusammen."),
        ("human", "{text}"),
    ])
    return prompt | modell | StrOutputParser()


def baue_translator(modell):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Du uebersetzt natuerlich und idiomatisch."),
        ("human", "Uebersetze nach {zielsprache}: {text}"),
    ])
    return prompt | modell | StrOutputParser()


def baue_analyser(modell):
    return modell.with_structured_output(Kurzanalyse)


def verarbeite(text: str, zielsprache: str) -> dict:
    """Dirigent: Pruefung, dann Chain A -> B -> C, dann Ergebnis-Paket."""
    pruefe_eingabe(text, zielsprache)  # VOR dem ersten API-Call!

    modell = get_chat_model(temperature=0.0)
    summarizer = baue_summarizer(modell)
    translator = baue_translator(modell)
    analyser = baue_analyser(modell)

    zusammenfassung = summarizer.invoke({"text": text})
    # Chain-Kombination: die Uebersetzung bekommt die ZUSAMMENFASSUNG als Input
    uebersetzung = translator.invoke({"zielsprache": zielsprache, "text": zusammenfassung})
    analyse = analyser.invoke(text)

    return {
        "zusammenfassung": zusammenfassung,
        "uebersetzung": uebersetzung,
        "analyse": analyse,
    }


def main() -> None:
    if is_offline_mode():
        print("OFFLINE-Modus: simulierte Modell-Antworten.\n")

    gueltiger_text = (
        "LangChain ist ein Framework, das die Arbeit mit Sprachmodellen "
        "vereinfacht. Es stellt Bausteine fuer Prompts, Ketten und "
        "Rueckgabewerte bereit. Dadurch werden Anwendungen wartbarer "
        "und Modelle leicht austauschbar."
    )

    print("=== Fall 1: gueltige Eingabe ===")
    try:
        ergebnis = verarbeite(gueltiger_text, "Englisch")
        print("Zusammenfassung:", ergebnis["zusammenfassung"])
        print("Uebersetzung:", ergebnis["uebersetzung"])
        print("Analyse:", ergebnis["analyse"])
    except Exception as fehler:
        print("Unerwarteter Fehler:", fehler)

    print("\n=== Fall 2: ungueltige Eingabe (zu kurz) ===")
    try:
        verarbeite("Zu kurz!", "Englisch")
    except ValueError as fehler:
        print("Eingabefehler (erwartet):", fehler)


if __name__ == "__main__":
    main()
