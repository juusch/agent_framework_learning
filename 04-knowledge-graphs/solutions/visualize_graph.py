"""Aufgabe 10.4 – Referenzloesung: Graph-Visualisierung.

Erzeugt Mermaid aus DATEN (nicht handgezeichnet) und eine Fokus-Ansicht.
Bonus-Kommentar unten: der pyvis-Einzeiler, der in Stufe 15 im Frontend
interaktiv wird.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from lernakademie.graph_store import GraphStore, baue_beispiel_graph


def to_mermaid_gefiltert(store: GraphStore, label: str) -> str:
    """Fokus-View: nur Nodes eines Labels plus deren direkte Nachbarn."""
    fokus = store.nodes(label)
    fokus_ids = {n.id for n in fokus}
    sichtbare_ids = set(fokus_ids)
    zeilen = ["flowchart LR"]
    for node in fokus:
        name = node.properties.get("name", f"n{node.id}")
        zeilen.append(f"    N{node.id}[\"{name}<br/>:{label}\"]")
        for kante, ziel in store.neighbors(node.id):
            if ziel.id not in sichtbare_ids:
                sichtbare_ids.add(ziel.id)
                ziel_name = ziel.properties.get("name", f"n{ziel.id}")
                ziel_label = ":".join(ziel.labels) or "Node"
                zeilen.append(f"    N{ziel.id}[\"{ziel_name}<br/>{ziel_label}\"]")
            zeilen.append(f"    N{node.id} --{kante.typ}--> N{kante.to_id}")
    return "\n".join(zeilen)


def main() -> None:
    store = baue_beispiel_graph()

    # 1) Gesamtsicht als Datei (GitHub rendert das direkt!)
    mermaid = store.to_mermaid()
    inhalt = f"```mermaid\n{mermaid}\n```"
    ausgabe = Path(__file__).resolve().parent / "diagramm.md"
    ausgabe.write_text(inhalt, encoding="utf-8")
    print("Gesamter Graph gespeichert in:", ausgabe.name)
    print(mermaid, "\n")

    # 2) Fokus-View: Departments + Nachbarn
    fokus = to_mermaid_gefiltert(store, "Department")
    print("Fokus-View (Department + Nachbarn):")
    print(fokus)

    # ------------------------------------------------------------------
    # BONUS-AUSBLICK (Stufe 15, Frontend) – nicht Teil der Aufgabe:
    # Interaktive Visualisierung mit pyvis braucht nur wenige Zeilen:
    #
    #   from pyvis.network import Network
    #   net = Network(directed=True)
    #   for node in store.nodes():
    #       net.add_node(node.id, label=node.properties.get("name", "?"))
    #   for kante in store.relationships():
    #       net.add_edge(kante.from_id, kante.to_id, label=kante.typ)
    #   net.save_graph("graph.html")   # -> im Browser oeffnen, Nodes ziehen!
    #
    # Genau das macht spaeter das Knowledge-Graph-Explorer-Frontend.
    # ------------------------------------------------------------------


if __name__ == "__main__":
    main()
