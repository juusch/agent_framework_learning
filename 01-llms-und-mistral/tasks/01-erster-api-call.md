# Aufgabe 1.1 – Dein erster API-Call an Mistral 🚀

**Schwierigkeit:** Leicht · **Zeit:** ~60 Min · ⚠️ **Kosten:** nur mit Key (offline: kostenlos)

## Lernziel
Du weißt, was bei einem API-Call technisch passiert, kennst Nachrichten-Rollen (system/user/assistant), Tokens und Kosten – und hast Mistral aus Python aufgerufen.

## Warum das wichtig ist
Bis Modul 0 war dein Programm allein auf der Welt. Ab jetzt redet es mit einer KI – und **jede** Anwendung der Akademie bis zum großen Assistenten gipfelt in genau diesem Moment. **Metapher – das Restaurant:** Dein Programm ist der Gast, die API der Kellner, das Modell die Küche. Bestellung (Prompt + API-Key als Mitgliedskarte) → Küche antwortet → Kellner bringt das Gericht. Du siehst die Küche nie – bemerkst aber, wenn sie zu ist (Fehler) oder überlastet (429).

## Konzept: Regel-Logik vs. LLM
Klassische Logik (Fahrkartenautomat) ist exakt und starr; ein LLM (belesener Assistent) versteht freie Formulierungen, kann aber irren (**Halluzination**). Beides wird dein Assistent später kombinieren. Details: [`solutions/logik_vs_ki_notizen.md`](../solutions/logik_vs_ki_notizen.md).

## Deine Mission
0. **(Neu)** Führe `python -m tools.test_llm_connection` aus – du siehst, welcher Anbieter aktiv ist (offline / Mistral / lokaler Server). Diese Konfiguration gilt für alle Aufgaben.
1. Schreibe `first_api_call.py`: Client über `get_api_client()` holen (liest Key/URL **nicht selbst** aus `.env`), System-Rolle „Du bist ein freundlicher Erklärbbär für Technik-Anfänger" + User-Rolle „Erkläre in zwei Sätzen, was eine API ist" senden, Antwort ausgeben.
2. Fehlerbehandlung: 401 (Key), 429 (Rate-Limit), Netzwerk → deutsche Meldungen statt Traceback.
3. **Token-Verständnis:** Führe `examples/token_zaehler.py` aus und schätze: Wie viele Tokens hat diese Aufgabe gekostet? (Faustregel: `zeichen // 4`)

## Akzeptanzkriterien
- [ ] Das Skript läuft ohne Key (Offline-Antwort) **und** mit Key (echte Antwort).
- [ ] Der API-Key steht nirgendwo im Quellcode.
- [ ] Du kannst die drei Nachrichten-Rollen benennen und erklären, was ein Token kostet.

## Hinweise
1. Client: `lernakademie.llm_client.get_api_client()` – liefert je nach `.env` den Mistral-SDK-Client, einen OpenAI-kompatiblen Client **oder** die Offline-Simulation. Deine Aufgabe bleibt identisch.
2. Antwort: `response.choices[0].message.content`
3. Kontextfenster = Schreibtischgröße: nur begrenzt viele Tokens passen gleichzeitig drauf.

## Reflexionsfragen
1. Warum steht der Key im Header und nicht im Code?
2. Was wären 100 API-Calls pro Tag in Kosten – und wie würdest du sie reduzieren?
3. Wo im Ablauf „Request → Küche → Response" macht sich ein langsames Netz bemerkbar?

## Referenzlösung + Walkthrough
→ [`solutions/first_api_call.py`](../solutions/first_api_call.py)

## Weiter
1.2 – aus einem Call wird ein **Gespräch**: Gedächtnis, Temperatur, dein erster Chatbot.
