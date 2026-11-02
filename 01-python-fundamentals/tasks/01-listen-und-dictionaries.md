# Aufgabe 1.1 – Listen & Dictionaries: dein Einkaufslisten-Manager 🛒

## Schwierigkeit
Anfänger

## Lernziel
Du kannst Informationen in **Listen** (geordnete Sammlungen) und **Dictionaries** (Schlüssel-Wert-Paaren) speichern, ergänzen und wiederfinden.

## Warum ist das wichtig?
Eine RAG-Anwendung (Stufe 4) speichert Dokumente in Listen; ein Chatbot verwaltet seinen Gesprächsverlauf als Liste von Nachrichten; Konfigurationen sind Dictionaries. Sammlungen sind das zweitwichtigste Werkzeug nach Variablen.

## Das Konzept einfach erklärt
- Eine **Liste** ist eine nummerierte Schublade: `einkauf[0]` ist das erste Fach (Index beginnt bei 0!).
- Ein **Dictionary** ist ein Wörterbuch: du suchst unter einem Stichwort („Milch") und findest den Eintrag („1.20 €").

**Metapher:** Die Liste ist eine Einkaufszettelrolle (Reihenfolge zählt), das Dictionary ist ein Preis-Schilderregal (Namen zählen, Reihenfolge egal).

## Die technische Erklärung
- `liste.append(wert)` hängt hinten an; `len(liste)` zählt; `for item in liste:` läuft alle durch.
- `dict["schluessel"]` liest einen Wert (Fehler, wenn er fehlt); `dict.get("schluessel", standard)` ist die sichere Variante; `dict["neu"] = wert` legt an.
- `for schluessel, wert in dict.items():` läuft über alles Paare.

## Voraussetzungen
- Variablen, Strings, Zahlen (Stufe 0)

## Deine Mission
Baue einen kleinen Einkaufslisten-Manager mit fest eingebauten Startdaten:
1. Eine Liste `einkauf` mit mindestens 3 Artikeln.
2. Ein Dictionary `preise`, das zu jedem Artikel den Preis (in Euro) speichert.
3. Gib die komplette Liste mit allen Preisen aus.
4. Berechne und gib die **Gesamtsumme** aus.
5. Füge einen neuen Artikel hinzu (in Liste **und** Preis-Dictionary) und gib die Liste erneut aus.

## Akzeptanzkriterien
- [ ] Die Ausgabe zeigt jeden Artikel mit Preis.
- [ ] Die Gesamtsumme stimmt (rechne per Hand nach!).
- [ ] Nach dem Hinzufügen erscheint der neue Artikel mit Preis und die Summe ändert sich.

## Hinweise
1. Summe über eine Schleife: `gesamt = 0` und in der Schleife `gesamt += preise[artikel]`.
2. Oder als Einzeiler (Kurzform, nach der Schleife verständlich): `sum(preise[a] for a in einkauf)`.
3. Zum hübschen Ausgeben: `f"{preis:.2f}"` zeigt immer zwei Nachkommastellen.

## Reflexionsfragen
1. Warum beginnt der Index einer Liste bei 0 und nicht bei 1?
2. Was passiert bei `preise["Kaviar"]`, wenn „Kaviar" nicht existiert – und welche sichere Alternative kennst du?
3. Wann würdest du eine Liste, wann ein Dictionary wählen?

## Häufige Fehler
| Fehler | Ursache | Lösung |
|---|---|---|
| `IndexError: list index out of range` | Index hinter dem Ende abgefragt | `len(liste)` prüfen; Index < len |
| `KeyError: 'Kaviar'` | Schlüssel existiert nicht | `.get(...)` oder vorher prüfen |
| falsche Summe | String statt Zahl addiert (`"1.20"`) | Preise als Zahl (`1.2`) speichern |

## Referenzlösung
→ [`solutions/einkaufsliste.py`](../solutions/einkaufsliste.py)

## Code-Walkthrough
In der Lösungsdatei: jede Funktionszeile dokumentiert; `main()` zeigt den Ablauf.

## Was haben wir gelernt?
Listen, Dictionaries, Schleifen, sichere Zugriffe, Aufsummieren.

## Was kommt als Nächstes?
In derselben Datei wirst du sehen, dass der Lösungsvorschlag den Code in kleine **Funktionen** aufteilt. Warum das keine Spielerei ist, sondern der Schlüssel zu wartbaren KI-Anwendungen, lernst du in Aufgabe 1.2.
