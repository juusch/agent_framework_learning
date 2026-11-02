"""Aufgabe 13.1 – Loesung: Vektor- vs. Graph-Retrieval im Vergleich.

Vier Fragen gehen an beide Systeme; die Auswertung zeigt,
welches System bei welchem Fragetyp gewinnt.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from lernakademie.graph_store import GraphStore
from lernakademie.offline_embeddings import get_embeddings, hat_bezug

DATA = Path(__file__).resolve().parents[2] / "data" / "firmenprofil.md"


def baue_vektor_index(k: int = 2):
    """Vektor-Index ueber das Firmenprofil (Stufe-4-Muster)."""
    text = DATA.read_text(encoding="utf-8")
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
    chunks = splitter.create_documents([text], [{"source": "firmenprofil.md"}])
    db = Chroma(collection_name="graphrag_vektor", embedding_function=get_embeddings())
    db.add_documents(chunks)
    return db.as_retriever(search_kwargs={"k": k})


def baue_wissens_graph() -> GraphStore:
    """Graph mit dem Firmenprofil-Wissen (manuell modelliert)."""
    store = GraphStore()
    anna = store.add_node(["Person"], name="Anna", rolle="Entwicklerin")
    ben = store.add_node(["Person"], name="Ben", rolle="Analyst")
    clara = store.add_node(["Person"], name="Clara", rolle="Abteilungsleitung")
    engineering = store.add_node(["Department"], name="Engineering")
    data_analytics = store.add_node(["Department"], name="Data & Analytics")
    projekt = store.add_node(["Project"], name="AI Assistant")

    store.add_relationship(clara, engineering, "LEADS")
    store.add_relationship(anna, engineering, "BELONGS_TO")
    store.add_relationship(ben, data_analytics, "BELONGS_TO")
    store.add_relationship(engineering, projekt, "WORKS_ON")
    store.add_relationship(data_analytics, projekt, "PROVIDES_DATA_FOR")
    store.add_relationship(anna, projekt, "CONTRIBUTES_TO")
    return store


def vektor_antwort(retriever, frage: str) -> str:
    treffer = retriever.invoke(frage)
    if not treffer:
        return "(nichts gefunden)"
    stelle = treffer[0].page_content.strip().replace("\n", " ")
    return f"[{treffer[0].metadata['source']}] {stelle[:130]}..."


def graph_antwort(store: GraphStore, frage: str) -> str:
    """Einfache strukturelle Traversierung fuer die Vergleichsfragen."""
    klein = frage.lower()
    ergebnisse = []

    # 1) Ben + Projekt: Emergenz-Pfad (steht so NICHT im Text!)
    if "ben" in klein and "ai assistant" in klein:
        ben = store.find_node("Person", name="Ben")
        for kante, abteilung in store.neighbors(ben.id, "BELONGS_TO"):
            for kante2, ziel in store.neighbors(abteilung.id):
                if ziel.properties.get("name") == "AI Assistant":
                    ergebnisse.append(
                        f"Ben --BELONGS_TO--> {abteilung.properties['name']} "
                        f"--{kante2.typ}--> AI Assistant")
        return "; ".join(ergebnisse) or "(kein Pfad)"

    # 2) Projekt-Uebersicht: alle direkten Vorgaenger-Kanten
    if "ai assistant" in klein and ("wer" in klein or "haengt" in klein
                                    or "traegt" in klein or "beitraegt" in klein):
        projekt = store.find_node("Project", name="AI Assistant")
        for kante in store.relationships():
            if kante.to_id == projekt.id:
                quell_node = store.nodes()[kante.from_id]
                ergebnisse.append(
                    f"{quell_node.properties['name']} --{kante.typ}--> AI Assistant")
        return "; ".join(ergebnisse) or "(nichts gefunden)"

    # 3) Abteilungs-Uebersicht
    if "abteilung" in klein:
        for node in store.nodes("Department"):
            ergebnisse.append(f"{node.properties['name']} (:Department)")
        return "; ".join(ergebnisse) or "(nichts gefunden)"

    return "(Frage nicht graph-foermig beantwortbar)"


FRAGEN = [
    ("Was steht ueber die Abteilung Engineering?", "Doku (Textinhalt)"),
    ("Wer haengt am AI Assistant dran?", "Graph (Verbindungen)"),
    ("Wie haengt Ben mit AI Assistant zusammen?", "Graph (Pfad/Emergenz)"),
    ("Was weiss man gesamt ueber das Projekt?", "Beide"),
]


def main() -> None:
    retriever = baue_vektor_index()
    store = baue_wissens_graph()
    print("Vergleich: dieselbe Frage an beide Systeme\n")
    print(f"{'Frage':44s} | {'Gewinner'}")
    print("-" * 80)
    for frage, erwartet in FRAGEN:
        vektor = vektor_antwort(retriever, frage)
        graph = graph_antwort(store, frage)
        print(f"FRAGE: {frage}\n  Vektor: {vektor[:110]}")
        print(f"  Graph : {graph[:110]}\n  Erwartung: {erwartet}\n")


if __name__ == "__main__":
    main()
