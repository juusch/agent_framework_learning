# Aufgabe 8.2 – Sicherheit, Kosten, Logging & der Abschluss 🔐💨📡

**Schwierigkeit:** Mittel · **Zeit:** ~60–90 Min · **Kosten:** keine

## Lernziel
Du kennst die Betreiber-Säulen – Key-Management, Budget-Bremsen, Logging/Tracing, Docker – und hast sie konkret an der finalen Anwendung nachvollzogen.

## Warum das wichtig ist
Die drei klassischen KI-Inzidenz-Klassen: **geleakte Keys**, **explodierende Kosten** (Loops!), **Fehlersuche ohne Spur**. Die Akademie hat für alle drei Muster gebaut – jetzt verstehst du sie als System.

## Deine Mission
1. **Logging & Tracing:** `solutions/logging_demo.py` studieren und ausführen: `@verfolge`-Decorator (Start/Ende/Dauer = Trace), Key-Maskierung (Test Included!), Kostenschätzer. Erweitere eine eigene Funktion um den Decorator.
2. **Kosten-Rechnung:** rechne mit `schaetze_kosten()` drei Szenarien (1 Frage, 100 Fragen, „Loop ohne Limit" = 100 Runden) – notiere deine Erkenntnis in einem Kommentar.
3. **Sicherheits-Audit der finalen App (lokal):** prüfe 5 Punkte – (a) Key nur in `.env`/Backend, (b) Pydantic an Endpunkten, (c) lesende Whitelist für Graph-Zugriff, (d) Freigabe-Pflicht für Schreibzugriffe, (e) Fehler → klare Meldungen, keine Tracebacks nach außen. Dokumentiere je 1 Satz Fund.
4. **Docker-Verständnis:** lies `final-project/.../backend/Dockerfile` und `docker-compose.yml`: Warum Abhängigkeiten zuerst (Cache)? Warum `.env` nie ins Image? Wie kommen Geheimnisse zur Laufzeit rein?
5. **🎓 Abschluss-Reflexion (Pflicht):** Beantworte schriftlich die finale Frage aus dem Vergleichs-Doc: *„Wann würdest du heute welche der drei Architekturen bauen?"* – mit je einem konkreten Projektbeispiel aus deinem Leben.

## Akzeptanzkriterien
- [ ] Trace-Ausgabe zeigt Reihenfolge + Dauer; Maskierung ist getestet.
- [ ] Dein Kostenkommentar nennt den Loop-Multiplikator.
- [ ] Das 5-Punkte-Audit ist mit je einem Fund dokumentiert.
- [ ] Deine Abschluss-Reflexion begründet alle drei Architekturen mit Beispielen.

## Hinweise
1. `schaetze_kosten(zeichen_in, zeichen_out)` nutzt die Faustregel `zeichen // 4` (Modul 1!).
2. LangSmith-Anbindung: nur Umgebungsvariablen (`LANGSMITH_TRACING=true` …) – ein Betreiber-Feature ohne Codeänderung; Grundlage verstanden in der Logging-Aufgabe.
3. Für die Abschluss-Reflexion: [`docs/same-problem-three-architectures.md`](../../docs/same-problem-three-architectures.md) noch einmal lesen.

## Reflexionsfragen
1. Warum ist „Logge alles" ebenso falsch wie „Logge nichts"? (PII, Kosten, Signal-Rauschen)
2. Dein Agent hat 500 € verbrannt – welche **drei** Bremsen aus der Akademie hätten das verhindert?
3. Was bleibt unsichtbar, wenn Logging nur Fehler protokolliert – und warum braucht man Success-Traces („ging, aber warum langsam")?

## Referenzlösung + Walkthrough
→ [`solutions/logging_demo.py`](../solutions/logging_demo.py), [`solutions/Dockerfile`](../solutions/Dockerfile), [`final-project/knowledge-research-agent/docker-compose.yml`](../../final-project/knowledge-research-agent/docker-compose.yml)

## Weiter
🎓 **Abschluss.** Du hast den Weg von „Was ist ein Terminal?" bis „Ich habe ein getestetes Multi-Quellen-Wissenssystem gebaut und kann jede Architekturentscheidung begründen" zurückgelegt. Jetzt: eigenes Projekt. Die Werkzeuge hast du.
