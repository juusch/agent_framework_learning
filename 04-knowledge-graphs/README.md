# Modul 4 – Knowledge Graphs: Wissen als Beziehungen 🕸️

**Ziel:** Du verstehst, **wann** Wissen aus Verbindungen besteht – und repräsentierst es zuerst in reinem Python (wie in Build 1!), dann in einer echten Graph-Datenbank (Neo4j + Cypher).

## Die intuitive Progression

| Stufe | Wissentlich? | Beispiel |
|---|---|---|
| Python-Dictionaries | Struktur, flüchtig | `{"name": "Anna", "abteilung": "Engineering"}` |
| **Graph-Datenstruktur** (Nodes + Kanten) | + Verbindungen als Daten | `Anna --WORKS_FOR--> Acme` |
| **Graph-Datenbank** (Neo4j) | + persistiert, durchfragbar (Cypher) | `MATCH (a)-[:WORKS_FOR]->(c) RETURN a, c` |
| **Knowledge Graph** | + Bedeutung/Schema (Ontologie) | Labels: Person/Company, Typen: WORKS_FOR, … |
| **Vektor-DB** (Build 2!) | Ähnlichkeit, nicht Struktur | findet sinngleiche **Texte**, folgt **keinen** Kanten |

**Metapher – Ermittlungsbrett vs. Buchregal:** Vektor-RAG ist das Buchregal („das Buch da drüben handelt vom Selben"); der Knowledge Graph ist das Ermittlungsbrett mit roten Fäden („Anna → arbeitet für → Acme → …"). Fragen wie *„Wie hängt Ben mit dem Projekt zusammen?"* beantwortet nur das Brett – selbst wenn der Satz nirgends geschrieben steht (**Emergenz**).

| # | Aufgabe | Zeit | DB nötig? |
|---|---|---|---|
| 4.1 | [`tasks/01-graphen-in-python.md`](tasks/01-graphen-in-python.md) – Entitäten, Beziehungen, Traversierung, Visualisierung | ~60 Min | nein |
| 4.2 | [`tasks/02-neo4j-und-cypher.md`](tasks/02-neo4j-und-cypher.md) – Neo4j, Cypher, Python-Brücke | ~60 Min | Docker – **Offline-Fallback vorhanden** |

**Ausführen:**
```bash
python3 04-knowledge-graphs/solutions/graph_queries.py
python3 04-knowledge-graphs/solutions/visualize_graph.py
python3 04-knowledge-graphs/solutions/python_neo4j_bridge.py   # mit Fallback
```

**Danach:** [`../05-build3-langgraph-graphrag/`](../05-build3-langgraph-graphrag/README.md) – **Build 3**: Graph trifft Vektor, LangGraph steuert.
