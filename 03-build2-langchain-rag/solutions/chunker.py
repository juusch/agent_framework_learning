"""Aufgabe 4.2 – Referenzloesung: Chunking & Embeddings.

Laeuft komplett offline (Offline-Embeddings = Schluesselwort-Vektoren).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from langchain_text_splitters import RecursiveCharacterTextSplitter

from lernakademie.mock_llm import is_offline_mode
from lernakademie.offline_embeddings import KEYWORDS, get_embeddings

DATA = Path(__file__).resolve().parents[1] / "data"

FRAGEN = [
    "Wie viele Urlaubstage habe ich?",
    "Bis wann muss der Urlaubsantrag gestellt werden?",
    "Wie sieht eine sichere Passwort-Regel aus?",
]


def cosine_aehnlichkeit(u: list[float], v: list[float]) -> float:
    """Punktprodukt (unsere Vektoren sind normalisiert -> entspricht Cosine)."""
    return sum(a * b for a, b in zip(u, v))


def main() -> None:
    if is_offline_mode():
        print("OFFLINE-Embeddings (Schluesselwort-Modell) aktiv.\n")

    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)

    for datei in sorted(DATA.glob("*.md")):
        text = datei.read_text(encoding="utf-8")
        chunks = splitter.split_text(text)
        print(f"{datei.name}: {len(chunks)} Chunks "
              f"(erster: {len(chunks[0])} Z., letzter: {len(chunks[-1])} Z.)")

    # Embeddings fuer die drei Fragen
    embeddings = get_embeddings()
    vektoren = [embeddings.embed_query(frage) for frage in FRAGEN]

    print("\nAehnlichkeitsmatrix (0.0 = kein Bezug, 1.0 = identisch):")
    for i, frage_i in enumerate(FRAGEN):
        zeile = [f"{cosine_aehnlichkeit(vektoren[i], vektoren[j]):.2f}"
                 for j in range(len(FRAGEN))]
        print(f"  {frage_i[:36]:38s} {zeile}")
    # Erwartung: Frage 1 und 2 (beide 'Urlaub') aehnlicher als jedes
    # Urlaubs-Paar zur Passwort-Frage.

    # Bonus: Was "bedeutet" der Vektor der ersten Frage im Offline-Modell?
    vektor = vektoren[0]
    aktiv = [KEYWORDS[i] for i, wert in enumerate(vektor) if wert > 0]
    print(f"\nAktive Schluesselwoerter von '{FRAGEN[0]}': {aktiv}")


if __name__ == "__main__":
    main()
