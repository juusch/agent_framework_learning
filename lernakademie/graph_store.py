"""In-Memory-Property-Graph – der Offline-Fundus fuer Knowledge-Graph-Uebungen.

Warum gibt es das?
- KG-Aufgaben sollen auch OHNE laufende Neo4j-Datenbank uebbar sein
  (genau wie der Mock-LLM das ohne Key ermoeglicht).
- Die Klasse bildet die Neo4j-Grundbegriffe 1:1 ab:
  Nodes (mit Labels + Properties) und Relationships
  (mit Typ + Properties, gerichtet, von/zu Node-IDs).

Zusaetzlich unterstuetzt `run_cypher` einen kleinen, transparenten
Cypher-Subset (READ-ONLY) – als Lernbruecke zu echtem Cypher:

  MATCH (n:Person) RETURN n
  MATCH (n:Person) WHERE n.name = 'Anna' RETURN n
  MATCH (a:Person)-[r:WORKS_FOR]->(c:Company) RETURN a, c
  MATCH (a {name: 'Anna'})-[r]->(b) RETURN a, type(r), b

Alles andere wirft einen verstaendlichen Fehler – bewusst: Der Subset
soll lehren, nicht Neo4j ersetzen.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class GraphNode:
    """Ein Knoten: eindeutige ID, Labels (z.B. ['Person']) und Properties."""
    id: int
    labels: List[str] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {"id": self.id, "labels": list(self.labels),
                "properties": dict(self.properties)}


@dataclass
class GraphRelationship:
    """Eine gerichtete Kante: Typ (z.B. WORKS_FOR) + Properties."""
    from_id: int
    to_id: int
    typ: str
    properties: Dict[str, Any] = field(default_factory=dict)


class GraphStore:
    """Property-Graph im Speicher (Offline-Pendant zu Neo4j)."""

    def __init__(self) -> None:
        self._nodes: Dict[int, GraphNode] = {}
        self._relationships: List[GraphRelationship] = []
        self._next_id = 0

    # ---------------- Schreiben -------------------------------------------

    def add_node(self, labels: List[str] | str, **properties: Any) -> int:
        """Legt einen Node an, liefert dessen ID zurueck."""
        if isinstance(labels, str):
            labels = [labels]
        node = GraphNode(id=self._next_id, labels=list(labels),
                         properties=dict(properties))
        self._nodes[node.id] = node
        self._next_id += 1
        return node.id

    def add_relationship(self, from_id: int, to_id: int, typ: str,
                         **properties: Any) -> None:
        """Legt eine gerichtete Kante an (beide Nodes muessen existieren)."""
        if from_id not in self._nodes or to_id not in self._nodes:
            raise ValueError("add_relationship: Node-ID existiert nicht.")
        self._relationships.append(
            GraphRelationship(from_id, to_id, typ.upper(), dict(properties)))

    def clear(self) -> None:
        self._nodes.clear()
        self._relationships.clear()
        self._next_id = 0

    # ---------------- Lesen -------------------------------------------------

    def nodes(self, label: Optional[str] = None) -> List[GraphNode]:
        """Alle Nodes – optional nach Label gefiltert."""
        if label is None:
            return list(self._nodes.values())
        return [n for n in self._nodes.values() if label in n.labels]

    def relationships(self, typ: Optional[str] = None) -> List[GraphRelationship]:
        """Alle Kanten – optional nach Typ gefiltert."""
        if typ is None:
            return list(self._relationships)
        return [r for r in self._relationships if r.typ == typ.upper()]

    def find_node(self, label: Optional[str] = None,
                  **properties: Any) -> Optional[GraphNode]:
        """Erster Node, der Label UND alle Properties erfuellt (oder None)."""
        for node in self.nodes(label):
            if all(node.properties.get(k) == v for k, v in properties.items()):
                return node
        return None

    def neighbors(self, node_id: int,
                   typ: Optional[str] = None) -> List[tuple[GraphRelationship, GraphNode]]:
        """Alle direkten Nachbarn: (Kante, Nachbar-Node) in Pfeilrichtung."""
        ergebnis = []
        for kante in self._relationships:
            if kante.from_id == node_id and (typ is None or kante.typ == typ.upper()):
                ergebnis.append((kante, self._nodes[kante.to_id]))
        return ergebnis

    def path(self, start_id: int, ziel_id: int, max_tiefe: int = 4) -> Optional[List[int]]:
        """Kuerzester Pfad (Breitensuche) zwischen zwei Nodes (IDs) oder None."""
        from collections import deque

        if start_id == ziel_id:
            return [start_id]
        warteschlange = deque([(start_id, [start_id])])
        besucht = {start_id}
        while warteschlange:
            aktuelle_id, pfad = warteschlange.popleft()
            if len(pfad) > max_tiefe:
                continue
            for _, nachbar in self.neighbors(aktuelle_id):
                if nachbar.id in besucht:
                    continue
                if nachbar.id == ziel_id:
                    return pfad + [nachbar.id]
                besucht.add(nachbar.id)
                warteschlange.append((nachbar.id, pfad + [nachbar.id]))
        return None
    # ---------------- Mini-Cypher (READ-ONLY) -----------------------------

    def run_cypher(self, query: str) -> List[Dict[str, Any]]:
        """Fuehrt einen kleinen, sicheren Cypher-Subset aus.

        Unterstuetzte Muster (kein Schreiben, kein Loeschen!):
          MATCH (n:Person) RETURN n
          MATCH (n:Person) WHERE n.name = 'Anna' RETURN n
          MATCH (a:Person)-[r:WORKS_FOR]->(c:Company) RETURN a, c
          MATCH (a {name: 'Anna'})-[r]->(b) RETURN a, type(r), b
        """
        query = " ".join(query.strip().split())
        if not query.upper().startswith("MATCH ") or " RETURN " not in query.upper():
            raise ValueError(
                "Nur lesende MATCH...RETURN-Abfragen sind im Offline-Subset "
                "erlaubt (kein CREATE/MERGE/DELETE)."
            )

        # WHERE-Syntax auf die aequivalente Property-Syntax normalisieren:
        #   MATCH (n:Person) WHERE n.name = 'Anna' RETURN n
        #   -> MATCH (n:Person {name: 'Anna'}) RETURN n
        where_muster = re.match(
            r"^MATCH \((\w+)(?::(\w+))?\) WHERE \w+\.(\w+) = '([^']+)' (RETURN .+)$",
            query)
        if where_muster:
            var, label, prop, wert, rest = where_muster.groups()
            label_teil = f":{label}" if label else ""
            query = f"MATCH ({var}{label_teil} {{{prop}: '{wert}'}}) {rest}"

        # Zwei Muster: mit oder ohne Beziehungsmuster
        ohne_rela = re.match(
            r"MATCH \((\w+)(?::(\w+))?(?: ?\{(\w+): ?'([^']+)'\})?\) RETURN (.+)$",
            query)
        mit_rela = re.match(
            r"MATCH \((\w+)(?::(\w+))?(?: ?\{(\w+): ?'([^']+)'\})?\)"
            r"-\[(\w+)(?::(\w+))?\]->\((\w+)(?::(\w+))?\) RETURN (.+)$",
            query)
        if not ohne_rela and not mit_rela:
            raise ValueError(
                "Abfrage passt auf keinen unterstuetzten Cypher-Subset. "
                "Beispiele: \"MATCH (n:Person) RETURN n\" oder "
                "\"MATCH (a:Person)-[r:WORKS_FOR]->(c:Company) RETURN a, c\""
            )

        def _start_nodes(label: Optional[str], prop: Optional[str], wert: Optional[str]):
            kandidaten = self.nodes(label)
            if prop:
                kandidaten = [n for n in kandidaten
                              if n.properties.get(prop) == wert]
            return kandidaten

        def _spalten(zeile: Dict[str, Any], return_teil: str,
                     rel_var: Optional[str] = None) -> Dict[str, Any]:
            ergebnis_zeile = {}
            for spalte in return_teil.split(","):
                spalte = spalte.strip()
                if rel_var and spalte == f"type({rel_var})":
                    ergebnis_zeile[spalte] = zeile[rel_var]
                elif spalte in zeile:
                    ergebnis_zeile[spalte] = zeile[spalte]
                else:
                    raise ValueError(f"Unbekannte RETURN-Spalte: {spalte}")
            return ergebnis_zeile

        zeilen: List[Dict[str, Any]] = []
        if ohne_rela:
            links, label_links, prop_links, wert_links, return_teil = ohne_rela.groups()
            for node in _start_nodes(label_links, prop_links, wert_links):
                zeilen.append(_spalten({links: node.to_dict()}, return_teil))
            return zeilen

        (links, label_links, prop_links, wert_links,
         rel_var, rel_typ, rechts, label_rechts, return_teil) = mit_rela.groups()
        for node in _start_nodes(label_links, prop_links, wert_links):
            for kante, ziel in self.neighbors(node.id, rel_typ):
                if label_rechts and label_rechts not in ziel.labels:
                    continue
                zeile = {links: node.to_dict(), rel_var: kante.typ,
                         rechts: ziel.to_dict()}
                zeilen.append(_spalten(zeile, return_teil, rel_var))
        return zeilen

    # ---------------- Visualisierung ---------------------------------------

    def to_mermaid(self) -> str:
        """Erzeugt Mermaid-Code fuer die Visualisierung (Markdown/GitHub!)."""
        zeilen = ["flowchart LR"]
        for node in self._nodes.values():
            name = node.properties.get("name", f"n{node.id}")
            label = ":".join(node.labels) or "Node"
            zeilen.append(f"    N{node.id}[\"{name}<br/>{label}\"]")
        for kante in self._relationships:
            zeilen.append(f"    N{kante.from_id} --{kante.typ}--> N{kante.to_id}")
        return "\n".join(zeilen)


# ---------------- Beispiel-Graph ( fuer Aufgaben & Tests) -------------------


def baue_beispiel_graph() -> GraphStore:
    """Beispiel-Firma: Anna/Ben, Acme, Engineering, Projekt 'AI Assistant'."""
    store = GraphStore()
    anna = store.add_node(["Person"], name="Anna", rolle="Entwicklerin")
    ben = store.add_node(["Person"], name="Ben", rolle="Analyst")
    acme = store.add_node(["Company"], name="Acme", branche="Technologie")
    engineering = store.add_node(["Department"], name="Engineering")
    projekt = store.add_node(["Project"], name="AI Assistant", status="aktiv")

    store.add_relationship(anna, acme, "WORKS_FOR", seit=2021)
    store.add_relationship(ben, acme, "WORKS_FOR", seit=2023)
    store.add_relationship(anna, engineering, "BELONGS_TO")
    store.add_relationship(engineering, projekt, "WORKS_ON")
    store.add_relationship(anna, projekt, "CONTRIBUTES_TO")
    return store
