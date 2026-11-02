"""Der LangGraph-Workflow des Research-Agenten.

Knoten: intent -> (route) -> vektor / graph / hybrid -> antwort.
Der State fuehrt Route, Doku-Fundstellen und Graph-Fakten getrennt –
die Antwort weist ihre Quellen aus (Stufe 13.2-Prinzip).
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TypedDict

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))  # Akademie-Wurzel
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # Projektordner

from langgraph.graph import END, START, StateGraph

from backend.retrieval.graph_api import suche_graph


class FrageZustand(TypedDict):
    frage: str
    route: str
    dokumente: list[dict]
    graph_fakten: list[str]
    antwort: str


def klassifiziere(frage: str) -> str:
    """Intent-Klassifikation: vektor | graph | hybrid.

    Offline: Regel-Logik (Stufe 14.1). Mit Key koennte hier ein
    LLM-Aufruf stehen – die Pipeline bleibt identisch.
    """
    klein = frage.lower()
    if any(w in klein for w in ("gesamt", "alles", "vergleich", "sowohl", "und was sagt")):
        return "hybrid"
    if any(w in klein for w in ("haengt", "zusammen?", "wer ", "beziehung",
                                "pfad", "verbind", "traegt bei", "arbeitet an")):
        return "graph"
    return "vektor"


def intent_node(state: FrageZustand) -> dict:
    return {"route": klassifiziere(state["frage"])}


def baue_workflow(wissensbasis, wissens_graph):
    """Fabrik: erzeugt den Workflow mit gebundenen Retrieval-Diensten."""

    def vektor_node(state: FrageZustand) -> dict:
        return {"dokumente": wissensbasis.suche(state["frage"])}

    def graph_node(state: FrageZustand) -> dict:
        return {"graph_fakten": suche_graph(wissens_graph, state["frage"])}

    def antwort_node(state: FrageZustand) -> dict:
        teile = []
        if state["dokumente"]:
            quellen = ", ".join(d["quelle"] for d in state["dokumente"])
            teile.append(f"aus Dokumenten ({quellen})")
        if state["graph_fakten"]:
            teile.append(f"aus Knowledge Graph ({len(state['graph_fakten'])} Fakt(en))")
        if not teile:
            return {"antwort": "Dazu habe ich in Dokumenten UND Graph nichts gefunden."}

        # Offline deterministisch; mit Key wuerde hier ein LLM formulieren:
        if state["route"] == "hybrid":
            kopf = "Hybrid-Antwort: "
        elif state["route"] == "graph":
            kopf = "Aus dem Knowledge Graph: "
        else:
            kopf = "Aus den Dokumenten: "
        return {"antwort": kopf + "; ".join(teile)}

    graph = StateGraph(FrageZustand)
    graph.add_node("intent", intent_node)
    graph.add_node("vektor", vektor_node)
    graph.add_node("graph", graph_node)
    graph.add_node("antwort", antwort_node)

    graph.add_edge(START, "intent")
    graph.add_conditional_edges("intent", lambda s: s["route"], {
        "vektor": "vektor", "graph": "graph", "hybrid": "vektor"})
    graph.add_conditional_edges("vektor", lambda s: (
        "graph" if s["route"] == "hybrid" else "antwort"), {
        "graph": "graph", "antwort": "antwort"})
    graph.add_edge("graph", "antwort")
    graph.add_edge("antwort", END)
    return graph.compile()
