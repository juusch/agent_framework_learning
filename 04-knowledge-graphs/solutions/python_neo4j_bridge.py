"""Aufgabe 11.2 – Referenzloesung: Python-Neo4j-Bruecke mit Fallback.

Architektur (die Signatur der Akademie):
    verbinde() -> Treiber ODER None
    bei None: derselbe Ablauf laeuft gegen den GraphStore (Offline)

MERGE statt CREATE: idempotent – mehrfaches Ausfahren dupliziert nichts.
Parameter ($name) statt f-Strings: Injection-Schutz (Stufe 9!).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from lernakademie.graph_store import baue_beispiel_graph

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORT = "lernakademie"


def verbinde():
    """Liefert einen Neo4j-Treiber oder None (DB nicht erreichbar)."""
    try:
        from neo4j import GraphDatabase

        treiber = GraphDatabase.driver(
            NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORT),
            connection_timeout=3)
        treiber.verify_connectivity()
        return treiber
    except Exception as fehler:
        print(f"Neo4j nicht erreichbar ({str(fehler)[:60]}...).")
        print("-> Offline-Fallback mit GraphStore aktiv.\n")
        return None


LADE_ANWEISUNGEN = """
MERGE (anna:Person {name: 'Anna'}) SET anna.rolle = 'Entwicklerin'
MERGE (ben:Person {name: 'Ben'}) SET ben.rolle = 'Analyst'
MERGE (acme:Company {name: 'Acme'}) SET acme.branche = 'Technologie'
MERGE (eng:Department {name: 'Engineering'})
MERGE (proj:Project {name: 'AI Assistant'}) SET proj.status = 'aktiv'
MERGE (anna)-[k1:WORKS_FOR]->(acme) SET k1.seit = 2021
MERGE (ben)-[k2:WORKS_FOR]->(acme) SET k2.seit = 2023
MERGE (anna)-[:BELONGS_TO]->(eng)
MERGE (eng)-[:WORKS_ON]->(proj)
MERGE (anna)-[:CONTRIBUTES_TO]->(proj)
"""


def lade_firmen_graph_neo4j(session) -> None:
    """Laedt den Firmen-Graph idempotent in Neo4j (ein Statement pro Zeile)."""
    for zeile in LADE_ANWEISUNGEN.strip()().splitlines():
        zeile = zeile.strip()
        if zeile:
            session.run(zeile)


def frage_neo4j(session, cypher: str, **parameter):
    """Parametrisierte Abfrage, Ergebnis als Liste von Dicts."""
    return [dict(datensatz) for datensatz in session.run(cypher, **parameter)]


def frage_fallback(store, cypher: str):
    """Dieselbe Abfrage im GraphStore (Subset aus Stufe 11.1)."""
    return store.run_cypher(cypher)


ABFRAGEN = [
    "MATCH (n:Person) RETURN n",
    "MATCH (n:Person) WHERE n.name = 'Anna' RETURN n",
    "MATCH (a:Person)-[r:WORKS_FOR]->(c:Company) RETURN a, c",
    "MATCH (a {name: 'Anna'})-[r]->(b) RETURN a, type(r), b",
]


def main() -> None:
    treiber = verbinde()

    if treiber is not None:
        with treiber.session() as session:
            lade_firmen_graph_neo4j(session)
            for abfrage in ABFRAGEN:
                ergebnis = frage_neo4j(session, abfrage)
                print(f"{abfrage}\n  -> {len(ergebnis)} Treffer")
        treiber.close()
        print("\n(Alle Abfragen gegen echtes Neo4j ausgefuehrt.)")
    else:
        store = baue_beispiel_graph()
        for abfrage in ABFRAGEN:
            ergebnis = frage_fallback(store, abfrage)
            print(f"{abfrage}\n  -> {len(ergebnis)} Treffer")
        print("\n(Fallback: identische Muster, gleiche Ergebnislogik.)")


if __name__ == "__main__":
    main()
