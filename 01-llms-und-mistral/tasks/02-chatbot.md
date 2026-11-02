# Aufgabe 1.2 – Dein erster Chatbot: Gedächtnis & Temperature 💬

**Schwierigkeit:** Leicht · **Zeit:** ~60 Min · ⚠️ **Kosten:** mit Key ein Call pro Nachricht

## Lernziel
Du baust eine Konversation mit **Gedächtnis** (Nachrichten-Historie als Liste) und steuerst das Verhalten über System-Nachricht und Temperature.

## Warum das wichtig ist
LLMs sind **gedächtnislos**: Jeder Aufruf ist ein isolierter Moment. „Gedächtnis" ist in Wahrheit Listen-Management – deine Modul-0-Fähigkeit! **Metapher:** Der Assistent hat Goldfisch-Gedächtnis; *du* führst das Protokoll (`messages`) und legst es bei jeder Frage komplett wieder auf den Tisch.

## Deine Mission
1. Baue `cli_chatbot.py`: Endlosschleife mit `input()`, `"exit"`/`"fertig"` beendet; Historie bleibt erhalten (Beweis: nenne zuerst deinen Namen, frage dann „Wie heiße ich?").
2. Historie pflegen: User-Eingabe **vor** dem Call anhängen, Modell-Antwort **nach** dem Call.
3. Budget-Bremse: Historie nach 20 Nachrichten kürzen – **die System-Nachricht (Index 0) immer behalten!**
4. **Temperature-Experiment** (siehe `messages_and_temperature.py`): dieselbe kreative Frage dreimal mit `temperature=0.0` und dreimal mit `0.9` – vergleiche die Einzigartigkeit der Antworten. Faustregel notieren: Fakten → niedrig, Ideen → hoch.

## Akzeptanzkriterien
- [ ] Der Bot erinnert sich innerhalb des Gesprächs (Beweis-Test bestanden).
- [ ] `"exit"` beendet sauber; leere Eingaben crashen nicht.
- [ ] Du kannst erklären, warum die System-Nachricht beim Kürzen gerettet werden muss.
- [ ] Dein Temperature-Kommentar enthält die Faustregel.

## Hinweise
1. Anhängen: `messages.append({"role": "user", "content": eingabe})`
2. Kürzen: `messages = [messages[0]] + messages[-19:]`
3. Offline: Der Mock spiegelt deine Eingaben – gut, um den **Ablauf** zu prüfen.

## Reflexionsfragen
1. Was kostet ein immer länger werdendes Gespräch an Tokens – und warum?
2. Warum wäre `temperature=1.0` für einen Rechtschreibkorrektor schlecht?
3. Worin unterscheidet sich dieses Kurzzeit-Gedächtnis von echtem Langzeit-Gedächtnis?

## Referenzlösung + Walkthrough
→ [`solutions/cli_chatbot.py`](../solutions/cli_chatbot.py), [`solutions/messages_and_temperature.py`](../solutions/messages_and_temperature.py)

## Weiter
🧱 [`../02-build1-python-assistent/`](../02-build1-python-assistent/README.md) – **Build 1**: derselbe Chatbot, aber mit echtem Wissen aus Dokumenten – in reinem Python, ohne jedes KI-Framework.
