# Aufgabe 9.3 – Docker & die Abschluss-Challenge 🐳🎓

## Schwierigkeit
Fortgeschritten

## Lernziel
Du verstehst, wie eine Python-Anwendung reproduzierbar verpackt wird (Docker-Grundlagen) – und bestehst die Abschluss-Challenge: **ein eigenes End-to-End-Projekt, selbstständig gebaut**.

## Warum ist das wichtig?
„Bei mir läuft es" ist der Klassiker der Softwarekrise. Docker löst das Grundproblem: **gleiche Umgebung überall** – Python-Version, Pakete, Code in einem definierten Abbild (Image), das als Container überall identisch läuft.

## Das Konzept einfach erklärt
**Metapher – der Container im Hafen:** Ein Frachtcontainer ist ein genormter Kasten: Was drin ist, bleibt drin; jeder Hafen (Server) kann ihn heben, ohne zu wissen, was innen passiert. Ein **Image** ist der abgeschlossene Bauplan-Inhalt, ein **Container** eine laufende Instanz davon. Das `Dockerfile` ist die **Packanleitung**.

## Die technische Erklärung
- `FROM python:3.12-slim` – Basis-Image (betriebssystem + Python).
- `WORKDIR /app`, `COPY . .` – Code hineinkopieren (mit `.dockerignore` für `.venv`, `.env`, Caches!).
- `RUN pip install -r requirements.txt` – Abhängigkeiten als eigene Schicht (Cache!).
- `CMD ["python", "skript.py"]` – Startbefehl.
- **Geheimnisse gehören NIEMALS ins Image:** API-Keys übergibt man zur Laufzeit als Umgebungsvariable (`docker run -e MISTRAL_API_KEY=...` oder `--env-file .env`).

## Deine Mission – Abschluss-Challenge

**Teil 1 (Docker):** Nutze das mitgelieferte [`solutions/Dockerfile`](../solutions/Dockerfile): Baue das Image, starte den Wissens-Assistenten als Container, prüfe, dass der Key über `--env-file` hereinkommt und `.env` **nicht** im Image landet (`docker run --rm image cat /app/.env` → Fehler!).

**Teil 2 (die Challenge):** Baue **eigenständig** (kein Kopieren ganzer Lösungen!) eine kleine End-to-End-Anwendung, die enthält:
1. **RAG** über eigene Dokumente (mindestens 2 Dateien),
2. einen **Graphen** mit mind. einer konditionalen Verzweigung,
3. **einen Agenten-Aspekt**: Tool oder Agent-Loop,
4. **eine Sicherheitsbremse**: Loop-Limit ODER Freigabe,
5. **Tests** (mind. 3, offline laufbar),
6. eine **Architektur-Beschreibung** (halbe Seite: Warum welches Muster wo?).

Themenidee: „Assistent für deine Lernnotizen", „Urlaubsplaner mit Regeln + Nachschlagen", eigener Vorschlag.

## Akzeptanzkriterien
- [ ] Der Container läuft mit deinem Skript als Startbefehl.
- [ ] Das Image enthält keine Geheimnisse (nachgewiesen).
- [ ] Deine Challenge-Anwendung erfüllt alle 6 Punkte oben.
- [ ] Du kannst jede Architektur-Entscheidung in einem Satz begründen.

## Hinweise
1. Docker nicht installiert? Die Packanleitung (Dockerfile) zu **verstehen** ist die halbe Miete – die Ausführung kann auch später auf einem Server passieren.
2. Beginne mit dem Graphen (Stufe 5), füge RAG (4) hinzu, dann Tool (6), dann Bremse, dann Tests.
3. Zeit einplanen: Das ist ein Wochenende, kein Abend. Und das ist okay.

## Reflexionsfragen
1. Warum darf `.env` nicht im Image sein, obwohl der Container sie doch „braucht"? (Trennung: Code vs. Konfiguration!)
2. Was würdeste als Erstes tun, wenn dein Container in Produktion 429-Fehler wirft? (Rate-Limit + Backoff + kleineres Modell – was zuerst?)

## Referenzlösung
→ [`solutions/Dockerfile`](../solutions/Dockerfile), [`solutions/.dockerignore`](../solutions/.dockerignore)

## Was haben wir gelernt?
Reproduzierbare Verpackung, Geheimnis-Trennung – und das Selbstvertrauen, ein komplettes Projekt allein zu planen und zu bauen.

## Was kommt als Nächstes?
🎓 **Abschluss.** Du hast den Weg von „Was ist ein Terminal?" bis „Ich habe ein Multi-Agenten-System gebaut und kann begründen, warum" zurückgelegt. Halte deinen Fortschritt in [`PROGRESS.md`](../../PROGRESS.md) fest – und fang dein eigenes Projekt an. Die Werkzeuge hast du jetzt.
