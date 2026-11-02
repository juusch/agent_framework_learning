# Aufgabe 4.4 – Dokumenten-QA-Assistent (RAG-Finale) 🎓

## Schwierigkeit
Mittel · ⚠️ **Kosten:** LLM- + Embedding-Calls nur mit Key

## Lernziel
Du baust eine vollständige RAG-Anwendung: Frage → Retrieval → Kontext-Injektion → Antwort mit Quellenangabe – inklusive ehrlicher „Weiß ich nicht"-Antwort.

## Warum ist das wichtig?
Das ist der Gipfel der Stufen 0–4: alle Bausteine (Dateien, Chunks, Embeddings, Vektor-DB, Retriever, Chains, strukturierte Ausgaben) zu **einem** produktionsnahen System verbunden. Genau so funktionieren Firmen-Chatbots über interne Dokumente.

## Das Konzept einfach erklärt
**Metapher – die offene Klausur:** Der Kandidat (LLM) bekommt die Frage **und** das aufgeschlagene Buch (die gefundenen Chunks). Anweisung: „Antworte **nur** mit dem, was im Buch steht – und schreib dazu, auf welcher Seite (Quelle) es steht. Wenn es nicht im Buch steht: sag das ehrlich." Damit ist Halluzination eingedämmt (nicht ausgeschlossen!) und die Antwort prüfbar.

## Die technische Erklärung
Der klassische RAG-Prompt hat drei Zutaten im Template: `{context}` (die gefundenen Chunks), `{question}`, plus Regeln („nur aus dem Kontext", „nenne die Quellen"). Die Pipeline:

```python
def hole_kontext(frage):  # RunnableLambda – deine Python-Logik als Chain-Baustein
    docs = retriever.invoke(frage)
    return "\n\n".join(d.page_content for d in docs)

chain = (RunnablePassthrough.assign(context=RunnableLambda(hole_kontext))
         | prompt | modell | StrOutputParser())
```

- `RunnablePassthrough` / `RunnableLambda` (aus `langchain_core.runnables`) erlauben es, Retriever-Ergebnisse **in** die Chain einzuschleusen, ohne das Dict `{"frage": ...}` zu verlieren.
- **Quellen** holst du separat aus den gefundenen Documents (`metadata["source"]`) – die Antwort des Modells ist Text, die Quellenliste liefert deine Logik. (Ehrlich: verlässlicher, als das Modell die Quellen „zitieren" zu lassen.)
- „Weiß ich nicht": erreichbar über klare Prompt-Regeln; **garantieren** kannst du es nie – deshalb Reflexionsfrage 3!

## Voraussetzungen
- Aufgaben 4.1–4.3

## Deine Mission
Baue `document_qa.py` mit der Funktion `beantworte(frage) -> dict`:
1. Kompletter Index (beide Handbücher laden, splitten, Chroma, Retriever `k=3`) – wiederverwendbar als Funktion `baue_retriever()`.
2. RAG-Chain mit Prompt-Regeln: „Antworte NUR auf Basis des Kontexts. Wenn die Antwort nicht drinsteht, sage: 'Das steht in den Dokumenten leider nicht.' Nenne die relevanteste Fundstelle."
3. Rückgabe-Dictionary mit `antwort` (Text) und `quellen` (Liste der Dateinamen der gefundenen Chunks).
4. **Drei Testfragen:** „Wie viele Urlaubstage gibt es?", „Wann verfällt Resturlaub?" und eine Frage, die **nicht** in den Dokumenten steht (z. B. „Wie hoch ist das Weihnachtsgeld?").
5. Gib Antwort + Quellen sauber aus. Offline-Modus: Die Antwort ist eine `[OFFLINE]`-Simulation, **aber** die Quellenliste zeigt dir echtes, korrektes Retrieval – prüfe sie!

## Akzeptanzkriterien
- [ ] Der Kontext kommt aus dem Retriever, nicht aus dem Code (keine festgeschriebenen Texte!).
- [ ] Antworten enthalten die relevante Info (mit Key) bzw. `[OFFLINE]`-Echo (ohne Key) – aber **Quellen** stimmen immer.
- [ ] Die Unbeantwortbare-Frage wird als solche erkannt (mit Key) bzw. führt nicht zu einer Quellen-„Erfindung".
- [ ] `beantworte()` gibt ein strukturiertes Dictionary zurück (testbar!).

## Hinweise
1. Bausteine importieren: `from langchain_core.runnables import RunnableLambda, RunnablePassthrough`
2. Kontext-Format: Chunks mit Trennzeilen verbinden, damit das Modell sie unterscheiden kann.
3. Quellen ohne Duplikate: `sorted({Path(d.metadata["source"]).name for d in docs})`.
4. Vor dem LLM-Call prüfen: Wenn der Retriever **nichts** Sinnvolles liefert (offline möglich), gib direkt die „nicht gefunden"-Antwort zurück –kostenloses Early-Exit!

## Reflexionsfragen
1. Wo genau in deiner Chain passiert **Retrieval** und wo **Generation** – und warum nennt sich das Ganze R**A**G?
2. Warum hängen wir die Quellen **selbst** an die Antwort, statt das Modell bitten, sie zu zitieren?
3. Warum ist „Antworte nur aus dem Kontext" eine **Eindämmung**, aber keine **Garantie** gegen Halluzination? (Denk an: ähnliche Chunks, die etwas anderes behaupten.)

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| `context` leer / KeyError im Prompt | hole_kontext wirklich an die Chain angeschlossen? `RunnablePassthrough.assign(...)` prüfen |
| Antwort halluziniert Details | Prompt-Regeln verschärfen; k kleiner wählen statt größer |
| Quellenliste fehlt | Retriever-Ergebnis separat sammeln, bevor die Chain läuft (siehe Lösung) |

## Referenzlösung
→ [`solutions/document_qa.py`](../solutions/document_qa.py)

## Code-Walkthrough
In der Lösungsdatei; besonders die Trennung von `hole_kontext()` (Retrieval), Chain (Generation) und `beantworte()` (Kombination).

## Was haben wir gelernt?
Der komplette RAG-Zyklus: Index bauen, kontextbasiert antworten, Quellen transparent machen, mit „nicht gefunden" umgehen.

## Was kommt als Nächstes?
🎉 **Du hast das Fundament geschafft!** Du kannst jetzt: programmieren, mit LLMs sprechen, Chains bauen und RAG-Anwendungen erstellen. Die nächsten Stufen (siehe [Lernfahrplan](../../docs/learning-roadmap.md)) heben dein Wissen auf Workflow-Ebene: LangGraph-Graphen, Agenten mit Tools, Multi-Agent-Systeme. Halte deinen Fortschritt in [`PROGRESS.md`](../../PROGRESS.md) fest!
