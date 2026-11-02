# Aufgabe 3.3 – Build 2 komplett: RAG-Assistent mit Quellen & Struktur 🎯

**Schwierigkeit:** Mittel · **Zeit:** ~60–90 Min · ⚠️ **Kosten:** LLM-Call nur mit Key

> **Benötigte Modell-Fähigkeit:** Structured Output / JSON (für die `Kurzanalyse`). Nicht jedes lokale Modell beherrscht das – Details & Auswege: [docs/local-ai-server.md](../../docs/local-ai-server.md) (Abschnitt Fähigkeiten).

## Lernziel
Du baust die **Build-2-Version deines Personal Knowledge Assistant** komplett: Retrieval → Kontext in die Chain → Antwort mit Quellen – plus strukturierte Ausgaben (Pydantic) und das ehrliche „Weiß ich nicht".

## Warum das wichtig ist
Das ist die Version, die wirklich nützlich ist: Sie beantwortet Fragen über **deine** Dokumente, zeigt die Fundstellen und erfindet nichts. Die Architektur ist exakt das Fundament für Build 3 (dort kommt der Graph als zweite Quelle dazu).

## Die Build-2-Architektur

```mermaid
flowchart LR
    F[Frage] --> RET[(Retriever)]
    RET --> KX[top-k Chunks + Metadaten]
    KX --> P[Prompt mit {context}] --> M[Modell] --> PAR[Parser]
    PAR --> A[Antwort]
    KX --> Q[Quellenliste<br/>aus Metadaten]
    Q --> A2[Antwort + Quellen]
```

## Deine Mission
1. **RAG-Chain:** Prompt mit `{context}` + `{question}` und der Regel „NUR aus dem Kontext; sonst: ehrlich sagen"; Retriever-Ergebnisse per `RunnablePassthrough().assign(context=RunnableLambda(...))` in die Chain einschleusen.
2. `beantworte(frage) -> dict` mit `antwort`, `quellen`, `gefundene_stellen` – Quellen stammen aus den Metadaten, nicht aus dem Modell!
3. **Strukturierte Ausgabe dazu:** `with_structured_output` + Pydantic (`Kurzanalyse`: thema, stichpunkte, schaetzwortzahl) – die Assistent-Antwort ist nicht immer nur Text!
4. **Test-Galerie (Pflicht):** „Wie viele Urlaubstage gibt es?" / „Wie beantrage ich freie Tage?" (der Build-1-Killer!) / eine Frage ohne Treffer.
5. **Frontend-Moment:** Führe `build2_assistant.py` aus (interaktiv) – dein Assistent, jetzt mit echter Qualität. Die Oberfläche aus 2.2 funktioniert damit direkt.

## Akzeptanzkriterien
- [ ] Der Kontext kommt aus dem Retriever, nirgendwo fest codiert.
- [ ] Antworten + Quellen kommen in einem strukturierten Dict zurück.
- [ ] Fragen ohne Treffer → ehrliche Antwort, keine Quellen.
- [ ] Du kannst begründen, warum die Quellen **separat** aus den Metadaten stammen statt vom Modell zitiert zu werden.

## Hinweise
1. `RunnableLambda`/`RunnablePassthrough` aus `langchain_core.runnables`
2. Offline: Retrieval echt, Formulierung simuliert – die Quellenliste prüfen!
3. Die `data/`-Dokumente sind dieselben wie in Build 1 – vergleiche die Antwortqualität direkt.

## Reflexionsfragen
1. Was hat Build 2 gegenüber Build 1 **einfacher** gemacht – und was ist **komplizierter** geworden (neue Begriffe, neue Fehlerquellen)?
2. Warum ist „Antworte nur aus dem Kontext" Eindämmung, aber keine Garantie gegen Halluzination?
3. Welche Frage bleibt unbeantwortet, obwohl die Information irgendwo steckt? (→ Beziehungen zwischen Entitäten – dein Einstieg in Modul 4!)

## Referenzlösung + Walkthrough
→ [`solutions/document_qa.py`](../solutions/document_qa.py) (Pipeline) und [`solutions/build2_assistant.py`](../solutions/build2_assistant.py) (interaktiver Assistent), [`solutions/structured_output.py`](../solutions/structured_output.py) (Pydantic).

## Weiter
🕸️ [`../04-knowledge-graphs/`](../../04-knowledge-graphs/README.md) – „Wer arbeitet woran?" braucht **Beziehungen**, keine Textähnlichkeit.
