"""Aufgabe 4.3 – Referenzloesung: Vektor-Datenbank (Chroma) & semantische Suche.

Laeuft mit echten Mistral-Embeddings (mit Key) oder offline mit
Schluesselwort-Embeddings (ohne Key, kostenlos).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from lernakademie.mock_llm import is_offline_mode
from lernakademie.offline_embeddings import get_embeddings

DATA = Path(__file__).resolve().parents[2] / "data"

FRAGEN = [
    "Wie viele Urlaubstage gibt es?",
    "Wann verfaellt Resturlaub?",
    "Wie richte ich VPN ein?",
    "Was sind die Passwort-Regeln?",
]


def lade_chunks() -> list:
    """Laedt alle Handbuch-Dateien und zerlegt sie in Chunks (mit Metadaten)."""
    from langchain_community.document_loaders import TextLoader

    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    alle_chunks = []
    for datei in sorted(DATA.glob("*.md")):
        dokumente = TextLoader(str(datei), encoding="utf-8").load()
        alle_chunks.extend(splitter.split_documents(dokumente))
    return alle_chunks


def baue_datenbank(chunks: list) -> Chroma:
    """Erstellt eine Chroma-Sammlung und speichert die Chunks.

    Ohne persist_directory laeuft die Datenbank im Speicher (neu pro Start) –
    fuer die Uebung ideal. Mit persist_directory="..." bleibt sie erhalten.
    """
    return Chroma(
        collection_name="handbuch",
        embedding_function=get_embeddings(),
    )


def main() -> None:
    if is_offline_mode():
        print("OFFLINE-Modus: Suche nach Schluesselwoertern der Dokumente.\n")

    chunks = lade_chunks()
    db = baue_datenbank(chunks)
    db.add_documents(chunks)
    print(f"{len(chunks)} Chunks in der Chroma-Sammlung gespeichert.\n")

    retriever = db.as_retriever(search_kwargs={"k": 3})
    for frage in FRAGEN:
        print(f"Frage: {frage}")
        gefunden = retriever.invoke(frage)
        for dokument in gefunden:
            quelle = Path(dokument.metadata["source"]).name
            auszug = dokument.page_content.strip().replace("\n", " ")[:150]
            print(f"  [{quelle}] {auszug}...")
        print()


if __name__ == "__main__":
    main()
