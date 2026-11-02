"""Aufgabe 10.1 – Referenzloesung: erster Graph in reinem Python."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from lernakademie.graph_store import GraphStore


def main() -> None:
    store = GraphStore()

    # Nodes: Entitaeten mit Label und Properties (IDs unbedingt merken!)
    anna_id = store.add_node(["Person"], name="Anna", rolle="Entwicklerin")
    acme_id = store.add_node(["Company"], name="Acme", branche="Technologie")
    engineering_id = store.add_node(["Department"], name="Engineering")
    projekt_id = store.add_node(["Project"], name="AI Assistant", status="aktiv")

    # Relationships: gerichtete Verbindungen zwischen IDs
    store.add_relationship(anna_id, acme_id, "WORKS_FOR", seit=2021)
    store.add_relationship(anna_id, engineering_id, "BELONGS_TO")
    store.add_relationship(engineering_id, projekt_id, "WORKS_ON")

    print(f"Nodes: {len(store.nodes())} | Relationships: {len(store.relationships())}")
    for node in store.nodes():
        labels = ":".join(node.labels)
        print(f"  [{node.id}] :{labels} {node.properties}")

    # Wiederauffindbarkeit pruefen
    anna = store.find_node("Person", name="Anna")
    assert anna is not None and anna.id == anna_id
    print(f"\nAnna wiedergefunden: ID {anna.id}")


if __name__ == "__main__":
    main()
