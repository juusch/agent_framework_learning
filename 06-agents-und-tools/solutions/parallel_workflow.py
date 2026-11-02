"""Aufgabe 7.1 – Referenzloesung: Parallele Pruefer + Zusammenfuehren.

Jeder Pruefer schreibt sein EIGENES Feld -> kein Schreibkonflikt.
Der Merge-Node wartet automatisch auf alle Zweige (Barriere).
"""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class KommissionsZustand(TypedDict):
    text: str
    befund_1: int      # Wortzahl
    befund_2: int      # Zeichenzahl
    befund_3: float    # durchschnittliche Wortlaenge
    bericht: str


def zaehle_woerter(state: KommissionsZustand) -> dict:
    return {"befund_1": len(state["text"].split())}


def zaehle_zeichen(state: KommissionsZustand) -> dict:
    return {"befund_2": len(state["text"])}


def durchschnittliche_wortlaenge(state: KommissionsZustand) -> dict:
    woerter = state["text"].split()
    return {"befund_3": round(sum(len(w) for w in woerter) / len(woerter), 2)}


def zusammenfuehren(state: KommissionsZustand) -> dict:
    """Laeuft erst, wenn ALLE drei Pruefer geliefert haben (Barriere)."""
    bericht = (
        f"Kommissionsbericht: {state['befund_1']} Woerter, "
        f"{state['befund_2']} Zeichen, "
        f"durchschnittliche Wortlaenge {state['befund_3']}."
    )
    return {"bericht": bericht}


def baue_graph():
    graph = StateGraph(KommissionsZustand)
    graph.add_node("zaehle_woerter", zaehle_woerter)
    graph.add_node("zaehle_zeichen", zaehle_zeichen)
    graph.add_node("wortlaenge", durchschnittliche_wortlaenge)
    graph.add_node("zusammenfuehren", zusammenfuehren)

    # Drei parallele Zweige ab START:
    graph.add_edge(START, "zaehle_woerter")
    graph.add_edge(START, "zaehle_zeichen")
    graph.add_edge(START, "wortlaenge")

    # ... und alle drei muessen vor der Zusammenfuehrung fertig sein:
    graph.add_edge("zaehle_woerter", "zusammenfuehren")
    graph.add_edge("zaehle_zeichen", "zusammenfuehren")
    graph.add_edge("wortlaenge", "zusammenfuehren")
    graph.add_edge("zusammenfuehren", END)
    return graph.compile()


def main() -> None:
    app = baue_graph()
    for text in ("Kurzer Test", "LangGraph macht parallele Workflows moeglich"):
        ergebnis = app.invoke({
            "text": text, "befund_1": 0, "befund_2": 0, "befund_3": 0.0, "bericht": "",
        })
        print(f"Text: '{text}'")
        print(f"  {ergebnis['bericht']}\n")


if __name__ == "__main__":
    main()
