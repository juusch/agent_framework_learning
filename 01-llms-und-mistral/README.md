# Modul 1 – LLMs & deine erste Mistral-Anwendung 🧠

**Ziel:** Du verstehst, was passiert, wenn Python mit einem LLM spricht – und hast deinen ersten API-Call und einen Chatbot gebaut.

| # | Aufgabe | Zeit | API? |
|---|---|---|---|
| 1.1 | [`tasks/01-erster-api-call.md`](tasks/01-erster-api-call.md) – Nachrichten, Tokens, Kosten | ~60 Min | ⚠️ nur mit Key |
| 1.2 | [`tasks/02-chatbot.md`](tasks/02-chatbot.md) – Chatbot mit Gedächtnis & Temperature | ~60 Min | ⚠️ nur mit Key |

**Anbieter-losgelöst:** Mistral ist das Standard-Beispiel – aber dieselben Aufgaben laufen auch mit **deinem lokalen AI-Server** oder jedem OpenAI-kompatiblen Endpoint. Umgeschaltet wird **nur in `.env`**, nie im Code: [docs/local-ai-server.md](../docs/local-ai-server.md). Ohne jede Konfiguration läuft alles im Offline-Modus (`[OFFLINE]`-Antworten, identischer Ablauf). Verbindung prüfen: `python -m tools.test_llm_connection`

> 💡 **Lektion „Dein KI-Modell ist austauschbar":** Ob Mistral, ein lokales Llama oder Qwen antwortet – die Aufgabe *„Sende eine Nachricht an ein LLM"* bleibt dieselbe. Diese Trennung (Anwendung → Schnittstelle → Anbieter) ist eine der wichtigsten Architektur-Erfahrungen der Akademie.

**Ausführen:**
```bash
python3 01-llms-und-mistral/solutions/first_api_call.py
python3 01-llms-und-mistral/solutions/messages_and_temperature.py
python3 01-llms-und-mistral/solutions/cli_chatbot.py
```

**Danach:** [`../02-build1-python-assistent/`](../02-build1-python-assistent/README.md) – **Build 1**: dein erster Personal Knowledge Assistant in reinem Python.
