"""Aufgabe 10.2 – Referenzloesung: Entitaeten, Labels & Properties.

Modellierungs-Kommentare (die eigentliche Lektion!):
1. WORKS_FOR als Kante (nicht Property `firma`), weil man traversieren
   will: "Wer alles arbeitet bei Acme?" -> Kante folgen statt Textvergleich.
2. `seit=2021` als KANTEN-Property: Die Zugehoerigkeit hat ein Datum –
   nicht Anna, nicht Acme. Typische "Beziehungs-Property".
3. Manager als zusaetzliches LABEL statt Property `ist_manager`, weil
   Label-Filter schneller und semantisch sauberer sind ("alle Manager").
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from lernakademie.graph_store import GraphStore


def baue_graph() -> GraphStore:
    store = GraphStore()

    anna = store.add_node(["Person", "Employee"], name="Anna",
                          rolle="Entwicklerin", eintrittsjahr=2021)
    ben = store.add_node(["Person", "Employee", "Manager"], name="Ben",
                         rolle="Analyst", eintrittsjahr=2023)
    acme = store.add_node(["Company"], name="Acme",
                          branche="Technologie", groesse=150)
    engineering = store.add_node(["Department"], name="Engineering",
                                 standort="Berlin")
    projekt = store.add_node(["Project"], name="AI Assistant",
                             status="aktiv", budget=100000)

    store.add_relationship(anna, acme, "WORKS_FOR", seit=2021)
    store.add_relationship(ben, acme, "WORKS_FOR", seit=2023)
    store.add_relationship(anna, engineering, "BELONGS_TO")
    store.add_relationship(engineering, projekt, "WORKS_ON")
    return store


def main() -> None:
    store = baue_graph()

    # Label-Filter in Aktion:
    print("Alle Employees:")
    for node in store.nodes("Employee"):
        print(f"  {node.properties['name']} ({node.properties['rolle']})")

    print("\nAlle Manager:")
    for node in store.nodes("Manager"):
        print(f"  {node.properties['name']}")

    print("\nAlle Personen:")
    for node in store.nodes("Person"):
        print(f"  {node.properties['name']} – Labels: {node.labels}")

    print("\nWORKS_FOR mit Kanten-Property:")
    for kante in store.relationships("WORKS_FOR"):
        von = store.nodes()[kante.from_id].properties["name"]
        zu = store.nodes()[kante.to_id].properties["name"]
        print(f"  {von} -> {zu} (seit {kante.properties.get('seit')})")


if __name__ == "__main__":
    main()
