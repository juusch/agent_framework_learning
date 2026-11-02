# Modul 7 – 🏁 Die finale Anwendung & ihr Frontend

**Ziel:** Dein Build-3-Assistent als vollständiges, bedienbares System: [**final-project/knowledge-research-agent/**](../final-project/knowledge-research-agent/README.md) – FastAPI-Backend, Streamlit-Frontend (Chat, Graph-Explorer, Dokumente, Prompt-Labor, Freigaben, Verlauf) und Docker Compose.

**Der rote Faden des Frontends in der Akademie:**
- Modul 2: erste Streamlit-Oberfläche (direkter Aufruf, 1 Datei)
- Modul 7: dieselbe Idee in voller Größe – **mit API-Schicht**, sessions, Freigaben über HTTP

| # | Aufgabe | Zeit |
|---|---|---|
| 7.1 | [`tasks/01-finale-anwendung.md`](tasks/01-finale-anwendung.md) – Backend live erleben & verstehen | ~90 Min |
| 7.2 | [`tasks/02-frontend-und-betrieb.md`](tasks/02-frontend-und-betrieb.md) – Alle Frontend-Seiten + Docker Compose + Architektur | ~60–90 Min |

**Schnellstart (offline, ohne Key):**
```bash
# Terminal 1 – Backend:
cd final-project/knowledge-research-agent && uvicorn backend.api.main:app --port 8000
# Terminal 2 – Frontend:
streamlit run final-project/knowledge-research-agent/frontend/app.py
# Oder alles auf einmal (inkl. Neo4j):
cd final-project/knowledge-research-agent && docker compose up --build
```

**Danach:** [`../08-testing-und-produktion/`](../08-testing-und-produktion/README.md) – dein System wird betriebsreif.
