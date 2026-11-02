"""Optionaler Seeder: Fuellt ein laufendes Neo4j mit dem Capstone-Graph.

Voraussetzung: docker compose up (Neo4j auf bolt://localhost:7687,
Passwort 'lernakademie'). Ohne laufendes Neo4j bricht das Skript mit
einer klaren Meldung ab – die Anwendung selbst laeuft auch ohne.

Aufruf (vom Akademie-Hauptordner):
    python "final-project/knowledge-research-agent/database/seed/seed_to_neo4j.py"
"""

from pathlib import Path

from neo4j import GraphDatabase

STATEMENTS = [
    "MERGE (anna:Person {name: 'Anna'}) SET anna.rolle = 'Entwicklerin'",
    "MERGE (ben:Person {name: 'Ben'}) SET ben.rolle = 'Analyst'",
    "MERGE (clara:Person {name: 'Clara'}) SET clara.rolle = 'Abteilungsleitung'",
    "MERGE (acme:Company {name: 'Acme'}) SET acme.branche = 'Technologie'",
    "MERGE (eng:Department {name: 'Engineering'})",
    "MERGE (dat:Department {name: 'Data & Analytics'})",
    "MERGE (forsch:Department {name: 'Forschung'})",
    "MERGE (proj:Project {name: 'AI Assistant'}) SET proj.status = 'aktiv'",
    "MERGE (anna)-[:WORKS_FOR]->(acme)",
    "MERGE (ben)-[:WORKS_FOR]->(acme)",
    "MERGE (anna)-[:BELONGS_TO]->(eng)",
    "MERGE (ben)-[:BELONGS_TO]->(dat)",
    "MERGE (clara)-[:LEADS]->(eng)",
    "MERGE (eng)-[:WORKS_ON]->(proj)",
    "MERGE (dat)-[:PROVIDES_DATA_FOR]->(proj)",
    "MERGE (forsch)-[:WORKS_ON]->(proj)",
    "MERGE (anna)-[:CONTRIBUTES_TO]->(proj)",
]


def main() -> None:
    try:
        treiber = GraphDatabase.driver(
            "bolt://localhost:7687", auth=("neo4j", "lernakademie"),
            connection_timeout=3)
        treiber.verify_connectivity()
    except Exception as fehler:
        print(f"Neo4j nicht erreichbar ({fehler}).")
        print("Starte es mit 'docker compose up' im Projektordner.")
        return

    with treiber.session() as session:
        for statement in STATEMENTS:
            session.run(statement)
    treiber.close()
    print(f"{len(STATEMENTS)} Statements ausgefuehrt – Graph ist in Neo4j.")


if __name__ == "__main__":
    main()
