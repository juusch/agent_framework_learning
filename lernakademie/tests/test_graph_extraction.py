"""Tests fuer Graph-Extraktion und sichere Cypher-Ausfuehrung."""

import os

os.environ.setdefault("ACADEMY_OFFLINE", "1")

import pytest

from lernakademie.graph_store import GraphStore
from lernakademie.graph_extraction import (
    extrahiere, fuelle_graph, ist_sicher, fuehre_sicher_aus, cypher_aus_frage,
)


def test_offline_extraktion():
    text = ("Anna arbeitet bei Acme und gehoert zu Engineering. "
            "Engineering arbeitet an AI Assistant.")
    ergebnis = extrahiere(text)
    namen = {e["name"] for e in ergebnis.entitaeten}
    assert {"Anna", "Acme", "Engineering"} <= namen
    assert len(ergebnis.beziehungen) >= 2
    typen = {b["typ"] for b in ergebnis.beziehungen}
    assert "WORKS_FOR" in typen


def test_graph_population_mit_entity_resolution():
    store = GraphStore()
    text = "Anna arbeitet bei Acme."
    erste = extrahiere(text)
    gesetzt1 = fuelle_graph(store, erste)
    assert gesetzt1 == 1 and len(store.nodes()) == 2

    # Derselbe Text nochmal: KEINE Duplikate (Entity Resolution!)
    zweite = extrahiere(text)
    gesetzt2 = fuelle_graph(store, zweite)
    assert gesetzt2 == 1  # Kante wird (im einfachen Store) erneut angelegt,
    assert len(store.nodes()) == 2  # aber Nodes nicht dupliziert


def test_cypher_sicherheitswhitelist():
    assert ist_sicher("MATCH (n:Person) RETURN n")
    assert not ist_sicher("CREATE (n:Person {name: 'X'})")
    assert not ist_sicher("MATCH (n) DELETE n")
    assert not ist_sicher("MERGE (n:Person) RETURN n")
    assert not ist_sicher("")  # leer

    store = GraphStore()
    with pytest.raises(ValueError):
        fuehre_sicher_aus(store, "MATCH (n) DETACH DELETE n")
    ergebnis = fuehre_sicher_aus(store, "MATCH (n) RETURN n")
    assert ergebnis == []


def test_frage_zu_cypher_fallback():
    cypher = cypher_aus_frage("Wo arbeitet Anna?")
    assert cypher == "MATCH (a {name: 'Anna'})-[r]->(b) RETURN a, type(r), b"
    assert ist_sicher(cypher)
    assert cypher_aus_frage("Was ist der Sinn des Lebens?") is None
