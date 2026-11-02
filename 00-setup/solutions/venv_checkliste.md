# Referenzlösung 1.3 – venv-Checkliste

Diese Aufgabe hat keine Python-Datei – sie ist eine Handgriff-Sequenz. Arbeite sie im Projektordner ab:

## 1. Umgebung anlegen (einmalig pro Projekt)

```bash
python -m venv .venv        # Windows (oder: py -m venv .venv)
python3 -m venv .venv       # macOS/Linux
```

→ Es entsteht ein Ordner `.venv` mit einer eigenen Python-Installation.

## 2. Aktivieren (in **jedem** neuen Terminal!)

```bash
.venv\Scripts\activate            # Windows (cmd)
source .venv/bin/activate         # macOS/Linux
```

→ Jetzt zeigt dein Prompt `(.venv)`.

## 3. Pakete installieren

```bash
pip install -r requirements.txt
```

## 4. Prüfen

```bash
pip list | findstr langchain      # Windows
pip list | grep langchain         # macOS/Linux
python 01-python-fundamentals/examples/venv_demonstration.py
```

→ Wenn das Skript die Paketversionen ausgibt, ist alles korrekt verkabelt.

## 5. Verlassen (optional)

```bash
deactivate
```

## Warum funktioniert das?

`activate` trägt den Pfad von `.venv` an den **Anfang** der Suchreihenfolge deines Terminals. Wenn du danach `python` oder `pip` tippst, wird zuerst die Kopie **im Projekt** gefunden – alle Installationen landen also im Projektwerkzeugkasten, nicht global.
