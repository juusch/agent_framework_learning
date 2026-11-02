# Aufgabe 10.2 – Entitäten, Labels & Properties 🏷️

## Schwierigkeit
Anfänger · **Kosten: keine**

## Lernziel
Du modellierst Entitäten sauber: mehrere Labels, sinnvolle Properties, und verstehst den Unterschied zwischen **Label** (Typ) und **Property** (Attribut).

## Warum ist das wichtig?
Die Qualität jedes Knowledge Graphs entscheidet sich beim **Modellieren** (Stichwort: Ontologie – welches „Schema" hat dein Wissen?). Ein `:Person`-Node mit Property `arbeitet_bei: "Acme"` verhindert Graph-Abfragen; eine `WORKS_FOR`-Kante ermöglicht sie. Faustregel: **Struktur (= Beziehungen, Labels) für das, was du abfragen willst; Properties für Details.**

## Das Konzept einfach erklärt
**Metapher – der Vereinsschrank:** Jedes Mitglied hat eine Mitgliedskarte (Node). Oben steht die Sparte (Label: :Tennis, :Finance – mehrfach möglich: jemand spielt Tennis UND ist im Vorstand). Auf der Karte stehen Details (Properties: Name, Beitrittsjahr). Die Karte selbst hängt im „spielt-mit"-Netzwerk (Beziehungen) – das Beitrittsjahr tut das nicht, es ist eine Notiz.

## Die technische Erklärung
- **Mehrfach-Labels:** `store.add_node(["Person", "Employee"], ...)` – ein Node kann mehrere Typen haben. Abfragen können nach jedem Label filtern.
- **Properties** sind Schlüssel-Wert-Paare; Werte können Zahlen, Strings, Booleans sein.
- **Modellierungs-Faustregeln:**
  1. Was du traversieren willst („folge allen Personen, die an X arbeiten") → **Relationship**.
  2. Was du nur anzeigen willst (Alter, Datum, Farbe) → **Property**.
  3. Einheitliche Property-Namen (`name`, nicht mal `Name`, mal `vorname`)!

## Voraussetzungen
- Aufgabe 10.1

## Deine Mission
Erweitere `first_graph.py` zu `entities_graph.py` (oder baue neu):
1. **Mehrfach-Labels:** Anna bekommt `["Person", "Employee"]`; Ben neu dazu mit `["Person", "Employee", "Manager"]`.
2. **Properties:** mind. 3 pro Person (name, rolle, eintrittsjahr) und mind. 2 pro Firma/Projekt.
3. **Modellierungs-Diskussion im Code (als Kommentar):** Schreibe zu drei Beispielen auf, warum du es als Kante oder als Property modelliert hast – z. B.: „seit=2021 an der WORKS_FOR-Kante, weil man abfragen will, wer seit wann dabei ist" vs. „eintrittsjahr am Node".
4. Abfragen: alle Nodes mit Label `Employee`; alle Nodes mit Label `Manager`; alle `Person`en.

## Akzeptanzkriterien
- [ ] Mindestens ein Node hat zwei Labels.
- [ ] Der Label-Filter (`store.nodes("Employee")`) liefert die richtige Teilmenge.
- [ ] Properties sind einheitlich benannt.
- [ ] Drei begründete Modellierungsentscheidungen sind als Kommentare dokumentiert.

## Hinweise
1. `store.nodes("Employee")` filtert nach Label.
2. Property an einer **Kante**: `store.add_relationship(a, b, "WORKS_FOR", seit=2021)` – die Property gehört der Beziehung („seit wann?"), nicht den Personen.
3. Denk an Aufgabe 1.1 zurück: `for node in store.nodes("Employee"): print(node.properties)`.

## Reflexionsfragen
1. Warum wäre `ist_manager: True` als Property schlechter als das Label `Manager` – und wann wäre sie trotzdem okay?
2. „Anna arbeitet SEIT 2021 bei Acme": Warum gehört `seit` an die **Kante** und nicht an Anna oder Acme?
3. Was passiert mit deinen Abfragen, wenn jemand `Vorname` statt `name` benutzt? (Skalierungs-Gift!)

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| Labels als Property (`typ: "Person"`) | Labels sind ein eigenes Konzept – `add_node(["Person"], ...)` |
| Inkonsistente Property-Namen | Konventionen vorher festlegen (Kommentar im Code!) |
| Kanten-Properties vergessen | Properties als **kwargs an `add_relationship` |

## Referenzlösung
→ [`solutions/entities_graph.py`](../solutions/entities_graph.py)

## Code-Walkthrough
In der Lösungsdatei; besonders die Modellierungs-Kommentare.

## Was haben wir gelernt?
Modellierung: Labels vs. Properties, Mehrfach-Labels, Kanten-Properties, Benennungsdisziplin.

## Was kommt als Nächstes?
Jetzt befragst du den Graph: Aufgabe 10.3 – Nachbarn finden, Kanten folgen, Pfade suchen – die Grundbewegung jedes Knowledge-Graph-Systems.
