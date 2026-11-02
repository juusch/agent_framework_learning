# Aufgabe 12.1 – Extraktion: Entitäten & Beziehungen aus Text 🔬

## Schwierigkeit
Leicht · ⚠️ **Kosten:** mit Key ein LLM-Call (offline: Regel-Fallback, kostenlos)

## Lernziel
Du lässt ein LLM (oder den Offline-Fallback) aus natürlichem Text **strukturierte** Entitäten und Beziehungen extrahieren – mit Pydantic als Vertrag (Stufe 3.3!).

## Warum ist das wichtig?
Der Graph wächst nur, wenn Wissen **automatisch** hineinkommt. Extraktion ist die Schnittstelle zwischen unstrukturierter Welt (Texte, E-Mails, Notizen) und strukturiertem Graph. Pydantic garantiert, dass das LLM liefert, was dein Code erwartet – derselbe Trick wie beim Content-Assistant.

## Das Konzept einfach erklärt
**Metapher – der Leser mit Formular:** Statt den Text frei zusammenzufassen, hält der LLM-Leser ein Formular hin: „Welche Dinge kommen vor? (Feld: Entitäten) Wie hängen sie zusammen? (Feld: Beziehungen)". Text rein, strukturierte Daten raus.

## Die technische Erklärung
- Pydantic-Modell `Extraktion` mit zwei Feldern: `entitaeten` (Liste von `{name, label}`) und `beziehungen` (Liste von `{von, typ, zu}`). Die `description`-Texte sagen dem LLM **was genau** gefragt ist.
- Mit Key: `modell.with_structured_output(Extraktion)` + Text-Prompt.
- Offline: `extrahiere_offline()` – Regel-Logik (bekannte Namen + Muster „X arbeitet bei Y") – gleiches Interface, damit du den **Datenfluss** übst.
- Wichtig: Das LLM schlägt vor, **Python entscheidet**: Labels werden normalisiert, Tippfehler bleiben Tippfehler (nichts landet ungeprüft im Graph – das ist Aufgabe 12.2).

## Voraussetzungen
- Stufe 3.3 (strukturierte Ausgaben), Stufe 10 (Entitäten/Beziehungen)

## Deine Mission
Baue `extract_to_graph.py` (Teil 1 – nur Extraktion):
1. Text selbst schreiben: 2–3 Sätze über die Firma (nutze bekannte Namen: Anna, Ben, Acme, Engineering, AI Assistant) – z. B. „Anna arbeitet bei Acme und gehört zu Engineering. Engineering arbeitet an AI Assistant."
2. `extrahiere(text)` aufrufen und das Ergebnis (Entitäten + Beziehungen) sauber ausgeben.
3. **Zweiter Text mit Stolperfallen:** Tippfehler („Anya") und ein unbekannter Name – beobachte, was passiert (offline: wird schlicht nicht erkannt – ehrlich!).
4. Kontrollfrage notieren: Warum ist ein Pydantic-Vertrag hier wichtiger als „bitte gib JSON zurück" im Prompt?

## Akzeptanzkriterien
- [ ] Die Extraktion liefert `entitaeten` mit `name` + `label` und `beziehungen` mit `von`/`typ`/`zu`.
- [ ] Beide Testtexte laufen ohne Crash (auch mit Stolperfallen).
- [ ] Die Ausgabe trennt klar: was erkannt wurde, was nicht.
- [ ] Du kannst den Unterschied „LLM schlägt vor / Python entscheidet" erklären.

## Hinweise
1. Nutze `extrahiere()` aus `lernakademie/graph_extraction.py` – es kapselt Key/Offline.
2. Labels: Person, Company, Department, Project (normalisiert – der Graph braucht Einheitlichkeit, Stufe 10.2!).
3. Offline formuliere Sätze mit Mustern wie „X arbeitet bei Y" – genau diese erkennt der Fallback.

## Reflexionsfragen
1. Warum führt „das LLM darf selbst Labels erfinden" langfristig zu Graph-Chaos? (Denk an `typ: "Person"` vs. `typ: "Mensch"`!)
2. Was würde passieren, wenn du 500 Dokumente extrahierst – und welche zwei Qualitätshebel hast du (Temperatur 0, klare Schemata)?
3. Warum ist die Extraktion der **teuerste** Teil der Pipeline – und wo könnte man cachen?

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| LLM liefert freies JSON statt Pydantic | `with_structured_output` nutzen (nicht selbst parsen) |
| Labels inkonsistent | Schema-Beschreibung präzisieren; offline: BEKANNTE_LABELS |
| Tippfehler frustrieren offline | erwartetes Verhalten! – echte LLMs sind toleranter, Entity Resolution (12.2) ist die echte Antwort |

## Referenzlösung
→ [`solutions/extract_to_graph.py`](../solutions/extract_to_graph.py)

## Code-Walkthrough
In der Lösungsdatei; besonders die Trennung Text → Extraktion → Ausgabe.

## Was haben wir gelernt?
LLM-Extraktion mit Pydantic-Vertrag, Offline-Fallback, Grenzen beider Modi.

## Was kommt als Nächstes?
Die Extraktion ist da – jetzt wird sie **Graph**: Aufgabe 12.2 überführt Entitäten und Beziehungen in den GraphStore, mit Entity Resolution gegen Duplikate.
