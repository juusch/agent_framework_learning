"""Projekt B – Loesung: KI-Recherche-Assistent.

Graph: planen -> 3x parallel recherchieren -> bewerten -> Bericht ->
Freigabe (interrupt) -> fertig.
Offline: Teilfragen per Regel-Logik, Recherche ueber echtes Handbuch-Retrieval.
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


class RechercheZustand(TypedDict):
    hauptfrage: str
    teilfragen: list[str]
    ergebnis_1: str
    ergebnis_2: str
    ergebnis_3: str
    qualitaet_ok: bool
    bericht: str


def _retriever():
    from langchain_community.document_loaders import TextLoader

    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    chunks = []
    for datei in sorted(DATA.glob("*.md")):
        chunks.extend(splitter.split_documents(
            TextLoader(str(datei), encoding="utf-8").load()))
    db = Chroma(collection_name="recherche", embedding_function=get_embeddings())
    db.add_documents(chunks)
    return db.as_retriever(search_kwargs={"k": 2})


def planen(state: RechercheZustand) -> dict:
    """M1: Hauptfrage in drei Teilfragen zerlegen."""
    thema = state["hauptfrage"].strip().rstrip("?")
    if is_offline_mode():
        teilfragen = [
            f"Was ist {thema}?",
            f"Wie funktioniert {thema}?",
            f"Welche Regeln gelten fuer {thema}?",
        ]
    else:
        modell = get_chat_model(temperature=0.2)
        antwort = modell.invoke(
            [("system", "Erzeuge genau 3 konkrete Teilfragen, eine pro Zeile."),
             ("human", f"Hauptfrage: {state['hauptfrage']}")]
        )
        teilfragen = [z.strip() for z in antwort.content.splitlines() if z.strip()][:3]
    print("Teilfragen:")
    for frage in teilfragen:
        print(f"  - {frage}")
    return {"teilfragen": teilfragen}


def _recherchiere(index: int, retriever=None) -> str:
    """Fabrik fuer einen Recherche-Node (offline: echtes Handbuch-Retrieval).

    WICHTIG: Der Index wird EINMAL gebaut und als Objekt geteilt –
    parallele Clients wuerden sich gegenseitig in die Quere kommen.
    """
    retriever = retriever or _retriever()
    def node(state: RechercheZustand) -> dict:
        frage = state["teilfragen"][index]
        if is_offline_mode():
            treffer = retriever.invoke(frage)
            texte = [d.page_content.strip().replace("\n", " ")[:120] for d in treffer]
            ergebnis = f"Zu '{frage}': " + (" | ".join(texte) if texte else "keine Treffer")
        else:
            modell = get_chat_model(temperature=0.0)
            ergebnis = modell.invoke(
                [("system", "Beantworte kurz in 2-3 Saetzen."),
                 ("human", frage)]).content
        return {f"ergebnis_{index + 1}": ergebnis}
    return node


def bewerten(state: RechercheZustand) -> dict:
    """M3: Qualitaetsgate – sind alle drei Ergebnisse substanziell?"""
    ergebnisse = [state["ergebnis_1"], state["ergebnis_2"], state["ergebnis_3"]]
    ok = all(len(e) > 20 and "keine Treffer" not in e for e in ergebnisse)
    print(f"Qualitaetsgate: {'ok' if ok else 'lueckenhaft'}")
    return {"qualitaet_ok": ok}


def bericht_schreiben(state: RechercheZustand) -> dict:
    """M4: Bericht – mit Freigabe-Pflicht VOR der 'Veroeffentlichung'."""
    inhalte = (f"1) {state['ergebnis_1']}\n"
               f"2) {state['ergebnis_2']}\n"
               f"3) {state['ergebnis_3']}")
    if is_offline_mode():
        bericht = (f"Forschungsbericht zu '{state['hauptfrage']}':\n{inhalte}\n"
                   f"Qualitaet: {'gut' if state['qualitaet_ok'] else 'lueckenhaft'}.")
    else:
        modell = get_chat_model(temperature=0.2)
        bericht = modell.invoke(
            [("system", "Schreibe aus den Befunden einen strukturierten Bericht."),
             ("human", inhalte)]).content

    freigabe = interrupt({
        "frage": "Bericht fertig. Veroeffentlichen?",
        "bericht": bericht[:300],
    })
    if not freigabe:
        return {"bericht": "(Veroeffentlichung abgelehnt)"}
    return {"bericht": bericht}


def baue_graph(retriever=None):
    retriever = retriever or _retriever()  # Index EINMAL bauen und teilen
    graph = StateGraph(RechercheZustand)
    graph.add_node("planen", planen)
    graph.add_node("recherche_1", _recherchiere(0, retriever))
    graph.add_node("recherche_2", _recherchiere(1, retriever))
    graph.add_node("recherche_3", _recherchiere(2, retriever))
    graph.add_node("bewerten", bewerten)
    graph.add_node("bericht", bericht_schreiben)

    graph.add_edge(START, "planen")
    # M2: parallel!
    graph.add_edge("planen", "recherche_1")
    graph.add_edge("planen", "recherche_2")
    graph.add_edge("planen", "recherche_3")
    for node in ("recherche_1", "recherche_2", "recherche_3"):
        graph.add_edge(node, "bewerten")
    graph.add_edge("bewerten", "bericht")
    graph.add_edge("bericht", END)
    return graph.compile(checkpointer=MemorySaver())


def main() -> None:
    if is_offline_mode():
        print("OFFLINE-Modus: Planung per Regel, Recherche ueber echtes "
              "Handbuch-Retrieval, Bericht simuliert.\n")

    retriever = _retriever()  # einmal pro Programmstart
    app = baue_graph(retriever)
    config = {"configurable": {"thread_id": "recherche-1"}}
    ergebnis = app.invoke({"hauptfrage": "Urlaub im Unternehmen"}, config)

    interrupts = ergebnis.get("__interrupt__")
    if interrupts:
        print("\nINTERRUPT:", interrupts[0].value["frage"])
        fortsetzung = app.invoke(Command(resume=True), config)
        ergebnis = fortsetzung

    print("\n---- Finale Bericht ----")
    print(ergebnis["bericht"][:600])


if __name__ == "__main__":
    main()
