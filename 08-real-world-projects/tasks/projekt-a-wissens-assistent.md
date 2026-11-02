# Projekt A – Persönlicher Wissens-Assistent 📚

## Schwierigkeit
Fortgeschritten · ⚠️ **Kosten:** LLM/Embedding-Calls nur mit Key (offline: Retrieval echt, Formulierungen simuliert)

## Lernziel & Warum
Du baust die vollständige RAG-Anwendung aus Stufe 4 zu einem **interaktiven Assistenten** aus: Dialogschleife, Gedächtnis der Fragen, mehrere Quellen, immer sichtbare Quellenangaben. Das ist das realistischste „erste eigene Produkt" – genau so funktionieren Firmen-Wissens-Chatbots.

## Konzept
Alles ist bekannt (Stufe 4): Dokumente → Chunks → Embeddings → Chroma → Retrieval → Kontext → LLM. Neu ist die **Verbindung** mit der Dialogschleife aus Stufe 2.4 und der Fehlerrobustheit aus Stufe 3.4.

## Deine Mission – in Meilensteinen

**M1 – Index als wiederverwendbares Modul:** Funktion `baue_index()`, die beide Handbücher lädt, splitte und einen Retriever liefert. Test: Drei Fragen, Treffer mit Quellen.

**M2 – Antwortfunktion:** `beantworte(frage, retriever) -> dict` mit `antwort`, `quellen`, `gefundene_stellen` (Anzahl). Enthält den „Weiß ich nicht"-Fallback.

**M3 – Dialogschleife:** Endlosschleife mit `input()`, `"exit"` beendet; jede Frage/Antwort wird im `verlauf` (Liste) protokolliert; am Ende Ausgabe der Statistik (Anzahl Fragen, unbeantwortete Fragen).

**M4 – Fehlerrobustheit:** Ungültige/leere Eingaben, Retriever ohne Treffer, Chroma-Neuaufbau-Fehler – nichts darf das Programm crashen.

## Akzeptanzkriterien
- [ ] Der Assistent beantwortet Fragen zu beiden Handbüchern mit Quellen.
- [ ] Fragen ohne Treffer führen zur ehrlichen Nicht-Gefunden-Antwort.
- [ ] `"exit"` beendet sauber mit Statistik.
- [ ] Der Index wird nur **einmal** pro Programmstart gebaut.

## Hinweise
1. Du darfst (und sollst!) aus Stufe 4 kopieren – das ist kein Betrug, sondern Software-Wiederverwendung. Verstehe jede kopierte Zeile!
2. Offline: Frag mit Begriffen aus den Dokumenten („Urlaub", „VPN", „Passwort", „Gehalt").

## Reflexionsfragen
1. Wo würdest du ansetzen, um die Antwortqualität zu verbessern (k? Chunkgröße? Prompt)?
2. Was kostet bei 100 Nutzern mit je 50 Fragen pro Tag am meisten – und wie dämpfst du das (Cache? kleineres Modell für simple Fragen?)

## Referenzlösung
→ [`solutions/knowledge_assistant.py`](../solutions/knowledge_assistant.py)

## Was haben wir gelernt?
Zusammensetzen ganzer Systeme, produktionsnaher Dialog, ehrliche Statistik über Grenzen des Systems.
