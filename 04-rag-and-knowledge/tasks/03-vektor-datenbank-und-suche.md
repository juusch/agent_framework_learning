# Aufgabe 4.3 – Vektor-Datenbank & semantische Suche 🗄️

## Schwierigkeit
Leicht · ⚠️ **Kosten:** Embedding-Aufrufe nur mit Key (offline: komplett kostenlos)

## Lernziel
Du speicherst Chunks mit Embeddings in einer echten Vektor-Datenbank (Chroma) und beantwortest Fragen über **Similarity Search** – die Retriever-Schnittstelle von LangChain.

## Warum ist das wichtig?
Die Vektor-DB ist die „Bibliothek nach Bedeutung" deines RAG-Systems. Der **Retriever** ist ihr einheitlicher Ausgabeschalter: `retriever.invoke(frage)` liefert die relevantesten Chunks – egal ob dahinter Chroma, FAISS oder ein Cloud-Dienst steckt. Genau diese Abstraktion nutzt die RAG-Chain in 4.4.

## Das Konzept einfach erklärt
**Metapher – die Bedeutungs-Bibliothek:** Eine normale Bibliothek sortiert nach Titel (Alphabet). Eine Vektor-DB sortiert nach **Bedeutung**: Du beschreibst, *worüber* du lesen willst, und der Bibliothekar bringt die sinngleichen Regale. Chroma macht das lokal, ohne Server – die „Bibliothek" ist ein Ordner auf deiner Festplatte.

## Die technische Erklärung
- `Chroma(collection_name=..., embedding_function=embeddings)` – mit `persist_directory` bleibt der Index zwischen Programmläufen erhalten; ohne läuft er im Speicher (frisch pro Start).
- `db.add_documents(chunks)` berechnet Embeddings, speichert Text + Metadaten + Vektor.
- `db.as_retriever(search_kwargs={"k": 3})` – Standard-Retriever: liefert die **k** ähnlichsten Chunks zur Frage.
- Der Retriever ist ein **Runnable**: `.invoke("Frage")` → Liste von Documents. Deshalb passt er später direkt in Chains (4.4)!

## Voraussetzungen
- Aufgabe 4.2 (Chunks, Embeddings, `get_embeddings()`)

## Deine Mission
Schreibe `vector_search.py`:
1. Lade **beide** Handbücher, splitte sie (`chunk_size=600, chunk_overlap=100`) – mit `split_documents`, damit die Metadaten (Quelldatei!) erhalten bleiben.
2. Baue eine Chroma-Sammlung `handbuch` und füge alle Chunks hinzu. Gib aus, wie viele Chunks gespeichert wurden.
3. Baue den Retriever (`k=3`) und stelle **vier** Fragen: „Wie viele Urlaubstage gibt es?", „Wann verfällt Resturlaub?", „Wie richte ich VPN ein?", „Was sind die Passwort-Regeln?".
4. Gib pro Frage die **Gefundenen Chunks** aus: Quelle (aus `metadata["source"]`) + die ersten ~150 Zeichen des Texts – nicht mehr! Du sollst sehen, *was* gefunden wurde, bevor das LLM es in 4.4 verarbeitet.
5. Bonus: Erhöhe `k` auf 6 und beobachte: Ab wann kommen auch *weniger* passende Chunks mit? Was kostet das (Tokens, Präzision)?

## Akzeptanzkriterien
- [ ] Alle Chunks beider Dokumente liegen in **einer** Chroma-Sammlung.
- [ ] Jede Ausgabe zeigt die **Quelle** (Dateiname).
- [ ] Die vier Fragen liefern erkennbar passende Chunks (offline: mit Schlüsselwörtern wie „Urlaub"/„Passwort"/„VPN").
- [ ] `k` ist ein Parameter, mit dem du gespielt hast – und du notierst deine Beobachtung als Kommentar.

## Hinweise
1. `TextLoader(...).load()` → Liste; `splitter.split_documents(dokumente)` behält `metadata`.
2. Quelle hübsch machen: `Path(dokument.metadata["source"]).name`
3. Chroma-Import: `from langchain_chroma import Chroma`
4. Chroma läuft ohne Key, wenn die Offline-Embeddings aktiv sind – nur dann funktionieren Suchen mit exakten Schlüsselwörtern.

## Reflexionsfragen
1. Warum ist die Retriever-Abstraktion (`as_retriever`) wertvoller als direkte `db.similarity_search(...)`-Aufrufe in deinem Anwendungscode?
2. Was würde passieren, wenn du Chunks mit **unterschiedlichen Embedding-Modellen** in dieselbe Sammlung mischst?
3. Welchen Einfluss hat `k` auf Antwortqualität, Kosten und Latenz – und wo liegt der klassische Kompromiss (Stichwort: „More context is not always better")?

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| Leere Suchergebnisse | Chunks nicht hinzugefügt (`add_documents` vergessen) oder falsche Collection |
| Offline-Treffer fehlen | Suchbegriffe nutzen; offline wird nur über Schlüsselwörter gesucht |
| Alte Daten stören | Persistenz-Ordner wechseln/leeren oder Collection-Namen ändern |

## Referenzlösung
→ [`solutions/vector_search.py`](../solutions/vector_search.py)

## Code-Walkthrough
In der Lösungsdatei; besonders der Aufbau `lade_chunks()` → `baue_datenbank()` → `suche()`.

## Was haben wir gelernt?
Vektor-DB-Grundlagen, Retriever als Runnable, Quellentransparenz, k-Tuning.

## Was kommt als Nächstes?
Der große Finale dieser Stufe: Du schließt den RAG-Kreis – Retriever-Ergebnisse **in den Prompt** injizieren und das LLM auf Basis der Chunks antworten lassen (mit Quellenangabe!). Das ist die Q&A-Anwendung, die du kenntest, bevor du wusstest, wie sie funktioniert.
