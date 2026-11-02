"""Aufgabe 13.2 – Loesung: Hybrid-Retrieval (Vektor + Graph).

Kernidee: BEIDE Quellen befragen, Ergebnisse sauber getrennt nach
Herkunft ausgeben (Quelltransparenz wie in Stufe 4.4).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from lernakademie.graph_store import GraphStore
from lernakademie.offline_embeddings import get_embeddings, hat_bezug

DATA = Path(__file__).resolve().parents[1] / "data" / "firmenprofil.md"


def baue_vektor_index(k: int = 2):
    text = DATA.read_text(encoding="utf-8")
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
    chunks = splitter.create_documents([text], [{"source": "firmenprofil.md"}])
    db = Chroma(collection_name="hybrid_vektor", embedding_function=get_embeddings())
    db.add_documents(chunks)
    return db.as_retriever(search_kwargs={"k": k})


def baue_wissens_graph() -> GraphStore:
    store = GraphStore()
    anna = store.add_node(["Person"], name="Anna", rolle="Entwicklerin")
    ben = store.add_node(["Person"], name="Ben", rolle="Analyst")
    engineering = store.add_node(["Department"], name="Engineering")
    analytics = store.add_node(["Department"], name="Data & Analytics")
    projekt = store.add_node(["Project"], name="AI Assistant")

    store.add_relationship(anna, engineering, "BELONGS_TO")
    store.add_relationship(ben, analytics, "BELONGS_TO")
    store.add_relationship(engineering, projekt, "WORKS_ON")
    store.add_relationship(analytics, projekt, "PROVIDES_DATA_FOR")
    store.add_relationship(anna, projekt, "CONTRIBUTES_TO")
    return store


def vektor_suche(retriever, frage: str) -> list[dict]:
    """Liefert [{quelle, textstelle}] – nur relevante Treffer.

    Offline-Ehrlichkeit: Ohne Schluesselwort-Bezug wuerde die Suche
    beliebige Chunks liefern – dann lieber 'kein Treffer' (Stufe-4-Muster).
    """
    if not hat_bezug(frage):
        return []
    treffer = retriever.invoke(frage)
    ergebnisse = []
    for dokument in treffer:
        textstelle = dokument.page_content.strip().replace("\n", " ")
        if len(textstelle) > 30:  # Minimalrelevanz
            ergebnisse.append({
                "quelle": Path(dokument.metadata["source"]).name,
                "textstelle": textstelle[:150] + "...",
            })
    return ergebnisse[:2]


def graph_suche(store: GraphStore, frage: str) -> list[str]:
    """Liefert Traversierungs-Fakten als Liste von 'A --REL--> B'-Strings."""
    klein = frage.lower()
    fakten = []

    projekt = store.find_node("Project", name="AI Assistant")
    for kante in store.relationships():
        ziel = store.nodes()[kante.to_id]
        quelle = store.nodes()[kante.from_id]
        if "ai assistant" in klein or "projekt" in klein:
            if ziel.id == projekt.id:
                fakten.append(
                    f"{quelle.properties['name']} --{kante.typ}--> "
                    f"{ziel.properties['name']}")
        if "ben" in klein and quelle.properties.get("name") == "Ben":
            fakten.append(
                f"Ben --{kante.typ}--> {ziel.properties['name']}")

    # Duplikate vermeiden
    return list(dict.fromkeys(fakten))


def hybrid_suche(store: GraphStore, retriever, frage: str) -> dict:
    """Die Hybrid-Pipeline: beide Quellen, getrennt ausgewiesen."""
    dokumente = vektor_suche(retriever, frage)
    graph_fakten = graph_suche(store, frage)

    if not dokumente and not graph_fakten:
        return {"antwort": "Dazu habe ich in Dokumenten UND Graph nichts gefunden.",
                "dokumente": [], "graph": []}

    return {
        "antwort": f"Hybrid-Ergebnis zu '{frage}': "
                   f"{len(dokumente)} Dokument-Fundstelle(n), "
                   f"{len(graph_fakten)} Graph-Fakt(en).",
        "dokumente": dokumente,
        "graph": graph_fakten,
    }


def main() -> None:
    retriever = baue_vektor_index()
    store = baue_wissens_graph()

    fragen = [
        ("dokumentlastig", "Was steht ueber die Abteilung Engineering?"),
        ("graphlastig", "Wer traegt zum AI Assistant bei?"),
        ("hybrid", "Was wissen wir gesamt ueber das Projekt AI Assistant?"),
        ("leer", "Gibt es Informationen zu Weihnachtsgeld?"),
    ]
    for typ, frage in fragen:
        ergebnis = hybrid_suche(store, retriever, frage)
        print(f"[{typ}] {frage}")
        print(f"  -> {ergebnis['antwort']}")
        for fund in ergebnis["dokumente"]:
            print(f"  Doku : ({fund['quelle']}) {fund['textstelle'][:80]}")
        for fakt in ergebnis["graph"]:
            print(f"  Graph: {fakt}")
        if not ergebnis["dokumente"] and not ergebnis["graph"]:
            print("  (keine Quelle hatte etwas)")
        print()


if __name__ == "__main__":
    main()
