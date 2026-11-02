# 🚀 START HERE – Dein Weg in 10 Minuten

Diese Anleitung führt dich von „Ich habe noch nie programmiert" bis zu deinem ersten laufenden Python-Programm. Arbeite sie **langsam und vollständig** durch – jedes Detail zählt.

---

## Schritt 1: Was ist hier überhaupt los? (5 Minuten Lektüre)

- **Programmieren** bedeutet, einem Computer in einer Sprache, die er versteht, Schritt-für-Schritt-Anweisungen zu geben.
- **Python** ist eine solche Sprache – besonders einsteigerfreundlich, weil sie fast wie Englisch liest.
- **Ein Terminal** (auch „Konsole" oder „Eingabeaufforderung" genannt) ist ein Fenster, in dem du dem Computer Befehle eintippst. Metapher: eine *Chat-Oberfläche für Profis* – statt mit einem Menschen chattest du mit deinem Computer.
- **Ein LLM** (Large Language Model, z. B. Mistral) ist eine Art „sehr belesener, aber manchmal unzuverlässiger Assistent": Es hat aus riesigen Textmengen gelernt, sinnvolle Antworten zu formulieren. Es *weiß* nichts – es *sagt* nur wahrscheinliche, meist passende Sätze.

Mehr Begriffe findest du im [Glossar](docs/glossary.md). Du musst sie **nicht** alle jetzt verstehen.

## Schritt 2: Python installieren

Lade Python **3.11 oder neuer** herunter: <https://www.python.org/downloads/>

- **Windows:** Wähle im Installer unbedingt **„Add python.exe to PATH"** aus, dann klicke auf *Install Now*. Prüfe danach im Terminal (Windows-Taste → „cmd" → Enter):
  ```bat
  python --version
  ```
- **macOS:** Nach der Installation öffne das *Terminal* (Cmd+Leertaste → „terminal"):
  ```bash
  python3 --version
  ```
- **Linux:** Python ist meist vorinstalliert:
  ```bash
  python3 --version
  ```

Wenn eine Versionsnummer erscheint (z. B. `Python 3.12.x`), hast du geschafft. ✅

> **Hakst du fest?** Der Abschnitt „Installation" in [docs/troubleshooting.md](docs/troubleshooting.md) löst die häufigsten Probleme.

## Schritt 3: VS Code installieren (dein „Schreibzimmer")

Ein **Editor** ist das Programm, in dem du Code schreibst – so wie Word für Texte da ist, ist VS Code für Code da.

1. Lade VS Code herunter: <https://code.visualstudio.com/>
2. Installiere die Erweiterung **„Python"** (von Microsoft): links auf das Puzzle-Symbol (Erweiterungen) → „Python" suchen → *Install*.

## Schritt 4: Das Terminal kennenlernen

Das Terminal ist dein wichtigstes Werkzeug. Öffne es (in VS Code: Menü *Terminal → New Terminal*) und probiere:

| Befehl | Bedeutung (Metapher) |
|---|---|
| `pwd` | „Wo stehe ich gerade?" (zeigt den aktuellen Ordner) – Windows: `cd` |
| `ls` | „Was liegt hier?" (listet Dateien auf) – Windows: `dir` |
| `cd ordnername` | „Gehe in diesen Ordner hinein" |
| `cd ..` | „Gehe einen Ordner zurück" |

## Schritt 5: Ein eigenes kleines Projekt anlegen

1. Erstelle dir einen Ordner, z. B. `meine-lernreise`, und öffne ihn in VS Code (*File → Open Folder*).
2. Öffne das Terminal in VS Code und lege eine Datei an:
   ```bash
   touch meins_erstes_programm.py
   ```
   (Windows-PowerShell: `ni meins_erstes_programm.py`)
3. Schreibe in die Datei:
   ```python
   print("Hallo Welt! Ich habe gerade mein erstes Programm geschrieben.")
   ```
4. Starte es im Terminal:
   ```bash
   python meins_erstes_programm.py
   ```
   (macOS/Linux: `python3 meins_erstes_programm.py`)

Herzlichen Glückwunsch – das war dein **Hello World**! 🎉

## Schritt 6: Weiter geht's

Öffne jetzt [`00-setup/README.md`](00-setup/README.md) und arbeite die erste richtige Aufgabe durch.

**Wichtig:** Die Akademie funktioniert wie ein Videospiel mit Levels. Überspringe nichts – jede Stufe baut auf der vorherigen auf.
