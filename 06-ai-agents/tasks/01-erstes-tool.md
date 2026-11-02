# Aufgabe 6.1 – Dein erstes Tool 🛠️

## Schwierigkeit
Leicht · ⚠️ **Kosten:** nur mit Key (offline: Tool-Calling wird simuliert)

## Lernziel
Du gibst einem LLM Zugang zu einer **eigenen Python-Funktion** und siehst zu, wie es entscheidet, sie zu benutzen – der Grundstein aller Agenten.

## Warum ist das wichtig?
Ohne Tools kann ein LLM nur *reden*. Mit Tools kann es *handeln*: rechnen, nachschlagen, Dateien lesen, APIs aufrufen. Genau hier verwandelt sich „Chatbot" in „Agent".

## Das Konzept einfach erklärt
**Metapher:** Du stellst einem neuen Mitarbeiter einen Werkzeugkasten auf den Tisch und sagst: „Das hier ist ein Taschenrechner. Benutz ihn, wenn du exakt rechnen musst." Der Mitarbeiter (das LLM) entscheidet selbst, ob er das Werkzeug braucht. Wichtig: Das Werkzeug macht **dein Python-Code** – das Modell *entscheidet* nur über den Einsatz und formuliert die Antwort.

## Die technische Erklärung
1. **Tool definieren:** eine Funktion + `@tool`-Dekorateur (aus `langchain_core.tools`). Der **Docstring** ist entscheidend – er ist die „Bedienungsanleitung", die das Modell liest, um zu entscheiden, ob das Werkzeug passt!
2. **Agent erstellen:** `create_agent(model, tools, system_prompt)` (aus `langchain.agents`) – baut intern einen LangGraph-Graphen: LLM → (eventuell) Tool → LLM → Antwort.
3. **Ablauf:** Das Modell erhält die Nachricht + Tool-Beschreibungen. Will es ein Tool nutzen, liefert es einen strukturierten `tool_call` (Name + Argumente). LangGraph führt dein Python aus, gibt das Ergebnis als `ToolMessage` zurück, und das Modell formuliert die finale Antwort.
4. Der Agent selbst ist ein Runnable: `.invoke({"messages": [...]})` – das State-Feld `messages` ist der Gesprächsverlauf (du kennst das Prinzip aus Stufe 2!).

## Voraussetzungen
- Stufe 5 (Graphen-Mechanik: State, Nodes, Loop – der Agent ist genau so ein Loop!)

## Deine Mission
Baue `first_tool_agent.py`:
1. Tool `wortzaehler(text: str)`: zählt Wörter (Docstring: „Zählt die Wörter eines Texts.").
2. Agent mit dem Akademie-Modell (`get_chat_model()`), dem Tool und der System-Prompt „Du bist ein Assistent, der Text-Statistiken liefert."
3. Frage den Agenten: „Wie viele Wörter hat der Satz: LangGraph macht Workflows steuerbar?" – gib die **finale Antwort** aus.
4. Kontrollfrage (Antwort per Print): „Erkläre, was ein Embedding ist." – der Agent sollte das Tool **nicht** benutzen.
5. Gib zur Kontrolle die **Typen der Nachrichten** im Ergebnis-State aus (`type(m).__name__` für jede Message) – so siehst du den Loop: HumanMessage → AIMessage(tool_calls) → ToolMessage → AIMessage.

## Akzeptanzkriterien
- [ ] Bei der Zähl-Frage liefert der Agent die korrekte Zahl (offline: simuliert über dein echtes Tool!).
- [ ] Der Docstring des Tools ist aussagekräftig.
- [ ] Die Nachrichten-Typen zeigen den Agenten-Loop (mit ToolMessage).
- [ ] Bei der Kontrollfrage kommt eine Antwort ohne Tool-Call.

## Hinweise
1. `from langchain_core.tools import tool` und `from langchain.agents import create_agent`
2. Finale Antwort: `ergebnis["messages"][-1].content`
3. Offline-Erinnerung: Die Simulation wählt ein Tool, wenn der **Tool-Name** in deiner Eingabe vorkommt – formuliere die Frage mit dem Tool-Namen (z. B. „nutze den wortzaehler").

## Reflexionsfragen
1. Warum ist der Docstring fast so wichtig wie der System-Prompt?
2. Wer führt die eigentliche Berechnung aus – das Modell oder dein Python? Was bedeutet das für die **Zuverlässigkeit** der Antwort?
3. Wo erkennst du in der Nachrichtenliste die „Beobachtung" im Planen-Handeln-Beobachten-Zyklus?

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| `tool_calls`-Format-Fehler beim Selbstbau | nicht selbst bauen – `create_agent` nutzen |
| Agent antwortet, ohne das Tool zu nutzen | Frage präziser stellen / Docstring schärfen (mit Key); offline: Tool-Namen nennen |
| Tool wirft TypeError | Argument-Namen der Funktion = Namen im tool_call prüfen |

## Referenzlösung
→ [`solutions/first_tool_agent.py`](../solutions/first_tool_agent.py)

## Code-Walkthrough
In der Lösungsdatei; besonders die Tool-Definition und die Nachrichten-Analyse.

## Was haben wir gelernt?
Tools definieren, Agent erstellen, Agenten-Loop in den Nachrichten lesen.

## Was kommt als Nächstes?
Ein Werkzeug war ein Beweis. Aufgabe 6.2 gibt dem Agenten eine **Werkzeugkiste** – und beobachtet, wie er wählt.
