# 🏛️ Architektur der Lernakademie

Diese Seite erklärt, **wie das Repository aufgebaut ist** und wie die technischen Bausteine zusammenwirken – auch für spätere Erweiterungen (Stufe 5–9).

## Verzeichnisstruktur

```
lernakademie/
├── README.md                    # Navigation -> START_HERE.ipynb
├── START_HERE.ipynb               # Einstieg: Setup, Jupyter-Basics, erste Aufgabe
├── PROGRESS.md                    # Checkliste (Notebook-Nummern)
├── requirements.txt / pyproject.toml / .env.example
├── notebooks/                     # 20 Lektionen in 11 Modul-Ordnern
│   ├── 01_python/ … 11_testing/
├── solutions/                     # 20 ausgefuehrte Loesungs-Notebooks
├── lernakademie/                  # zentrale Module: config, llm_client (Provider),
│   │                              # build1/build2 (Pipelines), graph_store (Neo4j-Pendant),
│   │                              # graph_extraction, mock_llm, offline_embeddings
├── frontend/                      # build1_chat.py (Lektion 06)
├── final-project/knowledge-research-agent/   # Capstone: FastAPI + Streamlit + Docker
├── data/                          # Wissensdokumente (alle Builds & Finale)
├── scripts/                       # Notebook-Baukasten (nbkit + Specs + build)
├── tests/                         # Akademie-Tests inkl. test_notebooks.py
├── tools/                         # test_llm_connection.py
└── docs/                          # Roadmap, Notebook-Guide, Glossar, Vergleich …
```

## Das Hilfs-Paket `lernakademie/`

Damit jede Loesung mit **und ohne** Mistral-API-Key laeuft, gibt es einen zentralen Schalter:

- `lernakademie/config.py`
  - laedt die `.env` (via `python-dotenv`),
  - entscheidet: echter Modus (Key vorhanden, nicht offline erzwungen) oder Offline-Modus.
- `lernakademie/mock_llm.py`
  - ein simuliertes Chat-Modell, das sich in Chains exakt wie ein echtes verhält (gleiche Schnittstelle), aber deterministische, klar mit `[OFFLINE]` markierte Antworten erzeugt. So koennen Lernende **kostenlos und ohne Anmeldung** alle Konzepte ueben und die Automatisierten Tests laufen ohne Credentials in CI.
- `lernakademie/offline_embeddings.py`
  - ein transparentes, schluesselwort-basiertes Embedding-Modell fuer die RAG-Stufe: Es erkennt definierte Schluesselwoerter und bildet daraus Vektoren. Es ist absichtlich simpel, damit Lernende **sehen**, was Embeddings tun – echte Embeddings von Mistral werden im Text erklaert und per Key automatisch verwendet.

### Warum dieses Design?

1. **Lernqualitaet:** Konzepte (Chains, Retrieval) lassen sich ohne Kosten-Sorge erforschen; der Wechsel zum echten Modell ist nur eine Zeile in `.env`.
2. **Testbarkeit:** Alle Tests (`pytest`) laufen ohne Netzwerk und ohne Geheimnisse – Voraussetzung fuer die GitHub-Actions-CI.
3. **Kein Leaking:** API-Keys liegen nur in der nicht versionierten `.env`.

## Versionsstrategie

Wir pinnen Hauptversionen (`langchain>=1.0,<2.0` u.s.w.), weil das LangChain-Ökosystem sich schnell bewegt. Upgrades werden dokumentiert, indem man die Range in `requirements.txt` anpasst und `pytest` laufen laesst.

## Erweiterung: Knowledge Graphs & Capstone-Frontend (Stufen 10–15)

- `lernakademie/graph_store.py` – In-Memory-Property-Graph als Neo4j-Offline-Pendant (wie MockChatModel zum LLM): Nodes/Labels/Properties, gerichtete Relationships, Breitensuche-Pfade und ein kleiner lesender **Mini-Cypher-Subset**. Läuft überall ohne Installation.
- `lernakademie/graph_extraction.py` – LLM-Gestützte Entitäts-/Beziehungs-Extraktion (Pydantic-Vertrag; offline Regel-Fallback), Graph-Population mit Entity Resolution und die **Sicherheits-Whitelist** (`ist_sicher`/`fuehre_sicher_aus`) für generierte Abfragen.
- **Capstone-Anwendung** (`final-project/knowledge-research-agent/`): FastAPI-Backend (api/models/retrieval/graphs/agents/services in Schichten), LangGraph-Workflow (Intent → Route → Vektor/Graph/Hybrid → Antwort mit Quellentrennung), Freigabe-Workflow (interrupt/resume, Audit-Log), Streamlit-Frontend (Chat, PyVis-Graph-Explorer, Dokumente, Prompt-Labor, Verlauf) und Docker Compose (App + optional Neo4j). Getestet über FastAPI-TestClient – 12 Tests, komplett offline.

## Stufen 5–9 (implementiert)

Die Stufenordner `05` bis `09` folgen exakt demselben Muster (README + tasks + solutions). LangGraph-bezogene Aufgaben enthaalten Mermaid-Diagramme direkt in den Task-Dateien. Der Mock (`lernakademie/mock_llm.py`) simuliert seit Stufe 6 auch Tool-Calling (bind_tools, tool_calls, finale Antwort nach Tool-Ergebnis), sodass Agenten-Loops, Checkpointer-Dialoge und Freigaben komplett offline lauffaehig und in CI getestet sind.
