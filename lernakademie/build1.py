"""BUILD 1 – Der Pure-Python-Wissensassistent als wiederverwendbares Modul.

Notebooks (Lektion 05/06) bauen jede Funktion zuerst von Hand; dieses
Modul ist die "Level-3"-Abstraktion desselben Codes (siehe Notebook-Guide).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from lernakademie.llm_client import get_api_client, get_model_name

DATA = Path(__file__).resolve().parents[1] / "data"
NICHT_GEFUNDEN = "Dazu habe ich in den Dokumenten leider nichts gefunden."


def _woerter(text: str) -> set[str]:
    text = (text.lower().replace("ü", "ue").replace("ä", "ae")
            .replace("ö", "oe"))
    return {w.strip(".,?!:;\"'()") for w in text.split() if len(w) >= 4}


def lade_dokumente() -> list[dict]:
    """Liest alle data/*.md und schneidet sie an ## -Ueberschriften."""
    abschnitte: list[dict] = []
    for datei in sorted(DATA.glob("*.md")):
        text = datei.read_text(encoding="utf-8")
        for teil in text.split("## ")[1:]:
            titel, *rest = teil.split("\n", 1)
            inhalt = rest[0].strip() if rest else ""
            if inhalt:
                abschnitte.append({"quelle": datei.name,
                                   "titel": titel.strip(), "text": inhalt})
    return abschnitte


def suche_relevant(frage: str, abschnitte: list[dict], top: int = 2) -> list[dict]:
    """Build-1-Suche: Wort-Ueberlappung (bewusst simpel – siehe Lektion 05)."""
    frage_woerter = _woerter(frage)
    scored = []
    for abschnitt in abschnitte:
        score = len(frage_woerter & _woerter(abschnitt["text"]))
        if score > 0:
            scored.append((score, abschnitt))
    scored.sort(key=lambda paar: paar[0], reverse=True)
    return [abschnitt for _, abschnitt in scored[:top]]


def baue_prompt(frage: str, abschnitte: list[dict]) -> str:
    kontext = "\n\n".join(
        f"[{a['quelle']} - {a['titel']}]\n{a['text']}" for a in abschnitte)
    return (
        "Du bist ein Assistent fuer Firmenhandbuecher. Antworte NUR auf Basis "
        "des folgenden Kontexts. Wenn die Antwort nicht im Kontext steht, sage: "
        "'Das steht in den Dokumenten leider nicht.'\n\n"
        f"Kontext:\n{kontext}\n\nFrage: {frage}"
    )


def beantworte(frage: str, abschnitte: list[dict]) -> dict[str, Any]:
    """Dirigent: Suche -> Prompt -> Modell -> Antwort + Quellen."""
    relevante = suche_relevant(frage, abschnitte)
    if not relevante:
        return {"antwort": NICHT_GEFUNDEN, "quellen": []}
    client = get_api_client()
    try:
        antwort = client.chat.complete(
            model=get_model_name(),
            messages=[{"role": "user", "content": baue_prompt(frage, relevante)}])
        text = antwort.choices[0].message.content
    except Exception as fehler:  # freundliche Fehlersicht statt Crash
        return {"antwort": f"Technisches Problem: {fehler}", "quellen": []}
    return {"antwort": text,
            "quellen": [f"{a['quelle']} - {a['titel']}" for a in relevante]}
