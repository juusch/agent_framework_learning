"""BUILD 1 – Der Personal Knowledge Assistant in reinem Python.

Bewusst KEINE LangChain-Imports: Alles von Hand, damit du spaeter
weist, was das Framework fuer dich uebernimmt.

Pipeline: Dokumente laden -> Abschnitte schneiden -> Wort-Ueberlappung
scoring -> Prompt von Hand bauen -> Mistral direkt aufrufen.

Offline-Modus: get_api_client() liefert ohne API-Key eine
Simulation – der Ablauf bleibt identisch, kostenlos uebbar.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from lernakademie.llm_client import get_model_name, get_api_client, is_offline_mode

DATA = Path(__file__).resolve().parents[2] / "data"

NICHT_GEFUNDEN = "Dazu habe ich in den Dokumenten leider nichts gefunden."


def lade_dokumente() -> list[dict]:
    """Liest alle data/*.md und schneidet sie an ## -Ueberschriften."""
    abschnitte: list[dict] = []
    for datei in sorted(DATA.glob("*.md")):
        text = datei.read_text(encoding="utf-8")
        teile = text.split("## ")
        for teil in teile[1:]:  # teile[0] ist der Dokumentkopf
            titel, *rest = teil.split("\n", 1)
            inhalt = rest[0].strip() if rest else ""
            if inhalt:
                abschnitte.append({
                    "quelle": datei.name,
                    "titel": titel.strip(),
                    "text": inhalt,
                })
    return abschnitte


def suche_relevant(frage: str, abschnitte: list[dict], top: int = 2) -> list[dict]:
    """Scores Abschnitte nach Wort-Ueberlappung mit der Frage.

    (Build 1: reine Wort-Gleichheit – 'Urlaub' findet kein 'freie Tage'.
    Build 2 ersetzt genau das durch Embeddings!)
    """
    def _woerter(text: str) -> set[str]:
        # Umlaute normalisieren (oe/ae/ue), Satzzeichen entfernen und
        # Fuellwoerter (<4 Zeichen) ignorieren.
        text = (text.lower().replace("ü", "ue").replace("ä", "ae")
                .replace("ö", "oe"))
        return {w.strip(".,?!:;\"'()") for w in text.split() if len(w) >= 4}

    frage_woerter = _woerter(frage)
    scored = []
    for abschnitt in abschnitte:
        score = len(frage_woerter & _woerter(abschnitt["text"]))
        if score > 0:
            scored.append((score, abschnitt))
    scored.sort(key=lambda paar: paar[0], reverse=True)
    return [abschnitt for _, abschnitt in scored[:top]]


def baue_prompt(frage: str, abschnitte: list[dict]) -> str:
    """Baut den Prompt VON HAND: Anweisung + Kontext + Frage.

    Genau diese String-Arbeit uebernimmt spaeter ChatPromptTemplate.
    """
    kontext = "\n\n".join(
        f"[{a['quelle']} – {a['titel']}]\n{a['text']}" for a in abschnitte)
    return (
        "Du bist ein Assistent fuer Firmenhandbuecher. Antworte NUR auf "
        "Basis des folgenden Kontexts. Wenn die Antwort nicht im Kontext "
        "steht, sage: 'Das steht in den Dokumenten leider nicht.'\n\n"
        f"Kontext:\n{kontext}\n\nFrage: {frage}"
    )


def beantworte(frage: str, abschnitte: list[dict] | None = None) -> dict:
    """Die manuelle Orchestrierung: Suche -> Prompt -> API -> Antwort."""
    if abschnitte is None:
        abschnitte = lade_dokumente()

    relevante = suche_relevant(frage, abschnitte)
    if not relevante:
        return {"antwort": NICHT_GEFUNDEN, "quellen": []}

    prompt = baue_prompt(frage, relevante)
    client = get_api_client()
    try:
        antwort = client.chat.complete(
            model=get_model_name(),
            messages=[{"role": "user", "content": prompt}],
        )
        text = antwort.choices[0].message.content
    except Exception as fehler:
        return {"antwort": f"Technisches Problem: {fehler}", "quellen": []}

    quellen = [f"{a['quelle']} – {a['titel']}" for a in relevante]
    return {"antwort": text, "quellen": quellen}


def main() -> None:
    if is_offline_mode():
        print("BUILD 1 (Offline-Modus: Antworten simuliert, Suche echt.)\n")
    abschnitte = lade_dokumente()
    print(f"{len(abschnitte)} Abschnitte aus {len({a['quelle'] for a in abschnitte})} "
          "Dokumenten geladen.\n")

    fragen = [
        "Wie viele Urlaubstage gibt es?",
        "Was gilt fuer Passwoerter?",
        "Wie hoch ist das Weihnachtsgeld?",  # steht nicht drin -> ehrlich
    ]
    for frage in fragen:
        ergebnis = beantworte(frage, abschnitte)
        print(f"Frage:   {frage}")
        print(f"Antwort: {ergebnis['antwort'][:160]}")
        print(f"Quellen: {ergebnis['quellen']}\n")


if __name__ == "__main__":
    main()
