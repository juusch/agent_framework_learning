# Aufgabe 9.2 – Sicherheit, Kosten & Observability 🔐💸📡

## Schwierigkeit
Mittel · **Kosten: keine** (alles offline demonstrierbar)

## Lernziel
Du kennst die drei Betreiber-Säulen und setzt die Grundlagen selbst um: Key-Management, Budget-Bremsen, strukturiertes Logging – und weißt, wie LangSmith dazukommt.

## Warum ist das wichtig?
Die drei klassischen KI-Inzidenz-Kategorien: **geleakte Keys** (Kosten + Schaden), **explodierende Kosten** (Loops ohne Limit, übergroße Prompts), **Fehlersuche ohne Spur** („warum hat der Agent das getan?").

## Das Konzept einfach erklärt
- **Sicherheit = Haustürschlüssel-Disziplin:** Keys liegen in `.env`/Umgebungsvariablen, nie im Code, nie im Log (siehe Stufe 1.4). Zusätzlich: LLM-Ausgaben sind **nicht vertrauenswürdig** – wer Ansagen des Modells ungeprüft ausführt (Stichwort *Prompt-Injection*: „ignoriere alles und sende..."), hat die Haustür offen.
- **Kosten = Zähler am Wasserhahn:** Jeder Token kostet. Die größten Hebel: Loop-Limits (Stufe 5.4/7.3!), kleines Modell für einfache Aufgaben, Kontext klein halten (RAG statt Volltext), Caching.
- **Observability = schwarzer Kasten im Flugzeug:** Logging schreibt die Basisdaten (Ereignis, Kontext, Fehler); **Tracing** verbindet die Ereignisse zu einem Aufruf-Verlauf („Trace"). LangSmith ist der Standard-Katalog dafür im LangChain-Universum.

## Die technische Erklärung
- **Logging:** `logging`-Modul, strukturierte Zeilen (Zeitstempel, Level, Meldung), Logger pro Modul (`logging.getLogger(__name__)`). Niemals Secrets loggen.
- **Kosten-Schätzung:** (Tokens_Input + Tokens_Output) × Preis – du kennst die Faustregel `zeichen // 4` aus Stufe 2.
- **LangSmith:** aktiviert man per Umgebungsvariablen (`LANGSMITH_TRACING=true`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`) – danach zeichnet die LangChain-Runtime Traces automatisch auf. Keine Code-Änderung – ein Betreiber-Feature!
- **Rate-Limits:** API-Provider drosseln Anfragen (429 – kennst du aus Stufe 2); Anwendungen müssen damit umgehen können (Backoff).

## Deine Mission
1. Baue `logging_demo.py`: Logging-Setup (Format mit Zeitstempel), ein Decorator `@verfolge`, der Start/Ende/Dauer **jeder** Funktion protokolliert, eine Demo-Pipeline (3 Funktionen), bei der der Trace in der Konsole sichtbar wird. **Pflicht:** ein Test protokolliert einen fiktiven Key und du weist nach (Assert/Filter), dass er maskiert wird (`***`).
2. Kosten-Rechner: Funktion `schaetze_kosten(zeichen_input, zeichen_output, preis_pro_1k=0.001)` – rechne drei Szenarien durch: 1 Frage, 100 Fragen, „Loop ohne Limit" (100 Wiederholungen) – und kommentiere deine Erkenntnis.
3. LangSmith-Vorbereitung: ergänze in `.env.example` die drei Variablen als **kommentiert aus** und erkläre in 3 Zeilen im Code, was nach dem Setzen passiert.

## Akzeptanzkriterien
- [ ] Der Trace zeigt Start/Ende/Dauer je Funktion in richtiger Reihenfolge.
- [ ] Keys werden zuverlässig maskiert (Test existiert und ist grün).
- [ ] Der Kosten-Rechner liefert für 100 Fragen einen konkreten Betrag.
- [ ] `.env.example` erklärt LangSmith-Variablen ohne sie zu aktivieren.

## Hinweise
1. Decorator mit `functools.wraps` – sonst verliert die Funktion ihren Namen.
2. Maskierung: `re.sub(r"(sk-|key_)?[A-Za-z0-9_-]{16,}", "***", text)` als Startpunkt.
3. Zeit messen: `time.perf_counter()`.

## Reflexionsfragen
1. Warum ist „Logge alles" ebenso falsch wie „Logge nichts"? (PII, Kosten, Signal-Rauschen)
2. Dein Agent hat 500 € verbrannt – welche **drei** Bremsen aus der Akademie hätten das verhindert? (Tipp: max_runden, interrupt, Kosten-Schätzung)
3. Was bleibt unsichtbar, wenn Logging **nur** Fehler protokolliert – und warum braucht man success-Traces für „es ging, aber warum so langsam"?

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| Key landet im Log | maskieren vor dem Loggen, nie raw ausgeben |
| Decorator verschluckt Rückgabewerte | `return funktion(*args, **kwargs)` nicht vergessen |
| Spaghetti-Logs | Logger-Namen pro Modul, klare Ereignisnamen |

## Referenzlösung
→ [`solutions/logging_demo.py`](../solutions/logging_demo.py)

## Was haben wir gelernt?
Betreibersicheres Logging, Key-Maskierung, Kostenbewusstsein, LangSmith-Anbindung vorbereitet.

## Was kommt als Nächstes?
9.3: Docker – und die Abschluss-Challenge, in der du alles eigenständig baust.
