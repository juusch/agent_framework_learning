# Aufgabe 11.2 – Python ↔ Neo4j: die Brücke 🌉

## Schwierigkeit
Mittel · **Kosten: keine** · **Offline-Fallback vorhanden**

## Lernziel
Du verbindest Python mit Neo4j, lädst den Firmen-Graph per Skript und liest Ergebnisse strukturiert aus – mit automatischem Fallback auf den GraphStore, wenn Neo4j nicht läuft.

## Warum ist das wichtig?
LLM-Agenten (Stufe 12+!) „sprechen" nicht direkt mit Neo4j – **dein Python** ist die Brücke: Es baut die Verbindung auf, sendet Cypher, übersetzt Ergebnisse. Genau diese Brücke wirst du in Stufe 14 als Tool einem Agenten geben. Wer sie versteht, versteht das ganze System.

## Das Konzept einfach erklärt
**Metapher – der Dolmetscher:** Python ist der Dolmetscher zwischen zwei Welten: dem Agenten (der Fragen stellt und Wörter versteht) und der Datenbank (die Cypher versteht und Daten hat). Der Dolmetscher übersetzt in beide Richtungen – und darf nie „einfach weiterreden", wenn eine Seite schweigt (Fehlerbehandlung!).

## Die technische Erklärung
- Treiber: `from neo4j import GraphDatabase; driver = GraphDatabase.driver(uri, auth=(user, passwort))` – URI: `bolt://localhost:7687`.
- Session + `run`: `with driver.session() as session: ergebnis = session.run(cypher)` – jeder Datensatz ist ein Dict-ähnliches Objekt (`.data()` liefert echte Listen von Dicts).
- **Parameter** (Sicherheit!): `session.run("MATCH (n:Person {name: $name}) RETURN n", name="Anna")` – niemals Strings in Cypher einsetzen (`f"..."` = SQL-Injection-Gefahr in Cypher-Form!).
- **Fallback-Muster** (die Akademie-Signatur): Erst Verbindungsversuch, bei Fehler klarer Hinweis + Weiterarbeit mit `GraphStore`. Der Lernende kann also JEDE Aufgabe machen.

## Voraussetzungen
- Aufgabe 11.1 (Cypher-Grundlagen), Docker oder Fallback

## Deine Mission
Baue `python_neo4j_bridge.py`:
1. Funktion `verbinde()` → liefert einen Neo4j-Treiber ODER `None` (mit Timeout-Schutz, try/except).
2. Funktion `lade_firmen_graph(session)` → erzeugt den Firmen-Graph in Neo4j (`MERGE` statt `CREATE` – idempotent, mehrfaches Ausführen erzeugt keine Duplikate!).
3. Funktion `frage(session, cypher, **parameter)` → führt Abfrage aus und liefert `.data()`-Ergebnisse.
4. `main()`: Wenn Verbindung → echtes Neo4j; sonst **Fallback** auf `GraphStore` mit demselben Mini-Cypher, plus Hinweis-Ausgabe.
5. Teste vier Abfragen (aus 11.1) in beiden Modi.

## Akzeptanzkriterien
- [ ] Das Skript läuft **mit** Neo4j (lädt Graph, fragt ab) und **ohne** (Fallback + Hinweis).
- [ ] `MERGE` verhindert Duplikate bei mehrfachem Lauf.
- [ ] Die Abfragen nutzen **Parameter** (`$name`), keine String-Einsetzung.
- [ ] Fehler (falsches Passwort, DB aus) führen zu klaren Meldungen, keinem Crash.

## Hinweise
1. Idempotenz: `MERGE (n:Person {name: 'Anna'})` – „finde oder lege an".
2. Verbindungs-Timeout: `GraphDatabase.driver(uri, auth=..., connection_timeout=3)` – und alles in try/except.
3. Der Fallback nutzt `GraphStore.run_cypher` – derSubset aus 11.1.
4. neo4j-Paket ist in `requirements.txt` (`neo4j>=5.0`).

## Reflexionsfragen
1. Warum ist `MERGE` für Skripte besser als `CREATE` – was wäre das Äquivalent beim RAG-Index (Stufe 4: `add_documents` mehrfach ausgeführt)?
2. Warum sind Cypher-Parameter mehr als Bequemlichkeit? (Denk an Stufe 9: Prompt-Injection + „LLM erzeugt Cypher" = doppelt gefährlich!)
3. Wo genau liegt die Verantwortung für Fehlerbehandlung: beim Treiber, beim Skript oder beim Agenten? Begründe deine Architektur-Entscheidung.

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| `ServiceUnavailable` | Neo4j läuft nicht / falscher Port → Fallback greift |
| Duplikate nach mehrfachem Lauf | `MERGE` statt `CREATE` |
| Injection-Risiko mit f-Strings | Parameter `$name` nutzen |

## Referenzlösung
→ [`solutions/python_neo4j_bridge.py`](../solutions/python_neo4j_bridge.py)

## Code-Walkthrough
In der Lösungsdatei; besonders das Verbindungs-und-Fallback-Muster und die parametrisierten Abfragen.

## Was haben wir gelernt?
Treiber, Sessions, MERGE-Idempotenz, Cypher-Parameter als Sicherheits-feature, robustes Fallback-Design.

## Was kommt als Nächstes?
Die Brücke steht. **Stufe 12** bringt die Revolution: Ein LLM liest natürlichsprachigen Text und **extrahiert daraus** Entitäten und Beziehungen – dein Graph füllt sich selbst.
