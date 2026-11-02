# Aufgabe 6.4 – Gedächtnis & menschliche Freigabe 🧠✋

## Schwierigkeit
Mittel · ⚠️ **Kosten:** nur mit Key

## Lernziel
Du gibst einem Agenten **Kurzzeit-Gedächtnis über mehrere Aufrufe** (Checkpointer) und baust einen **Human-in-the-Loop**: Vor einer sensiblen Aktion pausiert der Graph und wartet auf die Freigabe eines Menschen.

## Warum ist das wichtig?
1. Ohne Checkpointer vergisst ein Agent **alles** zwischen zwei `invoke()`-Aufrufen – „Wie hieß nochmal mein Anliegen?" wäre unmöglich.
2. Agenten, die Nebenwirkungen haben (E-Mail senden, etwas löschen, Geld bewegen), brauchen einen **Stopp vor der Ausführung**. Kein seriöses System lässt ein LLM ungefiltert auf Produktivsysteme los. Der Interrupt ist der Airbag.

## Das Konzept einfach erklärt
- **Checkpointer = Gesprächs-Aktenzeichen:** Jeder Aufruf mit derselben `thread_id` setzt dasselbe Gespräch fort. **Metapher:** ein Vorgangsordner im Büro – neues Personal am Schalter kann den Vorgang weiterführen, weil alles drinsteht.
- **Interrupt = Vier-Augen-Prinzip:** Der Agent hat den Auftrag fertig vorbereitet, hält aber inne und fragt: „Freigabe?" **Metapher:** ein Online-Banking-Transfer: alles ausgefüllt – der letzte Klick ist deiner.

## Die technische Erklärung
- `checkpointer=MemorySaver()` an `create_agent(...)` übergeben; Aufruf mit `config={"configurable": {"thread_id": "gespraech-1"}}`.
- Speicherort: `MemorySaver` = im RAM (genug für die Übung; Produktion: persistente Speicher wie SqliteSaver/Postgres – Stufe 9-Thema).
- **Freigabe:** ein Tool mit `interrupt()` (aus `langgraph.types`) pausiert die Ausführung und liefert die Frage zurück. Der Mensch antwortet mit `Command(resume=...)` und **demselben thread_id-Config** – der Graph läuft weiter, als wäre nichts gewesen.
- Achtung: `interrupt()` funktioniert nur mit Checkpointer (der Graph muss den angehaltenen Zustand ja sichern können).

## Voraussetzungen
- Aufgabe 6.2 (Agenten, Tools)

## Deine Mission
Baue `memory_approval_agent.py`:
1. Agent mit Checkpointer (`MemorySaver`) und Tool `notiz_anlegen(text: str)`.
2. Ein Tool `geheime_notiz(text: str)`: ruft **vor** dem Anlegen `interrupt({"frage": "Soll diese Notiz wirklich angelegt werden?", "text": text})` auf – nur bei Fortsetzung (`Command(resume=True)`) legt es die Notiz an (simuliert: print + Liste).
3. **Dialog 1 (Gedächtnis):** Erzähle dem Agenten deinen Namen (Aufruf 1), frage danach (Aufruf 2): „Wie heiße ich?" – mit **derselben** `thread_id`.
4. **Dialog 2 (Freigabe):** Bitte um eine geheime Notiz. Der Lauf unterbricht; gib die Interrupt-Frage aus; setze mit `Command(resume=True)` fort und zeige die Bestätigung.
5. **Kontroll-Dialog:** Wiederhole die Gedächtnisfrage mit **anderer** `thread_id` – der Agent erinnert sich **nicht**. Beweis, dass Gedächtnis an den Thread gebunden ist!

## Akzeptanzkriterien
- [ ] Mit gleicher thread_id erinnert sich der Agent an deinen Namen.
- [ ] Mit neuer thread_id ist das Gedächtnis leer.
- [ ] Der sensitive Lauf stoppt **vor** dem Anlegen und zeigt die Interrupt-Frage.
- [ ] Erst `Command(resume=True)` (mit gleichem Config) führt die Aktion aus.

## Hinweise
1. Interrupt lesen: Der Rückgabewert des invoke im pausierten Zustand enthält die Interrupt-Daten (in `__interrupt__`).
2. `from langgraph.types import interrupt, Command`
3. `Command(resume=True)` **mit demselben** `config` aufrufen – sonst findet LangGraph den angehaltenen Vorgang nicht.
4. Offline: Gedächtnis und Interrupt laufen komplett ohne Key – nur die Formulierungen sind simuliert.

## Reflexionsfragen
1. Warum funktioniert `interrupt()` ohne Checkpointer nicht? (Denk an die Fortsetzung: Woher weiß der Graph, wo er weitermachen soll?)
2. Was wäre das Äquivalent zu „Long-Term-Memory" über **Monate** – und warum ist ein thread-Checkpointer das noch nicht? (Stichwort: Store, Stufe 9/10 Ausblick)
3. Welche Aktionen würdest du in einem echten System **nie** ohne Freigabe erlauben – und welche gezielt doch?

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| „Agent vergisst alles" | Checkpointer + thread_id gesetzt? |
| Interrupt wird ignoriert | Checkpointer fehlt oder nicht im Agent registriert |
| Lauf findet angehaltenen Zustand nicht | resume mit **identischem** config aufrufen |

## Referenzlösung
→ [`solutions/memory_approval_agent.py`](../solutions/memory_approval_agent.py)

## Code-Walkthrough
In der Lösungsdatei; besonders das Freigabe-Tool und die resume-Logik in `main()`.

## Was haben wir gelernt?
Checkpointer/Threads, Kurzzeit-Gedächtnis, Interrupt + Command für Human-in-the-Loop.

## Was kommt als Nächstes?
Ein Agent ist ein Team-Mitglied. **Stufe 7** baut das Büro: mehrere Agenten, ein Supervisor, der koordiniert, Subgraphs als abgeschlossene Abteilungen und parallele Ausführung.
