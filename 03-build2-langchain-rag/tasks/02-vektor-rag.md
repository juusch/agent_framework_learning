# Aufgabe 3.2 – Vektor-RAG: Chunking, Embeddings & Chroma 🔢

**Schwierigkeit:** Mittel · **Zeit:** ~60 Min · **Kosten:** keine (offline komplett)

## Lernziel
Du verstehst, **warum** Embeddings die Wortsuche aus Build 1 schlagen, und baust den kompletten Retrieval-Stack: Splitter → Embeddings → Chroma → Retriever.

## Warum das wichtig ist
Build 1 fand „Urlaub" nur, wenn „Urlaub" wörtlich stand. **Metapher – die Bedeutungs-Landkarte:** Ein Embedding gibt jedem Text Koordinaten der *Bedeutung*; „freie Tage beantragen" und „Urlaubsantrag stellen" liegen dicht beieinander – **ohne ein gemeinsames Wort**. Eine Vektor-DB ist die Bibliothek, die nach Bedeutung statt nach Alphabet sortiert.

## Deine Mission
1. **Chunking:** `RecursiveCharacterTextSplitter(600, 100)` auf die Handbücher – verstehe die Parameter (zu klein = Sinn zerschnitten, zu groß = unpräzise + Kontextfenster).
2. **Embedding-Anschauung:** erzeuge Embeddings für 3 Fragen (`get_embeddings()`), miss paarweise Cosine-Ähnlichkeiten – erwartungsgemäß: themengleiche Fragen ähnlicher als themenfremde.
3. **Vektor-DB:** Chunks in Chroma speichern, Retriever (`k=3`) bauen, vier Fragen stellen, Treffer mit **Quellen** ausgeben.
4. **Direkter Vergleich mit Build 1:** „Wie beantrage ich freie Tage?" – gegen deine Build-1-Wortsuche UND den Retriever. Schreibe als Kommentar: Was findet welcher besser und warum?

## Akzeptanzkriterien
- [ ] Chunk-Overlap ist gesetzt – du kannst erklären, warum.
- [ ] Die Ähnlichkeitsmatrix zeigt plausible Werte.
- [ ] Der Retriever liefert Treffer mit Quellenangabe (Metadata!).
- [ ] Dein Build-1-vs-Build-2-Kommentar nennt einen konkreten Fragefall.

## Hinweise
1. `get_embeddings()` (Akademie) = offline Schlüsselwörter, mit Key echte Mistral-Embeddings.
2. Chroma: `from langchain_chroma import Chroma`; Retriever: `db.as_retriever(search_kwargs={"k": 3})`
3. `split_documents` behält Metadaten (`source`) – die Basis für Quellenangaben.

## Reflexionsfragen
1. Warum darf man Chunks mit verschiedenen Embedding-Modellen **nie** mischen?
2. Was kostet `k=6` gegenüber `k=3` – Latenz, Tokens, Präzision?
3. Was findet auch der beste Retriever **nicht**? (→ „Wer arbeitet mit wem zusammen?" – Beziehungen! Lösung: Modul 4/5)

## Referenzlösung + Walkthrough
→ [`solutions/chunker.py`](../solutions/chunker.py), [`solutions/vector_search.py`](../solutions/vector_search.py), [`solutions/document_loader.py`](../solutions/document_loader.py)

## Weiter
3.3 – du schließt Build 2 ab: RAG-Chain mit Quellen, strukturierten Ausgaben – und der Assistent antwortet auf Dokumentenbasis.
