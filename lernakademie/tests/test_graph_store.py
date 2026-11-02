"""Tests fuer den Offline-GraphStore (Property-Graph + Mini-Cypher)."""

import os

os.environ.setdefault("ACADEMY_OFFLINE", "1")

from lernakademie.graph_store import GraphStore, baue_beispiel_graph


def test_nodes_und_beziehungen():
    store = baue_beispiel_graph()
    assert len(store.nodes()) == 5
    assert len(store.nodes("Person")) == 2
    assert len(store.relationships("WORKS_FOR")) == 2

    anna = store.find_node("Person", name="Anna")
    assert anna is not None
    nachbarn = {node.properties["name"] for _, node in store.neighbors(anna.id)}
    assert nachbarn == {"Acme", "Engineering", "AI Assistant"}


def test_path_breitensuche():
    store = baue_beispiel_graph()
    anna = store.find_node("Person", name="Anna")
    acme = store.find_node("Company", name="Acme")
    projekt = store.find_node("Project", name="AI Assistant")
    assert store.path(anna.id, acme.id) == [anna.id, acme.id]
    # Ben -> Acme gibt es direkt, aber Ben hat keinen Pfad zum Projekt:
    ben = store.find_node("Person", name="Ben")
    assert store.path(ben.id, projekt.id) is None


def test_mermaid_ausgabe():
    store = baue_beispiel_graph()
    mermaid = store.to_mermaid()
    assert mermaid.startswith("flowchart LR")
    assert "--WORKS_FOR-->" in mermaid
    assert "Anna" in mermaid


def test_mini_cypher_subset():
    store = baue_beispiel_graph()

    personen = store.run_cypher("MATCH (n:Person) RETURN n")
    assert len(personen) == 2

    eine = store.run_cypher("MATCH (n:Person) WHERE n.name = 'Anna' RETURN n")
    assert len(eine) == 1 and eine[0]["n"]["properties"]["name"] == "Anna"

    paare = store.run_cypher(
        "MATCH (a:Person)-[r:WORKS_FOR]->(c:Company) RETURN a, c")
    assert len(paare) == 2

    typisiert = store.run_cypher(
        "MATCH (a {name: 'Anna'})-[r]->(b) RETURN a, type(r), b")
    assert len(typisiert) == 3
    assert any(zeile["type(r)"] == "CONTRIBUTES_TO" for zeile in typisiert)


def test_mini_cypher_lehnt_schreiben_ab():
    store = baue_beispiel_graph()
    for verboten in ("CREATE (n:Person {name: 'X'})",
                     "MATCH (n) DELETE n",
                     "MERGE (n:Person) RETURN n",
                     "MATCH (n) RETURN n.name LIMIT 1"):  # LIMIT nicht im Subset
        try:
            store.run_cypher(verboten)
        except ValueError:
            continue
        raise AssertionError(f"Abfrage haette abgelehnt werden muessen: {verboten}")
