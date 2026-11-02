"""Aufgabe 6.4 – Referenzloesung: Gedaechtnis (Checkpointer) + Freigabe (interrupt).

Wir bauen den Agenten-Loop hier bewusst SELBST (model -> tools -> model),
statt ihn hinter create_agent zu verstecken. So siehst du:
- der Agent ist ein LangGraph wie in Stufe 5, nur mit LLM-Node
- interrupt() pausiert mitten im Tool; Command(resume=True) macht weiter
- der Checkpointer haelt den State pro thread_id am Leben
"""

import sys
from pathlib import Path
from typing import Annotated, TypedDict

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.types import Command, interrupt

from lernakademie.llm_client import get_chat_model, is_offline_mode

ANGELEGTE_NOTIZEN: list[str] = []  # simulierter "Notizspeicher"


@tool
def notiz_anlegen(text: str) -> str:
    """Legt eine normale Notiz an."""
    ANGELEGTE_NOTIZEN.append(text)
    return f"Notiz angelegt ({len(text)} Zeichen)."


@tool
def geheime_notiz(text: str) -> str:
    """Legt eine geheime Notiz an – erfordert vorher die Freigabe eines Menschen."""
    # interrupt() pausiert den Lauf HIER und wartet auf Command(resume=...)
    freigabe = interrupt({
        "frage": "Soll diese geheime Notiz wirklich angelegt werden?",
        "text": text,
    })
    if freigabe:
        ANGELEGTE_NOTIZEN.append(f"[GEHEIM] {text}")
        return "Geheime Notiz angelegt – Freigabe erteilt."
    return "Aktion abgebrochen – keine Freigabe."


class AgentZustand(TypedDict):
    messages: Annotated[list, add_messages]  # Liste wächst pro Zug (Reduzierer)


def baue_agent():
    """Mini-Agent: model-Node entscheidet, ToolNode fuehrt aus, Loop bis fertig."""
    modell = get_chat_model(temperature=0.0).bind_tools([notiz_anlegen, geheime_notiz])
    tools = ToolNode([notiz_anlegen, geheime_notiz])

    def model_node(state: AgentZustand) -> dict:
        return {"messages": [modell.invoke(state["messages"])]}

    def weiche(state: AgentZustand) -> str:
        letzte = state["messages"][-1]
        return "tools" if getattr(letzte, "tool_calls", None) else END

    graph = StateGraph(AgentZustand)
    graph.add_node("model", model_node)
    graph.add_node("tools", tools)
    graph.add_edge(START, "model")
    graph.add_conditional_edges("model", weiche, {"tools": "tools", END: END})
    graph.add_edge("tools", "model")  # zurueck zum Modell -> Loop!
    return graph.compile(checkpointer=MemorySaver())


def frage(agent, thread_id: str, text: str):
    """Ein Gespraechszug im Thread `thread_id`."""
    config = {"configurable": {"thread_id": thread_id}}
    ergebnis = agent.invoke(
        {"messages": [HumanMessage(content=text)]}, config)
    return ergebnis["messages"][-1].content


def main() -> None:
    if is_offline_mode():
        print("OFFLINE-Modus: Formulierungen simuliert – Gedaechtnis, "
              "Interrupt und Fortsetzung sind echte LangGraph-Mechanik.\n")

    agent = baue_agent()

    # ---- Dialog 1: Gedaechtnis (gleiche thread_id!) ----------------------
    print("Dialog 1 (thread 'gespraech-1')")
    frage(agent, "gespraech-1", "Hallo! Ich heisse Alex und arbeite im Vertrieb.")
    frage(agent, "gespraech-1", "Wie heisse ich noch mal?")
    zustand1 = agent.get_state({"configurable": {"thread_id": "gespraech-1"}})
    print(f"  Nachrichten im Thread: {len(zustand1.values['messages'])}"
          "  <- Gedaechtnis ist gefuellt")

    # ---- Kontroll-Dialog: ANDERE thread_id -> kein Gedaechtnis ------------
    print("\nKontrolle (thread 'anderes-gespraech')")
    frage(agent, "anderes-gespraech", "Wie heisse ich noch mal?")
    zustand2 = agent.get_state({"configurable": {"thread_id": "anderes-gespraech"}})
    print(f"  Nachrichten im Thread: {len(zustand2.values['messages'])}"
          "  <- frisch und leer")

    # ---- Dialog 2: Freigabe per interrupt --------------------------------
    print("\nDialog 2: geheime Notiz (thread 'freigabe')")
    config = {"configurable": {"thread_id": "freigabe"}}
    ergebnis = agent.invoke(
        {"messages": [HumanMessage(content="Lege bitte die geheime Notiz "
                                            "'Gehaltsliste 2025' an.")]},
        config,
    )
    interrupts = ergebnis.get("__interrupt__")
    if interrupts:
        daten = interrupts[0].value
        print("  INTERRUPT – Freigabe noetig:", daten["frage"])
        print("  Betreffender Text:", daten["text"])

        fortsetzung = agent.invoke(Command(resume=True), config)
        print("  Nach Freigabe:", fortsetzung["messages"][-1].content[:120])

    print("\nAngelegte Notizen:", ANGELEGTE_NOTIZEN)


if __name__ == "__main__":
    main()
