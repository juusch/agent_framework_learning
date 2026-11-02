# Aufgabe 14.1 – Der Graph-Aware Agent 🔀🤖

## Schwierigkeit
Mittel · **Kosten: keine** (offline voll übbar)

## Lernziel
Du baust einen Agenten mit **zwei Retrieval-Tools** und einer Routing-Entscheidung (offline: Regel-Logik; mit Key: LLM), die je nach Fragen-Typ das passende Werkzeug wählt – inklusive Hybrid-Fall.

## Warum ist das wichtig?
Hybrid-Retrieval (13.2) ruft **immer beide** Quellen auf – teuer und langsam, wenn die Frage nur eine braucht. Der Agent hier trifft die Wahl: „Diese Frage ist dokumentlastig → nur Vektor", „Verbindungsfrage → nur Graph", „Gesamtfrage → beide". Das ist die produktive Reifung deiner Stufe-13-Erkenntnisse: **nicht mehr Struktur, sondern Entscheidung**.

## Das Konzept einfach erklärt
**Metapher – der Empfangschef mit zwei Fachabteilungen:** Der Empfang sieht die Anfrage und schickt den Gast entweder zur Dokumenten-Auskunft („Was steht geschrieben?") oder zum Akten-Archivar („Wie hängt es zusammen?") – oder, bei Gesamtfragen, zu beiden. Früher (13.2) lief der Gast immer durch beide Türen; jetzt entscheidet der Empfang gezielt.

## Die technische Erklärung
- Zwei Tools nach Stufe-6.3-Muster (Closure über gemeinsame Indizes):
  - `vektor_suche(frage)` → Fundstellen mit Quellen
  - `graph_abfrage(frage)` → Traversierungs-Fakten
- Die **Klassifikation** ist eine eigene Node (Stufe 5.3-Muster): Regel-Logik offline (Schlüsselwörter wie „haengt zusammen"/„wer" → graph; „was steht"/„steht drin" → vektor; „gesamt"/„alles"/„vergleich" → hybrid), mit Key ein LLM-Aufruf mit denselben drei Optionen.
- Der Graph: START → klassifizieren → konditionale Kanten zu den Tool-Nodes → Antwort-Node → END. (Auch eine create_agent-Variante mit bind_tools wäre möglich – die explizite Graph-Version zeigt dir das Routing.)
- Ergebnisse landen getrennt im State (`dokumente`, `graph_fakten`) – Quelltransparenz bleibt erhalten.

## Voraussetzungen
- Stufe 7 (konditionales Routing), Stufe 13 (beide Retrieval-Bausteine)

## Deine Mission
Baue `graph_aware_agent.py`:
1. Beide Indizes aufbauen (aus 13.2 wiederverwenden!) und die zwei Tools kapseln.
2. Klassifizierer `klassifiziere(frage) -> "vektor" | "graph" | "hybrid"` (offline: Regel-Logik mit begründeten Schlüsselwörtern; dokumentiere deine Regeln als Kommentare!).
3. LangGraph: klassifizieren → Routing zu einem/ beiden Tool-Nodes → antworten (führt State-Inhalte formatiert zusammen).
4. **Vier Testfragen** (je eine pro Zweig + eine „unklare", die sicher in Hybrid fällt).
5. Ausgabe pro Frage: gewählte Route + Ergebnisse.

## Akzeptanzkriterien
- [ ] Drei Routen existieren und werden korrekt gewählt.
- [ ] Die „dokumentlastige" Frage ruft NICHT den Graph auf (und umgekehrt).
- [ ] Die Hybrid-Frage ruft beide Tools auf.
- [ ] Der finale State trennt `dokumente` und `graph_fakten`.

## Hinweise
1. Routing: `add_conditional_edges("klassifizieren", weiche, {...})` (Stufe 5.3/7.3).
2. Für „beide Tools" beim Hybrid-Fall: zwei Tool-Nodes parallel (Stufe 7.1) oder sequentiell – beides gültig; begründe deine Wahl im Kommentar.
3. Offline-Regeln grob-granular halten: Es geht ums Muster, nicht um NLP-Perfektion.

## Reflexionsfragen
1. Was kostet die Fehlklassifikation (Dokument-Frage → Graph-Route)? Antwortqualität? Latenz? – Und wie könnte ein „Fallback auf Hybrid" bei unsicheren Fällen helfen?
2. Warum ist „Klassifikation als eigene Node" besser als die Entscheidung im Tool zu verstecken?
3. Vergleiche mit Stufe 6: Wann wäre ein voller `create_agent` mit Tool-Loop die bessere Wahl als dein festes Routing?

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| Beide Tools laufen immer | Routing-Pfad prüfen; Weiche mappingt wirklich nur die eine Route |
| Klassifikation ins Tool verschoben | eigene Node – sonst untestbar und undurchsichtig |
| State-Felder vermischt | `dokumente` und `graph_fakten` getrennt halten (13.2!) |

## Referenzlösung
→ [`solutions/graph_aware_agent.py`](../solutions/graph_aware_agent.py)

## Code-Walkthrough
In der Lösungsdatei; besonders die Weichen-Logik und die Hybrid-Verzweigung.

## Was haben wir gelernt?
Entscheidungsgesteuertes Retrieval, Routing über Fragetypen, Kostenbewusste Tool-Wahl.

## Was kommt als Nächstes?
Was, wenn der Agent den Graph **ändern** soll (neue Fakten eintragen, falsche löschen)? Genau dann braucht es die Bremse aus Stufe 6.4: Aufgabe 14.2 – Freigabe vor destruktiven Operationen.
