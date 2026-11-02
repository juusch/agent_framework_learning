# Aufgabe 12.2 – Graph-Population & Entity Resolution 🧩

## Schwierigkeit
Leicht · **Kosten: keine** (offline voll übbar)

## Lernziel
Du überführst Extraktions-Ergebnisse in den Graph – ohne Duplikate, dank **Entity Resolution**: „ist das schon drin?"

## Warum ist das wichtig?
Ein Graph, der „Acme" dreimal enthält (als „Acme", „ACME", „Acme GmbH"), ist unbrauchbar: Abfragen liefern Bruchstücke, Traversals reißen ab. Entity Resolution ist die **Qualitätswährung** jedes Knowledge Graphs. In echten Systemen ist sie ein eigenes Fachgebiet (Fuzzy-Matching, Embeddings für Namen) – hier lernst du das Grundprinzip.

## Das Konzept einfach erklärt
**Metapher – der Türsteher des Clubs:** Vor dem Einlass steht ein Türsteher mit Gästeliste: „Anna? Steht schon drauf – kein zweiter Armband-Ausweis!" Neue Gesichter kommen rein, bekannte nicht nochmal. Der Türsteher ist dein `find_node`-Check vor jedem `add_node`.

## Die technische Erklärung
- `fuelle_graph(store, extraktion)`:
  1. Für jede Entität: `find_node(label, name=...)` – existiert → ID wiederverwenden; sonst anlegen. → **Entity Resolution**
  2. Für jede Beziehung: IDs der beteiligten Entitäten nachschlagen → `add_relationship`. Fehlt eine Seite (Tippfehler!), wird die Kante **übersprungen** statt gecrasht – und du siehst es in der Ausgabe.
- ID-Zwischenspeicher (`ids`-Dict) hält den Lauf effizient.
- Für echte Neo4j-Systeme gilt dasselbe als `MERGE` (Stufe 11.2!) – hier siehst du, was MERGE intern tut.

## Voraussetzungen
- Aufgabe 12.1

## Deine Mission
Erweitere `extract_to_graph.py` (oder baue `population_demo.py`):
1. Lege einen leeren `GraphStore` an.
2. Extrahiere aus deinem Text (12.1) und fülle mit `fuelle_graph` – gib aus: angelegte Nodes, gesetzte Kanten.
3. **Der Duplikat-Test:** Extrahiere **denselben Text erneut** und fülle nochmal. Erwartung: keine neuen Nodes! (Beweis durch Ausgabe.)
4. **Der Fehlerfall:** Extrahiere einen Text mit einer Beziehung auf eine unbekannte Entität – die Kante wird übersprungen, das Programm läuft weiter.
5. Gib am Ende den Graph als Mermaid aus (Stufe 10.4!).

## Akzeptanzkriterien
- [ ] Der erste Füllvorgang erzeugt die erwarteten Nodes + Kanten.
- [ ] Der zweite Füllvorgang erzeugt **null** neue Nodes (Entity Resolution wirkt).
- [ ] Unvollständige Beziehungen werden übersprungen, nicht gecrasht.
- [ ] Mermaid-Ausgabe zeigt den gefüllten Graph.

## Hinweise
1. `fuelle_graph` gibt die Anzahl gesetzter Kanten zurück – nutze es für die Ausgaben.
2. Duplikat-Beweis: `len(store.nodes())` vor und nach dem zweiten Lauf vergleichen.
3. denk an Stufe 10.4: `store.to_mermaid()` – dein Debugging-Werkzeug.

## Reflexionsfragen
1. „Acme" vs. „ACME": Warum reicht exakter Namensvergleich nicht in echten Systemen – und welche zwei besseren Ansätze kennst du schon (kleinschreiben? Embeddings als „Bedeutungs-Vergleich"?)?
2. Warum ist es besser, eine unvollständige Kante zu **überspringen** statt „irgendwie" zu raten?
3. Was passiert bei 1000 Extraktionen ohne Resolution – und warum sieht man das oft erst spät?

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| Duplikate entstehen | find_node vor jedem add_node (oder fuelle_graph nutzen) |
| Kanten auf fehlende IDs crashen | fuelle_graph prüft beide Seiten (ids-Dict) |
| IDs mit Namen verwechselt | fuelle_graph verwaltet das Mapping selbst |

## Referenzlösung
→ [`solutions/extract_to_graph.py`](../solutions/extract_to_graph.py) (enthält alle drei Teile der Stufe)

## Code-Walkthrough
In der Lösungsdatei; besonders der Duplikat-Test und das überspringende Kanten-Handling.

## Was haben wir gelernt?
Graph-Population, Entity Resolution als Qualitätsprinzip, robustes Fehler-Skippen.

## Was kommt als Nächstes?
Der Graph ist gefüllt – jetzt fragst du ihn **natürlich**: Aufgabe 12.3 übersetzt „Wo arbeitet Anna?" via LLM zu Cypher – mit Sicherheits-Whitelist.
