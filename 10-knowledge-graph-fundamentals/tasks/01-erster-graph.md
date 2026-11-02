# Aufgabe 10.1 – Dein erster Graph (in reinem Python) 🕸️

## Schwierigkeit
Anfänger · **Kosten: keine** · **Datenbank: keine nötig**

## Lernziel
Du baust einen Knowledge Graph aus dem Nichts: Entitäten als Nodes, Verbindungen als Relationships – in reinem Python.

## Warum ist das wichtig?
Graphen sind die Datenstruktur für **strukturiertes Wissen**: Wer arbeitet wo? Wer arbeitet woran? Solche Fragen beantwortet Vektor-Suche nur schwach (sie findet ähnliche *Texte*), ein Graph *traversiert exakte Verbindungen*. Bevor du in Stufe 11 eine Datenbank installierst, verstehst du hier das Modell – das ist derselbe Lernpfad wie „erst Variablen, dann Datenbanken".

## Das Konzept einfach erklärt
**Metapher – das Ermittlungsbrett aus Krimiserien:** Die Ermittler stecken Fotos (Nodes) an eine Pinnwand und verbinden sie mit roten Fäden (Relationships): „Anna → arbeitet für → Acme". Jedes Foto hat Notizen (Properties: Name, Rolle). Nach einem *Faden* zu gehen (Traversal) enthüllt Muster, die auf keinem einzelnen Foto stehen.

Die Kern-Erkenntnis: **Der Graph speichert Verbindungen als Daten** – nicht als Sätze in einem Text. Dadurch ist „Wer arbeitet an Projekt X?" eine strukturelle Frage (Fäden folgen), keine Textsuche.

## Die technische Erklärung
Wir nutzen den `GraphStore` aus `lernakademie/graph_store.py` (den Offline-Pendant zu Neo4j, genau wie MockChatModel der Pendant zum LLM ist):
- `store.add_node(["Person"], name="Anna", rolle="Entwicklerin")` → legt einen Node mit **Label** und **Properties** an und liefert eine **ID**.
- `store.add_relationship(anna_id, acme_id, "WORKS_FOR", seit=2021)` → gerichtete Kante mit Typ und Properties.
- IDs sind wichtig: Beziehungen verbinden IDs, nicht Namen (zwei Personen können „Anna" heißen!).

## Voraussetzungen
- Stufe 1 (Dictionaries, Funktionen)

## Deine Mission
Baue `first_graph.py`:
1. Erzeuge einen leeren `GraphStore`.
2. Lege die vier Entitäten aus dem Firmen-Beispiel an: Anna (Person), Acme (Company), Engineering (Department), „AI Assistant" (Project) – jeweils mit mindestens einer Property.
3. Verbinde sie: Anna WORKS_FOR Acme, Anna BELONGS_TO Engineering, Engineering WORKS_ON AI Assistant. Vergiss nicht: **IDs merken!**
4. Gib aus: Anzahl Nodes, Anzahl Relationships, und alle Nodes mit ihren Labels.
5. Prüfe mit `store.find_node("Person", name="Anna")`, dass du Anna wiederfindest.

## Akzeptanzkriterien
- [ ] 4 Nodes mit Labels und mindestens je 1 Property existieren.
- [ ] 3 Relationships sind gerichtet angelegt (IDs, nicht Namen!).
- [ ] Die Ausgabe zeigt strukturiert Nodes und Kanten.
- [ ] Du kannst in einem Satz erklären, warum Beziehungen IDs statt Namen verbinden.

## Hinweise
1. IDs in Variablen sichern: `anna_id = store.add_node(...)` – dann `store.add_relationship(anna_id, acme_id, "WORKS_FOR")`.
2. Relationship-Typen in GROSSBUCHSTABen sind Konvention (WORKS_FOR, BELONGS_TO).
3. `print`-Ausgaben pro Schritt helfen, den Aufbau nachzuvollziehen.

## Reflexionsfragen
1. Was wäre verloren, wenn du dasselbe Wissen nur als Fließtext speicherst? Formuliere eine Frage, die der Text schwer, der Graph leicht beantwortet.
2. Warum sind Labels mehr als nur „Kategorien" – was erlauben sie in Abfragen später?
3. Zwei Leute heißen „Anna": Warum wäre `add_relationship("Anna", ...)` (per Name) ein Design-Fehler?

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| `add_relationship` wirft ValueError | IDs nicht gespeichert/gemischt – Nodes zuerst anlegen, IDs in Variablen |
| Properties fehlen | `add_node(["Person"], name="...")` – Properties als Schlüsselwort-Argumente |
| Relationship-Typ klein geschrieben | Konvention GROSSBUCHSTABEN (später bei Cypher wichtig) |

## Referenzlösung
→ [`solutions/first_graph.py`](../solutions/first_graph.py)

## Code-Walkthrough
In der Lösungsdatei, Zeile für Zeile kommentiert.

## Was haben wir gelernt?
Nodes, Labels, Properties, Relationships, ID-basierte Verbindungen.

## Was kommt als Nächstes?
Dein Graph existiert – jetzt willst du **Antworten** daraus ziehen: Aufgabe 10.2 vertieft Entitäten mit Properties, 10.3 fragt Beziehungen ab, 10.4 visualisiert alles.
