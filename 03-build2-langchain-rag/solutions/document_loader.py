"""Aufgabe 4.1 – Referenzloesung: Dokument laden & zusammenfassen.

Zwei Lade-Varianten im Vergleich:
1. pathlib (pur)      -> roher Text
2. TextLoader (LC)    -> Document mit .page_content und .metadata
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from lernakademie.mock_llm import get_chat_model, is_offline_mode

PFAD = Path(__file__).resolve().parents[1] / "data" / "mitarbeiter-handbuch.md"


def lade_pur(pfad: Path) -> str:
    """Variante 1: rohes Lesen – kein Framework, nur Python."""
    return pfad.read_text(encoding="utf-8")


def lade_mit_loader(pfad: Path):
    """Variante 2: LangChain TextLoader -> Document mit Metadaten."""
    from langchain_community.document_loaders import TextLoader

    dokumente = TextLoader(str(pfad), encoding="utf-8").load()
    return dokumente[0]  # bei einer Datei genau ein Document


def main() -> None:
    if is_offline_mode():
        print("OFFLINE-Modus: Zusammenfassung ist simuliert.\n")

    text = lade_pur(PFAD)
    dokument = lade_mit_loader(PFAD)

    print(f"Datei: {PFAD.name}")
    print(f"Zeichen: {len(text)} | Woerter: {len(text.split())}")
    print(f"Metadaten des Documents: {dokument.metadata}")
    print(f"Identischer Text? {text == dokument.page_content}")

    # Token-Schaetzung: Faustregel ~4 Zeichen pro Token.
    # Beispielmodell-Kontextfenster: ~32k Tokens -> unser Dokument
    # (~1,2k Zeichen / 4 = ~300 Tokens) passt locker hinein.
    print(f"Geschaetzte Tokens: {len(text) // 4}")

    # Zusammenfassungs-Chain wie in Stufe 3 – Input kommt jetzt aus der Datei
    modell = get_chat_model(temperature=0.0)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Du fasst Handbuecher in 3-4 Saetzen zusammen."),
        ("human", "{text}"),
    ])
    chain = prompt | modell | StrOutputParser()
    print("\nZusammenfassung:\n", chain.invoke({"text": text}))


if __name__ == "__main__":
    main()
