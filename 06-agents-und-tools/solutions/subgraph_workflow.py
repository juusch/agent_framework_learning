"""Aufgabe 7.2 – Referenzloesung: Subgraph als Abteilung.

Der Qualitaets-Loop (Stufe 5.4) wird als EIGENER Graph gebaut und im
aeusseren Graphen ueber eine Adapter-Funktion als eine Station genutzt.
"""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph


# ---------------- Subgraph: Abteilung Qualitaet ---------------------------

class LoopZustand(TypedDict):
    text: str
    bewertung: int
    versuche: int
    max_versuche: int


def entwerfen(state: LoopZustand) -> dict:
    versuche = state["versuche"] + 1
    return {"text": f"{state['text']} [Politur {versuche}]", "versuche": versuche}


def pruefen(state: LoopZustand) -> dict:
    bewertung = min(100, 30 + 25 * state["versuche"])
    return {"bewertung": bewertung}


def loop_weiche(state: LoopZustand) -> str:
    if state["bewertung"] >= 60 or state["versuche"] >= state["max_versuche"]:
        return "fertig"
    return "nachbessern"


def baue_qualitaets_loop():
    """Der Subgraph: eigenstaendig baubar UND testbar."""
    graph = StateGraph(LoopZustand)
    graph.add_node("entwerfen", entwerfen)
    graph.add_node("pruefen", pruefen)
    graph.add_edge(START, "entwerfen")
    graph.add_edge("entwerfen", "pruefen")
    graph.add_conditional_edges("pruefen", loop_weiche,
                                {"fertig": END, "nachbessern": "entwerfen"})
    return graph.compile()


# ---------------- Aeusserer Graph: das Gebaeude ----------------------------

class ProjektZustand(TypedDict):
    auftrag: str
    freigegebenes_produkt: str
    status: str


def vorbereiten(state: ProjektZustand) -> dict:
    print(f"Vorbereiten: Auftrag '{state['auftrag']}' geht an die Abteilung.")
    return {}


def qualitaet(state: ProjektZustand) -> dict:
    """Adapter: einzige Nahtstelle zwischen aeusserem und innerem State."""
    loop = baue_qualitaets_loop()
    ergebnis = loop.invoke({
        "text": state["auftrag"],
        "bewertung": 0,
        "versuche": 0,
        "max_versuche": 4,
    })
    # Uebersetzung zurueck in die Felder des AEUSSEREN Graphen:
    return {"freigegebenes_produkt": ergebnis["text"]}


def abschliessen(state: ProjektZustand) -> dict:
    return {"status": "versandbereit"}


def baue_projekt_graph():
    graph = StateGraph(ProjektZustand)
    graph.add_node("vorbereiten", vorbereiten)
    graph.add_node("qualitaet", qualitaet)  # <- ganzer Graph als Station!
    graph.add_node("abschliessen", abschliessen)
    graph.add_edge(START, "vorbereiten")
    graph.add_edge("vorbereiten", "qualitaet")
    graph.add_edge("qualitaet", "abschliessen")
    graph.add_edge("abschliessen", END)
    return graph.compile()


def main() -> None:
    # 1) Subgraph standalone testen (Kapselung zahlt sich aus):
    loop = baue_qualitaets_loop()
    solo = loop.invoke({"text": "Solo-Lauf", "bewertung": 0, "versuche": 0, "max_versuche": 3})
    print("Subgraph standalone:", solo["text"])

    # 2) Komplettes Gebaeude:
    app = baue_projekt_graph()
    ergebnis = app.invoke({
        "auftrag": "Produktbroschuere Entwurf v1",
        "freigegebenes_produkt": "",
        "status": "in Bearbeitung",
    })
    print("\nFinaler aeusserer State:")
    for feld, wert in ergebnis.items():
        print(f"  {feld}: {wert}")
    # Hinweis: bewertung/versuche des Loops tauchen hier NICHT auf.


if __name__ == "__main__":
    main()
