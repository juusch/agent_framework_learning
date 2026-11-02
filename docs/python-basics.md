# 🐍 Python-Grundlagen – dein Nachschlagewerk

Diese Seite fasst alles zusammen, was du in Stufe 0 und 1 brauchst. **Lies sie nicht in einem Zug** – nutze sie als Referenz während der Aufgaben.

## Skripte ausführen

```bash
python skript.py      # Windows
python3 skript.py     # macOS/Linux
```

## print – Ausgaben

```python
print("Hallo Welt")                 # einfacher Text
print("Name:", name, "Alter:", 30)  # mehrere Werte, mit Leerzeichen
print(f" Hallo {name}, du bist {alter} Jahre alt!")   # f-String: Werte einbetten
```

## Variablen – beschriftete Kisten

```python
name = "Anna"        # Text (String) in die Kiste "name" legen
alter = 30           # ganze Zahl (Integer)
groesse = 1.68       # Dezimalzahl (Float)
ist_muede = True     # Wahrheitswert (Boolean: True/False)
```

## Eingaben lesen

```python
name = input("Wie heißt du? ")
alter = int(input("Wie alt bist du? "))   # input liefert IMMER Text -> umwandeln
```

## Strings (Text)

```python
text.upper()                       # Grossbuchstaben
text.lower()                       # kleinbuchstaben
text.strip()                       # Leerzeichen an Anfang/Ende entfernen
len(text)                          # Zeichenanzahl
text.replace("alt", "neu")         # ersetzen
f"Hallo {text}"                    # einbetten
if "wort" in text: ...             # enthalten?
```

## Bedingungen

```python
if alter >= 18:
    print("Volljährig")
elif alter > 12:
    print("Jugendlich")
else:
    print("Kind")
```

Vergleiche: `==` gleich, `!=` ungleich, `>` `<` `>=` `<=`. Logik: `and`, `or`, `not`.

## Listen – nummerierte Schubladen

```python
einkauf = ["Milch", "Brot"]
einkauf.append("Butter")        # anhaengen
einkauf[0]                      # Zugriff per Index (startet bei 0!)
einkauf[1] = "Vollkornbrot"    # aendern
len(einkauf)                    # Anzahl
for item in einkauf:            # Schleife
    print(item)
```

## Dictionaries – Wörterbücher

```python
person = {"name": "Anna", "alter": 30}
person["name"]                  # Wert holen
person["stadt"] = "Berlin"      # neues Paar anlegen
person.get("plz", "unbekannt")  # sicher holen (kein Absturz, wenn fehlt)
for schluessel, wert in person.items():
    print(schluessel, "=", wert)
```

## Funktionen – wiederverwendbare Rezepte

```python
def begruesse(name, gruss="Hallo"):   # gruss hat einen Standardwert
    """Gibt eine Begruessung zurueck (Dokumentation)."""
    return f"{gruss}, {name}!"

nachricht = begruesse("Anna")          # -> "Hallo, Anna!"
nachricht = begruesse("Ben", "Moin")   # -> "Moin, Ben!"
```

## Imports und Pakete

```python
import math                     # Standardbibliothek
from datetime import date       # einzelnes Modul importieren

import rich                     # externes Paket -> vorher: pip install rich
```

Paket installieren (Terminal, nicht in Python!):

```bash
pip install rich
```

## Nützliche Module der Standardbibliothek

```python
import json                 # JSON lesen/schreiben
import random               # Zufall: random.choice(["a", "b"])
import os                   # Umgebungsvariablen: os.environ.get("NAME")
from pathlib import Path    # Dateipfade plattformuebergreifend
```

## Mit Dateien arbeiten

```python
from pathlib import Path

inhalt = Path("notiz.txt").read_text(encoding="utf-8")   # lesen
Path("ausgabe.txt").write_text("Hallo", encoding="utf-8") # schreiben
```

## Typische Fehler lesen

```
Traceback (most recent call last):
  File "skript.py", line 5, in <module>
NameError: name 'naem' is not defined
```

Lies von **unten nach oben**: Fehlerart (`NameError`), Bedeutung (`naem` existiert nicht), Ort (`skript.py`, Zeile 5). Meist ein Tippfehler.
