"""Aufgabe 14.2 – Loesung: Freigabe fuer destruktive Graph-Operationen.

Prinzip: Lesen erlaubt der Agent allein (Whitelist, Stufe 12.3) –
SCHREIBEN nur nach menschlicher Freigabe (interrupt + resume).
"""

import sys
from pathlib import Path
from typing import TypedDict

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from lernakademie.graph_store import GraphStore

VORGESCHLAGENE_FAKTEN = [
    {"von": "Clara", "typ": "LEADS", "zu": "Engineering",
     "grund": "Steht so im Firmenprofil."},
    {"von": "Ben", "typ": "MANAGES", "zu": "Acme",
     "grund": "Vermutung ohne Quelle – riskant!"},
]


class PflegeZustand(TypedDict):
    schritt: int
    audit_log: list[str]


def baue_graph() -> GraphStore:
    store = GraphStore()
    anna = store.add_node(["Person"], name="Anna")
    engineering = store.add_node(["Department"], name="Engineering")
    clara = store.add_node(["Person"], name="Clara", rolle="Abteilungsleitung")
    projekt = store.add_node(["Project"], name="AI Assistant")
    acme = store.add_node(["Company"], name="Acme")
    store.add_relationship(clara, engineering, "LEADS")
    store.add_relationship(anna, engineering, "BELONGS_TO")
    store.add_relationship(engineering, projekt, "WORKS_ON")
    return store


def fakt_anfordern(state: PflegeZustand) -> dict:
    """Naechsten vorgeschlagenen Fakt auswaehlen (offline: Liste)."""
    index = state["schritt"]
    if index >= len(VORGESCHLAGENE_FAKTEN):
        return {"schritt": index}
    print(f"Fakt {index + 1} vorgeschlagen: "
          f"{VORGESCHLAGENE_FAKTEN[index]['von']} "
          f"--{VORGESCHLAGENE_FAKTEN[index]['typ']}--> "
          f"{VORGESCHLAGENE_FAKTEN[index]['zu']}")
    return {"schritt": index + 1}


def baue_fakt_anlegen(store: GraphStore):
    """Node-Factory: legt den aktuellen Fakt NUR nach Freigabe an."""

    def node(state: PflegeZustand) -> dict:
        index = state["schritt"] - 1
        if index < 0 or index >= len(VORGESCHLAGENE_FAKTEN):
            return {}

        fakt = VORGESCHLAGENE_FAKTEN[index]

        # Der Stift schwebt ueber dem Formular: interrupt VOR der Aenderung
        freigabe = interrupt({
            "frage": "Soll dieser Fakt in den Knowledge Graph eingetragen werden?",
            "fakt": f"{fakt['von']} --{fakt['typ']}--> {fakt['zu']}",
            "grund": fakt["grund"],
        })

        if freigabe:
            von = store.find_node(None, name=fakt["von"])
            zu = store.find_node(None, name=fakt["zu"])
            if von and zu:
                store.add_relationship(von.id, zu.id, fakt["typ"])
                eintrag = (f"GENEHMIGT: {fakt['von']} --{fakt['typ']}--> "
                           f"{fakt['zu']}")
            else:
                eintrag = f"GENEHMIGT, aber Node fehlt: {fakt}"
        else:
            eintrag = (f"ABGELEHNT: {fakt['von']} --{fakt['typ']}--> "
                       f"{fakt['zu']} (Grund im Vorschlag: {fakt['grund']})")
        print(f"  -> {eintrag}")
        return {"audit_log": state["audit_log"] + [eintrag]}

    return node


def weiche(state: PflegeZustand) -> str:
    return "weiter" if state["schritt"] < len(VORGESCHLAGENE_FAKTEN) else "fertig"


def baue_workflow(store: GraphStore):
    graph = StateGraph(PflegeZustand)
    graph.add_node("fakt_anfordern", fakt_anfordern)
    graph.add_node("fakt_anlegen", baue_fakt_anlegen(store))
    graph.add_edge(START, "fakt_anfordern")
    graph.add_edge("fakt_anfordern", "fakt_anlegen")
    graph.add_conditional_edges("fakt_anlegen", weiche,
                                {"weiter": "fakt_anfordern", "fertig": END})
    # Ohne Checkpointer kein interrupt!
    return graph.compile(checkpointer=MemorySaver())


def main() -> None:
    store = baue_graph()
    workflow = baue_workflow(store)
    config = {"configurable": {"thread_id": "pflege-1"}}

    kanten_vorher = len(store.relationships())
    print(f"Kanten vor dem Lauf: {kanten_vorher}\n")

    ergebnis = workflow.invoke({"schritt": 0, "audit_log": []}, config)

    # Erster Fakt: freigeben; zweiter: ablehnen (Simulation einer
    # menschlichen Pruefung: Der 2. Fakt hat keinen Beleg!)
    for freigabe in (True, False):
        interrupts = ergebnis.get("__interrupt__")
        if not interrupts:
            break
        daten = interrupts[0].value
        print(f"INTERRUPT: {daten['frage']} | Fakt: {daten['fakt']}")
        print(f"  Grund des Vorschlags: {daten['grund']}")
        print(f"  Mensch entscheidet: {'Freigabe' if freigabe else 'Ablehnung'}\n")
        ergebnis = workflow.invoke(Command(resume=freigabe), config)

    kanten_nachher = len(store.relationships())
    print(f"Kanten nach dem Lauf: {kanten_nachher} "
          f"(erwartet: {kanten_vorher + 1} – nur der genehmigte Fakt!)")

    print("\n---- Audit-Log ----")
    for eintrag in ergebnis["audit_log"]:
        print(f"  - {eintrag}")


if __name__ == "__main__":
    main()
