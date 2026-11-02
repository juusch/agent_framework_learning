# Aufgabe 6.2 – Gedächtnis, Checkpointer & Freigaben 🧠✋

**Schwierigkeit:** Mittel · **Zeit:** ~60 Min · **Kosten:** keine (offline komplett)

## Lernziel
Du gibst einem Agenten Kurzzeit-Gedächtnis über mehrere Aufrufe (Checkpointer + `thread_id`) und baust Human-in-the-Loop mit `interrupt()`/`Command(resume=...)`.

## Warum das wichtig ist
Ohne Checkpointer vergisst der Agent alles zwischen zwei Aufrufen. Und: Agenten mit Nebenwirkungen brauchen einen Stopp vor der Ausführung – der Interrupt ist der Airbag (du kennst ihn schon aus Build 3; hier siehst du die Mechanik isolated und als handgebauter Agent-Loop).

## Konzepte
- **Checkpointer = Vorgangsordner:** gleiche `thread_id` = gleiches Gespräch; neue ID = leeres Blatt.
- **Interrupt = Vier-Augen-Prinzip:** der Agent hält den Stift über dem Formular; erst dein `resume=True` schreibt.
- Der Lösungs-Code baut den Agenten-Loop **sichtbar von Hand** (model → tools → model): So verstehst du, was `create_agent` internally tut.

## Deine Mission
1. Agent (handgebaut: `model`-Node + `ToolNode` + `add_messages`-State) mit `MemorySaver` und zwei Tools: `notiz_anlegen`, `geheime_notiz` (mit `interrupt()` **vor** dem Anlegen).
2. **Gedächtnis-Beweis:** Name nennen (Aufruf 1) → „Wie heiße ich?" (Aufruf 2, gleiche thread_id) ✓; dieselbe Frage mit **anderer** thread_id → leer.
3. **Freigabe-Beweis:** Lauf pausiert am Interrupt → Daten aus `__interrupt__` lesen → `Command(resume=True)` → Aktion ausgeführt; **und** `resume=False` → verworfen, kein Crash.
4. Zähle die Nachrichten im Thread-State (`get_state`) – dein Gedächtnis-Nachweis.

## Akzeptanzkriterien
- [ ] Gleiche thread_id erinnert; andere nicht.
- [ ] Der Lauf stoppt VOR der Aktion und zeigt die Interrupt-Frage.
- [ ] `resume=False` verwirft sauber; nichts wurde angelegt.
- [ ] Du kannst erklären, warum `interrupt` ohne Checkpointer nicht funktioniert.

## Hinweise
1. `Annotated[list, add_messages]` (aus `langgraph.graph.message`) – sonst wird die Liste ersetzt statt erweitert!
2. Resume mit **identischem** config.
3. Das ist exakt die Freigabe-Mechanik, die im Finale über HTTP läuft (Modul 7).

## Reflexionsfragen
1. Was wäre „Langzeit-Gedächtnis über Monate" – und warum ist ein thread-Checkpointer es noch nicht?
2. Welche Aktionen würdest du nie ohne Freigabe automatisieren – und welche gezielt doch?
3. Wo läge die Freigabe in einer Web-App? (Tipp: der Interrupt bleibt gleich – nur der Resume-Kanal ist das Frontend!)

## Referenzlösung + Walkthrough
→ [`solutions/memory_approval_agent.py`](../solutions/memory_approval_agent.py)

## Weiter
6.3 – wenn EIN Agent nicht reicht: Parallelität, Subgraphs und der Supervisor.
