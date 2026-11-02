# Aufgabe 5.2 – Hybrid-Retrieval: Vektor vs. Graph vs. Beide 🔀

**Schwierigkeit:** Mittel · **Zeit:** ~60 Min · **Kosten:** keine (offline komplett)

## Lernziel
Du beantwortest dieselben Fragen mit beiden Wissenssystemen, misst die Stärken – und baust Hybrid-Retrieval, das beide Quellen sauber getrennt ausweist.

## Warum das wichtig ist
Das Herz von Build 3. **Metapher:** Vektor-Suche = hilfsbereiter Ausleiher („ich glaube, *dieses* Kapitel meinst du" – unscharf, nach Bedeutung). Graph = Archivar mit Fadensystem („alles zu X hängt an *diesem* Faden" – exakt, nach Struktur). Hybrid = frag beide, lege beide Ergebnisse auf den Tisch – mit Herkunftsetikett.

| Frage | Gewinner |
|---|---|
| „Was steht über Urlaub?" | **Vektor** (sinngleiche Texte) |
| „Wer hängt am Projekt?" | **Graph** (exakte Traversierung) |
| „Wie hängt Ben mit dem Projekt zusammen?" | **Graph** (Emergenz: Pfad, der nirgends wörtlich steht!) |
| „Was wissen wir gesamt über X?" | **Hybrid** |

## Deine Mission
1. Beide Systeme aufbauen (Vektor-Index über `data/firmenprofil.md`; Graph mit Anna/Ben/Engineering/Data & Analytics/AI Assistant).
2. **Vergleich:** vier Fragen (eine pro Zeile der Tabelle) je an **beide** Systeme; Auswertung mit Begründung pro Frage.
3. **Emergenz-Beweis:** „Wie hängt Ben mit dem Projekt zusammen?" – der Graph traversiert `Ben → BELONGS_TO → Data & Analytics → PROVIDES_DATA_FOR → AI Assistant`, obwohl dieser Weg **nicht im Text steht**. Weise es nach!
4. **Hybrid-Pipeline:** `hybrid_suche(frage) -> {"dokumente": [...], "graph": [...], "antwort": ...}` – Quellen getrennt, plus ehrliches „nichts gefunden" wenn beide leer sind.

## Akzeptanzkriterien
- [ ] Alle vier Fragen liefert jedes System (oder ehrlich leer).
- [ ] Der Emergenz-Pfad ist als traversierte Kette sichtbar.
- [ ] Die Hybrid-Antwort trennt `dokumente` und `graph_fakten` sauber.
- [ ] Du leitest eine Faustregel ab: „Bei Fragen der Art X nehme ich …".

## Hinweise
1. Bausteine wiederverwenden: Retriever aus 3.2, Graph aus 4.1 – hier wird nur **kombiniert**!
2. Offline-Ehrlichkeit: `hat_bezug()` verhindert „beliebige" Treffer ohne Schlüsselwort.
3. Index nur **einmal** bauen und als Objekte weitergeben.

## Reflexionsfragen
1. Warum ist Quelltransparenz (Doku vs. Graph) vertrauensbildend – und was fehlt ihr, wenn der Graph falsch gepflegt wurde?
2. Zwei Retrieval-Aufrufe = doppelte Latenz. Wann wäre eine Vorab-Klassifikation besser – und welches Risiko trägt sie? (→ 5.4!)
3. Was würde passieren, wenn du die Graph-Antwort „schön formulieren" lässt und dabei Fakten verändert werden? (→ 5.3: Fakten bleiben wörtlich!)

## Referenzlösung + Walkthrough
→ [`solutions/vector_vs_graph.py`](../solutions/vector_vs_graph.py), [`solutions/hybrid_retrieval.py`](../solutions/hybrid_retrieval.py)

## Weiter
5.3 – der Graph füllt sich **selbst**: LLM extrahiert Entitäten/Beziehungen, und natürlichsprachige Fragen werden (sicher!) zu Cypher.
