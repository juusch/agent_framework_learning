# 🎓 LangChain & LangGraph Lernakademie

**Ein geführtes Programmier-Labor in Jupyter-Notebooks – von null bis zum eigenen KI-Agenten mit Frontend, auf Deutsch.**

> ### ▶️ Jetzt starten: [`START_HERE.ipynb`](START_HERE.ipynb)
> Das Notebook ist dein Einstieg, dein Setup-Check und dein first Win – in ~15 Minuten.

## Was ist das?

Diese Akademie folgt einem Leitprinzip: **Build It 3 Times.** Du baust denselben **Personal Knowledge Assistant** drei Mal – jedes Mal verstehst du mehr:

| Build | Werkzeuge | Ordner |
|---|---|---|
| 🧱 **Build 1** | reines Python + direkter LLM-Aufruf (alles von Hand!) | `notebooks/03_build_1/` |
| 🔗 **Build 2** | LangChain + Vektor-RAG (semantische Suche) | `notebooks/05_build_2/` |
| 🚀 **Build 3** | LangGraph + Knowledge Graph + Hybrid-Retrieval + Agent | `notebooks/08_build_3/` |

Vergleich der Architekturen: [docs/same-problem-three-architectures.md](docs/same-problem-three-architectures.md)

**Wie funktioniert lernen hier?** Jedes Notebook ist **Lektion + Tutorial + Aufgabe + Arbeitsplatz + Prüfung in einem**: Erklärung mit Metaphern → Beispiele zum Ausführen → deine Aufgabe mit Workspace-Zelle (`# YOUR CODE HERE`) → automatische Prüfe (`assert`) → Reflexion → nächste Lektion. Du verlässt das Notebook nicht.

## Voraussetzungen

- Ein Computer mit Windows, macOS oder Linux
- **Kein** Vorwissen in Programmierung
- Optional (nicht nötig zum Starten!): ein [Mistral-API-Key](https://console.mistral.ai/) **oder** ein lokaler AI-Server (LM Studio, Ollama, …) – ohne beides läuft alles im **Offline-Modus** (kostenlos, mit klar gekennzeichneten Simulations-Antworten)

## Installation

```bash
git clone https://github.com/juusch/agent_framework_learning
cd agent_framework_learning
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m ipykernel install --user --name=lernakademie
jupyter lab
```

Dann `START_HERE.ipynb` öffnen und dem Pfad folgen. Details: [docs/notebook-guide.md](docs/notebook-guide.md)

## Der Notebook-Lernpfad (21 Notebooks)

| # | Notebook | Modul |
|---|---|---|
| – | [START_HERE.ipynb](START_HERE.ipynb) | Einstieg + Setup + Mini-Aufgabe |
| 01–02 | `notebooks/01_python/` | Python-Grundlagen, Funktionen, venv & Keys |
| 03–04 | `notebooks/02_llm/` | erster LLM-Aufruf, Chatbot mit Gedächtnis |
| 05–06 | `notebooks/03_build_1/` | 🧱 **BUILD 1** + Wartungsschmerz + erste UI |
| 07–08 | `notebooks/04_langchain/` | Chains, Embeddings & Vektor-RAG |
| 09 | `notebooks/05_build_2/` | 🔗 **BUILD 2**: RAG-Assistent mit Quellen |
| 10–12 | `notebooks/06_knowledge_graph/` | Graphen in Python, Neo4j & Cypher, LLM-Extraktion |
| 13–14 | `notebooks/07_langgraph/` | Workflows (State, Routing, Loops), Hybrid-Retrieval |
| 15 | `notebooks/08_build_3/` | 🚀 **BUILD 3**: Hybrid-Agent mit Freigabe |
| 16–18 | `notebooks/09_agents/` | Tools & Agenten, Gedächtnis & Freigabe, Supervisor |
| 19 | `notebooks/10_capstone/` | 🏁 das finale System live getestet + Frontend-Start |
| 20 | `notebooks/11_testing/` | Testing, Evaluierung + Abschluss-Reflexion |

Zu jeder Lektion gibt es ein Lösungs-Notebook in `solutions/` (erst **nach** deinem Versuch öffnen!). Fortschritt abhaken: [PROGRESS.md](PROGRESS.md).

## 🖥️ Wo läuft deine KI? Du entscheidest (nur `.env`, kein Code!)

- **Mistral Cloud:** `MISTRAL_API_KEY` in `.env` eintragen.
- **Lokaler AI-Server** (LM Studio, Ollama, vLLM, LocalAI, llama.cpp): `LLM_BASE_URL` + `LLM_MODEL` konfigurieren (`LLM_API_KEY=` ist gültig – viele lokale Server brauchen keinen Key!).
- **Jeder OpenAI-kompatible Endpoint** – auch im Netzwerk oder in der Cloud.
- **Ohne alles:** Offline-Modus (jede Lektion läuft sofort, kostenlos).

Verbindung testen: `python -m tools.test_llm_connection` · Alles Weitere: [docs/local-ai-server.md](docs/local-ai-server.md)

## Das Finale

[`final-project/knowledge-research-agent/`](final-project/knowledge-research-agent/README.md) – dein Build-3-Assistent als lauffähiges System: FastAPI-Backend, Streamlit-Frontend (Chat, interaktiver Graph-Explorer, Dokument-Upload, Prompt-Labor, Freigaben, Verlauf), Docker Compose inkl. Neo4j. **In Lektion 19 testest du es von innen und startest es dann im Browser.**

## Qualitätsstandards

- **113 automatische Tests** (CI auf GitHub Actions): Akademie-Logik, Agenten, Graphen, Provider-Konfiguration **+ Notebook-Validierung** (Parsing, Syntax, Struktur, ausgeführte Lösungen)
- Alle 20 Lösungs-Notebooks wurden **komplett von frischen Kernels ausgeführt** (offline)
- Zentrale Anbieter-Konfiguration überall; keine Secrets im Repo
- Ehrlicher Validierungsbericht: [docs/FINAL_VALIDATION.md](docs/FINAL_VALIDATION.md)

## Weiterführendes

[Lernfahrplan](docs/learning-roadmap.md) · [Notebook-Guide](docs/notebook-guide.md) · [Lokale AI-Server](docs/local-ai-server.md) · [Glossar](docs/glossary.md) · [Troubleshooting](docs/troubleshooting.md) · [Architektur](docs/architecture.md) · [Mitmachen](CONTRIBUTING.md) · [Lizenz](LICENSE) (MIT)
