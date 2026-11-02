# Stufe 11 – Graph-Datenbanken: Neo4j & Cypher 🗄️

**Ziel:** Du überträgst dein Graph-Verständnis in eine **echte Graph-Datenbank**: Neo4j installieren, Daten anlegen, mit **Cypher** abfragen, aus Python verbinden.

## Warum eine Graph-Datenbank?

Dein `GraphStore` (Stufe 10) lebt im RAM – Programm zu, Daten weg. Und: Er kennt nur einfache Traversals. Eine Graph-Datenbank löst beides:

| | Relationale DB (SQL) | Graph-DB (Neo4j) |
|---|---|---|
| Denkt in | Tabellen, Zeilen, Fremdschlüssel | Nodes, Kanten direkt gespeichert |
| „Wer arbeitet an X?" | JOINs über 3 Tabellen (Aufwand wächst mit Tiefe) | Kanten folgen – **Aufwand wächst NICHT mit Datenmenge** |
| Schema | starr, vorher definiert | flexibel (Labels statt Tabellen) |
| Beziehungen | implizit (per IDs reconstruierbar) | **Daten erster Klasse** |

**Metapher:** Eine relationale DB ist ein Formularstapel – um herauszufinden, wer mit wem verbunden ist, musst du Stapel durchblättern und Nummern abgleichen. Eine Graph-DB ist das Ermittlungsbrett selbst: Der Faden **ist** die gespeicherte Verbindung.

Und gegenüber der **Vektor-DB** (Stufe 4): Vektor-DBs finden *sinngleiche Texte* (unscharf, nach Bedeutung), Graph-DBs folgen *exakten Verbindungen* (strukturiert, nach Beziehung). In Stufe 13 kombinierst du beide (GraphRAG).

## Neo4j-Sprach-ABC: Cypher

Cypher ist die Abfragesprache von Neo4j – ASCII-Art für Graphen:

```cypher
MATCH (a:Person {name: 'Anna'})-[:WORKS_FOR]->(c:Company)
RETURN a, c
```

Du **zeichnest** das Muster, das du suchst: `(a:Person)` Node mit Label, `[:WORKS_FOR]` Kante, `->` Richtung. Das erinnert dich an etwas? Richtig – unser Mini-Cypher im `GraphStore` ist absichtlich syntaktisch gleich, damit du im Offline-Modus dieselben Muster übst!

## Setup (zwei Wege)

### Weg A: Docker (empfohlen)

```bash
docker run -d --name neo4j-academy \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/lernakademie \
  neo4j:5
```

Dann im Browser: <http://localhost:7474> – Login `neo4j` / `lernakademie`.

### Weg B: Offline-Fallback (ohne Docker)

**Kein Docker? Kein Problem** – die Akademie bleibt nutzbar:
1. Der `GraphStore` akzeptiert denselben (kleinen) Cypher-Subset.
2. Die Referenzlösungen prüfen automatisch, ob Neo4j erreichbar ist – sonst laufen sie gegen den `GraphStore` und drucken einen Hinweis.

## Aufgaben

| # | Aufgabe | Schwierigkeit | Neo4j nötig? |
|---|---|---|---|
| 11.1 | [`tasks/01-neo4j-setup-und-cypher.md`](tasks/01-neo4j-setup-und-cypher.md) – Setup + erste Cypher-Abfragen | Leicht | für den echten Teil: ja; Fallback offline |
| 11.2 | [`tasks/02-python-und-neo4j.md`](tasks/02-python-und-neo4j.md) – Python-Anbindung + Firmen-Graph laden | Mittel | ja / Fallback offline |

## Ausführen

```bash
python3 11-graph-databases/solutions/cypher_practice.py
python3 11-graph-databases/solutions/python_neo4j_bridge.py
```

## Aktuelle API-Referenz

- [Neo4j Python-Treiber](https://neo4j.com/docs/python-manual/current/)
- [LangChain Neo4j-Integration](https://python.langchain.com/docs/integrations/graphs/neo4j/)
- [Neo4j Sandboxes (kostenlos, keine Installation)](https://neo4j.com/sandbox/)

## Danach
Weiter mit [`../12-graphs-und-llms/`](../12-graphs-und-llms/README.md): Du lässt ein LLM aus Text **automatisch** Entitäten und Beziehungen extrahieren und den Graph füllen.
