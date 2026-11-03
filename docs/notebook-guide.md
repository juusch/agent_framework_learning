# 📓 Notebook-Guide – die Akademie in Jupyter

> **Das Wichtigste:** Öffne `START_HERE.ipynb` – dort beginnt alles. Die Notebooks sind dein **geführtes Programmier-Labor**: lesen → verstehen → ausführen → experimentieren → selbst coden → prüfen → weiter.

## Setup (einmalig)

```bash
git clone https://github.com/juusch/agent_framework_learning
cd agent_framework_learning
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m ipykernel install --user --name=lernakademie
jupyter lab                        # oder: jupyter notebook
```

**Kernel auswählen:** Im Jupyter oben rechts auf „Python 3“ klicken → Kernel `lernakademie` wählen (das ist dein `.venv`). 

> Ohne Kernel-Registrierung funktioniert auch der Standard-Python-3-Kernel – **wenn** Jupyter aus der aktivierten venv gestartet wurde (`source .venv/bin/activate && jupyter lab`).

## Wie du mit einem Notebook arbeitest

| Situation | Was tun |
|---|---|
| Zelle ausführen | In die Zelle klicken → **Shift + Enter** |
| Irgendwas ist seltsam | **Kernel → Restart Kernel**, dann **Run → Run All Cells** |
| Komplett neu anfangen | Kernel neu starten + Notebook neu öffnen (nichts kann kaputtgehen) |
| „Wo soll ich schreiben?“ | Code-Zellen mit `# YOUR CODE HERE` |
| „Stimmt mein Ergebnis?“ | Die 🧪-Prüfzelle unter der Aufgabe ausführen (`assert` = automatische Prüfung) |
| Du hängst fest | `<details>`-Hinweise öffnen (erst nach eigenem Versuch!) |
| Vergleichen | `solutions/XX..._loesung.ipynb` – **nach** deinem Versuch |

## Der Aufbau jeder Lektion

```
Willkommen (Zeit, Schwierigkeit, Voraussetzungen, was du baust)
Lernziele (beobachtbar)
Setup (zentrale KI-Konfiguration – eine Zelle)
🧠 Konzept (WARUM → WAS → HOW mit Metaphern)
🔎 Beispiele (kleine Zellen, jede Ausgabe erklärt)
✏️ Deine Aufgabe (Workspace + Akzeptanzkriterien + 🧪 Prüfe)
💡 Hinweise (aufklappbar, gestaffelt)
📝 Reflexion (bei wichtigen Aufgaben)
➡️ Weiter (nächste Lektion)
```

## Die drei Ebenen des Codes

1. **Transparent (Lektion 1–15):** Du siehst jede Mechanik in der Zelle – nichts ist versteckt.
2. **Wiederverwendbar:** Wiederkehrendes wandert in Funktionen (in den Zellen selbst).
3. **Produktions-Abstraktion (`lernakademie/`):** Build-1- und Build-2-Pipelines existieren zusätzlich als Module (`lernakademie/build1.py`, `build2.py`) – **erst** nachdem du sie von Hand gebaut hast. So verstehst du, was eine Abstraktion für dich tut.

## Reproduzierbarkeit

- Jedes Notebook läuft **von oben nach unten mit frischem Kernel** („fresh kernel“) – keine versteckten Abhängigkeiten an frühere Notebooks.
- Die Lösungs-Notebooks in `solutions/` wurden automatisch **komplett ausgeführt** (offline) – ihre Outputs zeigen dir die erwarteten Ergebnisse.
- CI prüft (`tests/test_notebooks.py`): alle Notebooks parsen, jede Code-Zelle kompiliert, jede Lektion hat Lernziele/Aufgabe/Kriterien/Prüfe, der Lernpfad ist lückenlos.

## Neu bauen (für Maintainer)

```bash
python scripts/build_notebooks.py           # schreibt UND führt alle Loesungen aus (offline)
python scripts/build_notebooks.py --schnell # nur schreiben (CI-Modus)
```
