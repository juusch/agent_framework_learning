# Aufgabe 6.3 – Parallelität, Subgraphs & Supervisor 👔

**Schwierigkeit:** Fortgeschritten · **Zeit:** ~60–90 Min · **Kosten:** keine (offline komplett)

## Lernziel
Du orchestrierst mehrere Stationen: **parallel** mit Merge-Barriere, ganze Graphen als **Subgraph** (Abteilung), und ein **Supervisor**, der Agenten-Arbeit delegiert.

## Warum das wichtig ist
Drei Muster, die Multi-Agenten-Systeme tragen. **Metaphern:** Parallel = Kommission (alle prüfen dieselbe Akte, dann Sitzung); Subgraph = Abteilung als Black Box im Firmengebäude; Supervisor = Projektleitung, die einzeln delegiert und einsammelt (Spezialisten reden nie direkt miteinander!).

## Deine Mission
1. **Parallele Prüfer:** drei Nodes parallel von START, eigene Felder pro Zweig (kein Schreibkonflikt!), Merge-Node wartet auf alle (Barriere).
2. **Subgraph:** Qualitäts-Loop (5.1) als eigener Graph, im äußeren Graphen über Adapter-Funktion als EIN Node; beweise die Kapselung: innere Felder (`bewertung`, `versuche`) tauchen im äußeren State **nicht** auf; Subgraph läuft standalone.
3. **Supervisor:** drei Nodes (Recherche, Schreiben) + Supervisor-Node (Delegation: erst Recherche, dann Schreiben, dann FINISH), **Runden-Limit** gegen Endlos-Delegation; Ergebnis-Log im State; Beweis: `max_runden=1` bricht kontrolliert ab.

## Akzeptanzkriterien
- [ ] Der Merge läuft erst, wenn alle parallelen Zweige geliefert haben.
- [ ] Subgraph standalone testbar; Kapselung nachgewiesen.
- [ ] Der Supervisor delegiert in der richtigen Reihenfolge und terminiert immer.
- [ ] Du kannst begründen, warum Supervisor statt Agent-zu-Agent-Netz (Kommunikationspfade: n·(n−1)/2!).

## Hinweise
1. Parallele Schreibkonflikte: eigene Felder je Zweig.
2. Subgraph: nur **kompilierte** Graphen sind Nodes; Adapter übersetzt außen ↔ innen.
3. Supervisor offline per Regel-Logik – mit Key könnte derselbe Node ein LLM fragen (Pipeline identisch!).

## Reflexionsfragen
1. Was sind die zwei klassischen Supervisor-Fehler (Endlos-Delegation, falsche Delegation) – und welche zwei Bremsen hast du verbaut?
2. Wann ist ein einfacher sequenzieller Graph besser als ein Supervisor?
3. Wo steckt das Supervisor-Muster im Finale? (Schau dir `final-project/.../graphs/workflow.py` an – kleiner Verwandter!)

## Referenzlösung + Walkthrough
→ [`solutions/parallel_workflow.py`](../solutions/parallel_workflow.py), [`solutions/subgraph_workflow.py`](../solutions/subgraph_workflow.py), [`solutions/supervisor_workflow.py`](../solutions/supervisor_workflow.py)

## Weiter
🏁 [`../07-finale-app/`](../../07-finale-app/README.md) – die finale Anwendung: Build 3 in voller Größe + komplettes Frontend.
