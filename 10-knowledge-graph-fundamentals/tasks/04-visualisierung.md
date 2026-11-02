# Aufgabe 10.4 – Graph-Visualisierung 🎨

## Schwierigkeit
Leicht · **Kosten: keine**

## Lernziel
Du machst deinen Graph **sichtbar**: als Mermaid-Diagramm (in Markdown/GitHub darstellbar) und als Vorblick auf interaktive Visualisierung (PyVis, kommt in Stufe 15 im Frontend).

## Warum ist das wichtig?
Graphen sind visuelle Denkwerkzeuge: Ein Diagramm zeigt in Sekunden, was Abfragen in Minuten offenlegen. Und für Frontends gilt: Nutzer wollen Graphen **sehen** und klicken, nicht nur JSON lesen. Mermaid kennst du bereits aus Stufe 5 – jetzt erzeugst du es aus Daten statt es von Hand zu tippen.

## Das Konzept einfach erklärt
**Metapher – der Stadtplan:** Eine Liste von Straßen („Anna → Acme") ist korrekt, aber ein Plan macht Muster sichtbar: Acme als Zentrum, Anna mit drei Verbindungen. Visualisierung ist keine Deko – sie ist Analyse-Werkzeug und Kommunikationsmittel zugleich.

## Die technische Erklärung
- `store.to_mermaid()` erzeugt Mermaid-`flowchart`-Code aus deinen Daten: Nodes als beschriftete Boxen, Kanten als `--TYP-->`-Pfeile. GitHub rendert das in Markdown-Dateien direkt.
- Für **interaktive** Visualisierung gibt es später im Frontend (Stufe 15) **PyVis** (Python-Bibliothek, die HTML mit draggable Nodes erzeugt) – hier schaust du nur kurz in die Lösung hinein, um den Zusammenhang zu verstehen.
- Ausdrücklich KEIN Lernziel: selbst JavaScript zu schreiben. Du erzeugst Darstellung **aus Python-Daten**.

## Voraussetzungen
- Aufgabe 10.3

## Deine Mission
Baue `visualize_graph.py`:
1. Erzeuge den Firmen-Graph (eigener oder `baue_beispiel_graph()`).
2. Gib `to_mermaid()` aus und speichere den Code in `diagramm.md` (mit ```` ```mermaid ````-Umrandung!) – öffne die Datei auf GitHub/VS Code: gerenderter Graph!
3. Erweitere (Eigenleistung!): eine Funktion `to_mermaid_gefiltert(store, label)`, die nur Nodes eines Labels plus ihre direkten Nachbarn zeigt – ein „Fokus-View" auf `Department`.
4. Bonus (nur angucken, nicht bauen): Die Datei zeigt dir den pyvis-Einzeiler (`net.from_...`) in Kommentaren – damit du weißt, was in Stufe 15 auf dich kommt.

## Akzeptanzkriterien
- [ ] `diagramm.md` enthält lauffähigen Mermaid-Code (renders auf GitHub).
- [ ] Alle 5 Nodes und 5 Kanten des Firmen-Graphs sind sichtbar (inkl. Kanten-Typen).
- [ ] Die Fokus-View liefert korrekt nur Departments + Nachbarn.
- [ ] Du kannst erklären, warum Visualisierung aus **Daten** generiert wird statt von Hand gezeichnet.

## Hinweise
1. Datei schreiben: `Path("diagramm.md").write_text("```mermaid\n" + mermaid + "\n```")`
2. Der `to_mermaid()`-Code des GraphStore zeigt dir das Format – schau hinein (du verstehst jede Zeile!).
3. GitHub rendert Mermaid in jedem `.md` – dein erstes „Graph-Dashboard" ist eine simple Markdown-Datei.

## Reflexionsfragen
1. Warum ist „aus Daten generiert" die einzige haltbare Art für echte Anwendungen? (Handgezeichnetes veraltet bei der ersten Änderung!)
2. Was zeigt dir die Fokus-Ansicht, was der Gesamtsicht verborgen bleibt? Wann brauchst du welche?
3. Welche zwei Zusatzinformationen pro Node wären fürs Verständnis in der Visualisierung ideal (Label? Properties?) – und warum reicht beides nicht immer?

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| Mermaid wird nicht gerendert | ```` ```mermaid ````-Block verwenden (drei Backticks) |
| Umlaute brechen Mermaid | in Labels vermeiden oder HTML-Entities (`&uuml;`) – unser Store nutzt `ue`-Schreibweise |
| Fokus-View zeigt zu viel | nur Nodes des Labels + deren `neighbors`, nicht `relationships()` des ganzen Graphs |

## Referenzlösung
→ [`solutions/visualize_graph.py`](../solutions/visualize_graph.py)

## Code-Walkthrough
In der Lösungsdatei; besonders die Fokus-View-Funktion.

## Was haben wir gelernt?
Datengetriebene Visualisierung, Mermaid aus Graphdaten, Fokus-Ansichten.

## Was kommt als Nächstes?
Der Speicher-Graph im RAM ist verschwunden, sobald das Programm endet. **Stufe 11** bringt echte Persistenz: Neo4j, die Abfragesprache Cypher – und die Brücke von Python zur Datenbank. Dein GraphStore bleibt dabei als Offline-Fallback überall dort, wo keine DB läuft.
