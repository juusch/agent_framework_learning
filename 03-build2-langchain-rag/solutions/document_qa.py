"""Aufgabe 4.4 – Referenzloesung: Dokumenten-QA-Assistent (RAG).

Der komplette RAG-Zyklus:
  Frage -> Retriever -> Kontext in den Prompt -> LLM -> Antwort + Quellen
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

DATA = Path(__file__).resolve().parents[2] / "data"

NICHT_GEFUNDEN = "Das steht in den Dokumenten leider nicht."

PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "Du beantwortest Fragen NUR auf Basis des gegebenen Kontexts. "
     "Wenn die Antwort nicht im Kontext steht, antworte exakt mit: "
     "'Das steht in den Dokumenten leider nicht.' "
     "Nenne die relevanteste Fundstelle."),
    ("human", "Kontext:\n{context}\n\nFrage: {question}"),
])


def lade_chunks() -> list:
    from langchain_community.document_loaders import TextLoader

    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    alle_chunks = []
    for datei in sorted(DATA.glob("*.md")):
        alle_chunks.extend(splitter.split_documents(
            TextLoader(str(datei), encoding="utf-8").load()))
    return alle_chunks


def baue_retriever(k: int = 3):
    """Index bauen (laden -> splitten -> Chroma -> Retriever)."""
    chunks = lade_chunks()
    db = Chroma(collection_name="handbuch", embedding_function=get_embeddings())
    db.add_documents(chunks)
    return db.as_retriever(search_kwargs={"k": k})


def hole_kontext(frage: str, retriever) -> tuple[str, list[str]]:
    """Retrieval: liefert Kontext-Text UND die Quellen (fuer die Antwort).

    Offline-Frueh-Exit: Wenn die Frage kein bekanntes Schluesselwort
    enthaelt, wuerde die Suche beliebige Chunks liefern. Dann sagen wir
    ehrlich 'nicht gefunden' – kostenlos und ohne API-Call.
    """
    if is_offline_mode() and not hat_bezug(frage):
        return "", []
    dokumente = retriever.invoke(frage)
    if is_offline_mode():
        # Nur Chunks behalten, die wirklich einen Bezug zur Frage haben
        # (offline: Aehnlichkeit > 0), statt beliebiger Mithraeufer.
        embeddings = get_embeddings()
        frage_vektor = embeddings.embed_query(frage)
        dokumente = [
            d for d in dokumente
            if any(a * b for a, b in
                   zip(frage_vektor, embeddings.embed_query(d.page_content)))
        ]
        if not dokumente:
            return "", []
    kontext = "\n\n---\n\n".join(d.page_content for d in dokumente)
    quellen = sorted({Path(d.metadata["source"]).name for d in dokumente})
    return kontext, quellen


def beantworte(frage: str, retriever) -> dict:
    """Dirigent: Retrieval -> (frueher Exit wenn leer) -> RAG-Chain."""
    kontext, quellen = hole_kontext(frage, retriever)
    if not kontext.strip():
        return {"antwort": NICHT_GEFUNDEN, "quellen": []}

    modell = get_chat_model(temperature=0.0)

    def _kontext(_: dict) -> str:
        return kontext  # wir haben ihn schon geholt (Quellen mitnehmen!)

    chain = (
        RunnablePassthrough().assign(context=RunnableLambda(_kontext))
        | PROMPT
        | modell
        | StrOutputParser()
    )
    antwort = chain.invoke({"question": frage})
    return {"antwort": antwort, "quellen": quellen}


def main() -> None:
    if is_offline_mode():
        print("OFFLINE-Modus: Antwort simuliert, aber Retrieval + Quellen sind echt.\n")

    retriever = baue_retriever(k=3)
    fragen = [
        "Wie viele Urlaubstage gibt es?",
        "Bis wann muss ein Urlaubsantrag gestellt werden?",
        "Wie hoch ist das Weihnachtsgeld?",  # steht NICHT in den Dokumenten
    ]
    for frage in fragen:
        ergebnis = beantworte(frage, retriever)
        print(f"Frage: {frage}")
        print(f"Antwort: {ergebnis['antwort']}")
        print(f"Quellen: {ergebnis['quellen']}\n")


if __name__ == "__main__":
    main()
