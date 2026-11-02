# Aufgabe 0.2 – Variablen & Benutzereingabe 👋

## Schwierigkeit
Anfänger

## Lernziel
Du kannst Informationen in **Variablen** speichern, Zahlen und Text kombinieren und mit `input()` auf Eingaben des Benutzers reagieren.

## Warum ist das wichtig?
Jeder Chatbot – auch der mit Mistral, den du in Stufe 2 baust – macht genau drei Dinge: **Eingabe lesen → verarbeiten → Ausgabe erzeugen**. Diese Aufgabe baut dieses Muster zum ersten Mal, ganz ohne KI.

## Das Konzept einfach erklärt
Eine **Variable** ist eine beschriftete Kiste mit einem Inhalt. `name = "Anna"` legt den Text „Anna" in eine Kiste, die `name` heißt. **Metapher:** Ein Buffet mit beschrifteten Schüsseln – du stellst etwas hinein (`name = ...`), und später schaust du hinein (`name`), wann immer du willst.

`input("Frage: ")` zeigt die Frage im Terminal und **wartet**, bis der Benutzer etwas eintippt und Enter drückt. Das Eingegebene bekommst du als Text zurück.

## Die technische Erklärung
- `=` ist keine Mathematik-Gleichung, sondern eine **Zuweisung**: „Lege das rechts Stehende in die Kiste links."
- `input()` liefert **immer** einen String – auch wenn jemand „30" eintippt. Zum Rechnen musst du mit `int(...)` umwandeln.
- **f-Strings** (`f"Hallo {name}!"`) betten Variablen in Text ein.
- Typen, die du jetzt kennst: `str` (Text), `int` (ganze Zahl), `float` (Dezimalzahl), `bool` (`True`/`False`).

## Voraussetzungen
- Aufgabe 0.1 (Skript anlegen und ausführen)

## Deine Mission
Schreibe ein Programm `personal_greeting.py`, das:
1. den Benutzer nach Name und Alter fragt,
2. das Alter in eine Zahl umwandelt,
3. eine **personalisierte** Begrüßung ausgibt (z. B. „Hallo Anna! Nächstes Jahr wirst du 31."),
4. den Bereich prüft: wenn das Alter kleiner als 0 oder größer als 130 ist, gibt es eine freundliche Fehlermeldung statt der Begrüßung.

## Akzeptanzkriterien
- [ ] Das Programm fragt per `input()` Name **und** Alter ab.
- [ ] Mit dem Alter wird **gerechnet** (z. B. +1 fürs nächste Jahr) – das funktioniert nur nach Umwandlung in eine Zahl.
- [ ] Unsinnige Alterseingaben (z. B. `-5` oder `999`) führen zu einer Fehlermeldung, **ohne** dass das Programm abstürzt.
- [ ] Die Ausgabe ist personalisiert (der Name taucht auf).

## Hinweise
1. Zuweisung mit Abfrage kombinieren: `name = input("Wie heißt du? ")`
2. Umwandeln: `alter = int(input("Wie alt bist du? "))`
3. Bedingung: `if alter < 0 or alter > 130:` → `else:` …
4. Wenn du `int(...)` auf „dreißig" anwendest, stürzt Python ab – fange das mit `try:` / `except ValueError:` ab, **oder** prüfe erst mit `.isdigit()`. Beides ist okay; die Lösung nutzt `try/except`.

## Reflexionsfragen
1. Warum liefert `input()` immer Text, auch bei Zahleneingaben?
2. Was passiert in der Kiste `alter`, wenn du `alter = int(alter)` schreibst – und warum ist das keine Kreislogik?
3. Wo in diesem Programm ist „Eingabe → Verarbeitung → Ausgabe"? Skizziere die drei Teile.

## Häufige Fehler
| Fehler | Ursache | Lösung |
|---|---|---|
| `TypeError: can only concatenate str...` | Text und Zahl mit `+` gemischt | f-String nutzen: `f"{alter + 1}"` |
| `ValueError: invalid literal for int()` | Eingabe war kein Zahlentext | `try/except ValueError` um die Umwandlung |
| Programm endet sofort, ohne zu fragen | `input()` fehlt oder steht nach der Ausgabe | Reihenfolge prüfen |

## Referenzlösung
→ [`solutions/personal_greeting.py`](../solutions/personal_greeting.py)

## Code-Walkthrough
Siehe Kommentarblock in der Lösungsdatei: jede Zeile ist dort einzeln erklärt.

## Was haben wir gelernt?
- Variablen (String, Integer), Zuweisungen, f-Strings
- `input()` und die Typumwandlung mit `int()`
- `if/else`-Entscheidungen und Fehlerbehandlung mit `try/except`

## Was kommt als Nächstes?
Dein Programm kann jetzt zuhören und antworten. Stufe 1 gibt dir die restlichen Bausteine, die du für richtige Anwendungen brauchst: **Sammlungen** (Listen, Dictionaries), **Funktionen** und die **Projekt-Infrastruktur** (virtuelle Umgebungen, Pakete, API-Keys).
