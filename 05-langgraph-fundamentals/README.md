# Stufe 5 – LangGraph-Fundamente 🕸️

**Ziel:** Du verstehst, warum es LangGraph gibt, und baust eigene Workflows mit **State**, **Nodes**, **Edges** und **konditionalem Routing** – inklusive Schleifen.

## LangChain vs. LangGraph – der Satz, den du nie vergessen wirst

> **LangChain hilft dir, KI-Fähigkeiten zu verketten. LangGraph hilft dir, komplexe Workflows zu steuern, die mehrere Schritte, Entscheidungen, Schleifen und gemeinsamen Zustand enthalten.**

Chains (Stufe 3) sind Fließbänder: gerade Linien, immer vorwärts. Sobald dein Ablauf aber *verzweigt* („Wenn Rechnung → Station A, wenn Technik → Station B"), *wiederholt* („Antwort prüfen – nicht gut? Nochmal!") oder mehrere Stationen *gemeinsame Daten* brauchen, brauchst du einen **Graphen**.

**Metapher:** Ein Graph ist ein Bahnhofnetz:
- **State** = der gemeinsame Notizblock im Zug (jede Station liest und schreibt hinein)
- **Node** = eine Station, in der genau eine Person genau eine Arbeit erledigt
- **Edge** = ein Gleis von Station zu Station
- **Conditional Edge** = eine Weiche, die je nach Inhalt des Notizblocks entscheidet, welches Gleis der Zug nimmt
- **Loop** = ein Gleis zurück („noch nicht fertig – zurück zum Start!")

## Aufgaben

| # | Aufgabe | Schwierigkeit | API? |
|---|---|---|---|
| 5.1 | [`tasks/01-hello-graph.md`](tasks/01-hello-graph.md) | Anfänger | nein |
| 5.2 | [`tasks/02-state-und-nodes.md`](tasks/02-state-und-nodes.md) | Anfänger | nein |
| 5.3 | [`tasks/03-konditionales-routing.md`](tasks/03-konditionales-routing.md) | Leicht | nein |
| 5.4 | [`tasks/04-schleifen.md`](tasks/04-schleifen.md) | Mittel | nein |

**Das Schöne an dieser Stufe:** Alle Aufgaben funktionieren **ohne LLM und ohne Key** – die Nodes enthalten reine Python-Logik. So lernst du die Graphen-Mechanik isoliert, bevor in Stufe 6 LLM-Knoten dazukommen.

## Ausführen

```bash
python3 05-langgraph-fundamentals/solutions/hello_graph.py
python3 05-langgraph-fundamentals/solutions/state_chain.py
python3 05-langgraph-fundamentals/solutions/routing_graph.py
python3 05-langgraph-fundamentals/solutions/loop_graph.py
```

## Aktuelle API-Referenz

- [LangGraph-Übersicht](https://docs.langchain.com/oss/python/langgraph/overview)
- [StateGraph, START, END](https://docs.langchain.com/oss/python/langgraph/graph-api)

## Danach
Weiter mit [`../06-ai-agents/README.md`](../06-ai-agents/README.md): Du gibst einem Agenten **Werkzeuge** in die Hand – und der Graph entscheidet (per LLM), welches Werkzeug er wann benutzt.
