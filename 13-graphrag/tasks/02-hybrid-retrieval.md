# Aufgabe 13.2 – Hybrid-Retrieval: beide Welten kombinieren 🔀

## Schwierigkeit
Mittel · **Kosten: keine** (offline voll übbar)

## Lernziel
Du baust eine Retrieval-Pipeline, die **Vektor-Fundstellen und Graph-Fakten** in einer Antwort vereint – sauber getrennt nach Quelle (Dokument vs. Graph).

## Warum ist das wichtig?
Die interessantesten Fragen brauchen beides: „**Was** wissen wir über das Projekt (Dokumente) und **wer** hängt dran (Graph)?" Hybrid-Retrieval ist der Realitätscheck für GraphRAG-Systeme – und die Grundlage des Capstone-Projekts (final-project), das genau diese Architektur nutzt.

## Das Konzept einfach erklärt
**Metapher – der Nachforschungs-Tisch:** Der Detektiv legt zwei Stapel nebeneinander: links Zeitungsartikel (Vektor: „so wird es beschrieben"), rechts das Ermittlungsbrett (Graph: „so hängt es zusammen"). Erst die **Zusammenfassung beider Stapel** ist die vollständige Antwort – und jede Aussage trägt einen Zettel, aus welchem Stapel sie kommt (Quelltransparenz!).

## Die technische Erklärung
- `hybrid_suche(frage)` = 1) Vektor-Retrieval (Chunks) **und** 2) Graph-Retrieval (Traversierung/Cypher) parallel aufrufen, 3) Ergebnis strukturieren:
  ```python
  {
    "dokumente": [(quelle, textstelle), ...],
    "graph": ["Anna --CONTRIBUTES_TO--> AI Assistant", ...],
    "antwort": "zusammengefasster Text (offline: deterministisch)"
  }
  ```
- Getrennte Quellenangaben sind Pflicht: „aus Handbuch, Abschnitt X" vs. „aus Knowledge Graph (Traversierung)". Damit kannst du Vertrauen und Herkunft prüfen – wie in Stufe 4.4 gelernt.
- „Nur eine Quelle nötig"-Fragen: Die Pipeline kann Ergebnisse gewichten (einfach: „wenn Graph nichts fand, zeige nur Dokumente").

## Voraussetzungen
- Aufgabe 13.1

## Deine Mission
Baue `hybrid_retrieval.py`:
1. Beide Indizes aufbauen (Vektor + Graph aus 13.1 wiederverwenden!).
2. `hybrid_suche(frage)` wie oben beschrieben.
3. **Drei Fragen testen:** eine dokumentlastige („Was steht über die Abteilung Engineering?"), eine graphlastige („Wer traegt zum AI Assistant bei?"), eine hybride („Was wissen wir GESAMT ueber das AI-Assistant-Projekt?").
4. Die Ausgabe zeigt pro Frage klar getrennt: Doku-Fundstellen und Graph-Fakten.
5. Bonus: eine „leere" Frage (kein Treffer irgendwo) – ehrliche Antwort.

## Akzeptanzkriterien
- [ ] Die Antwortstruktur trennt `dokumente` und `graph` sauber.
- [ ] Die hybride Frage liefert aus **beiden** Quellen Inhalte.
- [ ] Die graphlastige Frage liefert Graph-Fakten (nicht Texte).
- [ ] Totaler Fehlschlag führt zu „nichts gefunden" statt Crash.

## Hinweise
1. Bausteine: `retriever.invoke` (Stufe 4), `fuehre_sicher_aus`/`neighbors` (Stufe 11/12) – du kennst schon alles!
2. Offline-Tipp: Die Fragen mit Namen und Wörtern aus dem Firmenprofil formulieren, damit die Keyword-Embeddings treffen.
3. Für „Wer traegt … bei?" nutze eine `CONTRIBUTES_TO`-Traversal – richte die Kante im Graph entsprechend ein.

## Reflexionsfragen
1. Warum ist Quelltransparenz (Doku vs. Graph) für Endnutzer vertrauensbildend – und was fehlt ihr noch, wenn der **Graph** falsch gepflegt wurde?
2. Zwei Retrieval-Aufrufe = doppelte Latenz und Kosten. Wann wäre eine Vorab-**Klassifikation** („nur eine Quelle nötig") besser – und welche Risiken trägt sie (Stufe 14 greift das auf)?
3. Wie sähe die Hybrid-Antwort aus, wenn das LLM die Endformatierung übernimmt (mit Key) – was darf es dabei **nicht** tun (Fakten erfinden!)?

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| Quellen vermischt | Struktur mit getrennten Feldern erzwingen |
| Graph-Fakten als Textformulierung „schöngefahren" | Fakten wörtlich lassen (Traversierungsergebnis), Formulierung nur drumherum |
| Doppelter Index-Aufbau pro Frage | einmal in main(), als Objekte weitergeben (Stufe 6.3-Muster!) |

## Referenzlösung
→ [`solutions/hybrid_retrieval.py`](../solutions/hybrid_retrieval.py)

## Code-Walkthrough
In der Lösungsdatei; besonders die Struktur der Hybrid-Antwort.

## Was haben wir gelernt?
Hybrid-Pipelines, Quelltransparenz, performante Index-Wiederverwendung.

## Was kommt als Nächstes?
**Stufe 14** gibt dem Hybrid-System ein Gehirn: Ein Agent entscheidet selbst (per LLM oder Regel), welche Strategie die Frage braucht – und fragt Menschen, bevor er destruktive Graph-Operationen ausführt.
