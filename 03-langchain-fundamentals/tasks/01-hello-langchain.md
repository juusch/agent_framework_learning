# Aufgabe 3.1 – Hello LangChain 🎈

## Schwierigkeit
Anfänger · ⚠️ **Kosten:** nur mit Key; ohne Key Offline-Modus (Ablauf identisch)

## Lernziel
Du startest dein erstes LangChain-Chat-Modell, sendest Nachrichten im LangChain-Format (Message-Objekte statt Dictionaries) und liest die Antwort korrekt aus.

## Warum ist das wichtig?
Ab jetzt arbeiten wir nicht mehr mit rohen API-Dictionaries, sondern mit LangChains Bausteinen. Der erste Baustin ist das **Chat-Modell-Objekt** – jede Chain, jeder Agent, jedes RAG-System baut darauf auf.

## Das Konzept einfach erklärt
Du kennst den Restaurant-Kellner (direkter API-Call). LangChain ist ein **_professionelles Bestellsystem_**: derselbe Kellner, aber du bestellst über ein Formular, das überall im Haus gleich aussieht. Der Vorteil kommt gleich (3.2), wenn wir Bestellungen **vorlagenisieren** und **anhängen**.

## Die technische Erklärung
- Chat-Modell erzeugen: `ChatMistralAI(model="mistral-small-latest", temperature=0.2)` (aus `langchain_mistralai`).
- Nachrichten sind jetzt **Objekte** aus `langchain_core.messages`: `SystemMessage`, `HumanMessage`, `AIMessage` – statt `{"role": ...}`-Dictionaries.
- `model.invoke([nachrichten])` liefert eine `AIMessage` zurück; der Text steckt in `.content`.
- Die Akademie-Lösungen nutzen `lernakademie.get_chat_model()`: das liefert je nach `.env` automatisch `ChatMistralAI` oder das Offline-Modell – **dein Lerncode bleibt identisch**.

## Voraussetzungen
- Stufe 2 (Rollen, Temperatur, API-Ablauf)

## Deine Mission
Schreibe `hello_langchain.py`:
1. Hole das Chat-Modell (per `get_chat_model()` aus der Akademie-Bibliothek oder direkt `ChatMistralAI` mit Key aus `.env`).
2. Baue die Nachrichten: `SystemMessage` (Persona: „Du bist ein Python-Tutor für absolute Anfänger.") + `HumanMessage` („Erkläre in einem Satz, was eine Variable ist.").
3. Rufe das Modell mit `.invoke()` auf und gib **nur den Text** (`.content`) aus.
4. Experimentiere: füge der Nachrichtenliste eine dritte Nachricht hinzu (`AIMessage` mit einer fingierten Assistenten-Antwort) und stelle dann als vierte Nachricht eine Rückfrage. Beobachte, wie die Historie mitwandert.

## Akzeptanzkriterien
- [ ] Das Skript läuft ohne Key (Offline-Antwort mit `[OFFLINE]`) und mit Key (echte Antwort).
- [ ] Die Ausgabe zeigt **nur den Antworttext**, nicht das ganze Antwortobjekt.
- [ ] Du kannst benennen, welches Objekt welche Rolle spielt.

## Hinweise
1. Importe: `from langchain_core.messages import SystemMessage, HumanMessage, AIMessage`
2. Invoke: `antwort = model.invoke([system, human])` → `antwort.content`
3. Der Objektansatz fühlt sich erst umständlicher an als Stufe 2 – versprochen, er zahlt sich ab 3.2 aus (Vorlagen + Verkettung).

## Reflexionsfragen
1. Was gewinnst du durch `SystemMessage(...)`-Objekte gegenüber Dictionaries? (Tipp: Typprüfung, einheitliches Interface, keine Tippfehler bei `"role"`)
2. Warum darf das Modell-Objekt in einer Variablen stecken bleiben, während du Nachrichten austauschst?
3. Wo erkennt du `temperature` im Vergleich zu Stufe 2 wieder?

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| `AIMessage`-Inhalt fehlt (leerer Text) | `.content` vergessen |
| `AttributeError: 'str' object has no attribute ...` | Messages als Strings übergeben – Objekte nutzen |
| KeyError/401 | Key in `.env` bzw. Offline-Modus prüfen |

## Referenzlösung
→ [`solutions/hello_langchain.py`](../solutions/hello_langchain.py)

## Code-Walkthrough
In der Lösungsdatei, Zeile für Zeile kommentiert.

## Was haben wir gelernt?
Chat-Modelle als Objekte, Message-Typen, `.invoke()`, der Austauschbarkeitstrick `get_chat_model()`.

## Was kommt als Nächstes?
Jetzt wird aus dem einzelnen Call ein **Fließband**: Prompt-Template + Modell + Parser, verbunden mit dem Pipe-Operator `|` – die berühmte **Chain**. Das ist der Kern von LangChain.
