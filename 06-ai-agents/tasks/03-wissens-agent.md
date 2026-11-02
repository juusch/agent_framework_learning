# Aufgabe 6.3 – Der Wissens-Agent: RAG als Tool 📚🤖

## Schwierigkeit
Mittel · ⚠️ **Kosten:** nur mit Key (offline: Retrieval echt, Antwort simuliert)

## Lernziel
Du kombinierst Stufe 4 (RAG) und Stufe 6 (Agenten): Der Agent entscheidet **selbst**, wann er im Firmengrundlagen-Index nachschlagen muss.

## Warum ist das wichtig?
Der wichtigste Praxiseinsatz von Agenten überhaupt: „Frag den Assistenten – er schlägt nach, wenn nötig." Der Unterschied zu Stufe 4.4: Dort hast **du** den Ablauf fest verdrahtet (immer retrieval). Hier ist das Nachschlagen **ein Werkzeug unter anderen** – der Agent nutzt es, wenn die Frage danach riecht.

## Das Konzept einfach erklärt
**Metapher:** Stufe 4.4 war ein Sachbearbeiter, der **jede** Anfrage erst ins Handbuch schauen lässt – auch „Guten Tag!". Der Wissens-Agent ist eine gute Rezeption: Smalltalk beantwortet sie direkt, Fachfragen landen **gezielt** im Nachschlagewerk. Werkzeug = „Handbuch nachschlagen (Stichwort)".

## Die technische Erklärung
- Das Tool bekommt das Retrieval **gekapselt**: Die Funktion `handbuch_suche(suchbegriff: str)` ruft intern Retriever auf und gibt formatierte Treffer (Text + Quelle) als String zurück. Der Agent sieht nur die Werkzeug-Schnittstelle – die RAG-Technik dahinter ist egal.
- **Latenz/Kosten-Gefahr:** Der Agent kann das Tool **mehrfach** mit verschiedenen Stichworten aufrufen. Für den Anfang okay; später (Stufe 9) begrenzt man Aufrufe (Recursion-Limit / Budget).
- Der Index wird **einmal beim Start** gebaut und bleibt im Tool-„Closure" – nicht pro Aufruf neu!

## Voraussetzungen
- Stufe 4.4 (Retriever), Aufgabe 6.2

## Deine Mission
Baue `knowledge_agent.py`:
1. Übernimm `baue_retriever()` (oder das gesamte Muster) aus Stufe 4.4 – Chroma + beide Handbücher + `k=3`.
2. Tool `handbuch_suche(suchbegriff: str)`: Retrieval, formatierter String aus Treffern mit Quellenangabe; **offline**: ohne Treffer → klarer Hinweis „keine passenden Stellen gefunden".
3. Agent mit **zwei** Tools: `handbuch_suche` und `uhrzeit` (aus 6.2 – zum Kontrast).
4. Drei Anfragen: „Was steht im Handbuch zu Urlaub?" / „Wie richte ich VPN ein?" / „Wie spät ist es?" – die letzte sollte **kein** Nachschlagen brauchen.
5. Auswertung: pro Anfrage anzeigen, welche Tool-Aufrufe passiert sind.

## Akzeptanzkriterien
- [ ] Der Index wird nur **einmal** gebaut (nicht pro Tool-Aufruf).
- [ ] Die Handbuch-Fragen führen zu Tool-Aufrufen mit Quellen in der Antwort.
- [ ] Die Uhrzeit-Frage kommt ohne `handbuch_suche` aus.
- [ ] Trefferlose Suchen ergeben eine klare Meldung, keinen Absturz.

## Hinweise
1. Closure-Muster:
   ```python
   def baue_such_tool(retriever):
       @tool
       def handbuch_suche(suchbegriff: str) -> str:
           ...  # nutzt retriever
       return handbuch_suche
   ```
2. Offline: Formuliere die Anfragen mit Begriffen aus den Dokumenten („Urlaub", „VPN"), sonst greift der Early-Exit „kein Treffer".
3. Erinnerung (Stufe 4): mit `hat_bezug()` kannst du offline ehrlich bleiben.

## Reflexionsfragen
1. Warum ist „RAG als Tool" flexibler als „RAG als feste Pipeline"? Nenne je einen konkreten Vor- **und** Nachteil.
2. Was passiert, wenn das Tool dem Agenten undeutliche Treffer zurückgibt? Wer ist schuld – Tool, Prompt oder Modell?
3. Wie würdest du dem Agenten ein **zweites** Werkzeug geben, das die gefundenen Stellen zusammenfasst? (Mehr Tool ≠ immer besser – warum?)

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| Index wird pro Aufruf neu gebaut (langsam!) | Retriever außerhalb der Tool-Funktion bauen |
| Agent schlägt immer nach, auch bei Smalltalk | System-Prompt schärfen („nutze das Nachschlagen nur für Fachfragen") |
| Tool wirft bei leerer Suche | Absicherung + Hinweistext |

## Referenzlösung
→ [`solutions/knowledge_agent.py`](../solutions/knowledge_agent.py)

## Code-Walkthrough
In der Lösungsdatei; besonders das Closure-Muster und die Treffer-Formatierung.

## Was haben wir gelernt?
RAG als Tool, Index-Wiederverwendung, gezieltes Nachschlagen.

## Was kommt als Nächstes?
Agenten mit Gedächtnis und Gnadenfrist: Aufgabe 6.4 ergänzt den **Checkpointer** (Gesprächsverlauf über mehrere Aufrufe) und einen **Freigabe-Schritt**, bevor der Agent heikle Aktionen ausführt.
