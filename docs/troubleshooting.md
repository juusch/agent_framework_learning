# 🔧 Troubleshooting – die häufigsten Probleme und ihre Lösungen

## Installation & Setup

**`python` wird nicht erkannt (Windows)**
- Python beim Installieren nicht „to PATH" hinzugefügt → Installer erneut starten, Haken setzen. Oder `py` statt `python` verwenden.
- Terminal nach der Installation neu öffnen.

**`pip install` schlägt fehl**
- Prüfe, ob die virtuelle Umgebung aktiv ist (Name in Klammern: `(.venv)`).
- Aktualisiere pip: `python -m pip install --upgrade pip`.

**`ModuleNotFoundError: No module named 'xyz'`**
- Das Paket ist nicht installiert oder die venv ist nicht aktiv. Lösung: `pip install -r requirements.txt` bzw. `pip install xyz`.
- Wichtig: VS Code nutzt manchmal das „falsche" Python. Unten rechts in VS Code die richtige Interpreter-Version (deine `.venv`) auswählen.

**Virtuelle Umgebung aktivieren**
- Windows (cmd): `.venv\Scripts\activate`
- Windows (PowerShell): falls Skripte blockiert werden: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
- macOS/Linux: `source .venv/bin/activate`

## API & Mistral

**`MISTRAL_API_KEY ist nicht gesetzt` oder Fehler 401 (unauthorized)**
- `.env`-Datei existiert? (Kopiere `.env.example` → `.env`.) Steht der Key dort ohne Anführungszeichen?
- Läuft das Skript aus dem Projekt-Ordner heraus? (`.env` wird relativ zum Ausführungsordner gesucht.)
- **Kein Key? Kein Problem:** Alle Lösungen laufen ohne Key automatisch im Offline-Modus.

**Fehler 429 (rate limit)**
- Zu viele Anfragen zu schnell. Warte kurz und reduziere die Anzahl der Aufrufe (z. B. Schleifen mit weniger Durchläufen).

**Antworten beginnen mit `[OFFLINE]`**
- Das ist der Offline-Modus. Entweder fehlt der Key in `.env`, oder `ACADEMY_OFFLINE=1` ist gesetzt. Kein Fehler – nur keine echten LLM-Aufrufe.

## Lokale AI-Server / OpenAI-kompatible Endpoints

**`Connection refused` beim Verbindungstest**
- Läuft dein Server? (LM Studio/Ollama starten.)
- Stimmt der Port in `LLM_BASE_URL`? Prüfe die Doku deines Servers.

**`404 ... /chat/completions`**
- Die URL passt nicht: meist fehlt das `/v1` am Ende (oder ist zu viel).
- Beispiel korrekt: `http://localhost:1234/v1`.

**`401`/`403`**
- Dein Server erwartet doch einen Key → `LLM_API_KEY` in `.env` setzen.
- Umgekehrt: ein alter Key stört? → `LLM_API_KEY=` leer lassen.

**`model not found`**
- `LLM_MODEL` muss exakt dem Namen entsprechen, den der Server meldet.

**Konfigurations-Fehler (`ValueError` aus `lernakademie/config.py`)**
- Die Meldung nennt die fehlende Variable (`LLM_BASE_URL` oder `LLM_MODEL`) – einfach in `.env` ergänzen.
- Ungültiger `LLM_PROVIDER`? Erlaubt: `mistral`, `openai_compatible`, `offline` (oder leer).

**Strukturierte Ausgaben schlagen fehl / Agent ruft Tools nicht auf**
- Nicht jedes (lokale) Modell beherrscht Tool-Calling bzw. JSON. Prüfe die Fähigkeiten-Tabelle in [local-ai-server.md](local-ai-server.md) – und übe im Zweifel im Offline-Modus (Simulation liefert immer gültige Strukturen).

**Verbindung schnell prüfen:** `python -m tools.test_llm_connection`

## Python-Grundlagen

**`SyntaxError`**
- Häufigste Ursachen: fehlender Doppelpunkt nach `if`/`for`/`def`, nicht geschlossene Anführungszeichen oder Klammern, deutsche Anführungszeichen („") statt `"`.
- Einrücken mit 4 Leerzeichen pro Ebene – niemals Tabs und Leerzeichen mischen.

**`IndentationError: expected an indented block`**
- Nach `if`, `for`, `def` usw. muss die nächste Zeile eingerückt sein (4 Leerzeichen).

**`TypeError: can only concatenate str (not "int") to str`**
- Text und Zahl mischen: nutze f-Strings, z. B. `f"Alter: {alter}"`.

**`input()` liefert immer Text**
- Auch Zahlen! Umwandeln mit `int(...)` bzw. `float(...)`.

## RAG & Vektor-Datenbank

**Die semantische Suche findet nichts Sinnvolles (Offline-Modus)**
- Die Offline-Embeddings erkennen nur die im Kapitel erklärten Schlüsselwörter. Formuliere deine Suchfrage mit Begriffen aus den Dokumenten (z. B. „Urlaub", „Passwort", „VPN"). Mit echten Mistral-Embeddings funktioniert auch umgangssprachliches Suchen.

**`chromadb`-Fehler beim ersten Start**
- Es wird beim ersten Aufruf ein lokaler Ordner angelegt – schreibrechte prüfen. Andere Versionen können helfen: `pip install -U langchain-chroma`.
