# Aufgabe 4.1 – Knowledge Graphs in reinem Python 🕸️

**Schwierigkeit:** Mittel · **Zeit:** ~60 Min · **Kosten:** keine

## Lernziel
Du baust einen Knowledge Graph von Hand: Entitäten (Nodes), Beziehungen (Relationships), Labels, Properties – und beantwortest Fragen durch **Traversierung**.

## Warum das wichtig ist
Wie Build 1 gilt auch hier: erst von Hand bauen, dann die Datenbank verstehen. Die Kern-Erkenntnis: **Der Graph speichert Verbindungen als Daten** – dadurch beantwortet er Fragen, die in keinem Text wörtlich stehen. **Metapher:** Das Ermittlungsbrett: Fotos (Nodes) + Notizen (Properties) + rote Fäden (Beziehungen). Einem Faden nachgehen (Traversal) enthüllt Muster.

## Deine Mission
1. **Erster Graph:** Nutze `lernakademie.graph_store.GraphStore` (der Offline-Pendant zu Neo4j, wie der Mock zum LLM): 4 Entitäten (Anna, Acme, Engineering, AI Assistant) mit Labels + Properties, IDs merken! Dann 3 Beziehungen (Anna WORKS_FOR Acme, Anna BELONGS_TO Engineering, Engineering WORKS_ON AI Assistant).
2. **Modellierung:** Gib Anna zwei Labels (`Person`, `Employee`) – warum Label statt Property `ist_mitarbeiter`? Dokumentiere 3 Modellierungs-Entscheidungen als Kommentar (Kante vs. Property!).
3. **Traversierung:** direkte Nachbarn von Anna; nur `WORKS_FOR`-Kanten; **zweistufig:** Anna → (BELONGS_TO) → Engineering → (WORKS_ON) → Projekt. Und: `path(Ben, Projekt)` → `None` – erkläre die Gerichtetheit!
4. **Visualisierung:** `store.to_mermaid()` in eine `diagramm.md` schreiben – GitHub rendert deinen Graph.

## Akzeptanzkriterien
- [ ] Nodes verbinden **IDs**, nicht Namen – du kannst begründen, warum.
- [ ] Die zweistufige Traversierung läuft mit zwei `neighbors`-Aufrufen.
- [ ] Das `None`-Ergebnis ist erklärt (Richtung der Kanten).
- [ ] `diagramm.md` zeigt den Graphen gerendert.

## Hinweise
1. IDs sichern: `anna_id = store.add_node(["Person"], name="Anna", ...)`
2. Kanten-Typen in GROSSBUCHSTABEN (Konvention, wird bei Cypher wichtig).
3. Warum der GraphStore statt eigenem Dict-Bau? Er ist dein **Neo4j-Trainingssystem** – dieselben Begriffe, offline lauffähig.

## Reflexionsfragen
1. Formuliere eine Frage, die der Text schwer, der Graph leicht beantwortet – warum?
2. „Acme" vs. „ACME": Warum reicht exakter Namensvergleich nicht, und wie heißt das Problem in echten Systemen? (→ Entity Resolution, Build 3!)
3. Was würde passieren, wenn Beziehungen als Property (`arbeitet_bei: "Acme"`) modelliert wären?

## Referenzlösung + Walkthrough
→ [`solutions/first_graph.py`](../solutions/first_graph.py), [`solutions/entities_graph.py`](../solutions/entities_graph.py), [`solutions/graph_queries.py`](../solutions/graph_queries.py), [`solutions/visualize_graph.py`](../solutions/visualize_graph.py)

## Weiter
4.2 – dieselben Konzepte in einer **echten Datenbank** mit einer **echten Abfragesprache**.
