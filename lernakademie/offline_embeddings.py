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
data/ (Projektwurzel).
"""

from __future__ import annotations

import math
from typing import List

from langchain_core.embeddings import Embeddings

from lernakademie.config import (  # noqa: F401  (PROVIDER_* fuer Lesbarkeit re-exportiert)
    PROVIDER_MISTRAL, PROVIDER_OFFLINE, PROVIDER_OPENAI, get_provider,
)

# Jedes Thema bekommt eine feste Dimension im Vektor.
KEYWORDS: List[str] = [
    "urlaub", "gehalt", "home-office", "homeoffice", "arbeitszeit",
    "kuendigung", "probezeit", "ueberstunden",
    "passwort", "passwoerter", "vpn", "laptop", "drucker", "software", "internet",
    "termin", "meeting", "e-mail", "urlaubsantrag",
    "python", "ki", "api",
    # Begriffe fuer das GraphRAG-Firmenprofil (Stufe 13):
    "engineering", "analytics", "abteilung", "projekt", "assistant",
    "ben", "clara", "weiterbildung", "nutzungsanalyse", "abteilungen",
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
    """Liefert Embeddings – abhaengig vom konfigurierten Anbieter.

    - offline oder openai_compatible (Standard): Schluesselwort-Embeddings.
      Sie laufen UEBERALL (auch ohne Embeddings-faehigen Server) und sind
      deterministisch – die RAG-Mechanik bleibt voll uebbar.
    - mistral: echte Mistral-Embeddings (semantische Suche).

    Fortgeschritten: Mit EMBEDDINGS=openai_compatible + EMBEDDINGS_MODEL
    kannst du die Embeddings-Schnittstelle deines OpenAI-kompatiblen
    Servers nutzen (falls er /v1/embeddings anbietet).
    """
    import os

    modus = os.environ.get("EMBEDDINGS", "auto").strip().lower()
    provider = get_provider()

    if modus == "openai_compatible" and provider != PROVIDER_OFFLINE:
        from langchain_openai import OpenAIEmbeddings

        from lernakademie.config import get_api_key, get_base_url

        return OpenAIEmbeddings(
            model=os.environ.get("EMBEDDINGS_MODEL", "text-embedding-all-minilm-l6-v2"),
            base_url=get_base_url(),
            api_key=get_api_key() or "not-required",
        )
    if provider == PROVIDER_MISTRAL:
        from langchain_mistralai import MistralAIEmbeddings

        return MistralAIEmbeddings(model="mistral-embed")
    return OfflineKeywordEmbeddings()


def hat_bezug(text: str) -> bool:
    """True, wenn der Text (offline) mindestens ein Schluesselwort enthaelt.

    Wird genutzt, um im Offline-Modus ehrlich 'kein Treffer' melden zu
    koennen, statt beliebige Chunks zurueckzugeben.
    """
    normalized = _normalize(text)
    return any(keyword in normalized for keyword in KEYWORDS)


__all__ = ["OfflineKeywordEmbeddings", "get_embeddings", "KEYWORDS", "hat_bezug"]
