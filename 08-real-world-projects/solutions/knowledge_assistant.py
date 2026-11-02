"""Projekt A – Loesung: Persoenlicher Wissens-Assistent (interaktives RAG).

Meilensteine der Aufgabe sind hier als klar getrennte Funktionen sichtbar:
M1 baue_index / M2 beantworte / M3 Dialogschleife / M4 Fehlerrobustheit.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter

from lernakademie.mock_llm import get_chat_model, is_offline_mode
from lernakademie.offline_embeddings import get_embeddings, hat_bezug

DATA = Path(__file__).resolve().parents[2] / "04-rag-and-knowledge" / "data"

PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "Du beantwortest Fragen NUR auf Basis des Kontexts. Ohne passenden "
     "Kontext: 'Das steht in den Dokumenten leider nicht.' "
     "Verweise auf die relevante Stelle."),
    ("human", "Kontext:\n{context}\n\nFrage: {question}"),
])


def baue_index(k: int = 3):
    """M1: Index EINMAL bauen (laden -> splitten -> Chroma -> Retriever)."""
    from langchain_community.document_loaders import TextLoader

    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    alle_chunks = []
    for datei in sorted(DATA.glob("*.md")):
        alle_chunks.extend(splitter.split_documents(
            TextLoader(str(datei), encoding="utf-8").load()))
    db = Chroma(collection_name="wissens_assistent",
                embedding_function=get_embeddings())
    db.add_documents(alle_chunks)
    return db.as_retriever(search_kwargs={"k": k})


def beantworte(frage: str, retriever) -> dict:
    """M2: Antwort + Quellen + ehrlicher Fallback."""
    if is_offline_mode() and not hat_bezug(frage):
        return {"antwort": "Das steht in den Dokumenten leider nicht.",
                "quellen": [], "gefundene_stellen": 0}

    dokumente = retriever.invoke(frage)
    if is_offline_mode():
        frage_vektor = get_embeddings().embed_query(frage)
        dokumente = [d for d in dokumente
                     if any(a * b for a, b in zip(
                         frage_vektor, get_embeddings().embed_query(d.page_content)))]
    if not dokumente:
        return {"antwort": "Das steht in den Dokumenten leider nicht.",
                "quellen": [], "gefundene_stellen": 0}

    kontext = "\n\n---\n\n".join(d.page_content for d in dokumente)
    quellen = sorted({Path(d.metadata["source"]).name for d in dokumente})

    modell = get_chat_model(temperature=0.0)

    def _kontext(_: dict) -> str:
        return kontext

    chain = (RunnablePassthrough().assign(context=RunnableLambda(_kontext))
             | PROMPT | modell | StrOutputParser())
    antwort = chain.invoke({"question": frage})
    return {"antwort": antwort, "quellen": quellen,
            "gefundene_stellen": len(dokumente)}


def dialog(retriever) -> None:
    """M3+M4: Dialogschleife mit Verlauf, Statistik und Fehlerrobustheit."""
    verlauf: list[dict] = []
    print("Wissens-Assistent (Handbuecher). 'exit' beendet.\n")
    while True:
        try:
            frage = input("Du: ").strip()
        except EOFError:
            break
        if not frage:
            continue
        if frage.lower() in ("exit", "fertig", "quit"):
            break
        try:
            ergebnis = beantworte(frage, retriever)
        except Exception as fehler:  # M4: nichts darf crashen
            print(f"Assistent: Technisches Problem ({fehler}).")
            continue
        verlauf.append(ergebnis)
        print(f"Assistent: {ergebnis['antwort']}")
        if ergebnis["quellen"]:
            print(f"Quellen: {', '.join(ergebnis['quellen'])} "
                  f"({ergebnis['gefundene_stellen']} Stellen)\n")

    unbeantwortet = sum(1 for e in verlauf if not e["quellen"])
    print(f"\nStatistik: {len(verlauf)} Fragen, davon {unbeantwortet} ohne Treffer.")


def main() -> None:
    if is_offline_mode():
        print("OFFLINE-Modus: Retrieval echt, Formulierungen simuliert.\n")
    retriever = baue_index()
    dialog(retriever)


if __name__ == "__main__":
    main()
