# 🎓 Capstone: Personal Knowledge & Research Agent

**Die Abschluss-Anwendung der Akademie:** Ein vollständiges System mit hybrider Wissensarchitektur (Vektor-DB + Knowledge Graph), LangGraph-Agenten-Workflow, FastAPI-Backend, Streamlit-Frontend und Human-in-the-Loop-Freigaben.

```mermaid
flowchart TB
    U[ Nutzer ] --> FE[ Streamlit-Frontend<br/>Chat / Graph / Dokumente / Labor ]
    FE -- HTTP/JSON --> BE[ FastAPI-Backend ]
    BE --> AG[ LangGraph-Agent<br/>Intent -> Routing -> Retrieval -> Antwort ]
    AG --> V[( Vektor-DB:<br/>Dokument-Chunks )]
    AG --> G[( Knowledge Graph:<br/>Entitaeten + Beziehungen )]
    AG --> INT{{ Freigabe?<br/>interrupt }}
    INT -- "resume" --> G
```

## Features

| Bereich | Was du machen kannst |
|---|---|
| **Chat mit Agent** | Fragen stellen; der Agent klassifiziert die Frage und wählt die Retrieval-Route (Vektor / Graph / Hybrid) |
| **Knowledge-Graph-Explorer** | Graph interaktiv sehen (PyVis), Nodes anklicken, Nachbarn erkunden, Entity-Suche |
| **Dokumente & RAG** | Text-Dokumente hochladen, Dokumentliste sehen, Fragen mit Quellenfundstellen |
| **Agent-Workflow-Ansicht** | Pro Antwort sehen: welche Route, welche Quellen, welche Fakten – getrennt nach Herkunft |
| **Prompt-Labor** | System-/User-Prompts und Temperature experimentell setzen – Wirkungen sofort sichtbar |
| **Freigaben (Human-in-the-Loop)** | Fakten-Vorschläge prüfen und genehmigen/ablehnen – destruktive Graph-Änderungen nur mit dir |
| **Verlauf** | Alle Fragen/Antworten mit Routen und Quellen nachlesen |

## Schnellstart (lokal, offline – ohne API-Key!)

```bash
# 1. Abhängigkeiten (Projektwurzel der Akademie):
pip install -r requirements.txt

# 2. Backend starten (vom Akademie-Hauptordner):
uvicorn "final-project.knowledge-research-agent.backend.api.main:app" --port 8000
#    (Alternative: cd final-project/knowledge-research-agent/backend &&
#      uvicorn api.main:app --port 8000)

# 3. Frontend starten (zweites Terminal):
streamlit run "final-project/knowledge-research-agent/frontend/app.py"
#    Browser öffnet sich automatisch (http://localhost:8501)
```

> **Anbieter-unabhängig (zentrale Konfiguration):** Diese Anwendung nutzt **dieselbe** Konfigurationsschicht wie die ganze Akademie (`lernakademie/config.py`). Sie läuft gegen Mistral Cloud, einen **lokalen AI-Server** (LM Studio, Ollama, vLLM …) oder jeden OpenAI-kompatiblen Endpoint – gesteuert **nur über `.env`**, ohne Codeänderung. Verbindung prüfen: `python -m tools.test_llm_connection`. Ohne jede Konfiguration läuft alles kostenfrei im Offline-Modus: Retrieval, Graph, Workflow und Freigaben sind echt; nur die Sprachformulierung des LLM ist simuliert (`[OFFLINE]`). Details: [docs/local-ai-server.md](../../docs/local-ai-server.md).

## Mit Docker Compose (inkl. Neo4j)

```bash
cd final-project/knowledge-research-agent
docker compose up --build
# Frontend: http://localhost:8501 | Backend-Doku: http://localhost:8000/docs
# Neo4j-Browser: http://localhost:7474 (neo4j / lernakademie)
```

Der Backend-Service nutzt ohne laufendes Neo4j automatisch den GraphStore-Fallback – die Anwendung startet also **immer**.

## Architektur (auch Aufgabe 15.3 zum Nachvollziehen)

```
final-project/knowledge-research-agent/
├── backend/
│   ├── api/         # FastAPI-Endpunkte (main.py)
│   ├── agents/      # Agent-Workflow-Logik (research_agent.py)
│   ├── graphs/      # LangGraph-Workflow (workflow.py: Intent -> Routing)
│   ├── retrieval/   # Vektor- + Graph-Retrieval (vector.py, graph_store_api.py)
│   ├── models/      # Pydantic-Schemas für Requests/Responses
│   ├── services/    # Sitzungen, Verlauf, Konfiguration
│   └── seed/        # Start-Dokumente (im Repo, offline nutzbar)
├── frontend/
│   ├── app.py       # Streamlit-Hauptoberfläche (Navigation)
│   ├── pages/       # Graph-Explorer, Prompt-Labor (python-file pages)
│   └── components/  # PyVis-Graph-Visualisierung
├── database/
│   ├── schema/      # Graph-Schema-Doku (Labels, Beziehungstypen)
│   └── seed/        # Seed-Graph-Daten
├── tests/           # API-Tests (laufen offline in CI)
├── docker-compose.yml
├── Dockerfile       (im backend/, siehe Compose)
└── .env.example
```

## Beispiel-Fragen zum Ausprobieren

- „Was wissen wir über das AI-Assistant-Projekt?" → **Hybrid** (Doku + Graph)
- „Wer hängt mit Anna zusammen?" → **Graph-Route** (Traversierung)
- „Was steht im Firmenprofil über Weiterbildung?" → **Vektor-Route**
- „Wie hängt Ben mit dem Projekt zusammen?" → **Graph-Route** (Emergenz!)

Jede Antwort zeigt ihre **Quellen** (Dokument-Fundstellen vs. Graph-Fakten) – du siehst immer, woher das Wissen kommt.

## Sicherheitshinweise

- API-Keys nur in `.env` (nie committen – siehe Akademie-Stufe 9).
- Graph-Schreibzugriffe **nur** über den Freigabe-Workflow (interrupt + resume).
- LLM-generierte Abfragen werden vor Ausführung durch die lesende Whititelist geprüft.
- `/status` und das Frontend zeigen Anbieter, Modell und Endpoint – **niemals** den API-Key.
- Lokaler Server übers Netzwerk? Authentifizierung aktivieren – Sicherheitshinweise: [docs/local-ai-server.md](../../docs/local-ai-server.md).
- Diese Anwendung ist ein **Lernsystem für den lokalen Betrieb** – vor einer Veröffentlichung im Internet: Stufe 15.3/9 (Auth, HTTPS, Rate-Limits) umsetzen.
