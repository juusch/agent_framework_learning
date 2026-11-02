"""Aufgabe 12.3 – Loesung: Frage -> Cypher -> sichere Ausfuehrung -> Antwort.

Die Sicherheits-Reihenfolge ist das Herzstueck:
    generiertes Cypher -> ist_sicher() -> erst dann Ausfuehrung.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from lernakademie.graph_extraction import (
    cypher_aus_frage, extrahiere, fuelle_graph,
    fuehre_sicher_aus, ist_sicher,
)
from lernakademie.graph_store import GraphStore
from lernakademie.llm_client import is_offline_mode

TEXT = ("Anna arbeitet bei Acme und gehoert zu Engineering. "
        "Ben arbeitet bei Acme. "
        "Engineering arbeitet an AI Assistant.")


def baue_graph() -> GraphStore:
    """Graph aus Text befuellen (12.1+12.2 wiederverwendet)."""
    store = GraphStore()
    fuelle_graph(store, extrahiere(TEXT))
    return store


def beantworte(store: GraphStore, frage: str) -> str:
    """Pipeline: Frage -> Cypher -> Sicherheitspruefung -> Ausfuehrung."""
    cypher = cypher_aus_frage(frage)
    if cypher is None:
        return ("Diese Frage kann ich mit dem Graph nicht beantworten "
                "(kein bekanntes Thema erkannt).")

    if not ist_sicher(cypher):
        return f"Abfrage aus Sicherheitsgruenden abgelehnt: {cypher}"

    zeilen = fuehre_sicher_aus(store, cypher)

    if not zeilen:
        return "Dazu habe ich im Graph nichts gefunden."

    # Ergebnis uebersetzen (deterministisch, ohne LLM):
    antwort_teile = []
    for zeile in zeilen:
        if "type(r)" in zeile:
            a = zeile["a"]["properties"].get("name", "?")
            rel = zeile["type(r)"]
            b = zeile["b"]["properties"].get("name", "?")
            antwort_teile.append(f"{a} --{rel}--> {b}")
        elif "n" in zeile:
            props = zeile["n"]["properties"]
            antwort_teile.append(str(props))
    return "; ".join(antwort_teile)


def main() -> None:
    if is_offline_mode():
        print("OFFLINE-Modus: Frage->Cypher per Regel-Fallback.\n")

    store = baue_graph()

    fragen = [
        "Wo arbeitet Anna?",
        "Was gibt es ueber Acme?",
        "Haengt Ben mit AI Assistant zusammen?",
    ]
    for frage in fragen:
        print(f"Frage: {frage}")
        print(f"Antwort: {beantworte(store, frage)}\n")

    # ---- Angriffs-Test: 'generiertes' Cypher mit DELETE ------------------
    print("Angriffs-Test (simuliert generierte destruktive Abfrage):")
    boese = "MATCH (n:Person) DETACH DELETE n"
    try:
        fuehre_sicher_aus(store, boese)
        print("  FEHLER IM DESIGN: wurde ausgefuehrt!")
    except ValueError as fehler:
        print(f"  Korrekt abgelehnt: {fehler}")


if __name__ == "__main__":
    main()
