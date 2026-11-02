# Aufgabe 4.2 – Chunking & Embeddings ✂️🔢

## Schwierigkeit
Leicht · **Kosten: keine** – die Offline-Embeddings laufen lokal!

## Lernziel
Du zerlegst Dokumente in sinnvolle **Chunks** und erzeugst **Embeddings** – die Zahlen-Übersetzung von Bedeutung. Du verstehst beides so gut, dass du es erklären kannst.

## Warum ist das wichtig?
Chunking + Embeddings sind das Herz von RAG. Suche „nach Bedeutung" statt nach Wortgleichheit wird erst möglich, wenn Text als Zahlenvektor vorliegt, deren Ähnlichkeit messbar ist.

## Das Konzept einfach erklärt
- **Chunking – Metapher:** Ein Buch in Kapitel-Lesezeichen zerlegen. Nicht zu klein (Sinn zerschnitten), nicht zu groß (Suche wird unpräzise, Kontextfenster platzt). Die Faustregel fürs erste: **500–1000 Zeichen pro Chunk**, mit Überlappung von ~100–200, damit keine Aussage an der Schnittstelle zerrissen wird.
- **Embedding – Metapher:** eine Landkarte der *Bedeutungen*: Jeder Text bekommt Koordinaten (einen Vektor). „Urlaubsantrag stellen" und „Wie beantrage ich Urlaub?" liegen auf dieser Karte nah beieinander – auch ohne ein gemeinsames Wort! Ähnlichkeit = Distanz auf der Bedeutungskarte.

## Die technische Erklärung
- `RecursiveCharacterTextSplitter(chunk_size=..., chunk_overlap=...)` aus `langchain_text_splitters` schneidet **hierarchisch**: erst an Absätzen, dann Sätzen, dann Wörtern – Chunks bleiben so natürlich.
- Ein Embedding-Modell hat eine **feste Vektorlänge** (z. B. 1024 Zahlen bei `mistral-embed`; unsere Offline-Version: eine Zahl pro Schlüsselwort).
- Ähnlichkeit misst man mit **Cosine Similarity** (Winkel zwischen Vektoren): 1.0 = gleichbedeutend, 0.0 = nichts gemeinsam.
- Die Akademie bietet zwei Varianten (siehe `lernakademie/offline_embeddings.py`): `OfflineKeywordEmbeddings` (kostenlos, transparent, erkennt Schlüsselwörter) und mit Key echte Mistral-Embeddings, die auch Sinn-Verwandtschaft verstehen.

## Voraussetzungen
- Aufgabe 4.1

## Deine Mission
Schreibe `chunker.py`:
1. Lade beide Handbücher aus `data/` und splitte **jedes** mit `RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)`.
2. Gib pro Dokument aus: Anzahl Chunks, Länge des ersten und letzten Chunks.
3. Erzeuge Embeddings für **drei** Testtexte: „Wie viele Urlaubstage habe ich?", „Resturlaub verfällt wann?", „Wie setze ich ein Passwort?" – mit `get_embeddings()` (offline oder echt, je nach Key).
4. Miss alle **Paar-Ähnlichkeiten** (Cosine) und gib sie als kleine Tabelle aus. Interpretiere: Welches Paar ist sich am ähnlichsten? Warum?
5. Bonus: Verwandle `OfflineKeywordEmbeddings`-Vektoren in eine lesbare Form – für welche Schlüsselwörter ist der Vektor „an"? (Das siehst du bei echten Modellen **nie** so transparent!)

## Akzeptanzkriterien
- [ ] Beide Dokumente sind gesplittet (je nach Größe ~5–15 Chunks).
- [ ] Chunk-Overlap ist gesetzt – und du kannst erklären, warum.
- [ ] Die Ähnlichkeitstabelle zeigt plausibel: themengleiche Fragen > themenfremde.
- [ ] Du kannst in 2 Sätzen erklären, was ein Embedding ist.

## Hinweise
1. Splitter: `splitter.split_text(text)` (reine Strings) oder `splitter.split_documents(docs)` (Documents mit Metadaten – besser, brauchen wir in 4.3!).
2. Cosine selbst rechnen: `sum(a*b for a,b in zip(u,v)) / (norm(u)*norm(v))` – oder einfacher: bei unseren normalisierten Vektoren genügt das Punktprodukt.
3. Offline-Erinnerung: Ohne Key erkennst du in der Tabelle logische Nähe nur bei **Schlüsselwort-Überschneidung** („Urlaub"-Fragen sind sich ähnlich, weil beide „urlaub" enthalten). Genau dieser Vorbehalt steht auch im Level-README.

## Reflexionsfragen
1. Warum würde `chunk_size=50` die Suche ruinieren? Warum `chunk_size=50000` auch?
2. Warum funktioniert Ähnlichkeitssuche mit Embeddings besser als klassische Wort-Suche („Urlaub" vs. „freie Tage")?
3. Unsere Offline-Embeddings: Wo genau liegt ihre Schwäche im Vergleich zu `mistral-embed` – und warum ist das für den **Lernfortschritt** trotzdem okay?

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| `chunk_overlap >= chunk_size` Fehler | Overlap immer **kleiner** als Size |
| Embedding-Vektoren unterschiedlich lang | nie zwei Modelle mischen; ein Modell pro Index |
| 0.0-Ähnlichkeit überall (offline) | Fragen enthalten keine Schlüsselwörter aus KEYWORDS – Begriffe aus den Dokumenten nutzen |

## Referenzlösung
→ [`solutions/chunker.py`](../solutions/chunker.py)

## Code-Walkthrough
In der Lösungsdatei; besonders die kleine `cosine_aehnlichkeit()`-Funktion.

## Was haben wir gelernt?
Chunking-Strategien, Embeddings als Bedeutungs-Koordinaten, Cosine-Similarity, Offline-vs-echte-Embeddings.

## Was kommt als Nächstes?
Du hast Chunks und Vektoren – jetzt braucht du einen **Aufbewahrungsort mit Suchfunktion**: eine Vektor-Datenbank. Aufgabe 4.3: Chroma speichert, indexiert und findet die sinngleichen Chunks.
