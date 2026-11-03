"""BUILD 2 – RAG-Assistent als wiederverwendbares Modul (Lektion 09).

Architektur identisch zum Notebook: Retriever (Chroma) -> Kontext in die
Chain (RunnablePassthrough/RunnableLambda) -> Antwort + Quellen aus
Metadaten -> ehrliches Nicht-gefunden ohne Treffer.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter

from lernakademie.llm_client import get_chat_model
from lernakademie.offline_embeddings import get_embeddings, hat_bezug

DATA = Path(__file__).resolve().parents[1] / "data"
NICHT_GEFUNDEN = "Das steht in den Dokumenten leider nicht."

PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "Du beantwortest Fragen NUR auf Basis des gegebenen Kontexts. "
     "Wenn die Antwort nicht im Kontext steht, antworte exakt mit: "
     "'Das steht in den Dokumenten leider nicht.'"),
    ("human", "Kontext:\n{context}\n\nFrage: {question}"),
])


def baue_retriever(k: int = 3):
    """Index einmalig bauen: laden -> splitten -> Chroma -> Retriever."""
    from langchain_community.document_loaders import TextLoader

    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    alle_chunks = []
    for datei in sorted(DATA.glob("*.md")):
        alle_chunks.extend(splitter.split_documents(
            TextLoader(str(datei), encoding="utf-8").load()))
    db = Chroma(collection_name="build2_modul", embedding_function=get_embeddings())
    db.add_documents(alle_chunks)
    return db.as_retriever(search_kwargs={"k": k})


def _relevante_docs(retriever, frage):
    """Liefert nur Treffer mit echtem Bezug (offline: Aehnlichkeit > 0)."""
    from lernakademie.config import is_offline_mode

    dokumente = retriever.invoke(frage)
    if is_offline_mode():
        embeddings = get_embeddings()
        frage_vektor = embeddings.embed_query(frage)
        dokumente = [
            d for d in dokumente
            if any(a * b for a, b in zip(
                frage_vektor, embeddings.embed_query(d.page_content)))]
    return dokumente


def baue_rag_chain(retriever):
    modell = get_chat_model(temperature=0.0)

    def _kontext(eingabe):
        frage = eingabe["question"]
        if not hat_bezug(frage):
            return ""
        return "\n\n---\n\n".join(
            d.page_content for d in _relevante_docs(retriever, frage))

    def _quellen(eingabe):
        frage = eingabe["question"]
        if not hat_bezug(frage):
            return []
        return sorted({Path(d.metadata["source"]).name
                       for d in _relevante_docs(retriever, frage)})

    chain = (RunnablePassthrough().assign(context=RunnableLambda(_kontext))
             | PROMPT | modell | StrOutputParser())
    return chain, _quellen


_RETRIEVER = None
_CHAIN = None
_QUELLEN = None


def beantworte(frage: str) -> dict[str, Any]:
    """Build-2-Pipeline mit Early-Exit und ehrlichen Quellen."""
    global _RETRIEVER, _CHAIN, _QUELLEN
    if _CHAIN is None:
        _RETRIEVER = baue_retriever()
        _CHAIN, _QUELLEN = baue_rag_chain(_RETRIEVER)

    if not hat_bezug(frage):
        return {"antwort": NICHT_GEFUNDEN, "quellen": [],
                "gefundene_stellen": 0}
    antwort = _CHAIN.invoke({"question": frage})
    quellen = _QUELLEN({"question": frage})
    if not quellen:
        return {"antwort": NICHT_GEFUNDEN, "quellen": [],
                "gefundene_stellen": 0}
    return {"antwort": antwort, "quellen": quellen,
            "gefundene_stellen": len(quellen)}
