# Aufgabe 7.1 – Die finale Anwendung live erleben 🏁

**Schwierigkeit:** Fortgeschritten · **Zeit:** ~90 Min · **Kosten:** offline komplett (mit Key: echte LLM-Formulierungen)

## Lernziel
Du startest das komplette Build-3-System, bedienst **jede** Funktion einmal – und erkennst jede Architektur-Entscheidung aus Modul 5 im Code wieder.

## Warum das wichtig ist
Du hast den Assistenten drei Mal gebaut. **Jetzt siehst du das Ziel in Aktion** – und zwar nicht als Demo, sondern als System mit API, Sitzungen, Freigaben und Quelltransparenz. Das ist der Moment, in dem sich die ganze Reise zusammenfügt.

## Deine Mission (Meilensteine)
1. **M1 – Start:** Backend starten (`uvicorn backend.api.main:app`), `/status` aufrufen (Modus erkennen!), `/docs` öffnen – lies die Endpunktliste: Wo erkennst du deine Aufgaben aus Modul 5 wieder?
2. **M2 – Chat mit Routen:** drei Fragen (vektorlastig, graphlastig, hybrid) – beobachte die Route-Badges und die getrennten Quellen (Doku vs. Graph).
3. **M3 – Wissensbasis:** Dokument hochladen (`/documents`), dann darüber fragen.
4. **M4 – Graph:** `/graph` aufrufen; im Frontend den Explorer bedienen (Node klicken, Properties, Verbindungen, Suche).
5. **M5 – Human-in-the-Loop:** Fakt vorschlagen (`/facts/propose`) → Interrupt-Daten lesen → **einmal genehmigen, einmal ablehnen** – Graph-Status vor/nach prüfen + Audit-Log.
6. **M6 – Code-Recognition:** Öffne `backend/graphs/workflow.py` und `backend/agents/approval.py` und markiere (Kommentar oder auf Papier): „Das ist meine Aufgabe 5.4" / „das ist 6.2" / „das ist 5.2". Mindestens 5 Treffer!

## Akzeptanzkriterien
- [ ] Alle Meilensteine durchgeführt; Backend läuft offline.
- [ ] Freigabe erteilt UND abgelehnt – Graph-Änderung nachweislich korrekt.
- [ ] Deine M6-Markierung benennt mindestens 5 Wiedererkennungen.
- [ ] Du kannst den Weg einer Frage von der Eingabe bis zur Antwort in einem Satz skizzieren.

## Hinweise
1. Alle Endpunkte gehen auch ohne Frontend per `/docs` („Try it out!") –erst API, dann UI ist eine gute Reihenfolge.
2. Offline gilt: Retrieval, Graph, Workflow, Freigaben sind **echt**; nur die Sprachformulierung ist simuliert.
3. Der TestClient-basierte Test-Satz läuft in CI – schau in `final-project/.../tests/`.

## Reflexionsfragen
1. Vergleiche mit deinem Build-1-Assistenten: Was von deinem damaligen Code steckt konzeptionell noch in diesem System?
2. Warum sitzt der Verlauf im **Backend** (Sessions), nicht im Frontend? (Vergleich mit Modul 2!)
3. Was wäre der nächste ehrliche Ausbauschritt, wenn 100 Nutzer kommen? (→ Modul 8!)

## Referenzlösung + Walkthrough
→ [`final-project/knowledge-research-agent/README.md`](../../final-project/knowledge-research-agent/README.md) (Setup + Architektur) und `solutions/architektur_notizen.md`.

## Weiter
7.2 – die Oberfläche komplett + Betrieb mit Docker.
