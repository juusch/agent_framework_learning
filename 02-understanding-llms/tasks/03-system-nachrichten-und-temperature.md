# Aufgabe 2.3 – System-Nachrichten & Temperature 🎛️

## Schwierigkeit
Leicht · ⚠️ **Kosten:** nur mit API-Key (Offline-Modus zeigt den Code-Ablauf, aber **nicht** die Verhaltensunterschiede – der ist dir bewusst).

## Lernziel
Du steuerst Ton und Kreativität eines LLM gezielt über die **System-Nachricht** und den **Temperature-Parameter**.

## Warum ist das wichtig?
Dieselbe Frage kann als nüchterner Fachtext, als Kinderbuch oder als Gedicht beantwortet werden. Der einzige Unterschied liegt in System-Nachricht und Temperature. Wer das steuert, beherrscht das wichtigste „Bedienpult" jeder LLM-Anwendung.

## Das Konzept einfach erklärt
- Die **System-Nachricht** ist die Stellenanweisung an den Assistenten, *bevor* der erste Kunde spricht. **Metapher:** du darfst dem Kellner vor Servicebeginn zuflüstern: „Sprich alle Gäste mit 'Eure Majestät' an."
- **Temperature** = Grad an „Zufall" bei der Wortwahl. **Metapher:** ein Jazz-Saxophonist: bei 0.0 spielt er die Noten exakt wie geschrieben; bei 1.0 improvisiert er frei – meist stimmig, manchmal überraschend.

## Die technische Erklärung
- `temperature` liegt typischerweise zwischen `0.0` und `1.0` (manche Modelle mehr): 0.0 = immer die wahrscheinlichste Antwort (deterministisch), höher = mehr Verteilung über Alternativen (kreativer, riskanter).
- Die System-Nachricht wird als `{"role": "system", "content": ...}` als **erste** Nachricht mitgeschickt.
- Faustregel: Fakten/Extraktion/Übersetzung → niedrige Temperature (0.0–0.2). Brainstorming/Ideen/Geschichten → hohe Temperature (0.7–1.0).

## Voraussetzungen
- Aufgabe 2.2 (Client, Nachrichten-Format)

## Deine Mission
Schreibe `messages_and_temperature.py`, das:
1. eine Funktion `frage(prompt, system, temperature)` kapselt (Parameter bleiben flexibel),
2. **Experiment A (Rolle):** dieselbe User-Frage („Erkläre, was Regenbögen sind") einmal mit System „Du bist ein Physik-Professor" und einmal mit „Du bist ein 6-jähriges Kind" stellt – gib beide Antworten aus,
3. **Experiment B (Temperature):** die Frage „Nenne ein kreatives Geschenk für eine Person, die Kaffee liebt" **dreimal** mit `temperature=0.0` und danach **dreimal** mit `temperature=0.9` stellt – gib alle sechs Antworten aus,
4. danach eine kurze Auswertung druckt: Bei welcher Temperature sind die Antworten sich ähnlicher? (Hinweis: bei 0.0 sollten die drei Antworten praktisch identisch sein!)

## Akzeptanzkriterien
- [ ] Beide Experimente laufen mit nur **einer** wiederverwendbaren Funktion.
- [ ] Mit Key: Du siehst einen sichtbaren Ton-Unterschied (Experiment A) und einen Wiederholungs-Unterschied (Experiment B).
- [ ] Ohne Key: Das Skript läuft im Offline-Modus durch und erklärt, warum die Unterschiede dort fehlen.
- [ ] Im Code steht ein Kommentar mit deiner Faustregel, wann niedrige/hohe Temperature passt.

## Hinweise
1. `client.chat.complete(..., temperature=0.0)` – der Parameter heißt genau so.
2. Sechs Aufrufe = sechs Antworten: nutze eine Schleife (`for i in range(3)`).
3. Miss den Unterschied: `set(antworten)` – bei Temperature 0.0 hat die Menge meist nur 1 Element.

## Reflexionsfragen
1. Warum wäre `temperature=1.0` eine schlechte Wahl für einen Rechtschreibkorrektor?
2. Warum ist die System-Nachricht mächtiger als „Bitte antworte wie ein Professor" **in** der User-Nachricht? (Beide gehen, aber die System-Rolle ist dafür *gebaut*.)
3. Was kosten 12 Aufrufe gegenüber 1 – und wie würdest du Experimente bei knappen Budget gestalten?

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| `temperature` als String `"0.0"` übergeben | Zahl nutzen: `0.0` |
| Kein Unterschied sichtbar | Modell prüfen; einfache Fragen liefern bei niedriger Temperature fast identische Antworten – nutze eine kreative Aufgabe (Experiment B) |
| Offline-Modus: alles identisch | Erwartetes Verhalten – die Simulation ist deterministisch |

## Referenzlösung
→ [`solutions/messages_and_temperature.py`](../solutions/messages_and_temperature.py)

## Code-Walkthrough
In der Lösungsdatei; beachte die kleine Funktion `drucke_block()` für saubere Ausgaben – Wiederverwendbarkeit zahlt sich sofort aus.

## Was haben wir gelernt?
Rollen-Steuerung (system), Temperature und ihre Effekte, Wiederholung als Verständnis-Hebel.

## Was kommt als Nächstes?
Einzelnachrichten waren Test-Feuer. Aufgabe 2.4 verwebt alles zu einem echten Chatbot mit **Gespruchsverlauf** – Nachrichten-Historie als Liste, genau wie du es in Aufgabe 1.1 geübt hast.
