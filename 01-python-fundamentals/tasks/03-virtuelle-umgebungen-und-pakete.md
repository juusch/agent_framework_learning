# Aufgabe 1.3 – Virtuelle Umgebungen & Pakete 📦

## Schwierigkeit
Anfänger

## Lernziel
Du kannst eine virtuelle Umgebung anlegen, aktivieren, Pakete installieren und verstehst, **warum** man das tut.

## Warum ist das wichtig?
Ohne `langchain` & Co. gibt es keine KI-Anwendung – und die installierst du **pro Projekt** in einer virtuellen Umgebung. Jede Anleitung dieser Akademie (ab Stufe 2) setzt voraus, dass du das beherrschst.

## Das Konzept einfach erklärt
Eine **virtuelle Umgebung** (venv) ist ein privater Werkzeugkasten für genau ein Projekt. **Metapher:** Ohne venv liegen alle Werkzeuge aller Projekte in einem gemeinsamen Bauwagen – irgendwann blockieren sich verschiedene Versionen. Mit venv hat jede Baustelle ihren eigenen Wagen.

Ein **Paket** ist von anderen geschriebener, installierbarer Code (z. B. `rich`). `pip` ist das Werkzeug, das Pakete aus dem Internet (PyPI) in deinen Werkzeugkasten legt.

## Die technische Erklärung
- `python -m venv .venv` legt einen Ordner `.venv` mit einer eigenen Python-Kopie + eigenem Paketordner an.
- Aktivieren lenkt den Befehl `python`/`pip` auf diese Kopie um:
  - Windows: `.venv\Scripts\activate`
  - macOS/Linux: `source .venv/bin/activate`
- `pip install -r requirements.txt` installiert genau die im Projekt gepinnten Pakete.
- `pip list` zeigt, was gerade installiert ist. `deactivate` verlässt die Umgebung.

## Voraussetzungen
- Terminal-Grundlagen (Stufe 0)

## Deine Mission
1. Lege im Projektordner eine virtuelle Umgebung an und aktiviere sie.
2. Installiere die Abhängigkeiten dieser Akademie: `pip install -r requirements.txt`
3. Prüfe mit `pip list`, dass z. B. `langchain` erscheint.
4. Führe die Demo-Datei aus: `python 01-python-fundamentals/examples/venv_demonstration.py`
5. Dokumentiere für dich: Was siehst du im Terminal-Prompt, wenn die Umgebung aktiv ist?

⚠️ **Kosten:** keine – alles lokal, keine API-Aufrufe.

## Akzeptanzkriterien
- [ ] Der Terminal-Prompt zeigt `(.venv)` (oder `.venv` in Klammern).
- [ ] `pip list` zeigt `langchain`, `langgraph`, `rich` u. a.
- [ ] Die Demo-Datei läuft ohne `ModuleNotFoundError`.
- [ ] Du kannst in einem Satz sagen, warum man nicht „global" installiert.

## Hinweise
1. Falscher Ordner? Die Datei `requirements.txt` liegt im Projekt-Hauptordner – `cd` dorthin.
2. Terminal neu geöffnet → Umgebung ist wieder **aus**; erneut aktivieren.
3. VS Code fragt evtl., welchen Interpreter es nutzen soll: unten rechts die Version aus `.venv` wählen (wichtig, sonst rote Wellenlinien trotz Installation).

## Reflexionsfragen
1. Zwei Projekte brauchen zwei verschiedene Versionen desselben Pakets. Wie löst die venv das?
2. Was würde passieren, wenn du `pip install langchain` machst, **ohne** die Umgebung zu aktivieren?
3. Warum liegt der Ordner `.venv` in `.gitignore` und wird nicht mit anderen geteilt?

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| `pip install` läuft, aber Skript findet Paket nicht | venv nicht aktiviert oder falscher Interpreter in VS Code |
| PowerShell blockiert Skripte | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `requirements.txt` nicht gefunden | ins Projekt-Hauptverzeichnis `cd`n |

## Referenzlösung
→ [`solutions/venv_checkliste.md`](../solutions/venv_checkliste.md) (Schritt-für-Schritt-Checkliste) und [`examples/venv_demonstration.py`](../examples/venv_demonstration.py)

## Was haben wir gelernt?
venv anlegen/aktivieren, Pakete installieren, warum Projektisolation wichtig ist.

## Was kommt als Nächstes?
Installierte Pakete allein reichen nicht: Deine zukünftigen Skripte brauchen den **Mistral-API-Key** – und der gehört niemals in den Code. Aufgabe 1.4 zeigt den professionellen Weg über `.env`.
