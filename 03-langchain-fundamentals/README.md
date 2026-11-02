# Stufe 3 – LangChain-Fundamente 🔗

**Ziel:** Du verstehst, **warum** LangChain existiert, und baust deine ersten Chains (Fließbänder): Prompt-Templates → Modell → Output-Parser, inklusive strukturierter Ausgaben und Fehlerbehandlung.

## Direkter API-Call vs. LangChain – der Unterschied in einem Bild

In Stufe 2 hast du direkt angerufen: *Bestellung an den Kellner, Antwort zurück.* Das funktioniert – für **einen** Schritt. Aber richtige Anwendungen sind **Fließbänder** mit vielen Schritten: Eingabe säubern → Prompt aus Vorlage füllen → Modell fragen → Antwort prüfen → formatieren → ggf. in Datenstruktur umwandeln. Alles von Hand zu orchestrieren wird schnell unübersichtlich.

LangChain liefert dafür:
1. **Einheitliche Schnittstelle** (Runnable): Prompt, Modell, Parser, eigene Funktionen – alles hat `.invoke()` und lässt sich mit `|` zum Fließband verketten.
2. **Wiederverwendbare Bausteine**: Prompt-Templates statt String-Zusammenkleberei, Output-Parser statt `json.loads`-Bastelarbeiten.
3. **Austauschbarkeit**: Du tauschst Mistral gegen ein anderes Modell in **einer** Zeile – der Rest des Fließbands bleibt unberührt.
4. **Später (Stufe 5+)**: Graphen, Agenten, Memory – alles baut auf diesen Bausteinen auf.

## Aufgaben

| # | Aufgabe | Schwierigkeit | API? |
|---|---|---|---|
| 3.1 | [`tasks/01-hello-langchain.md`](tasks/01-hello-langchain.md) | Anfänger | ⚠️ nur mit Key |
| 3.2 | [`tasks/02-prompt-templates-und-chains.md`](tasks/02-prompt-templates-und-chains.md) | Anfänger | ⚠️ nur mit Key |
| 3.3 | [`tasks/03-strukturierte-ausgaben.md`](tasks/03-strukturierte-ausgaben.md) | Leicht | ⚠️ nur mit Key |
| 3.4 | [`tasks/04-content-assistant.md`](tasks/04-content-assistant.md) | Mittel | ⚠️ nur mit Key |

## Ausführen

```bash
python3 03-langchain-fundamentals/solutions/hello_langchain.py
python3 03-langchain-fundamentals/solutions/summarizer_chain.py
python3 03-langchain-fundamentals/solutions/structured_output.py
python3 03-langchain-fundamentals/solutions/content_assistant.py
```

Alle Lösungen laufen **auch ohne Key** (Offline-Modus mit `[OFFLINE]`-Antworten) – so kannst du jedes Fließband-Verständnis kostenfrei üben.

## Aktuelle API-Referenz

- [LangChain Python-Doku](https://python.langchain.com/docs/) (v1.x – `ChatPromptTemplate` liegt in `langchain_core.prompts`)
- [Mistral-Integration](https://python.langchain.com/docs/integrations/chat/mistralai/)
- [Mistral AI Docs](https://docs.mistral.ai/)

## Danach
Weiter mit [`../04-rag-and-knowledge/README.md`](../04-rag-and-knowledge/README.md): Du gibst dem Modell Wissen von außerhalb.
