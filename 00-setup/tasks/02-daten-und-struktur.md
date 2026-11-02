# Aufgabe 0.2 – Daten & Struktur: Variablen, Listen, Dictionaries 📦

**Schwierigkeit:** Anfänger · **Zeit:** ~45 Min · **Kosten:** keine

## Lernziel
Informationen speichern (Variablen), sammeln (Listen), benannt ablegen (Dictionaries) und per `input()` einlesen.

## Warum das wichtig ist
Dein Knowledge Assistant wird Fragen entgegennehmen, Dokumente verwalten, Antworten strukturieren – **alles** baut auf Listen und Dictionaries. **Metapher:** Liste = nummerierte Schublade; Dictionary = Wörterbuch (Schlüssel → Wert).

## Deine Mission
1. **Persönliche Begrüßung:** Frage Name und Alter ab; prüfe das Alter (0–130, sonst freundliche Meldung); rechne `alter + 1` in die Ausgabe – `input()` liefert **immer Text**, also `int(...)` nötig!
2. **Einkaufslisten-Manager:** Liste mit 3 Artikeln + Preis-Dictionary; gib alles mit Preisen aus; berechne die Summe; füge einen Artikel hinzu (Liste **und** Dictionary) und gib erneut aus.

## Akzeptanzkriterien
- [ ] Beide Programme laufen ohne Absturz (auch bei Unsinn-Eingaben!).
- [ ] Die Summe stimmt (rechne per Hand nach).
- [ ] Du nutzt für die Summe eine Schleife über die Liste.
- [ ] Du kannst erklären, warum `preise["Kaviar"]` crashen kann und `.get()` sicherer ist.

## Hinweise
1. Sichere Eingaben: `int(...)` in `try/except ValueError` oder `.isdigit()` vorher prüfen.
2. hübsche Zahlen: `f"{preis:.2f}"`
3. Nachschlagewerk: [`docs/python-basics.md`](../../docs/python-basics.md)

## Reflexionsfragen
1. Warum beginnt der Listen-Index bei 0?
2. Wann wählst du eine Liste, wann ein Dictionary? Nenne je ein Beispiel aus deinem Alltag.

## Referenzlösung + Walkthrough
→ [`solutions/personal_greeting.py`](../solutions/personal_greeting.py) (Eingabe → Prüfung → Ausgabe) und [`solutions/einkaufsliste.py`](../solutions/einkaufsliste.py) (Funktionen + `main()`).

## Weiter
0.3 – Wiederverwendbarer Code (Funktionen), saubere Projekte (venv) und sichere API-Keys.
