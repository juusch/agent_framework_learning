"""Aufgabe 14.1 – Loesung: Graph-Aware Agent mit Routing.

Der Agent klassifiziert die Frage (vektor | graph | hybrid) und ruft
NUR die noetigen Retrieval-Tools auf. Quelltransparenz bleibt.
"""

import sys
from pathlib import Path
from typing import TypedDict

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import END, START, StateGraph

from lernakademie.graph_store import GraphStore
from lernakademie.offline_embeddings import get_embeddings, hat_bezug

DATA = Path(__file__).resolve().parents[2] / "data" / "firmenprofil.md"


class AgentZustand(TypedDict):
    frage: str
    route: str
    dokumente: list[dict]
    graph_fakten: list[str]
    antwort: str


def baue_vektor_index(k: int = 2):
    text = DATA.read_text(encoding="utf-8")
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
    chunks = splitter.create_documents([text], [{"source": "firmenprofil.md"}])
    db = Chroma(collection_name="graph_agent_vektor",
                embedding_function=get_embeddings())
    db.add_documents(chunks)
    return db.as_retriever(search_kwargs={"k": k})


def baue_wissens_graph() -> GraphStore:
    store = GraphStore()
    anna = store.add_node(["Person"], name="Anna")
    ben = store.add_node(["Person"], name="Ben")
    engineering = store.add_node(["Department"], name="Engineering")
    analytics = store.add_node(["Department"], name="Data & Analytics")
    projekt = store.add_node(["Project"], name="AI Assistant")
    store.add_relationship(anna, engineering, "BELONGS_TO")
    store.add_relationship(ben, analytics, "BELONGS_TO")
    store.add_relationship(engineering, projekt, "WORKS_ON")
    store.add_relationship(analytics, projekt, "PROVIDES_DATA_FOR")
    store.add_relationship(anna, projekt, "CONTRIBUTES_TO")
    return store


def klassifiziere(frage: str) -> str:
    """Regel-Logik (offline). Mit Key: LLM mit denselben drei Optionen.

    Regeln (bewusst grob granular – Muster vor Perfektion):
    - Verbindungs-Fragen: 'haengt zusammen', 'wer ... dran', 'pfad',
      'beziehung' -> graph
    - Text-/Inhalts-Fragen: 'was steht', 'steht drin', 'zusammenfassen' -> vektor
    - Gesamt-Fragen: 'gesamt', 'alles', 'vergleich', 'sowohl' -> hybrid
    """
    klein = frage.lower()
    verbindungs_woerter = ("haengt", "zusammen?", "wer", "beziehung", "pfad", "verbind")
    if any(wort in klein for wort in verbindungs_woerter):
        return "graph"
    if any(wort in klein for wort in ("gesamt", "alles", "vergleich", "sowohl")):
        return "hybrid"
    return "vektor"


def klassifizieren_node(state: AgentZustand) -> dict:
    route = klassifiziere(state["frage"])
    print(f"  Klassifikation: '{state['frage'][:40]}' -> {route}")
    return {"route": route}


def baue_vektor_node(retriever):
    def node(state: AgentZustand) -> dict:
        if not hat_bezug(state["frage"]):
            return {"dokumente": []}
        treffer = retriever.invoke(state["frage"])[:2]
        dokumente = [{"quelle": Path(t.metadata["source"]).name,
                      "textstelle": t.page_content.strip().replace("\n", " ")[:120]}
                     for t in treffer]
        return {"dokumente": dokumente}
    return node


def baue_graph_node(store: GraphStore):
    def node(state: AgentZustand) -> dict:
        klein = state["frage"].lower()
        fakten = []
        projekt = store.find_node("Project", name="AI Assistant")
        if projekt:
            for kante in store.relationships():
                if kante.to_id == projekt.id:
                    quelle = store.nodes()[kante.from_id]
                    fakten.append(
                        f"{quelle.properties['name']} --{kante.typ}--> AI Assistant")
        if "ben" in klein:
            ben = store.find_node("Person", name="Ben")
            for kante, abteilung in store.neighbors(ben.id, "BELONGS_TO"):
                for kante2, ziel in store.neighbors(abteilung.id):
                    fakten.append(f"Ben --BELONGS_TO--> "
                                  f"{abteilung.properties['name']} "
                                  f"--{kante2.typ}--> {ziel.properties['name']}")
        return {"graph_fakten": list(dict.fromkeys(fakten))}
    return node


def antworten(state: AgentZustand) -> dict:
    teile = [f"Route: {state['route']}"]
    if state["dokumente"]:
        teile.append(f"Dokumente: {len(state['dokumente'])} Fundstelle(n)")
    if state["graph_fakten"]:
        teile.append(f"Graph: {len(state['graph_fakten'])} Fakt(en)")
    if not state["dokumente"] and not state["graph_fakten"]:
        teile.append("keine Quelle hatte etwas")
    return {"antwort": " | ".join(teile)}


def baue_agent(store: GraphStore, retriever):
    graph = StateGraph(AgentZustand)
    graph.add_node("klassifizieren", klassifizieren_node)
    graph.add_node("vektor_suche", baue_vektor_node(retriever))
    graph.add_node("graph_abfrage", baue_graph_node(store))
    graph.add_node("antworten", antworten)

    graph.add_edge(START, "klassifizieren")
    graph.add_conditional_edges("klassifizieren", lambda s: s["route"], {
        "vektor": "vektor_suche",
        "graph": "graph_abfrage",
        "hybrid": "vektor_suche",
    })
    # Hybrid: nach der Vektor-Suche geht es ZUSAETZLICH zum Graph
    graph.add_conditional_edges("vektor_suche", lambda s: (
        "graph_abfrage" if s["route"] == "hybrid" else "antworten"), {
        "graph_abfrage": "graph_abfrage", "antworten": "antworten"})
    graph.add_edge("graph_abfrage", "antworten")
    graph.add_edge("antworten", END)
    return graph.compile()


def main() -> None:
    store = baue_wissens_graph()
    retriever = baue_vektor_index()
    agent = baue_agent(store, retriever)

    fragen = [
        ("vektor", "Was steht ueber die Abteilung Engineering?"),
        ("graph", "Wer haengt am AI Assistant dran?"),
        ("graph", "Wie haengt Ben mit dem AI Assistant zusammen?"),
        ("hybrid", "Was wissen wir gesamt ueber das Projekt?"),
    ]
    for erwartet, frage in fragen:
        ergebnis = agent.invoke({"frage": frage, "route": "",
                                 "dokumente": [], "graph_fakten": [], "antwort": ""})
        print(f"Frage: {frage}")
        print(f"  {ergebnis['antwort']}")
        for fakt in ergebnis["graph_fakten"][:2]:
            print(f"    Graph-Fakt: {fakt}")
        print()


if __name__ == "__main__":
    main()
