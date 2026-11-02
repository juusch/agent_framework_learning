# 🎓 LangChain & LangGraph Lernakademie

**Von absolut null bis zu eigenen KI-Anwendungen – auf Deutsch, Schritt für Schritt, mit echten Übungen.**

Willkommen! Dieses Repository ist eine geführte Lernreise. Es ist **keine** Sammlung von Dokumentation und auch kein Code-Snippet-Archiv, sondern eine strukturierte, aufgabengetriebene Akademie für Menschen, die noch **nie programmiert** haben.

## Für wen ist das?

Du bist hier genau richtig, wenn du:

- noch nie eine Zeile Python geschrieben hast,
- nicht weißt, was ein Terminal, eine API oder ein „LLM" ist,
- irgendwann eigene KI-Anwendungen mit **LangChain**, **LangGraph** und **Mistral AI** bauen möchtest,
- am besten durch Ausprobieren, Wiederholen und kleine Erfolge lernst.

## Wie funktioniert die Akademie?

1. **Lies [`START_HERE.md`](START_HERE.md)** – dort startest du in 10 Minuten mit deinem ersten Programm.
2. Arbeite die Lernstufen **in Reihenfolge** durch (siehe [Lernfahrplan](docs/learning-roadmap.md)).
3. Jede Aufgabe folgt immer demselben Aufbau: Konzept erklärt → deine Mission → Hinweise → **dein Versuch** → Referenzlösung mit Zeile-für-Zeile-Walkthrough.
4. Trage deinen Fortschritt in [`PROGRESS.md`](PROGRESS.md) ein.

## Die Lernstufen

| Stufe | Ordner | Thema | Meilenstein |
|---|---|---|---|
| 0 | [`00-getting-started/`](00-getting-started/) | Einrichtung + erstes Programm | Hello World 🎉 |
| 1 | [`01-python-fundamentals/`](01-python-fundamentals/) | Python-Grundlagen, venv, API-Keys | Kleines Persönlichkeits-Programm |
| 2 | [`02-understanding-llms/`](02-understanding-llms/) | LLMs, Tokens, APIs, Mistral | Erster API-Call + Chatbot |
| 3 | [`03-langchain-fundamentals/`](03-langchain-fundamentals/) | LangChain: Prompts, Chains, strukturierte Ausgaben | Content-Assistant |
| 4 | [`04-rag-and-knowledge/`](04-rag-and-knowledge/) | RAG: Dokumente, Embeddings, Vektor-DB | Dokumenten-QA-Assistent |
| 5 | [`05-langgraph-fundamentals/`](05-langgraph-fundamentals/) | LangGraph: State, Nodes, Edges, Routing, Loops | Erster eigener Graph |
| 6 | [`06-ai-agents/`](06-ai-agents/) | Agenten: Tools, Memory, Checkpointer, Freigabe | Wissens-Agent |
| 7 | [`07-advanced-langgraph/`](07-advanced-langgraph/) | Parallelität, Subgraphs, Supervisor | Multi-Agent-System |
| 8 | [`08-real-world-projects/`](08-real-world-projects/) | 4 vollständige Projekte in Meilensteinen | Eigenes End-to-End-Projekt |
| 9 | [`09-production/`](09-production/) | Testing, Sicherheit, Logging, Docker | Abschluss-Challenge 🎓 |
| 10 | [`10-knowledge-graph-fundamentals/`](10-knowledge-graph-fundamentals/) | Knowledge Graphs: Nodes, Beziehungen, Traversierung | erster eigener Graph |
| 11 | [`11-graph-databases/`](11-graph-databases/) | Neo4j, Cypher, Python-Brücke | echte Graph-DB |
| 12 | [`12-graphs-und-llms/`](12-graphs-und-llms/) | LLM-Extraktion, NL→Cypher mit Sicherheits-Whitelist | selbstfüllender Graph |
| 13 | [`13-graphrag/`](13-graphrag/) | Vektor vs. Graph vs. Hybrid-Retrieval | GraphRAG |
| 14 | [`14-graph-agents/`](14-graph-agents/) | Graph-Aware Agents, Freigabe für Graph-Schreibzugriffe | Hybrid-Agent |
| 15 | [`15-frontend/`](15-frontend/) | FastAPI + Streamlit: UI↔Backend-Konzepte | erste Web-Oberfläche |
| 🎓 | [`final-project/knowledge-research-agent/`](final-project/knowledge-research-agent/) | **Capstone:** Wissens- & Recherche-Agent mit Frontend | komplette Anwendung |

## 🕸️ Neu: Knowledge Graphs & Frontend

Die Akademie wurde um zwei Dimensionen erweitert: **Knowledge Graphs** (Stufen 10–14: Graphen in Python, Neo4j/Cypher, LLM-Extraktion, GraphRAG, graph-aware Agents) und ein **vollständiges Frontend** (Stufe 15: FastAPI + Streamlit) – gekrönt vom Capstone-Projekt [final-project/knowledge-research-agent/](final-project/knowledge-research-agent/README.md): eine lauffähige Anwendung mit Chat, interaktivem Graph-Explorer (PyVis), Dokument-RAG, Prompt-Labor, Verlauf und Human-in-the-Loop-Freigaben – **offline nutzbar, mit Docker Compose (inkl. Neo4j) für den vollen Betrieb**.

## 💰 Kosten: Fast alles ist kostenlos

Wir nutzen zwei Modi:

- **Offline-Modus (Standard):** Jede Übung läuft auch **ohne API-Key und ohne Kosten**, weil ein klar gekennzeichneter simulierter LLM-Modus (`[OFFLINE]`) verwendet wird.
- **Echter Mistral-Modus:** Sobald du einen Mistral-API-Key in `.env` einträgst (siehe [`.env.example`](.env.example)), verwendet jede Lösung automatisch das echte Modell.

Aufgaben, die mit ⚠️ **Kosten** markiert sind, führen echte API-Aufrufe aus, wenn ein Key vorhanden ist – ohne Key laufen sie automatisch im Offline-Modus weiter.

## Voraussetzungen

- Ein Computer mit Windows, macOS oder Linux.
- Internetzugang (für die Installation von Python und Paketen).
- **Kein** Vorwissen in Programmierung.

## Schnellstart (3 Schritte)

```bash
# 1. Python 3.11+ installieren (siehe START_HERE.md), dann:
python -m venv .venv

# 2. Virtuelle Umgebung aktivieren
#    Windows:  .venv\Scripts\activate
#    macOS/Linux: source .venv/bin/activate

# 3. Abhängigkeiten installieren
pip install -r requirements.txt
```

Kopiere anschließend `.env.example` zu `.env`, wenn du echte Mistral-Aufrufe machen möchtest.

## Mitmachen

Fehler gefunden oder Ideen? [`CONTRIBUTING.md`](CONTRIBUTING.md) erklärt, wie du helfen kannst.

## Lizenz

MIT – siehe [`LICENSE`](LICENSE). Die mitgelieferten Übungsdaten (`04-rag-and-knowledge/data/`) sind frei erfunden.
