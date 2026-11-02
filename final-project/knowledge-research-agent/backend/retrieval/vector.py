"""Vektor-Retrieval: Dokumenten-Wissensbasis (in-memory).

Nutzte InMemoryVectorStore (langchain_core) mit den Akademie-Embeddings:
offline = Schluesselwort-Modell, mit Key = echte Mistral-Embeddings.
Neue Dokumente lassen sich zur Laufzeit hinzufuegen (Upload im Frontend).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))  # Akademie-Wurzel
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # Projektordner

from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

from lernakademie.offline_embeddings import get_embeddings, hat_bezug

SEED_ORDNER = Path(__file__).resolve().parents[1] / "seed" / "documents"


class Wissensbasis:
    """Verwaltet Dokumente + Vektor-Index (Wiederverwendung: Stufe-4-Muster)."""

    def __init__(self) -> None:
        self._splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                                        chunk_overlap=80)
        self._store = InMemoryVectorStore(embedding=get_embeddings())
        self._dokumente: list[dict] = []  # [{titel, zeichen}]
        for datei in sorted(SEED_ORDNER.glob("*.md")):
            self.hinzufuegen(datei.stem, datei.read_text(encoding="utf-8"))

    def hinzufuegen(self, titel: str, inhalt: str) -> int:
        """Legt ein Dokument im Index ab; liefert die Anzahl neuer Chunks."""
        chunks = self._splitter.split_documents(
            [Document(page_content=inhalt, metadata={"quelle": titel})])
        self._store.add_documents(chunks)
        self._dokumente.append({"titel": titel, "zeichen": len(inhalt)})
        return len(chunks)

    def suche(self, frage: str, k: int = 2) -> list[dict]:
        """Semantische Suche. Offline-Ehrlichkeit: ohne Schluesselwort-Bezug
        wuerden beliebige Chunks kommen – dann lieber nichts (Stufe 4.4)."""
        if not hat_bezug(frage):
            return []
        treffer = self._store.similarity_search(frage, k=k)
        ergebnisse = []
        for dokument in treffer:
            textstelle = dokument.page_content.strip().replace("\n", " ")
            if len(textstelle) > 30:
                ergebnisse.append({
                    "quelle": dokument.metadata.get("quelle", "unbekannt"),
                    "textstelle": textstelle[:180] + ("..." if len(textstelle) > 180 else ""),
                })
        return ergebnisse

    def liste(self) -> list[dict]:
        return list(self._dokumente)
