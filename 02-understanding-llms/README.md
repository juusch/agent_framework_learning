# Stufe 2 – LLMs verstehen 🧠

**Ziel:** Du verstehst, was passiert, wenn Python mit einem KI-Modell spricht – und du hast deinen ersten echten API-Call an Mistral gemacht (oder ihn im Offline-Modus simuliert) und einen Chatbot gebaut.

## Die großen Fragen dieser Stufe

- Was ist ein LLM und warum ist es „manchmal unzuverlässig"?
- Was sind Tokens, was das Kontextfenster, was Temperature?
- Was ist eine API und wie fliegen Nachrichten hin und her?
- Wie entstehen Kosten?

## Voraussetzungen

- Stufe 1 abgeschlossen (venv aktiv, `.env` verstanden)
- Optional (empfohlen, aber **nicht nötig**): ein Mistral-API-Key in `.env`
  → kostenlos anlegen unter <https://console.mistral.ai/>. **Ohne Key läuft alles automatisch im Offline-Modus** – dann siehst du klar mit `[OFFLINE]` markierte simulierte Antworten.

## Aufgaben

| # | Aufgabe | Schwierigkeit | API? |
|---|---|---|---|
| 2.1 | [`tasks/01-logik-vs-ki.md`](tasks/01-logik-vs-ki.md) | Anfänger | nein |
| 2.2 | [`tasks/02-erster-api-call.md`](tasks/02-erster-api-call.md) | Anfänger | ⚠️ nur mit Key |
| 2.3 | [`tasks/03-system-nachrichten-und-temperature.md`](tasks/03-system-nachrichten-und-temperature.md) | Leicht | ⚠️ nur mit Key |
| 2.4 | [`tasks/04-chatbot.md`](tasks/04-chatbot.md) | Leicht | ⚠️ nur mit Key |

## Ausführen

```bash
python3 02-understanding-llms/examples/token_zaehler.py
python3 02-understanding-llms/solutions/first_api_call.py
python3 02-understanding-llms/solutions/messages_and_temperature.py
python3 02-understanding-llms/solutions/cli_chatbot.py
```

## Was du danach kannst

Du weißt, was bei einem API-Call technisch passiert, kannst System-/User-Nachrichten gezielt einsetzen, das Verhalten über Temperature steuern und einen Chatbot mit Gesprächsverlauf bauen – die perfekte Basis für LangChain (Stufe 3).
