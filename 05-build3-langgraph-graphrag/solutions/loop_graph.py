"""Aufgabe 5.4 – Referenzloesung: Schleife mit Sicherheitsbremse.

Loop: entwerfen -> pruefen -> (nicht gut & Versuche uebrig?) -> entwerfen
Zwei Endbedingungen: Qualität erreicht ODER Limit erreicht.
"""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class PolierZustand(TypedDict):
    text: str
    bewertung: int
    versuche: int
    max_versuche: int
    historie: list[str]


def entwerfen(state: PolierZustand) -> dict:
    """Simulierte Verbesserung: haengt pro Durchgang einen Zusatz an."""
    neuer_versuch = state["versuche"] + 1
    text = f"{state['text']} (Politur {neuer_versuch})"
    print(f"  entwerfen: Durchgang {neuer_versuch}")
    return {
        "text": text,
        "versuche": neuer_versuch,
        "historie": state["historie"] + [text],
    }


def pruefen(state: PolierZustand) -> dict:
    """Einfache Metrik: jede Politur +25 Punkte, Grundqualitaet aus Laenge."""
    basis = min(30, len(state["text"]) // 10)
    bewertung = min(100, basis + 25 * state["versuche"])
    print(f"  pruefen: Bewertung {bewertung}")
    return {"bewertung": bewertung}


def weiche(state: PolierZustand) -> str:
    """Doppel-Bedingung: gut genug ODER Limit erreicht -> Ende."""
    if state["bewertung"] >= 60:
        return "fertig"
    if state["versuche"] >= state["max_versuche"]:
        return "fertig"
    return "nachbessern"


def baue_graph():
    graph = StateGraph(PolierZustand)
    graph.add_node("entwerfen", entwerfen)
    graph.add_node("pruefen", pruefen)

    graph.add_edge(START, "entwerfen")
    graph.add_edge("entwerfen", "pruefen")
    graph.add_conditional_edges(
        "pruefen",
        weiche,
        {"fertig": END, "nachbessern": "entwerfen"},
    )
    return graph.compile()


def main() -> None:
    app = baue_graph()
    ergebnis = app.invoke({
        "text": "Mein erster Entwurf",
        "bewertung": 0,
        "versuche": 0,
        "max_versuche": 5,
        "historie": [],
    })
    print("\nFinaler Text:", ergebnis["text"])
    print(f"Versuche: {ergebnis['versuche']} | Bewertung: {ergebnis['bewertung']}")
    print("Historie:")
    for schritt in ergebnis["historie"]:
        print(f"  - {schritt}")


if __name__ == "__main__":
    main()
