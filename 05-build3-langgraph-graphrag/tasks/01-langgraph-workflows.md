# Aufgabe 5.1 – LangGraph: State, Nodes, Edges & Routing 🕸️

**Schwierigkeit:** Mittel · **Zeit:** ~60–90 Min · **Kosten:** keine (reine Python-Logik!)

## Lernziel
Du beherrschst die LangGraph-Grundbewegungen: gemeinsamer State, Nodes, konditionale Kanten (Routing) und Schleifen mit Limit.

## Warum das wichtig ist
Chains (Build 2) sind gerade Linien. Echte Workflows – und dein Build-3-Assistent! – **verzweigen** (Vektor oder Graph?) und **wiederholen** (Qualitäts-Loop). **Metapher – das Bahnhofnetz:** State = Notizbuch im Zug (alle Stationen lesen/schreiben), Node = Station (eine klare Aufgabe), Edge = Gleis, konditionaler Edge = Weiche, Loop = Rückgleis.

## Deine Mission
1. **Hello Graph:** Schema (TypedDict) → Node-Funktion → `START → node → END` → `compile()` → `invoke()`. Dann ein zweiter Node – Nodes geben nur **Änderungen** zurück (Merge!).
2. **Drei-Stationen-Workflow:** drei Nodes teilen sich einen State; Node 3 liest Felder von Node 1 **und** 2.
3. **Routing (die Weiche):** Support-Router – `klassifizieren` (schreibende Station) + drei Antwort-Nodes; `add_conditional_edges` mit Mapping-Dict; teste alle drei Kategorien.
4. **Loop mit Bremse:** entwerfen → prüfen → (nicht gut & `versuche < max`?) → zurück; Historie im State sichtbar führen. **Bonus-Verständnis:** Was passiert ohne Runden-Limit?

## Akzeptanzkriterien
- [ ] Nodes geben nur Diffs zurück; der finale State enthält alles.
- [ ] Alle drei Router-Kategorien landen bei ihrem eigenen Antwort-Node.
- [ ] Der Loop endet **immer** – auch bei „schlechten" Werten (Doppel-Bedingung!).
- [ ] Du kannst Weichen-Funktion (liest nur) von Klassifizierung (schreibt) trennen und begründen.

## Hinweise
1. `from langgraph.graph import StateGraph, START, END`
2. `graph.add_conditional_edges("klassifizieren", weiche, {"rechnung": "antwort_rechnung", ...})`
3. Listen im State: **neue Liste** zurückgeben (`state["historie"] + [x]`), nicht mutieren!

## Reflexionsfragen
1. Warum sind „alle reden mit dem Notizbuch" und „keiner redet direkt" dasselbe Design wie bei deinem Build-3-Agenten (Intent → Route)?
2. Was wäre der Loop in einem echten LLM-Workflow – und was kostet er unbegrenzt?
3. Wo könnte ein Subgraph helfen, wenn der Qualitäts-Loop wiederverwendbar sein soll? (→ Modul 6.3!)

## Referenzlösung + Walkthrough
→ [`solutions/hello_graph.py`](../solutions/hello_graph.py), [`solutions/state_chain.py`](../solutions/state_chain.py), [`solutions/routing_graph.py`](../solutions/routing_graph.py), [`solutions/loop_graph.py`](../solutions/loop_graph.py)

## Weiter
5.2 – die Weiche entscheidet bald zwischen **Wissensquellen**: Vektor, Graph – oder beide.
