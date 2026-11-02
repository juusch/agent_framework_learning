# Aufgabe 1.5 – Mini-Projekt: Persönlicher Assistent (Logik-Version) 🤖

## Schwierigkeit
Leicht

## Lernziel
Du baust eigenständig ein vollständiges, interaktives Programm, das Eingaben versteht, Entscheidungen trifft und personalisiert antwortet – der Vorläufer deines KI-Chatbots.

## Warum ist das wichtig?
Hier zeigst du, dass du Stufe 0 + 1 **zusammen** anwenden kannst. Wichtig für das Verständnis von KI: Dein Assistent folgt festen Regeln (`if/elif`). Ab Stufe 2 übernimmt ein LLM die „Antwort-Fabrik" – und genau dann wirst du die Grenzen der Regel-Logik (Steifheit, Pflegeaufwand) schmerzhaft vermissen bzw. schätzen lernen: Das ist der Dreh- und Angelpunkt, **warum** man LLMs verwendet.

## Das Konzept einfach erklärt
Ein regelbasierter Assistent ist ein Fahrkartenautomat: Drücke Knopf A → Ticket A. Er ist perfekt verlässlich, aber er kann nur, was einprogrammiert wurde. Ein LLM-Assistent (später!) ist eher ein netter Bahnhofsmitarbeiter: versteht auch unklare Fragen, kann aber auch mal Unsinn erwidern.

## Die technische Erklärung
- Programme gliedern wir in **Funktionen** (Eingabe lesen, Entscheidung treffen, Antwort bauen) und eine `main()`-Funktion als Dirigent.
- Eine **Endlosschleife** (`while True:`) mit einem Abbruchwort (`"fertig"`) hält das Gespräch am Laufen.
- Das Beenden erfolgt mit `break` – und alles Unbekannte bekommt eine Standardantwort (`else`).

## Voraussetzungen
- Aufgaben 0.1–1.4 (besonders Funktionen und `.env`)

## Deine Mission
Baue `personal_assistant.py`, der:
1. zu Beginn den Namen aus `.env` (`BEISPIEL_NAME`) oder per `input()` erfragt (falls nicht gesetzt),
2. in einer Schleife Befehle entgegennimmt,
3. auf mindestens **drei** Schlüsselwörter reagiert, z. B.:
   - `"zeit"` → aktuelle Uhrzeit (mit `datetime`),
   - `"witz"` → einen zufälligen Witz aus einer **Liste** (mit `random.choice`),
   - `"einkauf"` → zeigt die vorbereitete Einkaufsliste aus Aufgabe 1.1,
4. mit `"fertig"` sich verabschiedet und endet,
5. alles Unbekannte freundlich quittiert und die Befehle aufzählt.

## Akzeptanzkriterien
- [ ] Das Programm läuft in einer Schleife und stürzt bei keiner Eingabe ab.
- [ ] Drei Schlüsselwörter funktionieren.
- [ ] `"fertig"` beendet sauber.
- [ ] Unbekannte Eingaben bekommen eine hilfreiche Antwort (kein Absturz, kein Ignorieren).
- [ ] Der Code ist in Funktionen gegliedert.

## Hinweise
1. Schlüsselwort-Check: `if "zeit" in eingabe.lower():` – findet das Wort auch mitten im Satz.
2. Witzliste: `witze = ["...", "..."]`, dann `random.choice(witze)`.
3. Uhrzeit hübsch: `datetime.now().strftime("%H:%M")`.
4. Wenn du `.env` nutzen willst: `load_dotenv()` nicht vergessen.

## Reflexionsfragen
1. Was passiert, wenn der Benutzer „wie spät ist es bitte?" tippt – warum funktioniert deine Erkennung trotzdem?
2. Was müsstest du tun, damit der Assistent **jede** Frage zur Uhrzeit versteht, egal wie formuliert? Wo sind die Grenzen der `if`-Logik?
3. Genau diese Lücke (Antworten auf unvorhersehbare Formulierungen) schließt ab Stufe 2 das LLM. Notiere dir einen Satz, den du vom LLM erwarten würdest.

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| Programm läuft endlos ohne Abbruchmöglichkeit | `if eingabe.lower() == "fertig": break` |
| Groß-/Kleinschreibung bricht die Erkennung | Eingabe mit `.lower()` normalisieren |
| Alles in `main()` untestbar | Logik in Funktionen auslagern (siehe Lösung) |

## Referenzlösung
→ [`solutions/personal_assistant.py`](../solutions/personal_assistant.py)

## Code-Walkthrough
In der Lösungsdatei; achte auf die Trennung: `finde_antwort()` (reine Logik, testbar!) vs. `main()` (Gesprächsschleife, Ein-/Ausgabe).

## Was haben wir gelernt?
Komplette Programmstruktur: Konfiguration, Funktionen, Schleifen, Entscheidungslogik – und wo fest programmierte Logik an ihre Grenzen stößt.

## Was kommt als Nächstes?
Stufe 2: Du ersetzt deine Regel-Antworten durch ein echtes Large Language Model (Mistral). Du wirst Tokens, Temperatur und Nachrichten-Rollen kennenlernen – und deinen ersten echten API-Call machen (mit Offline-Modus, falls du noch keinen Key hast).
