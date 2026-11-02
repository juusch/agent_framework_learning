# Aufgabe 0.1 – Hello World 🎉

## Schwierigkeit
Anfänger

## Lernziel
Nach dieser Aufgabe kannst du ein Python-Skript erstellen, speichern und vom Terminal aus starten.

## Warum ist das wichtig?
Jede KI-Anwendung, jeder Chatbot, jede Automatisierung beginnt so: Du schreibst Text in eine Datei und lässt Python diese Datei ausführen. Das ist der Grundbaustein von allem, was folgt.

## Das Konzept einfach erklärt
Ein **Programm** ist eine Liste von Anweisungen, die der Computer der Reihe nach ausführt. `print(...)` heißt wörtlich: „Gib das auf dem Bildschirm aus." **Metapher:** Python ist ein sehr gehorsamer, aber sehr wörtlicher Mitarbeiter – er macht genau das, was in der Datei steht, Zeile für Zeile. Nicht mehr, nicht weniger.

## Die technische Erklärung
- Dateien mit der Endung `.py` enthalten Python-Code.
- Der Befehl `python datei.py` (Windows) bzw. `python3 datei.py` (macOS/Linux) liest die Datei und führt jede Zeile von oben nach unten aus.
- `print("...")` ist eine eingebaute *Funktion*, die ihren Inhalt als Text im Terminal ausgibt.

## Voraussetzungen
- Python installiert (siehe [`START_HERE.md`](../../START_HERE.md), Schritt 2)
- Ein Editor (z. B. VS Code)
- Ein Terminal

## Deine Mission
1. Erstelle im Projektordner eine Datei `hello_world.py`.
2. Schreibe hinein: eine `print`-Ausgabe mit einem persönlichen Begrüßungstext.
3. Führe sie im Terminal aus.
4. **Bonus:** Füge eine zweite `print`-Zeile hinzu und beobachte, dass die Ausgaben in genau der Reihenfolge erscheinen, in der sie im Code stehen.

## Akzeptanzkriterien
- [ ] Die Datei heißt `hello_world.py`.
- [ ] Beim Ausführen erscheint dein Text im Terminal.
- [ ] Du kannst in einem Satz erklären, was `print` tut.

## Hinweise
1. Der Text muss in Anführungszeichen stehen – einfache `'...'` oder doppelte `"..."` sind beide erlaubt. Deutsche Anführungszeichen „..." funktionieren **nicht**.
2. Achte darauf, dass du im Terminal in dem Ordner bist, in dem die Datei liegt (`cd` dorthin oder Datei mit Rechtsklick → „Im Terminal öffnen").
3. Wenn `python` nicht gefunden wird: Unter Windows heißt der Befehl manchmal `py`, unter macOS/Linux immer `python3`.

## Reflexionsfragen
1. Was passiert, wenn du die Anführungszeichen weglässt? (Probier es aus!)
2. Warum ist die Reihenfolge der Ausgaben wichtig für später, wenn ganze Programme aus vielen Zeilen bestehen?

## Häufige Fehler
| Fehler | Ursache | Lösung |
|---|---|---|
| `SyntaxError` | Anführungszeichen fehlen oder sind deutsch („") | gerade `'` oder `"` verwenden |
| `can't open file 'hello_world.py'` | falscher Ordner im Terminal | `cd` in den Ordner mit der Datei |
| `python: command not found` | Python nicht im PATH | `python3`/`py` nutzen oder Installation wiederholen |

## Referenzlösung
→ [`solutions/hello_world.py`](../solutions/hello_world.py)

## Code-Walkthrough
- Zeile 1: `print(...)` – gibt den Text in den Klammern aus. Alles in `"` ist ein **String** (Text).
- Zeile 3 (Bonus): zeigt, dass Python Zeilen der Reihe nach abarbeitet.

## Was haben wir gelernt?
- Skripte erstellen, speichern, ausführen
- `print`, Strings, die Ausführungsreihenfolge

## Was kommt als Nächstes?
Bislang redet dein Programm *an* den Menschen. In Aufgabe 0.2 lernen wir **Variablen** – benannte „Kisten" für Werte – und `input()`, damit dein Programm zuhören kann. Genau daraus wird später der „Chat"-Teil deines Chatbots.
