# Aufgabe 4.2 – Graph-Datenbanken: Neo4j & Cypher 🗄️

**Schwierigkeit:** Mittel · **Zeit:** ~60 Min · **Docker für den echten Teil** · **Offline-Fallback vorhanden**

## Lernziel
Du startest Neo4j (Docker), schreibst deine ersten Cypher-Abfragen und verbindest Python mit der Datenbank – mit MERGE-Idempotenz, Parametern und Fallback.

## Warum das wichtig ist
Der GraphStore (4.1) lebt im RAM und kann nur einfache Traversals. Neo4j löst beides: **Persistenz** + eine mächtige Abfragesprache. **Metapher – Cypher als ASCII-Art:** Du *zeichnest* das gesuchte Muster wörtlich: `MATCH (a:Person)-[:WORKS_FOR]->(c) RETURN a, c` – Pfeil, Klammern, Label. Wer Graphen denken kann, kann Cypher lesen.

## Deine Mission
**Teil 1 – Setup (wenn Docker vorhanden):**
```bash
docker run -d --name neo4j-academy -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/lernakademie neo4j:5
```
1. Lege den Firmen-Graph im Browser (http://localhost:7474) per Cypher an (`CREATE`/`MATCH`+`CREATE`); tippe die vier Muster aus der Lösung.
**Teil 2 – immer möglich (Fallback):**
2. Führe `solutions/cypher_practice.py` aus – dieselben Muster laufen gegen den GraphStore; **Sicherheits-Experiment:** probiere `CREATE`/`DELETE` und beobachte die Ablehnung (lesender Subset!).
**Teil 3 – Python-Brücke:**
3. `solutions/python_neo4j_bridge.py`: `verbinde()` (Timeout, `None` bei Ausfall), Graph per **MERGE** laden (idempotent!), Abfragen mit **Parametern** (`$name`), Fallback auf GraphStore mit Hinweis.

## Akzeptanzkriterien
- [ ] Die vier MATCH-Muster liefern korrekte Ergebnisse (Browser oder Fallback).
- [ ] Schreibende Befehle werden im Fallback abgelehnt – du verstehst das als Schutzprinzip.
- [ ] Doppeltes Ausführen des Lade-Skripts erzeugt **keine** Duplikate (MERGE).
- [ ] Abfragen nutzen Parameter statt f-Strings – du kannst das Injection-Risiko erklären.

## Hinweise
1. MERGE = „finde oder lege an" – das Neo4j-Äquivalent von Entity Resolution.
2. Ohne Docker läuft alles im Fallback – die Aufgabe bleibt vollständig machbar!
3. Cypher kennt auch ungerichtete Muster `-[r]-`; unser Fallback bleibt bewusst gerichtet (Stufe-4.1-Wissen).

## Reflexionsfragen
1. SQL-JOIN vs. Kante: Wie viele „Sprünge" bräuchte eine relationale DB für „Wer arbeitet an AI Assistant?" – und warum skaliert Graph-Traversal besser?
2. Warum sind Cypher-Parameter mehr als Bequemlichkeit? (Denk an Modul 8: LLM-generierte Abfragen + Injection!)
3. Was müsste passieren, bevor dein Build-3-Assistent **schreibend** auf Neo4j darf? (→ Freigabe, Aufgabe 5.4!)

## Referenzlösung + Walkthrough
→ [`solutions/cypher_practice.py`](../solutions/cypher_practice.py), [`solutions/python_neo4j_bridge.py`](../solutions/python_neo4j_bridge.py)

## Weiter
🚀 [`../05-build3-langgraph-graphrag/`](../../05-build3-langgraph-graphrag/README.md) – **Build 3**: beide Wissenssysteme (Vektor + Graph) unter einer LangGraph-Steuerung.
