# Aufgabe 3.2 – Prompt-Templates & Chains: dein Zusammenfasser 📝

## Schwierigkeit
Anfänger · ⚠️ **Kosten:** nur mit Key

## Lernziel
Du baust eine **Chain** (Fließband) aus Prompt-Template, Modell und Output-Parser – wiederverwendbar für beliebige Texte.

## Warum ist das wichtig?
Ein Prompt-Template ist der Unterschied zwischen „Code für genau eine Frage" und „**Werkzeug** für unendlich viele Fragen". Und die Chain-Verkettung (`|`) ist das Muster, dem du in **allen** folgenden Stufen begegnest (RAG-Pipelines in Stufe 4 sind Chains!).

## Das Konzept einfach erklärt
**Metapher – das Fließband:** Ein Arbeiter schneidet Bleche zurecht (Prompt-Template füllt deine Werte in die Vorlage), der nächste lackiert (das Modell antwortet), der letzte prüft und verpackt (der Output-Parser macht aus dem rohen `AIMessage`-Objekt einen sauberen String). Übergabepunkt ist immer das **Fließband selbst** – die Chain.

## Die technische Erklärung
- `ChatPromptTemplate.from_messages([...])` baut eine Vorlage mit Platzhaltern wie `{text}` und `{stil}`.
- `prompt.invoke({"text": ...})` füllt die Platzhalter → Ergebnis ist ein PromptValue („fertiges Bestellformular").
- **Runnable-Schnittstelle**: alles hat `.invoke()`; mit `|` werden Runnables verkettet: `chain = prompt | model | parser`. Links fließt ein Dictionary rein, rechts kommt das Endergebnis raus.
- `StrOutputParser()` macht aus der `AIMessage` einen reinen String.

## Voraussetzungen
- Aufgabe 3.1

## Deine Mission
Baue `summarizer_chain.py`:
1. Ein Prompt-Template mit **zwei** Variablen: `{text}` (der zusammenzufassende Text) und `{stil}` (z. B. „kurz", „bullet points", „für Kinder").
2. Die Chain: Template → Modell → StrOutputParser.
3. Teste dieselbe Chain mit **demselben Text**, aber drei verschiedenen Stilen – die Chain bleibt unverändert, nur die Eingabe ändert sich!
4. Bonus: baue eine zweite Mini-Chain **Übersetzer** (Variable `{text}`, `{zielsprache}`) und rufe beide nacheinander auf.

## Akzeptanzkriterien
- [ ] Die Chain ist in **einer** Variablen definiert und mehrfach aufrufbar (`.invoke({...})`).
- [ ] Das Template enthält echte Platzhalter, keine festen Texte.
- [ ] Die Ausgabe ist ein String (Parser!), kein `AIMessage`-Objekt.
- [ ] Der Bonus-Übersetzer nutzt dasselbe Modell-Objekt (Wiederverwendung).

## Hinweise
1. Vorlage: `ChatPromptTemplate.from_messages([("system", "Du fasst Texte zusammen..."), ("human", "Fasse zusammen ({stil}): {text}")])`
2. Kette: `chain = prompt | model | StrOutputParser()` – importiere aus `langchain_core.output_parsers`.
3. Aufruf immer mit **allen** Platzhaltern: `chain.invoke({"stil": "kurz", "text": "..."})` – fehlt einer, gibt es einen Fehler (Pydantic-Validierung deiner Eingabe!).

## Reflexionsfragen
1. Was passiert, wenn du beim `invoke` einen Platzhalter vergisst – und warum ist dieser *Fehler* ein Feature (Validierung)?
2. Warum ist es eine Chain, wenn doch nur ein Modell-Call passiert? (Tipp: zähle die Runnables: 3!)
3. Wie würdest du das Fließband erweitern, um **vor** dem Modell den Eingabetext zu kürzen? (Denk an `RunnableLambda` – kommt in 3.4 dran.)

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| `missing required argument` beim invoke | alle Platzhalter im Dict übergeben |
| `AIMessage(...)` als Ausgabe | `StrOutputParser` an die Chain hängen |
| falscher Import (`langchain.prompts` alt) | aktuell: `from langchain_core.prompts import ChatPromptTemplate` |

## Referenzlösung
→ [`solutions/summarizer_chain.py`](../solutions/summarizer_chain.py)

## Code-Walkthrough
In der Lösungsdatei; achte auf den Aufbau `baue_chain()` (Fabrikfunktion) – Chains wie Werkzeuge bauen und wiederverwenden.

## Was haben wir gelernt?
Prompt-Templates, Runnables, `|`-Verkettung, Output-Parser, Chain-Wiederverwendung.

## Was kommt als Nächstes?
Bislang kommen aus dem Modell **Strings** zurück. Aber Anwendungen brauchen **Daten**: Titel, Listen, Zahlen, Objekte. Aufgabe 3.3: strukturierte Ausgaben mit Pydantic – die Grundlage jeder ernsthaften KI-Automatisierung.
