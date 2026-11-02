# Modul 6 – Agenten, Werkzeuge & fortgeschrittene Workflows 🤖

**Ziel:** Vertiefung über Build 3 hinaus: vollwertige Agenten mit **Tools**, **Gedächtnis** (Checkpointer) und **Supervisor**-Mustern für Multi-Agenten-Systeme.

**Wann Agent – wann deterministischer Workflow?** (aus Build 3 gelernt): Ablauf bekannt und fest → Graph/Chain (billig, prüfbar). Welches Werkzeug nötig ist, hängt vom Einzelfall ab → Agent. Faustregel: **so deterministisch wie möglich, so agentic wie nötig.**

| # | Aufgabe | Zeit | API? |
|---|---|---|---|
| 6.1 | [`tasks/01-agenten-mit-werkzeugen.md`](tasks/01-agenten-mit-werkzeugen.md) – Tools, Agent-Loop, create_agent | ~60 Min | ⚠️ nur mit Key |
| 6.2 | [`tasks/02-gedaechtnis-und-freigaben.md`](tasks/02-gedaechtnis-und-freigaben.md) – Checkpointer, thread-Gedächtnis, Interrupt | ~60 Min | offline komplett |
| 6.3 | [`tasks/03-supervisor-und-parallelitaet.md`](tasks/03-supervisor-und-parallelitaet.md) – Paralleles, Subgraphs, Supervisor | ~60–90 Min | offline komplett |

**Ausführen:**
```bash
python3 06-agents-und-tools/solutions/toolbox_agent.py
python3 06-agents-und-tools/solutions/memory_approval_agent.py
python3 06-agents-und-tools/solutions/supervisor_workflow.py
```

**Danach:** [`../07-finale-app/`](../07-finale-app/README.md) – die große Anwendung mit vollem Frontend.
