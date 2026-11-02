# Modul 8 – Testing & Produktion 🚀

**Ziel:** Vom „läuft bei mir" zum „läuft zuverlässig": automatisierte Tests, Evaluierung, Sicherheit, Kostenbewusstsein, Logging – und der Abschluss deiner Akademie.

| # | Aufgabe | Zeit |
|---|---|---|
| 8.1 | [`tasks/01-testing-und-evaluierung.md`](tasks/01-testing-und-evaluierung.md) – Tests & Antwort-Evaluierung | ~60 Min |
| 8.2 | [`tasks/02-sicherheit-kosten-betrieb.md`](tasks/02-sicherheit-kosten-betrieb.md) – Keys, Budget, Logging, Docker, Abschluss | ~60–90 Min |

**Ausführen:**
```bash
pytest                                        # alle Akademie-Tests (offline!)
pytest final-project/knowledge-research-agent/tests   # Capstone-API-Tests
python3 08-testing-und-produktion/solutions/evaluation.py
python3 08-testing-und-produktion/solutions/logging_demo.py
```

**Die Grundprinzipien:** Deterministisches zuerst bauen · offline testbar (diese Akademie ist das Beispiel: 40+ Tests ohne Key in CI) · Geheimnisse nie im Code · Budget & Bremsen (Loop-Limits!) · Nachvollziehbarkeit (Logging/Traces) · Mensch am Hebel (Freigaben).

**Danach:** 🎓 Du hast es geschafft – von „Hello World" bis zu einem getesteten, dockerisierten Knowledge-Agenten mit Frontend. Halte deinen Fortschritt in [`PROGRESS.md`](../PROGRESS.md) fest und baue dein eigenes Projekt.
