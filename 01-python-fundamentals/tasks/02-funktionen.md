# Aufgabe 1.2 – Funktionen & Imports: deine Code-Werkstatt 🔧

## Schwierigkeit
Anfänger

## Lernziel
Du kannst eigenes Verhalten in **Funktionen** verpacken, Parameter und Rückgabewerte nutzen und Module mit `import` einbinden.

## Warum ist das wichtig?
LangChain-Anwendungen bestehen aus vielen kleinen, benannten Schritten („Prompt bauen", „Modell aufrufen", „Antwort formatieren"). Funktionen sind die Form, in der du solche Schritte schreibst und **wiederverwendest**. Imports sind der Weg, fremde Bausteine (z. B. `datetime` oder später `langchain`) in deinen Code zu holen.

## Das Konzept einfach erklärt
Eine Funktion ist ein **Rezept mit Namen**: einmal aufgeschrieben (`def`), immer wieder kochbar. Zutaten heißen **Parameter**, das fertige Gericht heißt **Rückgabewert** (`return`).

**Metapher:** Ein Kaffeevollautomat: du drückst einen Knopf (Funktionsaufruf), wählst Zutaten (Argumente) und bekommst ein Ergebnis – ohne die Maschine jedes Mal neu zu erfinden.

## Die technische Erklärung
- `def name(parameter):` definiert; `return` gibt zurück und beendet die Funktion.
- **Standardwerte**: `def kaffee(bohnen="arabica")` – aufrufbar mit oder ohne Argument.
- `import modul` / `from modul import ding`: holt fremden Code in den eigenen.
- Gute Funktionen machen **eine** Sache und sind am Namen erkennbar (`berechne_summe` statt `mache_zeugs`).

## Voraussetzungen
- Stufe 0 (Variablen, Bedingungen), Aufgabe 1.1 (Listen)

## Deine Mission
Schreibe `funktions_werkstatt.py` mit drei Funktionen:
1. `begruessung(name, stil="hoeflich")` → gibt je nach Stil (`"hoeflich"` oder `"locker"`) einen passenden Begrüßungssatz **zurück**.
2. `durchschnitt(zahlen: list)` → gibt den Durchschnitt einer Zahlenliste zurück (leere Liste: `0` statt Absturz!).
3. `ist_arbeitszeit(stunde: int)` → `True`, wenn die Stunde zwischen 9 und 17 liegt, sonst `False`.

Nutze danach in `main()` mindestens **zwei Module der Standardbibliothek** (`datetime` für die aktuelle Stunde, `random` für eine zufällige Zahl) und rufe alle deine Funktionen auf.

## Akzeptanzkriterien
- [ ] Alle drei Funktionen liefern bei den Beispielen aus `main()` plausible Ergebnisse.
- [ ] `durchschnitt([])` ergibt `0` **ohne** Fehler (`ZeroDivisionError`).
- [ ] `begruessung` funktioniert mit und ohne zweites Argument.
- [ ] `datetime` und `random` sind importiert und werden benutzt.

## Hinweise
1. Standardwert im Kopf: `def begruessung(name, stil="hoeflich"):` – dann ist `begruessung("Anna")` erlaubt.
2. Leere Liste abfangen: `if not zahlen: return 0` **vor** der Division.
3. Aktuelle Stunde: `from datetime import datetime` und dann `datetime.now().hour`.
4. Zufallszahl: `import random`, `random.randint(1, 6)`.

## Reflexionsfragen
1. Was ist der Unterschied zwischen `print` (zeigen) und `return` (zurückgeben) in einer Funktion – und warum ist `return` für Tests so wichtig?
2. Warum darf eine Funktion nicht `mache_alles()` heißen?
3. Was macht `from datetime import datetime` anders als `import datetime`?

## Häufige Fehler
| Fehler | Ursache | Lösung |
|---|---|---|
| Funktion gibt `None` zurück | `print` statt `return` verwendet | `return ergebnis` |
| `ZeroDivisionError` | leere Liste durch `len(...)=0` geteilt | leere Liste vorher abfangen |
| `TypeError: missing argument` | Pflichtparameter beim Aufruf vergessen | Standardwert setzen oder Argument übergeben |
| `IndentationError` | Uneinheitliches Einrücken | 4 Leerzeichen pro Ebene |

## Referenzlösung
→ [`solutions/funktions_werkstatt.py`](../solutions/funktions_werkstatt.py)

## Code-Walkthrough
Kommentiert Zeile für Zeile in der Lösungsdatei; beachte: keine Funktion macht `input()` – reine Funktionen sind leichter testbar.

## Was haben wir gelernt?
Funktionen, Parameter, Standardwerte, Rückgabewerte, Imports, defensive Absicherung gegen Abstürze.

## Was kommt als Nächstes?
Du hast jetzt Sprachfundament. Aber echte Projekte benutzen **fremde Pakete** (`langchain`!). Damit sich Projekte nicht in die Quere kommen, gibt es virtuelle Umgebungen – Aufgabe 1.3.
