"""Aufgabe 12.1 + 12.2 – Loesung: Extraktion -> Graph-Population.

Zeigt: Text -> Extraktion (LLM/Regel) -> GraphStore inkl. Entity
Resolution (Duplikat-Test!) und Fehler-Skippen bei unvollstaendigen
Beziehungen.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from lernakademie.graph_extraction import extrahiere, fuelle_graph
from lernakademie.graph_store import GraphStore
from lernakademie.mock_llm import is_offline_mode

TEXT = ("Anna arbeitet bei Acme und gehoert zu Engineering. "
        "Ben arbeitet bei Acme. "
        "Engineering arbeitet an AI Assistant.")


def main() -> None:
    if is_offline_mode():
        print("OFFLINE-Modus: Extraktion per Regel-Fallback.\n")

    # ---- Teil 1: Extraktion (Aufgabe 12.1) -------------------------------
    extraktion = extrahiere(TEXT)
    print("Erkannte Entitaeten:")
    for entitaet in extraktion.entitaeten:
        print(f"  - {entitaet['name']} ({entitaet['label']})")
    print("Erkannte Beziehungen:")
    for beziehung in extraktion.beziehungen:
        print(f"  - {beziehung['von']} --{beziehung['typ']}--> {beziehung['zu']}")

    # Stolperfalle: Tippfehler werden (offline) ehrlich nicht erkannt
    fehler_text = "Anya arbeitet bei Acme."
    fehler_extraktion = extrahiere(fehler_text)
    print(f"\nStolperfall 'Anya': {len(fehler_extraktion.entitaeten)} "
          f"Entitaet(en) erkannt (offline erwartet: nur Acme).")

    # ---- Teil 2: Graph-Population (Aufgabe 12.2) ------------------------
    store = GraphStore()
    kanten = fuelle_graph(store, extraktion)
    print(f"\nErster FUELlauf: {len(store.nodes())} Nodes, {kanten} Kanten")

    # Duplikat-Test: derselbe Text nochmal -> KEINE neuen Nodes!
    zweite = extrahiere(TEXT)
    kanten2 = fuelle_graph(store, zweite)
    print(f"Zweiter Lauf   : {len(store.nodes())} Nodes, {kanten2} Kanten "
          "(Entity Resolution: Nodes duerfen NICHT gestiegen sein)")

    # Fehlerfall: Beziehung auf unbekannte Entitaet wird uebersprungen
    unvollstaendig = extrahiere("Zoe arbeitet bei Acme.")  # Zoe unbekannt
    vor_kanten = len(store.relationships())
    fuelle_graph(store, unvollstaendig)
    print(f"Unvollstaendig  : {vor_kanten} -> {len(store.relationships())} Kanten "
          "(Acme-Kante nur, wenn Zoe erkannt wurde; sonst skip ohne Crash)")

    print("\nMermaid-Ansicht des gefuellten Graphs:")
    print(store.to_mermaid())


if __name__ == "__main__":
    main()
