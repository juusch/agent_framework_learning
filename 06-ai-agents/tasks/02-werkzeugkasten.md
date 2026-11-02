# Aufgabe 6.2 – Der Werkzeugkasten: Agent mit mehreren Tools 🧰

## Schwierigkeit
Leicht · ⚠️ **Kosten:** nur mit Key

## Lernziel
Du baust einen Agenten mit **mehreren** Tools (Taschenrechner, Uhrzeit, Zufall) und untersuchst, wie die Tool-Auswahl funktioniert.

## Warum ist das wichtig?
Echte Agenten haben 5–20 Tools. Die spannende Frage ist nicht mehr „kann er ein Tool benutzen", sondern **„wählt er das richtige?"** – und was passiert, wenn Werkzeuge sich in ihren Beschreibungen überlappen.

## Das Konzept einfach erklärt
**Metapher:** Der Handwerker bekommt einen **ganzen Kasten**: Hammer, Zange, Bohrer. Auf jedem Werkzeug steht ein Schild (Docstring), was es kann. Der Auftrag entscheidet die Auswahl. Überlappen zwei Schilder („zum Schlagen" / „zum Klopfen"), wird die Wahl zufälliger – **gute Schilder sind gutes Agentendesign**.

## Die technische Erklärung
- `create_agent(model, tools=[tool_a, tool_b, tool_c], system_prompt=...)` – alle Tools werden dem Modell mit Name, Beschreibung und **Argument-Schema** (aus den Typ-Hints!) angekündigt.
- Das Modell wählt per tool_call **Name + Argumente**. Aus einem String-Parameter macht es z. B. `"12 * 7"`.
- **Sicher in Tools:** Tools sind normaler Python-Code – Exceptions darin stoppen den Agenten; fange sie im Tool ab und gib eine verständliche Fehlermeldung als String zurück (der Agent kann darauf reagieren!). Das ist die Basis von Fehlerrobustheit (Stufe 8).

## Voraussetzungen
- Aufgabe 6.1

## Deine Mission
Baue `toolbox_agent.py` mit **drei** Tools:
1. `taschenrechner(expression: str)` – werte mathematische Ausdrücke sicher aus (Tipp: `eval` nie mit rohen Nutzereingaben! Nutze eine Whitelist oder `ast.literal_eval`-Stil; unsere Lösung parst einfache `zahl operator zahl`-Muster selbst).
2. `uhrzeit()` – liefert die aktuelle Uhrzeit formatiert (`datetime.now().strftime("%H:%M")`).
3. `zufallszahl(minimum: int, maximum: int)` – `random.randint`, mit Absicherung gegen Minimum > Maximum.

Dann:
4. System-Prompt: „Du bist ein Alltags-Assistent und nutzt deine Werkzeuge, wann immer exakte Antworten nötig sind."
5. Stelle drei Anfragen (je eines der Tools betreffend) und eine Anfrage **ohne** Tool-Bedarf.
6. Auswertung: Gib pro Anfrage aus, welches Tool (falls eines) benutzt wurde – aus `ergebnis["messages"]` die `tool_calls` lesen.

## Akzeptanzkriterien
- [ ] Drei Tools mit sauberen Docstrings und Typ-Hints sind registriert.
- [ ] Der Rechner verarbeitet mind. `12 * 7` korrekt (offline: dein Python rechnet!).
- [ ] Ungültige Rechner-Eingaben (`"abc"`) führen zu einer **freundlichen Fehlermeldung**, nicht zum Absturz.
- [ ] Die Auswertung zeigt pro Anfrage das gewählte (oder kein) Tool.

## Hinweise
1. Tool-Schema kommt aus den Funktions-Parametern: `def taschenrechner(expression: str) -> str:` – Name & Typ-Hints nicht schlampen!
2. Tool-Loop analysieren: `[m for m in ergebnis["messages"] if getattr(m, "tool_calls", None)]`
3. Offline: Tool-Namen in den Anfragen nennen („…mit dem taschenrechner…").

## Reflexionsfragen
1. Warum verbietet man `eval` mit Nutzereingaben – und was wäre das Schlimmste, das ein „kreativer" Nutzer über einen Agenten anstellen könnte? (Sicherheitsstichwort: Prompt-Injection, mehr in Stufe 9)
2. Zwei Tools mit fast gleichem Docstring – was passiert mit der Auswahl? Wie verhinderst du das?
3. Warum geben Tools **Strings** zurück, auch wenn das Ergebnis eine Zahl ist? (Tipp: Wie „liest" das Modell das Ergebnis?)

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| Tool-Absturz killt den Agenten | try/except **im** Tool, Fehler als Text zurückgeben |
| Falsches Tool gewählt | Docstrings unterscheidbarer formulieren |
| `minimum > maximum` – Randfall | im Tool absichern und klar melden |

## Referenzlösung
→ [`solutions/toolbox_agent.py`](../solutions/toolbox_agent.py)

## Code-Walkthrough
In der Lösungsdatei; besonders der sichere Mini-Parser statt `eval`.

## Was haben wir gelernt?
Multi-Tool-Registrierung, Tool-Auswahl, Fehlersicherheit in Tools.

## Was kommt als Nächstes?
Der Werkzeugkasten wird nützlich, wenn die Werkzeuge **Wissen** zugänglich machen: Aufgabe 6.3 verbindet deinen Stufe-4-RAG mit einem Agenten – der Wissens-Agent kann auf Anfrage in den Handbüchern nachschlagen.
