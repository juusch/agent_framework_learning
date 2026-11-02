"""Transparente Schluesselwort-Embeddings fuer die RAG-Stufe (Offline-Modus).

Warum so simpel?
- Lernende sollen SEEHEN, was ein Embedding tut: Text -> Zahlenvektor.
- Diese Version erkennt definierte Schluesselwoerter und bildet daraus
  einen Vektor. Aehnliche Texte (gleiche Schluesselwoerter) bekommen
  aehnliche Vektoren – genau das Prinzip echter Embeddings, nur
  verstaendlich und kostenlos.
- Mit MISTRAL_API_KEY wird stattdessen das echte Mistral-Embedding-Modell
  verwendet (siehe get_embeddings unten): Dann versteht die Suche auch
  Umschreibungen statt nur exakter Schluesselwoerter.

Die Schluesselwoerter passen zu den Uebungsdokumenten in
04-rag-and-knowledge/data/.
"""

from __future__ import annotations

import math
from typing import List

from langchain_core.embeddings import Embeddings

from lernakademie.config import is_offline_mode

# Jedes Thema bekommt eine feste Dimension im Vektor.
KEYWORDS: List[str] = [
    "urlaub", "gehalt", "home-office", "homeoffice", "arbeitszeit",
    "kuendigung", "probezeit", "ueberstunden",
    "passwort", "vpn", "laptop", "drucker", "software", "internet",
    "termin", "meeting", "e-mail", "urlaubsantrag",
    "python", "ki", "api",
]


def _normalize(text: str) -> str:
    return text.lower().replace("ü", "ue").replace("ä", "ae").replace("ö", "oe")


class OfflineKeywordEmbeddings(Embeddings):
    """Bestimmt Vektoren ueber Schluesselwort-Treffer (Dimension = len(KEYWORDS))."""

    def _vector(self, text: str) -> List[float]:
        normalized = _normalize(text)
        # Teilstring-Treffer: findet 'urlaub' auch in 'Resturlaub'
        vector = [
            1.0 if keyword in normalized else 0.0
            for keyword in KEYWORDS
        ]
        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            return vector
        return [value / norm for value in vector]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._vector(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        return self._vector(text)


def get_embeddings() -> Embeddings:
    """Liefert Embeddings: echt (Mistral) oder offline (Schluesselwoerter)."""
    if is_offline_mode():
        return OfflineKeywordEmbeddings()
    from langchain_mistralai import MistralAIEmbeddings

    return MistralAIEmbeddings(model="mistral-embed")


def hat_bezug(text: str) -> bool:
    """True, wenn der Text (offline) mindestens ein Schluesselwort enthaelt.

    Wird genutzt, um im Offline-Modus ehrlich 'kein Treffer' melden zu
    koennen, statt beliebige Chunks zurueckzugeben.
    """
    normalized = _normalize(text)
    return any(keyword in normalized for keyword in KEYWORDS)


__all__ = ["OfflineKeywordEmbeddings", "get_embeddings", "KEYWORDS", "hat_bezug"]
