# 🎓 LangChain & LangGraph Lernakademie

**Von absolut null bis zum eigenen KI-Agenten mit Frontend – auf Deutsch, Schritt für Schritt.**

Diese Akademie folgt einem Leitprinzip: **Build It 3 Times.** Du baust denselben **Personal Knowledge Assistant** drei Mal – jedes Mal mit besseren Werkzeugen, jedes Mal mit tieferem Verständnis:

> 🧱 **Build 1** – Pure Python: alles von Hand verstehen
> 🔗 **Build 2** – LangChain + Vektor-RAG: semantische Suche, Fließband-Chains
> 🚀 **Build 3** – LangGraph + Knowledge Graph + Hybrid-Retrieval: der vollwertige Agent

→ Die vollständige Gegenüberstellung: **[„Same Problem, Three Architectures"](docs/same-problem-three-architectures.md)**

## Für wen?

Noch nie programmiert? Kein Terminal, keine API, kein LLM gesehen? **Genau richtig hier.** Du brauchst nur einen Computer, Internet und Neugier – kein Vorwissen.

## Der Weg in 9 Modulen (~23 Aufgaben, je 30–90 Min)

| Modul | Thema | Build |
|---|---|---|
| 0 | [`00-setup/`](00-setup/) – Python, Terminal, Funktionen, venv, API-Keys | – |
| 1 | [`01-llms-und-mistral/`](01-llms-und-mistral/) – erster API-Call, Chatbot, Temperature | – |
| 2 | [`02-build1-python-assistent/`](02-build1-python-assistent/) – **BUILD 1**: der Assistent in reinem Python + erste Oberfläche | 🧱 1 |
| 3 | [`03-build2-langchain-rag/`](03-build2-langchain-rag/) – **BUILD 2**: Chains, Embeddings, Vektor-RAG | 🔗 2 |
| 4 | [`04-knowledge-graphs/`](04-knowledge-graphs/) – Graphen in Python, Neo4j & Cypher | – |
| 5 | [`05-build3-langgraph-graphrag/`](05-build3-langgraph-graphrag/) – **BUILD 3**: LangGraph, Hybrid-Retrieval, Freigaben | 🚀 3 |
| 6 | [`06-agents-und-tools/`](06-agents-und-tools/) – Agenten-Vertiefung: Tools, Gedächtnis, Supervisor | – |
| 7 | [`07-finale-app/`](07-finale-app/) – die finale Anwendung + komplettes Frontend + Docker | 🏁 |
| 8 | [`08-testing-und-produktion/`](08-testing-und-produktion/) – Testing, Sicherheit, Betrieb, Abschluss | – |

**Das Finale:** [`final-project/knowledge-research-agent/`](final-project/knowledge-research-agent/README.md) – dein Build-3-Assistent als lauffähiges System: FastAPI-Backend, Streamlit-Frontend (Chat, interaktiver Graph-Explorer, Dokument-Upload, Prompt-Labor, Freigaben), Docker Compose inkl. Neo4j.

## 🖥️ Wo läuft deine KI? Du entscheidest (nur `.env`, kein Code!)

Die Akademie ist **anbieter-unabhängig** – dieselben Aufgaben laufen mit:

- **Mistral Cloud** (Standard-Beispiel): `MISTRAL_API_KEY` in `.env` eintragen.
- **Lokalem AI-Server** (LM Studio, Ollama, vLLM, LocalAI, llama.cpp …): `LLM_BASE_URL` + `LLM_MODEL` konfigurieren.
- **Jedem OpenAI-kompatiblen Endpoint** – auch im Netzwerk oder in der Cloud.
- **Ohne alles:** Offline-Modus (Simulation – jede Lösung läuft kostenlos und komplett).

Verbindung testen nach jeder Änderung: `python -m tools.test_llm_connection`
Alles Wissenswerte: **[docs/local-ai-server.md](docs/local-ai-server.md)**

## 💰 Kosten: fast alles ist kostenlos

Zwei Modi, automatisch gewählt: **Ohne API-Key** läuft jede Lösung im Offline-Modus (klar gekennzeichnete `[OFFLINE]`-Antworten; Retrieval, Graphen, Workflows und Freigaben sind trotzdem echt). **Mit** `MISTRAL_API_KEY` in `.env` wird alles zu echten Mistral-Anwendungen – oder zu deinem lokalen Server. Aufgaben mit echten API-Kosten sind mit ⚠️ markiert.

## Schnellstart

```bash
python -m venv .venv                       # 1. Umgebung
source .venv/bin/activate                  #    Windows: .venv\Scripts\activate
pip install -r requirements.txt            # 2. Abhängigkeiten
cp .env.example .env                      #    (optional: Key oder lokalen Server eintragen)
python -m tools.test_llm_connection        #    Verbindung testen
python3 00-setup/solutions/hello_world.py  # 3. Los geht's!
```

Dann: [`START_HERE.md`](START_HERE.md) lesen → [`PROGRESS.md`](PROGRESS.md) als Checkliste nutzen.

## Das Lernversprechen

Wenn du durch bist, hast du die Stationen erlebt:

1. „Ich kann Python eine KI anrufen lassen."
2. „Ich verstehe, was LangChain mir abnimmt."
3. „Ich verstehe, wie Vektor-Datenbanken Wissen finden."
4. „Ich verstehe, wie Knowledge Graphen Beziehungen darstellen."
5. „Ich habe einen Agenten gebaut, der **alles** kombiniert – und bediene ihn über ein echtes Frontend."

## Weiterführendes

[Lernfahrplan](docs/learning-roadmap.md) · [Lokale AI-Server](docs/local-ai-server.md) · [Glossar](docs/glossary.md) · [Troubleshooting](docs/troubleshooting.md) · [Python-Basics](docs/python-basics.md) · [Architektur](docs/architecture.md) · [Mitmachen](CONTRIBUTING.md) · [Lizenz](LICENSE) (MIT)
