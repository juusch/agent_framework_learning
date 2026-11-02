# Aufgabe 3.3 – Strukturierte Ausgaben mit Pydantic 🗂️

## Schwierigkeit
Leicht · ⚠️ **Kosten:** nur mit Key

## Lernziel
Du zwingst das Modell, **validierte Daten** statt Fließtext zu liefern: ein Pydantic-Objekt mit garantierten Feldern und Typen.

## Warum ist das wichtig?
Ein Chatbot darf Text faseln – eine Anwendung, die weiterverarbeitet, braucht `titel: str`, `dauer_minuten: int`, `zutaten: list[str]`. Strukturierte Ausgaben sind die Brücke zwischen „KI antwortet" und „Software rechnet weiter". Pydantic prüft dabei **automatisch**, dass das Modell geliefert hat, was du bestellt hast.

## Das Konzept einfach erklärt
**Metapher – Formular statt Brief:** Ohne Struktur schreibt das Modell einen freien Brief. Mit `with_structured_output(RezeptIdee)` händest du ihm ein **vorgedrucktes Formular** aus: Feld für Feld muss es ausfüllen. Pydantic ist der Kontrolleur am Schalter: Fehlt ein Pflichtfeld oder ist eine Zahl kein Zahl → sofort meckert er (und wir können neu anfragen oder fehlerbehandeln).

## Die technische Erklärung
1. Du definierst eine **Pydantic-Klasse** (erbt von `BaseModel`): Feldnamen + Typen + `Field(..., description=...)`. Die Beschreibung ist Teil der Anweisung an das Modell!
2. `modell.with_structured_output(RezeptIdee)` liefert eine Chain, die statt Text direkt **geprüfte Objekte** zurückgibt.
3. Unter der Haube nutzt LangChain die JSON-Mode/Tool-Fähigkeiten des Modells (Mistral unterstützt beides) und validiert das Ergebnis gegen deine Klasse – bei echten Modellen inklusive automatischem Reparatur-Retry.
4. Danach arbeitest du normal in Python: `rezept.titel`, `rezept.dauer_minuten` – mit Autovervollständigung und Typprüfung.

## Voraussetzungen
- Aufgabe 3.2 (Chains, Templates)

## Deine Mission
Schreibe `structured_output.py`:
1. Definiere das Pydantic-Modell `RezeptIdee`: `titel: str`, `zutaten: list[str]`, `dauer_minuten: int`, `schwierigkeit: str` (mit Beschreibungen pro Feld!).
2. Baue die strukturierte Chain und rufe sie mit „Ich habe Nudeln, Tomaten und Knoblauch da" auf.
3. Gib danach **Feld für Feld** aus – und zeige, dass du normal damit rechnen kannst (z. B. Ausdruck: „Für {n} Zutaten brauchst du {dauer} Minuten").
4. Zweites Modell nach Wahl (z. B. `Kurzanalyse` mit `stimmung: str`, `schaetzung_thema: str`, `has_fragezeichen: bool`) – teste es mit einem Satz deiner Wahl.
5. Fehlerbehandlung: falls die strukturierte Kette eine `ValidationError` wirft, fange sie ab und gib eine verständliche Meldung aus.

## Akzeptanzkriterien
- [ ] Beide Modelle sind Pydantic-Klassen mit `Field(..., description=...)`.
- [ ] Die Rückgabe ist ein **Objekt** mit Attributzugriff, kein JSON-String.
- [ ] Du kannst mit den Feldern **rechnen** (Zutaten zählen, Minuten verdoppeln o. ä.).
- [ ] Ein `try/except` um die Validierung existiert.

## Hinweise
1. Importe: `from pydantic import BaseModel, Field`
2. Beschreibungen sind wichtig: `titel: str = Field(description="Kreativer Rezeptname")` – das Modell liest sie mit!
3. `chain = modell.with_structured_output(RezeptIdee)`; Aufruf: `chain.invoke("Ich habe Nudeln...")` (hier reicht die nackige User-Eingabe).
4. Offline-Modus: Die Akademie-Simulation füllt das Formular mit `[OFFLINE]`-Platzhaltern – perfekt, um den **Datenfluss** zu üben; die Feldtypen werden dabei echt validiert.

## Reflexionsfragen
1. Warum sind `description`-Texte für die Qualität der Ausgabe fast so wichtig wie der Prompt selbst?
2. Was wäre riskanter: `float`-Division mit einem vom Modell gelieferten `int`, oder freitextliche „30 Minuten" auszuparsen? Warum?
3. Wo würde dich strukturierte Ausgabe in Stufe 4 (RAG) entlasten können? (Tipp: Antworten mit Quellenangabe)

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| `ValidationError` beim invoke | Feldtypen prüfen; Modell-Antwort war kein passendes JSON → beschreibende Felder verbessern |
| Rückgabe wirkt wie Dict, kein Punkt-Zugriff | prüfen, ob du `with_structured_output` nutzt (nicht `JsonOutputParser`-Bastellösung) |
| leere Liste als Ausgabe bei realen Modellen | Prompt präzisieren („mindestens 3 Zutaten") |

## Referenzlösung
→ [`solutions/structured_output.py`](../solutions/structured_output.py)

## Code-Walkthrough
In der Lösungsdatei; besonders die `Field(description=...)`-Details und das try/except.

## Was haben wir gelernt?
Pydantic-Schemata, `with_structured_output`, Validierung als Sicherheitsnetz, rechnen mit KI-Ausgaben.

## Was kommt als Nächstes?
Abschlussprojekt der Stufe: Du kombinierst **alles** (Templates, Chains, strukturierte Ausgaben, Fehlerbehandlung) zu einem Content-Assistant – einem kleinen, aber echten Werkzeug.
