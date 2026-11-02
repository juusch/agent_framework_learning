# Aufgabe 10.3 – Beziehungen abfragen & Traversierung 🔍

## Schwierigkeit
Leicht · **Kosten: keine**

## Lernziel
Du beantwortest Fragen über deinen Graph: direkte Nachbarn, Kanten-Typen, Pfade – die Grundbewegung des **Graph-Traversal**.

## Warum ist das wichtig?
Das ist der eigentliche Grund, Knowledge Graphs zu bauen: Fragen, die **Verbindungen** betreffen („Wer arbeitet an X?", „Wie hängen A und B zusammen?"), beantwortet Traversierung exakt – während Vektor-Suche nur „ähnliche Texte" liefert. Genau diese Abfragen wirst du in Stufe 12–14 einem LLM als Werkzeug geben.

## Das Konzept einfach erklärt
**Metapher – U-Bahn-Fahren im Gehirn:** Von Station Anna fährst du alle Linien ab, die dort abgehen (neighbors). Jede Linie hat einen Namen (WORKS_FOR). Möchtest du wissen, ob Anna „irgendwie" mit dem Projekt verbunden ist, fährst du Umwege – der Route-Planner findet den kürzesten Weg (`path`). Ein Umweg mit 2 Stationen ist eine Antwort, die **in keinem Text steht** – sie entsteht durch Fahren.

## Die technische Erklärung
- `store.neighbors(node_id)` → Liste `(kante, ziel_node)`: alle ausgehenden Verbindungen.
- `store.neighbors(node_id, "WORKS_FOR")` → nur ein Kanten-Typ (gefiltertes Traversal).
- `store.relationships("WORKS_FOR")` → alle Kanten dieses Typs im Graph.
- `store.path(start_id, ziel_id)` → kürzester Pfad (Breitensuche) oder `None` – „sind die beiden verbunden?" in einem Aufruf.
- **Wichtig:** Traversal ist gerichtet! `A → B` heißt nicht `B → A`. (Neo4j kennt ungerichtete Abfragen; unser Offline-Store bleibt bewusst einfach.)

## Voraussetzungen
- Aufgaben 10.1–10.2

## Deine Mission
Baue `graph_queries.py` auf dem Firmen-Graph (nutze `baue_beispiel_graph()` oder baue eigenen):
1. **Direkte Nachbarn:** Alle ausgehenden Verbindungen von Anna – mit Typ und Zielname.
2. **Gefiltert:** Nur Annas `WORKS_FOR`-Kante (inkl. Property `seit`).
3. **Überblick:** Alle `WORKS_FOR`-Kanten im Graph (wer arbeitet wo?).
4. **Pfadfrage:** Existiert ein Pfad von Engineering zu „AI Assistant"? Und von Ben zu „AI Assistant"? Gib beide Ergebnisse aus und **erkläre** das `None`.
5. **Zweistufiges Traversal:** Finde über `neighbors` von Anna, dann von deren Nachbarn, ob Anna (über Engineering) mit dem Projekt verbunden ist – in zwei Schritten, ohne `path` zu benutzen.

## Akzeptanzkriterien
- [ ] Alle fünf Abfragen liefern strukturierte Ausgaben.
- [ ] Die `None`-Erklärung (Ben → Projekt) ist nachvollziehbar begründet.
- [ ] Die zweistufige Traversierung nutzt **zwei** `neighbors`-Aufrufe.
- [ ] Du kannst „gerichtet" in einem Satz erklären.

## Hinweise
1. `for kante, ziel in store.neighbors(anna_id): print(kante.typ, "→", ziel.properties["name"])`
2. Kanten-Property auslesen: `kante.properties.get("seit")`
3. Beim zweistufigen Traversal: Nimm `BELONGS_TO`-Nachbarn von Anna (Engineering), dann dort `WORKS_ON`.

## Reflexionsfragen
1. „Anna arbeitet an AI Assistant" steht so **nirgends** als direkte Kante – wie hast du es trotzdem beantwortet? Was macht das mit dem Begriff „Wissen"?
2. Warum liefert `path(Ben, Projekt)` None – obwohl beide mit Acme verbunden sind? (Richtung! Ben → Acme, aber kein Weg Ben → … → Projekt.)
3. Was würde ein LLM tun, um diese Frage zu beantworten, wenn es nur Text hätte? Und warum ist das Ergebnis dort unsicher?

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| `path(a, b)` None erwartet andersrum | Richtung beachten: `path(b, a)` probieren |
| `neighbors` gibt Paare, nicht Nodes | `for kante, ziel in ...` entpacken |
| `None`-Ergebnis als Bug missverstanden | None ist die Antwort: „kein Pfad" |

## Referenzlösung
→ [`solutions/graph_queries.py`](../solutions/graph_queries.py)

## Code-Walkthrough
In der Lösungsdatei; besonders die zweistufige Traversierung als explizite Schleifen.

## Was haben wir gelernt?
Nachbarn, gefilterte Traversierung, Pfade, Gerichtetheit, emergente Antworten.

## Was kommt als Nächstes?
„Was du siehst, verstehst du": 10.4 visualisiert deinen Graph (Mermaid) und bereitet die grafische Exploration vor, die später im Frontend (Stufe 15) interaktiv wird.
