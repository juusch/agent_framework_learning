# Aufgabe 11.1 – Neo4j-Setup & erste Cypher-Abfragen 🐳

## Schwierigkeit
Leicht · **Kosten: keine** (Neo4j läuft lokal) · **Offline-Fallback vorhanden**

## Lernziel
Du startest Neo4j (Docker), legst Daten per Cypher an und stellst deine ersten Abfragen – in **Neo4j Browser** und im **GraphStore** (Fallback).

## Warum ist das wichtig?
Cypher ist die Sprache, in der später (Stufe 12) dein LLM „sprechen" wird, damit Agenten Graph-Fragen beantworten können. Du musst die Grundbewegungen flüssig beherrschen: `CREATE`, `MATCH`, `RETURN`, Kanten-Muster, `WHERE`.

## Das Konzept einfach erklärt
**Metapher:** Cypher ist ASCII-Art für Graphen. `(a:Person)-[:WORKS_FOR]->(c)` **zeigt** wörtlich das Bild, das du suchst – Pfeil, Klammern, Label. SQL beschreibt dagegen Verknüpfungslogik abstrakt. Deshalb gilt: Wer Graphen *denken* kann, kann Cypher *lesen*.

## Die technische Erklärung
- `CREATE (n:Person {name: 'Anna'})` – Node anlegen.
- `CREATE (a)-[:WORKS_FOR {seit: 2021}]->(b)` – Kante anlegen (zwischen per MATCH gefundenen Nodes).
- `MATCH (n:Person) RETURN n` – alle Personen.
- `MATCH (a)-[r:WORKS_FOR]->(c) RETURN a.name, c.name, r.seit` – Muster mit Kante + Properties in der Rückgabe.
- Labels, Properties, Richtung – alles Begriffe aus Stufe 10, jetzt in echter Syntax.
- **Neo4j Browser** (http://localhost:7474) rendert Ergebnisse als **klickbaren Graph** – deine Mermaid-Arbeit aus 10.4, nur interaktiv.

## Voraussetzungen
- Stufe 10 (Konzepte!) – idealerweise Docker installiert (Stufe 9.3)

## Deine Mission
**Teil 1 – Setup (wenn Docker vorhanden):**
1. Starte Neo4j (Befehl steht im Level-README; Passwort: `lernakademie`).
2. Öffne den Browser, lege die 5 Nodes des Firmen-Graphs per `CREATE` an, danach die 5 Kanten (erst `MATCH`, dann `CREATE` der Kante).
3. Tippe die vier Abfragen aus der Aufgabe (unten) und beobachte die Visualisierung.

**Teil 2 – dieselben Cypher-Muster im Fallback (immer möglich):**
4. Baue `cypher_practice.py`: nutze `run_cypher` des GraphStore (mit `baue_beispiel_graph()`) für die vier Muster.
5. **Sicherheits-Experiment (wichtig für Stufe 12!):** Probiere `CREATE` und `DELETE` im `run_cypher` – beobachte die **ablehnende Fehlermeldung**, und verstehe: ein lesender Subset ist Schutz gegen aus Versehen (oder per Prompt-Injection!) zerstörte Daten.

Die vier Abfragen:
```cypher
MATCH (n:Person) RETURN n
MATCH (n:Person) WHERE n.name = 'Anna' RETURN n
MATCH (a:Person)-[r:WORKS_FOR]->(c:Company) RETURN a, c
MATCH (a {name: 'Anna'})-[r]->(b) RETURN a, type(r), b
```

## Akzeptanzkriterien
- [ ] Mit Docker: Der Firmen-Graph existiert in Neo4j und ist im Browser sichtbar.
- [ ] Ohne Docker: Alle vier Abfragen laufen über `run_cypher` (Fallback) mit korrekten Ergebnissen.
- [ ] Schreibende Befehle wurden im Fallback **bewusst** ausprobiert und abgelehnt.
- [ ] Du kannst jedes der vier Muster in einem Satz erklären.

## Hinweise
1. Docker-Befehl im Level-README; `docker logs neo4j-academy` zeigt dir den Startfortschritt.
2. Im Browser: mehrere Befehle mit Semikolon trennen oder einzeln senden.
3. Der Fallback-Subset verlangt genau die obigen Muster-Formen – die Fehlermeldung sagt dir, was nicht passt.

## Reflexionsfragen
1. Warum ist die Richtung `(a)->(b)` in Cypher wichtig – was passiert bei `(a)<-(b)`?
2. Vergleiche SQL-JOIN vs. Kante: Wie viele „Sprünge" braucht eine relationale DB für „Wer arbeitet an AI Assistant?" (Personen → Abteilungen → Projekte)?
3. Warum haben wir im Offline-Subset bewusst auf CREATE/DELETE verzichtet – und wann braucht echte Software trotzdem Schreibrechte (und wie schützt man die, Stufe 14)?

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| Docker startet nicht | `docker logs neo4j-academy`; Port frei? `docker rm` alter Container |
| Browser-Login schlägt fehl | Passwort aus dem `docker run`-Befehl (`lernakademie`) |
| Fallback: „kein unterstuetztes Subset" | Muster exakt an obigen Beispielen orientieren |

## Referenzlösung
→ [`solutions/cypher_practice.py`](../solutions/cypher_practice.py)

## Code-Walkthrough
In der Lösungsdatei; inklusive des Sicherheits-Experiments mit abgelehnten Schreibbefehlen.

## Was haben wir gelernt?
Neo4j-Setup, Cypher-Grundmuster, Browser-Visualisierung, Schreibschutz im Offline-Subset.

## Was kommt als Nächstes?
Cyper tippen kannst du – jetzt verbinde **Python** mit der Datenbank: Aufgabe 11.2 baut die Brücke (`neo4j`-Treiber), die später dein LLM nutzen wird.
