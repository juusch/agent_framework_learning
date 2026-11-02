"""Aufgabe 7.3 – Referenzloesung: Supervisor-Multi-Agent-System.

Supervisor entscheidet je Runde, welcher Fach-Agent als Naechstes
arbeitet (offline per Regel-Logik, mit Key als LLM-Aufruf).
Loop-Schutz: max_runden begrenzt die Delegation.
"""

import sys
from pathlib import Path
from typing import TypedDict

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from langgraph.graph import END, START, StateGraph

from lernakademie.mock_llm import get_chat_model, is_offline_mode

AGENTEN = ("recherche_agent", "schreib_agent")


class ProjektZustand(TypedDict):
    auftrag: str
    naechster_schritt: str
    stichpunkte: list[str]
    bericht: str
    ergebnis_log: list[str]
    runden: int
    max_runden: int


# ---------------- Fach-Agenten ---------------------------------------------


def recherche_agent(state: ProjektZustand) -> dict:
    """Sammelt Stichpunkte (offline deterministisch, mit Key per LLM)."""
    if is_offline_mode():
        stichpunkte = [
            f"RAG kombiniert Suche und Textgenerierung ({state['auftrag']}).",
            "Embeddings machen Aehnlichkeit messbar.",
            "Quellenangaben schaffen Vertrauen.",
        ]
    else:
        modell = get_chat_model(temperature=0.2)
        antwort = modell.invoke(
            [("system", "Nenne genau 3 kurze Stichpunkte als Liste."),
             ("human", f"Thema: {state['auftrag']}")]
        )
        stichpunkte = [zeile.strip("- ") for zeile in antwort.content.splitlines() if zeile.strip()][:3]
    return {
        "stichpunkte": stichpunkte,
        "ergebnis_log": state["ergebnis_log"] + ["recherche_agent: 3 Stichpunkte"],
    }


def schreib_agent(state: ProjektZustand) -> dict:
    """Formuliert den Bericht aus den Stichpunkten."""
    if is_offline_mode():
        punkte = " ".join(state["stichpunkte"])
        bericht = f"Bericht zu '{state['auftrag']}': {punkte}"
    else:
        modell = get_chat_model(temperature=0.2)
        antwort = modell.invoke(
            [("system", "Schreibe einen kompakten Abschlussbericht."),
             ("human", "Stichpunkte: " + " ".join(state["stichpunkte"]))]
        )
        bericht = antwort.content
    return {
        "bericht": bericht,
        "ergebnis_log": state["ergebnis_log"] + ["schreib_agent: Bericht erstellt"],
    }


# ---------------- Supervisor ------------------------------------------------


def supervisor(state: ProjektZustand) -> dict:
    """Projektleitung: entscheidet den naechsten Schritt.

    Offline: deterministische Regel-Logik (erst Recherche, dann
    Schreiben, dann FINISH). Mit Key: LLM-Entscheidung.
    """
    if is_offline_mode():
        if not state["stichpunkte"]:
            schritt = "recherche_agent"
        elif not state["bericht"]:
            schritt = "schreib_agent"
        else:
            schritt = "FINISH"
    else:
        modell = get_chat_model(temperature=0.0)
        kontext = (
            f"Auftrag: {state['auftrag']}\n"
            f"Stichpunkte vorhanden: {bool(state['stichpunkte'])}\n"
            f"Bericht vorhanden: {bool(state['bericht'])}\n"
            "Verfuegbare Agenten: recherche_agent, schreib_agent oder FINISH.\n"
            "Antworte NUR mit einem der drei Woerter."
        )
        antwort = modell.invoke([("system", "Du bist ein Supervisor."),
                                 ("human", kontext)])
        schritt = antwort.content.strip()
        if schritt not in AGENTEN + ("FINISH",):
            schritt = "FINISH"  # unbekannte Antwort -> sicher abbrechen

    # Loop-Schutz: nie laenger delegieren als max_runden
    if state["runden"] >= state["max_runden"]:
        schritt = "FINISH"

    print(f"  Supervisor entscheidet: {schritt} (Runde {state['runden'] + 1})")
    return {"naechster_schritt": schritt, "runden": state["runden"] + 1}


def weiche(state: ProjektZustand) -> str:
    return state["naechster_schritt"]


# ---------------- Graph -----------------------------------------------------


def baue_supervisor_graph():
    graph = StateGraph(ProjektZustand)
    graph.add_node("supervisor", supervisor)
    graph.add_node("recherche_agent", recherche_agent)
    graph.add_node("schreib_agent", schreib_agent)

    graph.add_edge(START, "supervisor")
    graph.add_conditional_edges("supervisor", weiche, {
        "recherche_agent": "recherche_agent",
        "schreib_agent": "schreib_agent",
        "FINISH": END,
    })
    # Agenten melden sich ZURUECK beim Supervisor:
    graph.add_edge("recherche_agent", "supervisor")
    graph.add_edge("schreib_agent", "supervisor")
    return graph.compile()


def main() -> None:
    if is_offline_mode():
        print("OFFLINE-Modus: Supervisor-Entscheidungen per Regel-Logik.\n")

    app = baue_supervisor_graph()
    ergebnis = app.invoke({
        "auftrag": "Kurzdokumentation ueber RAG",
        "naechster_schritt": "",
        "stichpunkte": [],
        "bericht": "",
        "ergebnis_log": [],
        "runden": 0,
        "max_runden": 5,
    })
    print("\nErgebnis-Log:")
    for eintrag in ergebnis["ergebnis_log"]:
        print(f"  - {eintrag}")
    print("\nFinbericht:", ergebnis["bericht"][:200])

    # Loop-Schutz demonstrieren: hartes Limit -> fruehes FINISH
    print("\nKontrolle mit max_runden=1:")
    knapp = app.invoke({
        "auftrag": "Test", "naechster_schritt": "", "stichpunkte": [],
        "bericht": "", "ergebnis_log": [], "runden": 0, "max_runden": 1,
    })
    print("  Log:", knapp["ergebnis_log"] or "(sofort beendet)")


if __name__ == "__main__":
    main()
