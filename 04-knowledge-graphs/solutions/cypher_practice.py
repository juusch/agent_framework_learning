"""Aufgabe 11.1 – Referenzloesung: Cypher-Uebung im GraphStore-Fallback.

Fuer echte Neo4j-Aufrufe: Start-Skript im Level-README (Docker) und
die vier Abfragen im Neo4j Browser eintippen. Dieses Skript uebt die
gleichen Muster im Offline-Fallback.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from lernakademie.graph_store import baue_beispiel_graph

ABFRAGEN = [
    "MATCH (n:Person) RETURN n",
    "MATCH (n:Person) WHERE n.name = 'Anna' RETURN n",
    "MATCH (a:Person)-[r:WORKS_FOR]->(c:Company) RETURN a, c",
    "MATCH (a {name: 'Anna'})-[r]->(b) RETURN a, type(r), b",
]

VERBOTEN = [
    "CREATE (n:Person {name: 'Boesewicht'})",
    "MATCH (n) DELETE n",
]


def main() -> None:
    store = baue_beispiel_graph()
    print("Offline-Fallback: dieselben Cypher-Muster wie in Neo4j.\n")

    for abfrage in ABFRAGEN:
        ergebnis = store.run_cypher(abfrage)
        print(f"Cypher: {abfrage}")
        print(f"  -> {len(ergebnis)} Treffer")
        for zeile in ergebnis[:2]:
            print(f"     {zeile}")
        print()

    # Sicherheits-Experiment: Schreibbefehle MUSS der Subset ablehnen.
    print("Sicherheits-Experiment (schreibende Befehle):")
    for befehl in VERBOTEN:
        try:
            store.run_cypher(befehl)
            print(f"  {befehl} -> FEHLER IM DESIGN: wurde ausgefuehrt!")
        except ValueError as fehler:
            print(f"  {befehl}")
            print(f"    -> korrekt abgelehnt: {str(fehler)[:60]}...")


if __name__ == "__main__":
    main()
