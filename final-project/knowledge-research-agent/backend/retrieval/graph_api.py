"""Graph-Retrieval: der Knowledge Graph der Anwendung.

Nutzt den Akademie-GraphStore (Offline-Pendant zu Neo4j, Stufe 11).
Neue Fakten nur ueber den Freigabe-Workflow in agents/approval.py!
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))  # Akademie-Wurzel
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # Projektordner

from lernakademie.graph_store import GraphStore


def baue_wissens_graph() -> GraphStore:
    """Seed-Graph (modelliert nach database/schema/graph_schema.md)."""
    store = GraphStore()
    anna = store.add_node(["Person"], name="Anna", rolle="Entwicklerin")
    ben = store.add_node(["Person"], name="Ben", rolle="Analyst")
    clara = store.add_node(["Person"], name="Clara", rolle="Abteilungsleitung")
    acme = store.add_node(["Company"], name="Acme", branche="Technologie")
    engineering = store.add_node(["Department"], name="Engineering")
    analytics = store.add_node(["Department"], name="Data & Analytics")
    forschung = store.add_node(["Department"], name="Forschung")
    projekt = store.add_node(["Project"], name="AI Assistant", status="aktiv")

    store.add_relationship(anna, acme, "WORKS_FOR")
    store.add_relationship(ben, acme, "WORKS_FOR")
    store.add_relationship(anna, engineering, "BELONGS_TO")
    store.add_relationship(ben, analytics, "BELONGS_TO")
    store.add_relationship(clara, engineering, "LEADS")
    store.add_relationship(engineering, projekt, "WORKS_ON")
    store.add_relationship(analytics, projekt, "PROVIDES_DATA_FOR")
    store.add_relationship(forschung, projekt, "WORKS_ON")
    store.add_relationship(anna, projekt, "CONTRIBUTES_TO")
    return store


def suche_graph(store: GraphStore, frage: str) -> list[str]:
    """Beantwortet Verbindungs-Fragen durch Traversierung (Stufe 13/14).

    Gibt Fakten der Form 'A --REL--> B' zurueck – Quelltransparenz pur.
    """
    klein = frage.lower()
    fakten: list[str] = []

    def _name(node) -> str:
        return node.properties.get("name", "?")

    # 1) Direkte Nachbarn einer genannten Entitaet
    for node in store.nodes():
        name_klein = _name(node).lower()
        if name_klein and name_klein in klein:
            for kante, ziel in store.neighbors(node.id):
                fakten.append(f"{_name(node)} --{kante.typ}--> {_name(ziel)}")

    # 2) Vorgaenger des Projekts ('Wer haengt am Projekt dran?')
    projekt = store.find_node("Project", name="AI Assistant")
    if projekt and ("projekt" in klein or "ai assistant" in klein):
        for kante in store.relationships():
            if kante.to_id == projekt.id:
                quelle = store.nodes()[kante.from_id]
                fakten.append(f"{_name(quelle)} --{kante.typ}--> AI Assistant")

    # Duplikate entfernen, Reihenfolge behalten
    return list(dict.fromkeys(fakten))


def graph_als_dto(store: GraphStore) -> dict:
    """Liefert Nodes/Edges als darstellbare Struktur (Frontend/PyVis)."""
    nodes = [
        {"id": n.id, "label": ":".join(n.labels), "name": n.properties.get("name", "?"),
         "properties": n.properties}
        for n in store.nodes()
    ]
    edges = [
        {"von": k.from_id, "zu": k.to_id, "typ": k.typ}
        for k in store.relationships()
    ]
    return {"nodes": nodes, "edges": edges}
