# Aufgabe 3.4 – Mini-Projekt: Content-Assistant ✍️

## Schwierigkeit
Mittel · ⚠️ **Kosten:** nur mit Key (offline: Ablauf vollständig übbar)

## Lernziel
Du kombinierst Prompt-Templates, Chains, strukturierte Ausgaben, Fehlerbehandlung und eigene Python-Logik zu einer kleinen, mehrsprachigen Anwendung.

## Warum ist das wichtig?
Das ist der „Übungsraum" für alles, was danach kommt: In Stufe 4 (RAG) baust du **genau solche** Kombinationen – nur dass der Kontext statt von dir aus Dokumenten kommt. Wer diesen Assistant versteht, versteht RAG vorab zur Hälfte.

## Das Konzept einfach erklärt
Stell dir eine Redaktions-Abteilung vor: Du gibst einen rohen Text ab. Station 1 **zusammenfassen** (Chain A), Station 2 **übersetzen** (Chain B), Station 3 **verschlagworten/strukturieren** (Chain C mit Pydantic), und die Qualitätskontrolle prüft vorher, ob der Auftrag stimmig ist (deine Python-Logik). Am Ende bekommst du ein fertiges „Redaktions-Paket".

## Die technische Erklärung
- Du baust **drei unabhängige Chains** als Werkzeuge (Fabrikfunktionen wie in 3.2).
- Eine eigene Funktion (z. B. `pruefe_eingabe()`) validiert **vor** jedem API-Call: leerer Text? Mindestlänge? Ziel-Sprache erlaubt? Das schützt Kosten und Nerven – und ist Muster für robuste Anwendungen.
- Optional als Chain-Baustein: `RunnableLambda(funktion)` verpackt normale Python-Funktionen in eine Runnable und macht sie `|`-verkettbar.
- Am Ende **kombinierst** du die Ergebnisse in einem Dictionary – die „Antwort" deiner Anwendung.

## Voraussetzungen
- Aufgaben 3.1–3.3

## Deine Mission
Baue `content_assistant.py` mit der Funktion `verarbeite(text, zielsprache)`:
1. **Qualitätskontrolle zuerst:** `pruefe_eingabe()` – Text nicht leer, mindestens 50 Zeichen, `zielsprache` in einer erlaubten Liste `("Englisch", "Spanisch", "Franzoesisch")`; sonst `ValueError` mit klarer deutscher Meldung.
2. Chain A: Zusammenfassung (Template-Variable `{text}`) → String.
3. Chain B: Übersetzung der **Zusammenfassung** (nicht des Originals! Variable `{text}`, `{zielsprache}`) → String.
4. Chain C: strukturierte Analyse des Originaltextes mit Pydantic `Kurzanalyse` (`thema: str`, `stichpunkte: list[str]`, `schaetzwortzahl: int`).
5. Rückgabe eines Dictionaries mit allen Ergebnissen (`zusammenfassung`, `uebersetzung`, `analyse`) + `main()` mit zwei Demonstrationen: einmal gültig, einmal **absichtlich ungültig** (zu kurzer Text), gefangen per `try/except`.

## Akzeptanzkriterien
- [ ] Ungültige Eingaben werfen `ValueError` **bevor** irgend ein API-Call passiert.
- [ ] Die Übersetzung nutzt die Zusammenfassung als Eingabe (Chain-Kombination!).
- [ ] Die Analyse ist ein validiertes Pydantic-Objekt mit `Field(description=...)`.
- [ ] Die Rückgabe ist ein strukturiertes Dictionary.
- [ ] Die `main()` demonstriert Fehlerfall **und** Erfolgsfall.

## Hinweise
1. Fabrikfunktionen: `def baue_summarizer(modell): ... return prompt | modell | StrOutputParser()`
2. Liste erlaubter Sprachen als Konstante oben (dann weiß der Leser sofort, was konfigurierbar ist).
3. Beim Fehlerfall in main: `except ValueError as e: print("Eingabefehler:", e)`
4. Bonus-Verkettung: `chain = pruefung | prompt | ...` mit `RunnableLambda(pruefe_eingabe)` – probier es, **wenn** du die Grundversion sicher hast.

## Reflexionsfragen
1. Warum prüfen wir VOR dem API-Call – was sparen wir konkret (Geld? Zeit? Zuverlässigkeit)?
2. Wo genau entscheidet in diesem Assistant **Python-Logik** und wo **das LLM**? (Skizziere die Grenze – sie ist die wichtigste Architekturlinie überhaupt.)
3. Was müsste sich ändern, damit `verarbeite()` asynchron 100 Texte auf einmal verarbeitet? (Erst nur gedanklich – Stufe 9 wird das aufgreifen.)

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| Chain-Variablen vergessen (`{zielsprache}` nicht im Dict) | invoke-Dict gegen Template checken |
| Übersetzung nimmt Original statt Zusammenfassung | Chain-Eingaben bewusst lesen: fließt der richtige Wert ein? |
| `ValueError` crasht das Demo-Programm | try/except um den ungültigen Aufruf in main |

## Referenzlösung
→ [`solutions/content_assistant.py`](../solutions/content_assistant.py)

## Code-Walkthrough
In der Lösungsdatei; besonders die Trennung Fabrik / Prüfung / Verarbeitung.

## Was haben wir gelernt?
Kombinieren von Chains, Defensive Programmierung vor API-Kosten, strukturierte Ergebnis-Pakete, klare Logik/LLM-Grenze.

## Was kommt als Nächstes?
Stufe 4 – RAG. Dein Content-Assistent kann nur mit dem arbeiten, was du ihm in den Prompt schreibst. RAG gibt Modellen einen **Nachschlagewerk-Keller**: Dokumente laden, zerlegen, in Embeddings übersetzen, relevantes Wissen finden – und erst dann fragen. Los geht's!
