# Aufgabe 4.1 – Dokument laden & zusammenfassen 📄

## Schwierigkeit
Anfänger · ⚠️ **Kosten:** nur mit Key (Offline: Ablauf identisch)

## Lernziel
Du lädst ein Dokument in deine Anwendung, machst den Text für den Computer nutzbar und lässt ihn zusammenfassen – der erste Schritt jeden RAG-Systems.

## Warum ist das wichtig?
Bislang hast du jeden Prompt abgetippt. Jetzt lernt dein Programm, **selbst** zu lesen: Dateien als Wissensquelle. Ohne dieses Fundament kein RAG.

## Das Konzept einfach erklärt
**Metapher:** Ein Dokument ist ein ganzes Buch; dein Programm braucht den reinen Text daraus (ohne Buchdeckel, ohne Formatierung). Ein **Document Loader** ist der Buchscanner: Er macht aus einer Datei ein `Document`-Objekt mit `.page_content` (der Text) und `.metadata` (Infos wie Dateiname – wichtig für Quellenangaben!).

## Die technische Erklärung
- `pathlib.Path` liest rohe Textdateien; LangChain-Loader (z. B. `TextLoader` aus `langchain_community.document_loaders`) kapseln das und liefern standardisierte `Document`-Objekte.
- Wir verwenden hier bewusst die schlanke Variante: `TextLoader` bzw. `Path.read_text` – du siehst, dass „Laden" keine Magie ist, sondern Dateilesen mit Metadaten-Drumherum.
- Anschließend nutzt du deine Stufe-3-Kenntnisse: Chain aus Prompt-Template + Modell + Parser – nur dass der `{text}` jetzt aus einer Datei kommt.

## Voraussetzungen
- Stufe 3 (Chains, Templates, Parser)

## Deine Mission
Schreibe `document_loader.py`:
1. Lade `04-rag-and-knowledge/data/mitarbeiter-handbuch.md` und gib aus: Dateiname, Anzahl Zeichen, Anzahl Wörter (Tipp: `len(text.split())`).
2. Lade das Dokument auch mit `TextLoader` und vergleiche: kommt derselbe Text heraus? Was steht in `.metadata`?
3. Baue eine Zusammenfassungs-Chain (Template mit `{text}`) und lasse das **gesamte** Dokument zusammenfassen (mit Key: echte Zusammenfassung; ohne: `[OFFLINE]`-Echo).
4. **Achtung, Fallstrick:** Schätze die Token-Zahl des Dokuments (`len(text) // 4`). Rechne aus, ob es in das Kontextfenster eines kleinen Modells passt – notiere deine Schätzung als Kommentar.

## Akzeptanzkriterien
- [ ] Beide Lade-Varianten liefern denselben Text.
- [ ] Die Metadaten enthalten den Quelldateinamen.
- [ ] Die Zusammenfassungs-Chain läuft auf dem geladenen Text.
- [ ] Dein Code enthält die Token-Schätzung als Kommentar.

## Hinweise
1. `TextLoader(pfad, encoding="utf-8").load()` liefert eine Liste mit **einem** Document.
2. `document.page_content` = Text, `document.metadata` = Dictionary mit `"source"`.
3. Chain wiederverwenden: `prompt | modell | StrOutputParser()` – wie in 3.2.

## Reflexionsfragen
1. Warum sind Metadaten (z. B. Dateiname) für den *Endnutzer* deiner Anwendung wichtig – wann siehst du sie wieder? (Stichwort: Quellenangabe in 4.4)
2. Was passiert, wenn das Dokument **zu groß** fürs Kontextfenster ist – und warum ist genau das die Motivation für Chunking (4.2)?
3. Warum wäre „einfach alles in einen Prompt stopfen" für 100 Dokumente keine Lösung (Kosten? Präzision? Kontextfenster?)

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| `FileNotFoundError` | Pfad relativ zum Projektordner angeben; Skript aus dem Projektordner starten |
| Umlaute werden falsch angezeigt | `encoding="utf-8"` beim Laden |
| TextLoader-Importfehler | `langchain-community` installiert? (in `requirements.txt`; alternativ `Path.read_text` nutzen) |

## Referenzlösung
→ [`solutions/document_loader.py`](../solutions/document_loader.py)

## Code-Walkthrough
In der Lösungsdatei; besonders der direkte Vergleich beider Lade-Varianten.

## Was haben wir gelernt?
Dokumente laden, Document-Objekte, Metadaten, die Grenzen des Kontextfensters.

## Was kommt als Nächstes?
Ein ganzes Dokument passt selten als ganzer Kontext – und die **relevanten** 2 Sätze stecken irgendwo im Wortsalat. Aufgabe 4.2: Wir zerlegen Dokumente in Chunks und übersetzen sie in Embeddings.
