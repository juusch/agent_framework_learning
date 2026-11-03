# 🎓 Einstieg – aber der echte Einstieg ist das Notebook!

**Diese Seite ist nur die Tür. Das Lernen passiert in Jupyter:**

## ▶️ [START_HERE.ipynb öffnen](START_HERE.ipynb)

Dort findest du in ~15 Minuten:
1. Was du in dieser Akademie baust (denselben Assistenten **dreimal**)
2. Wie Notebook-Zellen funktionieren (Shift + Enter!)
3. Deinen Setup-Check (Umgebung + KI-Konfiguration)
4. Deine erste Mini-Aufgabe mit automatischer Prüfung
5. Den kompletten Lernpfad (21 Notebooks)

## Kein Jupyter installiert?

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m ipykernel install --user --name=lernakademie
jupyter lab
```

Dann `START_HERE.ipynb` öffnen. Details: [docs/notebook-guide.md](docs/notebook-guide.md)
