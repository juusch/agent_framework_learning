"""Aufgabe 5.1 – Referenzloesung: Hello Graph.

Mechanik: Schema -> Node -> Kanten -> compile -> invoke.
"""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class Zustand(TypedDict):
    """Der gemeinsame Notizblock (hier: ein einziges Feld)."""
    begruessung: str


def begruessen(state: Zustand) -> dict:
    """Node: liefert nur die AENDERUNG zurueck (Merge-Prinzip)."""
    return {"begruessung": "Hallo LangGraph!"}


def verabschieden(state: Zustand) -> dict:
    """Bonus-Node: erweitert das vorhandene Feld (liest + schreibt)."""
    return {"begruessung": state["begruessung"] + " ... und tschuess!"}


def baue_graph():
    """Fabrikfunktion: Graph definieren und kompilieren."""
    graph = StateGraph(Zustand)
    graph.add_node("begruessen", begruessen)
    graph.add_node("verabschieden", verabschieden)

    graph.add_edge(START, "begruessen")
    graph.add_edge("begruessen", "verabschieden")
    graph.add_edge("verabschieden", END)
    return graph.compile()


def main() -> None:
    app = baue_graph()
    ergebnis = app.invoke({"begruessung": ""})
    print("Finaler State:", ergebnis)
    # Erwartung: {'begruessung': 'Hallo LangGraph! ... und tschuess!'}


if __name__ == "__main__":
    main()
