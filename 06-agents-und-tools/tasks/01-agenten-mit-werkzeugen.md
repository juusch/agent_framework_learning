# Aufgabe 6.1 – Agenten mit Werkzeugen 🛠️

**Schwierigkeit:** Mittel · **Zeit:** ~60 Min · ⚠️ **Kosten:** nur mit Key (offline: Tool-Calling simuliert)

> **Benötigte Modell-Fähigkeit:** Tool-Calling. Wenn dein (lokales) Modell keine Werkzeuge unterstützt, ruft der Agent Tools nicht auf – dann im Offline-Modus üben (Simulation zeigt den kompletten Loop) oder ein tool-fähiges Modell wählen. Details: [docs/local-ai-server.md](../../docs/local-ai-server.md)

## Lernziel
Du gibst einem LLM Python-Funktionen als **Tools** und beobachtest den Agenten-Loop: planen → Werkzeug wählen → ausführen → antworten.

## Warum das wichtig ist
Ohne Tools kann ein LLM nur *reden*; mit Tools *handelt* es. **Metapher:** Der neue Mitarbeiter bekommt einen Werkzeugkasten; auf jedem Werkzeug steht (Docstring!), wofür es da ist. **Der Docstring ist die Bedienungsanleitung** – der Agent wählt danach!

## Deine Mission
1. **Erstes Tool:** `@tool` + `wortzaehler`; Agent per `create_agent` (aus `langchain.agents` – der aktuellen API); Frage mit Tool-Bedarf; **Kontrollfrage** ohne Tool-Bedarf. Lies die Nachrichtentypen im Ergebnis: `AIMessage(tool_calls)` → `ToolMessage` → finale `AIMessage` = der Loop!
2. **Werkzeugkasten:** drei Tools – `taschenrechner` (**sicherer Mini-Parser statt `eval`!**), `uhrzeit`, `zufallszahl` (Absicherung gegen minimum > maximum). Fehler im Tool = freundliche Rückgabe, kein Crash.
3. **Wissens-Tool:** `handbuch_suche` über den Stufe-3.2-Retriever (Closure-Muster: Index **einmal** bauen!). Der Agent schlägt nur bei Fachfragen nach.

## Akzeptanzkriterien
- [ ] Der Agent wählt passende Tools und lässt die Kontrollfragen ohne Tool laufen.
- [ ] Der Rechner verarbeitet `12 * 7` korrekt; `abc` → klare Fehlermeldung statt Crash.
- [ ] Der Index wird nur einmal pro Programmstart gebaut.
- [ ] Du kannst jeden Schritt des Loops den Nachrichtentypen zuordnen.

## Hinweise
1. `from langchain_core.tools import tool`, `from langchain.agents import create_agent`
2. Offline: die Akademie-Simulation wählt Tools per Tool-**Namen** in der Frage – formuliere accordingly.
3. `ergebnis["messages"][-1].content` ist die finale Antwort.

## Reflexionsfragen
1. Wer führt die Berechnung aus – Modell oder dein Python? Was heißt das für die Zuverlässigkeit?
2. Warum sind überlappende Docstrings gefährlich für die Tool-Auswahl?
3. Wann wäre ein fester Graph (wie in Build 3) besser als ein freier Agent? Nenne je ein Beispiel.

## Referenzlösung + Walkthrough
→ [`solutions/first_tool_agent.py`](../solutions/first_tool_agent.py), [`solutions/toolbox_agent.py`](../solutions/toolbox_agent.py), [`solutions/knowledge_agent.py`](../solutions/knowledge_agent.py)

## Weiter
6.2 – der Agent bekommt ein Gedächtnis über Aufrufe hinweg – und bremst heikle Aktionen.
