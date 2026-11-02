"""Projekt C – Loesung: Multi-Agent-Business-Assistent.

Supervisor (Stufe 7.3) koordiniert drei Fach-Agenten:
Analyse -> Recherche -> Aufbereitung -> Freigabe (interrupt) -> FINISH.
"""

import sys
from pathlib import Path
from typing import TypedDict

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from lernakademie.mock_llm import get_chat_model, is_offline_mode
from lernakademie.offline_embeddings import get_embeddings

DATA = Path(__file__).resolve().parents[2] / "04-rag-and-knowledge" / "data"


class BusinessZustand(TypedDict):
    anfrage: str
    kategorie: str
    befund: str
    ergebnis: str
    protokoll: list[str]
    runden: int
    max_runden: int


def _retriever():
    from langchain_community.document_loaders import TextLoader

    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    chunks = []
    for datei in sorted(DATA.glob("*.md")):
        chunks.extend(splitter.split_documents(
            TextLoader(str(datei), encoding="utf-8").load()))
    db = Chroma(collection_name="business", embedding_function=get_embeddings())
    db.add_documents(chunks)
    return db.as_retriever(search_kwargs={"k": 2})


def analyse_agent(state: BusinessZustand) -> dict:
    """M1a: klassifiziert die Anfrage."""
    text = state["anfrage"].lower()
    if "urlaub" in text or "gehalt" in text:
        kategorie = "personal"
    elif "vpn" in text or "passwort" in text or "laptop" in text:
        kategorie = "it"
    else:
        kategorie = "allgemein"
    return {"kategorie": kategorie,
            "protokoll": state["protokoll"] + [f"analyse_agent: Kategorie {kategorie}"]}


def recherche_agent(state: BusinessZustand) -> dict:
    """M1b: schlaegt im Handbuch nach (offline: echtes Retrieval)."""
    treffer = _retriever().invoke(state["anfrage"])
    texte = [d.page_content.strip().replace("\n", " ")[:120] for d in treffer]
    befund = " | ".join(texte) if texte else "keine Treffer"
    return {"befund": befund,
            "protokoll": state["protokoll"] + ["recherche_agent: Befund erhoben"]}


def aufbereitungs_agent(state: BusinessZustand) -> dict:
    """M1c+M3: formatiert das Ergebnis – Freigabe VOR dem 'Versenden'."""
    ergebnis = (f"Sehr geehrte Kundin, sehr geehrter Kunde,\n\n"
                f"zu Ihrer Anfrage ({state['kategorie']}): {state['befund'][:200]}\n\n"
                f"Mit freundlichen Gruessen, Ihr Service-Team")

    freigabe = interrupt({
        "frage": "Ergebnis an den Kunden versenden?",
        "ergebnis": ergebnis[:200],
    })
    if not freigabe:
        return {"ergebnis": "(abgelehnt)",
                "protokoll": state["protokoll"] + ["aufbereitung: abgelehnt"]}
    return {"ergebnis": ergebnis,
            "protokoll": state["protokoll"] + ["aufbereitung: versendet"]}


def supervisor(state: BusinessZustand) -> dict:
    """M2: Delegations-Reihenfolge mit Loop-Schutz."""
    if not state["kategorie"]:
        schritt = "analyse_agent"
    elif not state["befund"]:
        schritt = "recherche_agent"
    elif not state["ergebnis"]:
        schritt = "aufbereitungs_agent"
    else:
        schritt = "FINISH"

    if state["runden"] >= state["max_runden"]:
        schritt = "FINISH"

    print(f"  Supervisor -> {schritt} (Runde {state['runden'] + 1})")
    return {"runden": state["runden"] + 1,
            "protokoll": state["protokoll"] + [f"supervisor: {schritt}"]}


def weiche(state: BusinessZustand) -> str:
    return ("FINISH" if state["runden"] > state["max_runden"]
            or (state["ergebnis"] and "abgelehnt" not in state["ergebnis"])
            else "weiter")


def baue_graph():
    graph = StateGraph(BusinessZustand)
    graph.add_node("supervisor", supervisor)
    graph.add_node("analyse_agent", analyse_agent)
    graph.add_node("recherche_agent", recherche_agent)
    graph.add_node("aufbereitungs_agent", aufbereitungs_agent)

    graph.add_edge(START, "supervisor")
    graph.add_edge("analyse_agent", "supervisor")
    graph.add_edge("recherche_agent", "supervisor")
    # Aufbereitung endet IMMER im END (Freigabe entscheidet im Tool):
    graph.add_edge("aufbereitungs_agent", END)

    def sup_weiche(state: BusinessZustand) -> str:
        if state["runden"] > state["max_runden"]:
            return END
        if not state["kategorie"]:
            return "analyse_agent"
        if not state["befund"]:
            return "recherche_agent"
        if not state["ergebnis"]:
            return "aufbereitungs_agent"
        return END

    graph.add_conditional_edges("supervisor", sup_weiche, {
        "analyse_agent": "analyse_agent",
        "recherche_agent": "recherche_agent",
        "aufbereitungs_agent": "aufbereitungs_agent",
        END: END,
    })
    return graph.compile(checkpointer=MemorySaver())


def main() -> None:
    if is_offline_mode():
        print("OFFLINE-Modus: Delegation per Regel-Logik, Retrieval echt.\n")

    app = baue_graph()
    config = {"configurable": {"thread_id": "business-1"}}
    ergebnis = app.invoke({
        "anfrage": "Wie viele Urlaubstage habe ich?",
        "kategorie": "", "befund": "", "ergebnis": "",
        "protokoll": [], "runden": 0, "max_runden": 6,
    }, config)

    interrupts = ergebnis.get("__interrupt__")
    if interrupts:
        print("\nINTERRUPT:", interrupts[0].value["frage"])
        ergebnis = app.invoke(Command(resume=True), config)

    print("\n---- Protokoll ----")
    for eintrag in ergebnis["protokoll"]:
        print(f"  - {eintrag}")
    print("\n---- Ergebnis ----")
    print(ergebnis["ergebnis"][:400])


if __name__ == "__main__":
    main()
