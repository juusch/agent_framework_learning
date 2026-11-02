"""Projekt D – Loesung: Autonomer Workflow-Assistent.

Plan -> Ausfuehrungs-Loop mit Fortschritt, Risiko-Klassen (Freigabe
per interrupt), Fehlererholung (1 Wiederholung) und Abschluss-Protokoll.
"""

import sys
from pathlib import Path
from typing import TypedDict

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from lernakademie.mock_llm import get_chat_model, is_offline_mode

# Simulierte Aktionen (in echt: E-Mail-API, Ticketsystem, ...)


def notiz_anlegen(text: str) -> str:
    return f"Notiz '{text}' angelegt."


def bericht_erstellen(text: str) -> str:
    return f"Bericht '{text}' erstellt."


def e_mail_versenden(text: str) -> str:
    return f"E-Mail an das Team versendet: '{text}'."


AKTIONEN = {
    "notiz": notiz_anlegen,
    "bericht": bericht_erstellen,
    "e-mail": e_mail_versenden,
}


class WorkflowZustand(TypedDict):
    auftrag: str
    schritte: list[dict]     # [{name, typ, risiko, status, versuche}]
    protokoll: list[str]
    fehler: str


def planen(state: WorkflowZustand) -> dict:
    """M1: Auftrag -> Schrittliste (offline per Schluesselwoertern)."""
    text = state["auftrag"].lower()
    schritte = []
    if "notiz" in text:
        schritte.append({"name": "Notiz anlegen", "typ": "notiz",
                         "risiko": "info", "status": "offen", "versuche": 0})
    if "bericht" in text:
        schritte.append({"name": "Bericht erstellen", "typ": "bericht",
                         "risiko": "info", "status": "offen", "versuche": 0})
    if "e-mail" in text or "mail" in text:
        schritte.append({"name": "E-Mail versenden", "typ": "e-mail",
                         "risiko": "sensibel", "status": "offen", "versuche": 0})
    if not schritte:  # immer mindestens ein Schritt
        schritte.append({"name": "Notiz anlegen", "typ": "notiz",
                         "risiko": "info", "status": "offen", "versuche": 0})
    print("Plan:")
    for s in schritte:
        print(f"  - {s['name']} (Risiko: {s['risiko']})")
    return {"schritte": schritte}


def _naechster_offener_schritt(schritte: list[dict]):
    for index, schritt in enumerate(schritte):
        if schritt["status"] in ("offen", "wiederholung"):
            return index
    return None


def ausfuehren(state: WorkflowZustand) -> dict:
    """M2+M3+M4: naechsten Schritt ausfuehren – mit Freigabe & Wiederholung."""
    schritte = [dict(s) for s in state["schritte"]]
    protokoll = list(state["protokoll"])
    index = _naechster_offener_schritt(schritte)
    if index is None:
        return {}
    schritt = schritte[index]

    if schritt["risiko"] == "sensibel" and schritt["versuche"] == 0:
        freigabe = interrupt({
            "frage": f"Freigabe noetig: '{schritt['name']}' ausfuehren?",
            "schritt": schritt["name"],
        })
        if not freigabe:
            schritt["status"] = "abgelehnt"
            protokoll.append(f"{schritt['name']}: abgelehnt (keine Freigabe)")
            return {"schritte": schritte, "protokoll": protokoll}

    if schritt["typ"] == "fehler_test":
        # simulierter Dauerfehler fuer M4
        erfolgreich, meldung = False, "simulierter Ausfall"
    else:
        aktion = AKTIONEN.get(schritt["typ"], notiz_anlegen)
        erfolgreich, meldung = True, aktion(state["auftrag"])

    if erfolgreich:
        schritt["status"] = "erledigt"
        protokoll.append(f"{schritt['name']}: erledigt ({meldung})")
    elif schritt["versuche"] < 1:
        # M4: genau EINE Wiederholung erlauben
        schritt["versuche"] += 1
        schritt["status"] = "wiederholung"
        protokoll.append(f"{schritt['name']}: Fehler -> Wiederholung")
    else:
        schritt["status"] = "fehlgeschlagen"
        protokoll.append(f"{schritt['name']}: fehlgeschlagen (2 Versuche)")

    return {"schritte": schritte, "protokoll": protokoll}


def weiche(state: WorkflowZustand) -> str:
    if _naechster_offener_schritt(state["schritte"]) is None:
        return "fertig"
    return "weiter"


def baue_graph():
    graph = StateGraph(WorkflowZustand)
    graph.add_node("planen", planen)
    graph.add_node("ausfuehren", ausfuehren)
    graph.add_edge(START, "planen")
    graph.add_edge("planen", "ausfuehren")
    graph.add_conditional_edges("ausfuehren", weiche,
                                {"weiter": "ausfuehren", "fertig": END})
    return graph.compile(checkpointer=MemorySaver())


def main() -> None:
    if is_offline_mode():
        print("OFFLINE-Modus: Planung per Schluesselwoertern, "
              "Aktionen simuliert.\n")

    app = baue_graph()
    config = {"configurable": {"thread_id": "workflow-1"}}
    ergebnis = app.invoke({
        "auftrag": "Erstelle den Wochenbericht, lege eine Notiz an und "
                   "sende die E-Mail an das Team.",
        "schritte": [], "protokoll": [], "fehler": "",
    }, config)

    # Freigabe fuer den sensiblen E-Mail-Schritt abwarten:
    while ergebnis.get("__interrupt__"):
        frage = ergebnis["__interrupt__"][0].value
        print("\nINTERRUPT:", frage["frage"])
        ergebnis = app.invoke(Command(resume=True), config)

    print("\n---- Abschluss-Protokoll ----")
    for eintrag in ergebnis["protokoll"]:
        print(f"  - {eintrag}")
    print("\nSchrittstatus:")
    for schritt in ergebnis["schritte"]:
        print(f"  - {schritt['name']}: {schritt['status']}")


if __name__ == "__main__":
    main()
