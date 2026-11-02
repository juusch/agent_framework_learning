# Stufe 9 – Produktion & darüber hinaus 🚀

**Ziel:** Vom „läuft bei mir" zum „läuft zuverlässig": Testing & Evaluierung, Sicherheit & Kosten, Observability, Docker – und deine Abschluss-Challenge.

## Warum diese Stufe anders ist

Bis Stufe 8 warst du **Bauer**. Jetzt wirst du **Betreiber**: Niemand nutzt eine KI-Anwendung, die bei der ersten seltsamen Eingabe crasht, deren Kosten unbekannt sind und deren Fehler niemand nachvollziehen kann.

## Aufgaben

| # | Aufgabe | Schwierigkeit |
|---|---|---|
| 9.1 | [`tasks/01-testing-und-evaluierung.md`](tasks/01-testing-und-evaluierung.md) – Tests & Antwort-Evaluierung | Mittel |
| 9.2 | [`tasks/02-sicherheit-kosten-observability.md`](tasks/02-sicherheit-kosten-observability.md) – Keys, Budget, Logging, LangSmith | Mittel |
| 9.3 | [`tasks/03-docker-und-abschluss.md`](tasks/03-docker-und-abschluss.md) – Docker + Abschluss-Challenge | Fortgeschritten |

## Ausführen

```bash
pytest                                   # alle Akademie-Tests (offline!)
python3 09-production/solutions/evaluation.py       # Antwort-Evaluierung
python3 09-production/solutions/logging_demo.py      # Logging & Tracing
docker build -t lernakademie .           # Docker (Aufgabe 9.3)
```

## Die Grundprinzipien auf einen Blick

1. **Deterministisches zuerst:** Alles, was keine KI braucht, deterministisch bauen (billiger, testbar, verlässlich).
2. **Offline-Testbar:** Diese Akademie ist das Beispiel – 15+ Tests ohne Key, ohne Kosten, in CI.
3. **Geheimnisse nie im Code:** `.env` + `.gitignore` + Umgebungsvariablen im Deployment.
4. **Budget & Bremsen:** Loop-Limits, max_tokens, k klein halten, ein Modell für einfache Aufgaben.
5. **Nachvollziehbarkeit:** strukturierte Logs pro Aufruf; mit LangSmith komplette Traces.
6. **Mensch am Hebel:** Sensible Aktionen nur mit Freigabe (Stufe 6.4, 8D).

## Danach

Herzlichen Glückwunsch – mit der Abschluss-Challenge hast du die Akademie durchlaufen. [docs/learning-roadmap.md](../docs/learning-roadmap.md) nennt Ausblick-Thema für Ausblick (LangSmith-Vertiefung, Async/Parallelität, Cloud-Deployment, Evals-at-Scale).
