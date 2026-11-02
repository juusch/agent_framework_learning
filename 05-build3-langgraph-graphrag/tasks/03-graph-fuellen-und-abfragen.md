# Aufgabe 5.3 – Vom Text in den Graph: Extraktion & NL→Cypher 🧪

**Schwierigkeit:** Fortgeschritten · **Zeit:** ~60–90 Min · ⚠️ **Kosten:** mit Key LLM-Calls (offline: Regel-Fallback)

## Lernziel
Du lässt ein LLM Entitäten und Beziehungen aus Text extrahieren, fühlst den Graph mit **Entity Resolution** – und übersetzt natürliche Fragen in Cypher, abgesichert durch eine **Whitelist**.

## Warum das wichtig ist
Bislang hast du den Graph von Hand gepflegt. Ab jetzt kann er aus Dokumenten wachsen (Extraktion) und per Frage beantwortet werden (NL→Cypher). **Das Risiko:** Generierte Abfragen sind nicht vertrauenswürdig – ein injizierter Prompt kann `DELETE` erzeugen. Die Bremse: deterministische Whitelist **vor** jeder Ausführung.

## Konzepte
- **Extraktion:** Pydantic-Vertrag (`entitaeten`, `beziehungen`) – das LLM schlägt vor, **Python entscheidet**.
- **Entity Resolution:** `find_node` vor jedem Anlegen – „Acme" zweimal wäre Graph-Gift.
- **NL→Cypher:** Frage → Abfrage → `ist_sicher()` → Ausführung → formatierte Antwort. Der Angriffs-Test (`DETACH DELETE`) wird **abgelehnt – Pflichtnachweis!**

## Deine Mission
1. `extrahiere(text)` – mit Pydantic-Schema (offline: `extrahiere_offline`); teste einen Text mit 3 Beziehungen + einen mit Tippfehler („Anya") – was passiert ehrlich?
2. `fuelle_graph(store, extraktion)` – inkl. **Duplikat-Beweis**: derselbe Text zweimal → null neue Nodes!
3. `beantworte(frage)`: Pipeline Frage → Cypher → `ist_sicher` → ausführen → lesbare Antwort.
4. **Angriffs-Test (Pflicht):** simuliere „generiertes" `MATCH (n) DETACH DELETE n` – zeige die Ablehnung.

## Akzeptanzkriterien
- [ ] Extraktion liefert strukturierte Entitäten + Beziehungen (mit Label!).
- [ ] Der Duplikat-Test zeigt: Entity Resolution wirkt.
- [ ] Drei Fragen werden über den Graph beantwortet (mit Quellen-Fakten).
- [ ] Der Angriffs-Test wird abgelehnt – und du kannst begründen, warum die Prüfung **deterministischer Code** sein muss (kein LLM!).

## Hinweise
1. Alles fertig in `lernakademie/graph_extraction.py` – lies den Code, dann nutze ihn!
2. Offline-Extraktion erkennt bekannte Namen + Muster („X arbeitet bei Y").
3. Denke an Modul 4.2: Parameter statt String-Einsetzung gilt auch hier.

## Reflexionsfragen
1. Warum führt „das LLM darf Labels frei erfinden" zu Graph-Chaos – und was ist die Folge für Abfragen?
2. Was ist der Unterschied zwischen der Ablehnung eines Syntaxfehlers und der Ablehnung eines Angriffs – und warum sollten die **Meldungen** unterschiedlich ausfallen?
3. Was kostet die Extraktion bei 500 Dokumenten – und wo würdest du cachen?

## Referenzlösung + Walkthrough
→ [`solutions/extract_to_graph.py`](../solutions/extract_to_graph.py), [`solutions/nl_to_cypher.py`](../solutions/nl_to_cypher.py)

## Weiter
5.4 – **Build 3 komplett**: der Agent wählt die Route (Vektor/Graph/Hybrid) – und Graph-Änderungen nur mit Freigabe.
