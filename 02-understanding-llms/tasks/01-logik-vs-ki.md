# Aufgabe 2.1 – Traditionelle Logik vs. KI ⚖️

## Schwierigkeit
Anfänger

## Lernziel
Du kannst in eigenen Worten erklären, **wann** klassische Programmierung passt und wann ein LLM – und zwar aus Erfahrung, nicht aus Theorie.

## Warum ist das wichtig?
Der häufigste Fehler in KI-Projekten ist, ein LLM für Probleme einzusetzen, die mit 5 Zeilen `if` besser gelöst sind (teuer, langsam, unzuverlässig) – oder umgekehrt mit `if`-Wüsten „KI" zu simulieren, wo Sprachverständnis nötig wäre. Diese Aufgabe schärft dein Urteil, bevor du einen Cent ausgibst.

## Das Konzept einfach erklärt
- **Klassische Logik** = Fahrkartenautomat: exakt vorhersehbar, endlos zuverlässig, aber starr. Rechnet immer `2 + 2 = 4`.
- **LLM** = belesener Assistent: versteht „Ich will morgen früh weg von hier" auch, wenn du keine Fahrkarte explizit erwähnt hast – kann sich aber auch mal irren oder etwas erfinden (**Halluzination**).

## Die technische Erklärung
- Klassisch: Regeln vom Menschen → 100 % deterministische Ausführung.
- LLM: hat aus Wahrscheinlichkeiten gelernt, welches Wort gut zum vorherigen Text passt. Es gibt daher **keine Garantie** für Richtigkeit – wohl aber Flexibilität für beliebige Formulierungen. Gesteuert wird es über *Prompts* (Anweisungen) und *Parameter* (z. B. Temperature, Aufgabe 2.3).

## Voraussetzungen
- Stufe 1 (Funktionen, `if/elif`)

## Deine Mission
Kein neues Programm – sondern ein **Gedanken- und Code-Experiment** mit dem Assistenten aus Aufgabe 1.5:
1. Führe `01-python-fundamentals/solutions/personal_assistant.py` aus.
2. Probiere fünf **verschieden formulierte** Uhrzeit-Fragen: „zeit", „wie spät ist es?", „sag mir die Uhrzeit bitte", „Uhrzeit?", „kannst du mir sagen, wie spät es gerade ist?".
3. Notiere: Wie viele davon versteht der Regel-Assistent?
4. Schreibe in `notizen_logik_vs_ki.md` (lege sie in deinem eigenen Lernordner an): eine Tabelle mit den Spalten *Frage / verstanden? / warum*. Darunter 3 Sätze: Wann wäre ein LLM hier besser? Wann ist die Regel besser? Was kostet dich die Regel-Lösung, wenn du 10 000 Frageformulierungen abdecken willst?

## Akzeptanzkriterien
- [ ] Du hast mind. 5 unterschiedliche Formulierungen getestet.
- [ ] Deine Tabelle erklärt pro Frage, warum sie funktioniert oder scheitert.
- [ ] Du kannst in 2 Sätzen begründen: Warum skaliert `if`-Logik schlecht für natürliches Sprachverständnis?

## Hinweise
1. Der Regel-Assistent prüft nur, ob das Wort „zeit" *enthalten* ist (`.lower()` + `in`). „Uhrzeit" enthält „zeit" – funktioniert das auch? Prüfe!
2. Überlege: Wie viele `if`-Zweige bräuchtest du für „Kannste mir ma sagen wie spät det is?" (Umgangssprache, Tippfehler)?

## Reflexionsfragen
1. Warum kann eine Regel-Anweisung korrekt sein, ein LLM aber trotzdem der bessere Werkzeugwahl?
2. Warum umgekehrt ein LLM für „Wenn Alter < 18: Zugriff verweigern" die falsche Werkzeugwahl ist (Stichwort: Zuverlässigkeit/Prüfbarkeit)?
3. Was ist eine Halluzination und warum ist sie bei Regeln unmöglich?

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| „Die Regeln sind blöd" | Nein – sie sind *exakt*. Falsch eingesetzt, nicht falsch gebaut. |
| Nur eine Frageform getestet | teste absichtlich krumme Formulierungen und Tippfehler |

## Referenzlösung
→ [`solutions/logik_vs_ki_notizen.md`](../solutions/logik_vs_ki_notizen.md) (Muster-Notizen mit Erwartungen)

## Was haben wir gelernt?
Die Stärken-/Schwächen-Logik von Regeln vs. LLM – die wichtigste Architekturentscheidung jeder KI-Anwendung.

## Was kommt als Nächstes?
Jetzt lässt du zum ersten Mal *echt* (oder simuliert) ein LLM antworten: Aufgabe 2.2 – dein erster API-Call an Mistral.
