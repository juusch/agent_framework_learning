"""Aufgabe 10.3 – Referenzloesung: Beziehungen abfragen & Traversierung."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from lernakademie.graph_store import baue_beispiel_graph


def main() -> None:
    store = baue_beispiel_graph()
    anna = store.find_node("Person", name="Anna")
    engineering = store.find_node("Department", name="Engineering")
    projekt = store.find_node("Project", name="AI Assistant")
    ben = store.find_node("Person", name="Ben")

    # 1) Direkte Nachbarn von Anna (alle Kanten-Typen)
    print("1) Annas ausgehende Verbindungen:")
    for kante, ziel in store.neighbors(anna.id):
        print(f"  -{kante.typ}-> {ziel.properties['name']}")

    # 2) Gefilterte Traversierung: nur WORKS_FOR
    print("\n2) Annas WORKS_FOR (inkl. Kanten-Property):")
    for kante, ziel in store.neighbors(anna.id, "WORKS_FOR"):
        print(f"  -WORKS_FOR-> {ziel.properties['name']} "
              f"(seit {kante.properties.get('seit')})")

    # 3) Alle WORKS_FOR-Kanten im Graph
    print("\n3) Wer arbeitet wo?")
    for kante in store.relationships("WORKS_FOR"):
        von = store.nodes()[kante.from_id]
        zu = store.nodes()[kante.to_id]
        print(f"  {von.properties['name']} -> {zu.properties['name']}")

    # 4) Pfadfragen
    pfad_a = store.path(engineering.id, projekt.id)
    pfad_b = store.path(ben.id, projekt.id)
    print(f"\n4) Pfad Engineering -> AI Assistant: {pfad_a}")
    print(f"   Pfad Ben -> AI Assistant: {pfad_b}")
    print("   Erklärung: Ben hat nur WORKS_FOR->Acme; von Acme fuehrt KEINE")
    print("   Kante zum Projekt (Gerichtetheit!). Also: kein Pfad = None.")

    # 5) Zweistufiges Traversal von Hand: Anna -> Engineering -> Projekt
    print("\n5) Zweistufig von Anna zum Projekt:")
    gefunden = False
    for kante, nachbar in store.neighbors(anna.id, "BELONGS_TO"):
        for kante2, ziel2 in store.neighbors(nachbar.id, "WORKS_ON"):
            print(f"  Anna -{kante.typ}-> {nachbar.properties['name']} "
                  f"-{kante2.typ}-> {ziel2.properties['name']}")
            gefunden = True
    print(f"  => Anna ist (indirekt) mit dem Projekt verbunden: {gefunden}")
    # Die direkte Kante CONTRIBUTES_TO existiert zwar auch – aber der
    # zweistufige Weg zeigt: Wissen entsteht hier durch TRAVERSAL.


if __name__ == "__main__":
    main()
