"""Freigabe-Workflow fuer Fakten (Human-in-the-Loop, Stufe 14.2-Muster).

Ablauf:
  vorschlagen -> [interrupt: Freigabe?] -> anlegen/verwerfen -> protokollieren

Der interrupt pausiert den Lauf im Backend; das Frontend (oder curl)
setzt mit Command(resume=True/False) und derselben thread_id fort.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TypedDict

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))  # Akademie-Wurzel
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # Projektordner

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt



AUDIT_LOG: list[str] = []  #prozessglobal, fuer GET /audit


class FreigabeZustand(TypedDict):
    von: str
    typ: str
    zu: str
    grund: str
    thread_id: str
    ergebnis: str


def vorschlagen(state: FreigabeZustand) -> dict:
    """Bereitet den Fakt vor (hier: ungeprueft aus dem Request; mit Key
    koennte ein LLM den Vorschlag samt Grund extrahieren)."""
    return {}


def anlegen(state: FreigabeZustand) -> dict:
    """Interrupt VOR der Aenderung – der Mensch entscheidet (Stufe 14.2)."""
    freigabe = interrupt({
        "frage": "Soll dieser Fakt in den Knowledge Graph eingetragen werden?",
        "fakt": f"{state['von']} --{state['typ']}--> {state['zu']}",
        "grund": state["grund"] or "(kein Grund angegeben)",
    })
    if freigabe:
        eintrag = f"GENEHMIGT: {state['von']} --{state['typ']}--> {state['zu']}"
    else:
        eintrag = f"ABGELEHNT: {state['von']} --{state['typ']}--> {state['zu']}"
    AUDIT_LOG.append(eintrag)
    print("AUDIT:", eintrag)  # serverseitiges Logging
    return {"ergebnis": eintrag}


def baue_freigabe_workflow(store):
    """Fabrik: bindet den Graph-Store (die angestrebte Aenderung wird in
    der API nach erfolgreicher Freigabe ausgefuehrt – der Store ist hier
    bewusst nicht direkt eingebunden, damit der Workflow reine
    Entscheidungslogik bleibt (testbar ohne Nebenwirkungen))."""

    graph = StateGraph(FreigabeZustand)
    graph.add_node("vorschlagen", vorschlagen)
    graph.add_node("anlegen", anlegen)
    graph.add_edge(START, "vorschlagen")
    graph.add_edge("vorschlagen", "anlegen")
    graph.add_edge("anlegen", END)
    return graph.compile(checkpointer=MemorySaver())

