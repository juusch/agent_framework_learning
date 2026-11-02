# Referenzlösung 2.1 – Muster-Notizen: Logik vs. KI

## Test-Tabelle (regelbasierter Assistent aus Aufgabe 1.5)

| Frage | verstanden? | warum |
|---|---|---|
| „zeit" | ✅ | exakter Treffer des Suchworts |
| „wie spät ist es?" | ❌ | enthält „spät"/„es", aber nicht „zeit" (auch nicht als Teilwort: „spät" ≠ „zeit") |
| „sag mir die Uhrzeit bitte" | ✅ | „Uhr**zeit**" enthält den Teilstring „zeit" – Zufallstreffer! |
| „Uhrzeit?" | ✅ | dito |
| „kannst du mir sagen, wie spät es gerade ist?" | ❌ | „spät" statt „zeit" |

Zwischenbilanz: 3 von 5 – und die Treffer beruhen teils auf einem **String-Zufall** („Uhrzeit" enthält „zeit"), nicht auf Verstehen. „spät" scheitert konsequent. Das ist keine Seltenheit, sondern das normale Verhalten von Wortlisten-Logik.

## Warum `if`-Logik für Sprachverständnis schlecht skaliert

Um 10 000 Formulierungen abzudecken, bräuchte ich 10 000 Zweige (plus Pflege für Umgangssprache, Tippfehler, Dialekt: „kannste mir ma …"). Jede neue Variante = neuer Code + neuer Test. Ein LLM deckt diese Varianten **ohne eine einzige zusätzliche Zeile** ab, weil es Sprachmuster gelernt hat – bezahlt mit Unschärfen (Halluzinationsrisiko, Kosten).

## Wann was?

- **Regeln:** exakte, prüfbare Entscheidungen (Alter < 18 → Zugriff verweigern; Preis > 100 € → Rabatt). 100 % verlässlich, gratis, prüfbar.
- **LLM:** offene Formulierungen, Zusammenfassen, Übersetzen, Erklären, strukturieren. Flexibel, aber nie 100 % exakt und nie gratis.

## Fazit für die weitere Akademie

Klare Architekturidee: **Regeln für Entscheidungen mit Konsequenzen, LLMs für Sprache und Wissen.** Gute KI-Anwendungen kombinieren beides (und Stufe 6 zeigt dir Agenten, die Tools aufrufen – genau diese Trennung).
