# Aufgabe 2.4 – Dein Kommandozeilen-Chatbot 💬

## Schwierigkeit
Leicht · ⚠️ **Kosten:** mit Key ein API-Call pro Nachricht (zehn Nachrichten ≈ wenige Cent bei `mistral-small`); ohne Key komplett kostenlos (Offline-Modus).

## Lernziel
Du baust eine Konversation mit **Gedächtnis**: Der Chatbot erinnert sich an den bisherigen Gesprächsverlauf, weil du die Nachrichten-Historie als Liste mitschickst.

## Warum ist das wichtig?
LLMs sind **gedächtnislos**. Jeder API-Call ist ein unabhaengiger, isolierter Moment – das Modell „erinnert" sich nur an das, was du in `messages` mitschickst. Das ist das wichtigste Missverständnis über Chatbots, und du wirst es hier mit eigenen Händen sichtbar machen.

## Das Konzept einfach erklärt
**Metapher:** Das Modell ist ein Assistent mit Goldfisch-Gedächtnis und ohne Notizblock. Ein Chatbot „mit Gedächtnis" ist in Wahrheit: *Du* als Programmierer führst ein Protokoll (die Liste `messages`) und legst es bei jeder Frage **komplett** wieder auf den Tisch. Gedächtnis ist unter dieser Betrachtung kein Magie-Feature, sondern listen-Management – deine Stufe-1-Fähigkeit!

## Die technische Erklärung
1. Start: `messages = [{"role": "system", "content": "Du bist ..."}]`
2. Pro Runde: User-Eingabe als `{"role": "user", ...}` an die Liste **anhängen**.
3. Ganze Liste an die API senden; die Antwort als `{"role": "assistant", ...}` an die Liste **anhängen**.
4. Wächst die Historie über das **Kontextfenster** hinaus, wird der Anfang abgeschnitten (später, in Stufe 4/6, lernst du geordnete Kürzung). Hier: Historical budget klein halten (z. B. nach 20 Nachrichten cutten).

## Voraussetzungen
- Aufgabe 2.2 + 2.3

## Deine Mission
Baue `cli_chatbot.py`:
1. System-Persona deiner Wahl (z. B. „Du bist ein freundlicher Lern-Coach, der geduldig Fragen zu Python und KI beantwortet – kurz und klar, ohne Fachchinesisch.")
2. Endlosschleife mit Eingabeaufforderung; `"exit"` oder `"fertig"` beendet.
3. Der Verlauf bleibt erhalten: Frage als Beweis den Bot nach deinem Namen („Wie heiße ich?"), nachdem du ihn vorher genannt hast.
4. Absicherung: leere Eingaben überspringen; Historie nach 20 Nachrichten kürzen (älteste first).
5. Am Ende eine kurze Verabschiedung.

## Akzeptanzkriterien
- [ ] Der Bot antwortet auf jede Eingabe (mit Key: individuell; ohne: `[OFFLINE]`-Simulation).
- [ ] Der Bot erinnert sich (Beweis-Test, s.o.).
- [ ] `"exit"`/`"fertig"` beendet sauber; leere Eingaben crashen nicht.
- [ ] Im Code ist die Historie als Liste sichtbar gepflegt (append nach jedem Turn).

## Hinweise
1. Anhängen: `messages.append({"role": "user", "content": eingabe})` – VOR dem API-Call.
2. Antwort merken: `messages.append({"role": "assistant", "content": antwort})` – NACH dem Call.
3. Kürzen: `if len(messages) > 20: messages = [messages[0]] + messages[-19:]` – **behalte** die System-Nachricht (Index 0)!
4. Offline-Testen: Der Mock antwortet mit `[OFFLINE]` und spiegelt deine Eingaben – gut, um den *Ablauf* zu prüfen.

## Reflexionsfragen
1. Warum muss die System-Nachricht beim Kürzen gerettet werden?
2. Was passiert mit dem Token-Verbrauch (und deinen Kosten), je länger das Gespräch wird?
3. Worin unterscheidet sich dieses „Kurzzeit-Gedächtnis" von echtem Langzeit-Gedächtnis (Stichwort für Stufe 6: Checkpointer)?

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| Bot „vergisst" alles | Historie wird nicht mitgeschickt oder nicht verlängert |
| 400er Fehler nach vielen Runden | Kontextfenster überschritten → Historie kürzen |
| System-Persona verschwindet | Kürzung hat die erste Nachricht entfernt → sie immer behalten |

## Referenzlösung
→ [`solutions/cli_chatbot.py`](../solutions/cli_chatbot.py)

## Code-Walkthrough
In der Lösungsdatei; besonders wichtig: die Funktion `sende_und_merke()` – sie kapselt „callen + merken", das Herzstück.

## Was haben wir gelernt?
Nachrichten-Historie als Liste, echtes Chat-Gedächtnis, Budget-Kontrolle für Kontextfenster, robuste Schleifen.

## Was kommt als Nächstes?
Herzlichen Glückwunsch – du hast eine funktionierende KI-Unterhaltung gebaut! In Stufe 3 wirst du feststellen: wenn du jetzt Prompt, Modell und Antwort-Nachverarbeitung kombinieren willst, wird der Code schnell spaghetti-artig. Genau dafür gibt es LangChain – Chains, Prompt-Templates und strukturierte Ausgaben erwarten dich.
