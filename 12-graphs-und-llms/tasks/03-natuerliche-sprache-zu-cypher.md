# Aufgabe 12.3 – Natürliche Sprache → Cypher → Antwort 🗣️→💾

## Schwierigkeit
Mittel · ⚠️ **Kosten:** mit Key LLM-Call (offline: Regel-Fallback)

## Lernziel
Du baust die Pipeline: natürliche Frage → generiertes Cypher → **Sicherheitsprüfung** → Ausführung → verständliche Antwort.

## Warum ist das wichtig?
Das ist „GraphQ&A": Nutzer fragen in Worten, der Graph antwortet in Fakten. Aber – der kritischste Punkt der ganzen Stufe: **generierte Abfragen sind nicht vertrauenswürdig.** Ein Nutzer (oder eine injizierte Anweisung) kann das LLM zu `DELETE`-Statements verleiten. Ohne Prüfung vor der Ausführung gibst du einem LLM die Löschtaste. Deshalb: Whitelist zuerst, Ausführung danach.

## Das Konzept einfach erklärt
**Metapher – der Übersetzer mit Notar:** Das LLM übersetzt deine Frage in „Graphisch" (Cypher). Aber bevor der übersetzte Satz ausgeführt wird, prüft ein **Notar** (`ist_sicher`): „Nur Lesen erlaubt!" Alles andere – ob Tippfehler oder Angriff – wird abgelehnt, mit klarer Begründung. Der Notar ist deterministischer Python-Code, **kein** LLM (LLMs prüfen keine Sicherheitsregeln zuverlässig – Regeln schon).

## Die technische Erklärung
- `ist_sicher(cypher)`: startet mit `MATCH`, enthält `RETURN`, enthält **keines** der verbotenen Schlüsselwörter (CREATE, DELETE, MERGE, SET, DROP, DETACH, ...). 
- `fuehre_sicher_aus(store, cypher)`: erst Prüfung, dann `run_cypher`; bei Ablehnung `ValueError` mit Klartext.
- `cypher_aus_frage(frage)`: offline-Regel-Fallback (erkannte Namen + „arbeitet"-Muster → Mini-Cypher); mit Key würde hier ein LLM-Prompt stehen – der Rest der Pipeline bleibt **identisch**.
- Ergebnis-Übersetzung: Rows (Dicts) → menschenlesbarer Satz (Python-Formatierung, kein LLM nötig!).

## Voraussetzungen
- Aufgabe 12.2, Stufe 11.1 (Cypher-Muster)

## Deine Mission
Baue `nl_to_cypher.py`:
1. Befülle den Graph (aus 12.2 – wiederverwenden!).
2. Funktion `beantworte(frage)` – Pipeline: Frage → Cypher (offline: `cypher_aus_frage`) → `ist_sicher` → ausführen → formatierte Antwort.
3. Teste **drei** Fragen: „Wo arbeitet Anna?" / „Was gibt es über Acme?" / „Hängt Ben mit AI Assistant zusammen?".
4. **Der Angriffs-Test (Pflicht!):** Baue eine „boshafte" Frage, deren generiertes Cypher (simuliere: schreibe es von Hand als „generiert") `DETACH DELETE` enthält – zeige, dass `fuehre_sicher_aus` sie **ablehnt**.
5. Bei nicht übersetzbarer Frage: ehrliche Antwort („kann ich nicht beantworten") statt Rätseln.

## Akzeptanzkriterien
- [ ] Drei Fragen liefern korrekte, lesbare Antworten aus dem Graph.
- [ ] Der Angriffs-Test wird abgelehnt – mit klarer Fehlermeldung.
- [ ] Bei Nicht-Übersetzbarkeit gibt es eine ehrliche Fallback-Antwort.
- [ ] Du kannst begründen, warum die Sicherheitsprüfung **deterministischer Code** sein muss.

## Hinweise
1. Nutze `cypher_aus_frage`, `ist_sicher`, `fuehre_sicher_aus` aus `lernakademie/graph_extraction.py`.
2. Antworten formatieren: z. B. `", ".join(...)` über die Ergebniszeilen.
3. Denke an die Reflexion: Woher weiß `ist_sicher` von neuen Angriffsformen? (Grenzen des Blacklist-Ansatzes – es ist eine Whitelist, aber trotzdem: Defense in Depth, mehr in Stufe 14!)

## Reflexionsfragen
1. Warum „nur lesend" als Standard – und wie würde ein System Schreibrechte sicher geben? (Stichwort Stufe 14: Freigabe-Interrupt!)
2. Was ist der Unterschied zwischen der Ablehnung eines Syntaxfehlers und der Ablehnung eines Angriffs – und warum sollte die **Meldung** unterschiedlich ausfallen?
3. Vergleiche: Vektor-RAG (Stufe 4) beantwortet „Was steht über X?" – was antwortet GraphQ&A besser und warum?

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| Unsichere Abfrage wird ausgeführt | IMMER fuehre_sicher_aus statt run_cypher direkt |
| Antworten unlesbar (Dict-Dump) | Ergebnisse in Sätze formatieren |
| Offline: Fragen werden nicht erkannt | bekannte Namen + „arbeitet"-Muster nutzen |

## Referenzlösung
→ [`solutions/nl_to_cypher.py`](../solutions/nl_to_cypher.py)

## Code-Walkthrough
In der Lösungsdatei; besonders die Pipeline-Reihenfolge und der Angriffs-Test.

## Was haben wir gelernt?
NL→Cypher-Pipeline, Whitelist-Sicherheit, ehrliche Fallbacks, Ergebnis-Übersetzung.

## Was kommt als Nächstes?
Zwei Wissenssysteme gelernt (Vektor-DB, Graph). **Stufe 13** stellt sie gegeneinander – und kombiniert sie zu Hybrid-Retrieval (GraphRAG).
