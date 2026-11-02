"""Aufgabe 5.2 – Referenzloesung: State & Nodes (Werkstatt).

Drei Nodes teilen sich EINEN State: jede liest, was vorherige
geschrieben haben, und traegt ihre eigenen Aenderungen ein.
"""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class WerkstattZustand(TypedDict):
    rohtext: str
    woerter: int
    titel: str
    fertig: bool


def analysieren(state: WerkstattZustand) -> dict:
    """Node 1: zaehlt Woerter (liest rohtext, schreibt woerter)."""
    return {"woerter": len(state["rohtext"].split())}


def aufbereiten(state: WerkstattZustand) -> dict:
    """Node 2: baut Titel aus den ersten 3 Woertern (liest rohtext)."""
    titel = " ".join(state["rohtext"].split()[:3]).upper()
    return {"titel": titel}


def abschliessen(state: WerkstattZustand) -> dict:
    """Node 3: liest woerter UND titel, setzt fertig-Flag."""
    print(f"Abschluss: '{state['titel']}' mit {state['woerter']} Woertern.")
    return {"fertig": True}


def baue_graph():
    graph = StateGraph(WerkstattZustand)
    graph.add_node("analysieren", analysieren)
    graph.add_node("aufbereiten", aufbereiten)
    graph.add_node("abschliessen", abschliessen)

    graph.add_edge(START, "analysieren")
    graph.add_edge("analysieren", "aufbereiten")
    graph.add_edge("aufbereiten", "abschliessen")
    graph.add_edge("abschliessen", END)
    return graph.compile()


def main() -> None:
    app = baue_graph()
    ergebnis = app.invoke({
        "rohtext": "KI-Anwendungen bestehen aus vielen kleinen Bausteinen",
        "woerter": 0,
        "titel": "",
        "fertig": False,
    })
    print("Finaler State:", ergebnis)
    # ergebnis['woerter'] von analysieren, ['titel'] von aufbereiten,
    # ['fertig'] von abschliessen – alles im gemeinsamen Notizblock.


if __name__ == "__main__":
    main()
