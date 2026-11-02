# Aufgabe 14.2 – Freigabe für destruktive Graph-Operationen ✋💾

## Schwierigkeit
Mittel · **Kosten: keine** (offline voll übbar)

## Lernziel
Du baust die sicherheitskritische Ergänzung zum Graph-Agenten: **Schreiboperationen** (Fakten anlegen/löschen) laufen nur nach menschlicher Freigabe (Interrupt + Resume).

## Warum ist das wichtig?
Stufe 12.3 schützte über eine **lesende Whitelist**. Aber irgendwann muss der Graph **gepflegt** werden: neue Fakten aus Dokumenten, Korrekturen, Bereinigungen. Die Regel im Ernst: **Lesen darf der Agent allein – Schreiben nur mit Mensch.** Ein hallucinierter oder injizierter Fakt im Graph vergiftet jede zukünftige Antwort (der Graph „erinnert sich" falsch!). Die Freigabe ist das Gegengift – Muster aus Stufe 6.4/8D.

## Das Konzept einfach erklärt
**Metapher – die Krankenakte:** Pfleger dürfen die Akte **lesen** (Whitelist). Aber ein Eintrag („Patient ist gegen Penicillin allergisch"!) passiert nur nach ärztlicher **Gegenzeichnung** – weil ein falscher Eintrag dauerhaft Schaden anrichtet. Die Gegenzeichnung ist der `interrupt()`: Der Agent **hält den Stift über dem Formular** und wartet.

## Die technische Erklärung
- Schreib-Tool `fakt_anlegen(subject, rel, obj)`: ruft **vor** dem `store.add_relationship(...)` ein `interrupt({...})` auf – im Interrupt-Value stehen **alle Details** (wer/was/womit begründet?), damit der Mensch informiert entscheiden kann.
- Fortsetzung per `Command(resume=True/False)` mit **demselben thread_id-Config** (Stufe 6.4!). Ablehnen → Änderung wird verworfen, Workflow läuft weiter (kein Crash!).
- Der Checkpointer hält den angehaltenen Lauf fest – ohne ihn kein Interrupt.
- **Design-Regel für dein State:** `aenderungen`-Liste protokolliert jede Freigabe UND jede Ablehnung (Audit-Log!).

## Voraussetzungen
- Aufgabe 14.1, Stufe 6.4 (Interrupt + Command)

## Deine Mission
Baue `approval_graph_ops.py`:
1. Graph aus 13.2 aufbauen. Checkpointer anhängen (MemorySaver).
2. Tool `fakt_anlegen(subject, rel, obj)`: Interrupt mit allen Details → bei Freigabe: Kante anlegen (mit Entity Resolution via `find_node`!), bei Ablehnung: Übersichtliche Rückgabe „abgelehnt".
3. **Workflow-Graph:** `fakt_anfordern` (bereitet den Fakt vor – offline: vorgegebene Fakten-Liste; mit Key: LLM extrahiert aus Text) → `fakt_anlegen` (mit Interrupt) → `protokollieren`.
4. **Zwei Läufe demonstrieren:** ein guter Fakt („Clara LEADS Engineering") → Freigabe → Graph enthält ihn danach (Beweis!). Ein riskanter Fakt → **Ablehnung** → Graph unverändert.
5. Abschließend das Audit-Log ausgeben (Freigaben und Ablehnungen).

## Akzeptanzkriterien
- [ ] Der Lauf stoppt VOR der Änderung und zeigt die Fakten-Details.
- [ ] `resume=True` führt zur sichtbaren Graph-Änderung (Beweis per Ausgabe).
- [ ] `resume=False` verwirft die Änderung sauber – Graph unverändert.
- [ ] Das Audit-Log listet beide Vorfälle.
- [ ] Auch der abgelehnte Lauf beendet den Workflow ordentlich.

## Hinweise
1. Interrupt-Daten reichhaltig: `{"frage": ..., "fakt": {"von":..., "typ":..., "zu":...}, "grund": ...}`
2. Beweis führen: Kanten-Anzahl vor/nach dem Lauf ausgeben.
3. Ablehnung ist KEIN Fehlerfall: Der Workflow endet normal, nur ohne die Änderung.

## Reflexionsfragen
1. Warum reicht die Whitelist aus 12.3 allein nicht, wenn das System „Fakten aus Dokumenten lernen" soll?
2. Was ist schlimmer: ein falscher Fakt im Graph oder eine falsche Textstelle im Vektor-Index? (Denk an Dauerhaftigkeit und Vererbung auf traversierte Antworten!)
3. Wo lagert man in Produktion die Freigabe aus (E-Mail-Queue, Web-UI, Chat-Rückfrage) – und was ändert sich am Code? (Nichts! Der interrupt bleibt – nur der Resume-Kanal ist ein Frontend. Genau das baut Stufe 15!)

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| interrupt ohne Checkpointer | MemorySaver an compile() übergeben |
| Änderung passiert vor dem interrupt | interrupt als ERSTE Zeile im Tool |
| Ablehnung crasht den Lauf | normales RETURN „abgelehnt", kein Exception |

## Referenzlösung
→ [`solutions/approval_graph_ops.py`](../solutions/approval_graph_ops.py)

## Code-Walkthrough
In der Lösungsdatei; besonders Interrupt-Payload, Resume-Zweige und Audit-Log.

## Was haben wir gelernt?
Schreibschutz für Graphen, Human-in-the-Loop für Datenpflege, Audit-Logs.

## Was kommt als Nächstes?
Damit ist die Agenten-Reise komplett: RAG, Graph, Hybrid, Entscheidungen, Freigaben. **Stufe 15** macht all das **sichtbar und bedienbar**: FastAPI-Backend + Streamlit-Frontend – und danach das große Capstone-Projekt.
