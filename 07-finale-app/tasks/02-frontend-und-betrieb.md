# Aufgabe 7.2 – Frontend komplett, API-Schicht & Docker-Betrieb 🖥️

**Schwierigkeit:** Fortgeschritten · **Zeit:** ~60–90 Min · **Kosten:** offline komplett

## Lernziel
Du verstehst, **warum** zwischen Streamlit und Agent eine FastAPI-Schicht liegt, bedienst alle Frontend-Seiten und bringst das System mit Docker Compose (inkl. Neo4j) zum Laufen.

## Was du VERSTEHEN musst (nicht selbst baust)
- **Streamlit** = reines Python, kein JS; Skript läuft pro Interaktion neu → `session_state` als Gedächtnis (Modul 2!).
- **FastAPI** = Schicht für Austauschbarkeit (morgen React/Handy-App an denselben Endpunkten), Geheimnisse nur im Backend, testbar ohne UI.
- **PyVis** = Graph-Visualisierung aus Python-Daten (dein `to_mermaid()` aus 4.1 – jetzt interaktiv!).
- **Sicherheit:** Key niemals im Frontend (F12!), Pydantic an jedem Endpunkt, lesende Whitelist (5.3), Freigabe-Pflicht (5.4). Was (bewusst) fehlt: Login – lokal okay, im Internet Pflicht (Modul 8).

## Deine Mission
1. **Frontend-Tour (alle 7 Bereiche):** Chat (Routen-Badges, Quellen-Expander) · Graph-Explorer (klicken, suchen, Properties) · Dokumente (Upload + Liste + Probe-Frage) · Prompt-Labor (System/User/Temperature live) · Freigaben (genehmigen + ablehnen, Audit) · Verlauf · Status-Sidebar.
2. **Lehr-Version lesen:** `solutions/api_server.py` + `solutions/chat_app.py` (die schlanke Modul-15-Variante): Erkläre in 3 Sätzen den Unterschied zum direkten Aufruf aus Modul 2 – wann reicht direkter Aufruf, wann braucht es die API?
3. **Docker-Betrieb:** `docker compose up --build` im final-project-Ordner; prüfe: Backend-Doku (8000/docs), Frontend (8501), Neo4j-Browser (7474). **Beweis:** `.env` ist NICHT im Image (Check per Dockerfile-Kommentar verstehen).
4. **Fehler-Fall:** Backend stoppen, Frontend öffnen → saubere Fehlermeldung statt White-Screen?

## Akzeptanzkriterien
- [ ] Alle 7 Bereiche einmal bedient (mit konkreter Beobachtung je Bereich).
- [ ] Deine 3-Sätze-Erklärung „direkt vs. API" ist nachvollziehbar.
- [ ] Docker-Compose-Stack läuft; Neo4j erreichbar; Geheimnisse nicht im Image.
- [ ] Der Backend-aus-Fall zeigt eine verständliche Fehlermeldung.

## Hinweise
1. Reihenfolge immer: Backend zuerst, dann Frontend (sonst „connection refused").
2. Ohne Docker: alles läuft auch lokal ohne Neo4j (GraphStore-Fallback im Backend).
3. Nutze `/docs`, um zu prüfen, dass jede UI-Aktion wirklich nur HTTP spricht.

## Reflexionsfragen
1. Warum ist „Streamlit ruft direkt LangChain auf" schneller zu bauen – und warum trotzdem die falsche Architektur für alles, was wächst?
2. Der Interrupt pausiert das **Backend**, nicht den Browser – warum genau funktioniert Freigabe übers Web trotzdem?
3. Was fehlt vor einer Veröffentlichung im Internet? (Nenne 5 Punkte – Modul 8 vertieft sie!)

## Referenzlösung + Walkthrough
→ [`final-project/knowledge-research-agent/`](../../final-project/knowledge-research-agent/README.md), [`solutions/api_server.py`](../solutions/api_server.py), [`solutions/chat_app.py`](../solutions/chat_app.py), [`solutions/architektur_notizen.md`](../solutions/architektur_notizen.md)

## Weiter
[`../08-testing-und-produktion/`](../../08-testing-und-produktion/README.md) – Testing, Sicherheit, Betrieb: dein System wird ernst.
