# Referenzlösung 15.3 – Architektur-Notizen (Muster)

## Nachweis-Experimente: erwartete Beobachtungen

**1. Kein Key im Frontend** – In `frontend/app.py` (Capstone) existiert kein `MISTRAL_API_KEY`, kein `os.environ["MISTRAL..."]`. Der Schlüssel liegt ausschließlich in der Backend-`.env`. Begründung: Alles, was im Frontend läge, wäre im Browser des Nutzers sichtbar (Dev-Tools!) – wie eine Kreditkarte auf dem Tisch.

**3. Human-in-the-Loop übers Web** – Der Freigabe-Dialog im Capstone ist ein normaler UI-Dialog; das dahinterliegende Backend hat den LangGraph-Workflow per `interrupt()` **angehalten** (Zustand im Checkpointer gesichert) und wartet. Der Klick auf „Genehmigen" schickt einen Request mit `resume=True` – der angehaltene Workflow **läuft an derselben Stelle weiter**. Pausieren im Web funktioniert, weil der Zustand serverseitig lebt, nicht im Browser.

**4. API-Sicherheit** – Nachweis-Kriterien: Pydantic-Schemas an jedem Endpunkt (422 bei Müll), lesende Whitelist für Graph-Zugriffe (`ist_sicher`), Freigabe-Pflicht für Schreibzugriffe. Bewusst fehlend (lokal okay): Login/Auth – im Internet Pflicht: HTTPS, Authentifizierung, Rate-Limits, CORS-Regeln.

**6. Offline/Online als Systemmerkmal** – Ohne Key: Statusanzeige „offline" (aus `/status`), alle Features laufen, Antworten mit `[OFFLINE]`-Prefix. Der Modus ist kein Bugfix, sondern ein **Design-Merkmal** der Akademie: Lernen ohne Kosten und ohne Anmeldung.

## Architektur-Skizze (Muster-Antwort)

Frage → Streamlit-Widget → `requests.post` → FastAPI-Endpunkt (Validierung) → Service-Schicht (Hybrid-Agent) → parallel: Vektor-Retrieval + Graph-Retrieval → Antwort-Synthese → JSON → Streamlit rendert Sprechblase.

## Reflexions-Muster-Antworten

1. „Direkt aufrufen" wäre schneller – aber koppelt UI und Logik unauflöslich: kein zweiter Client möglich, Geheimnisse im UI-Prozess, keine API-Tests. Ab dem ersten zweiten Nutzer (oder dem ersten Wunsch nach anderer Oberfläche) zahlt die Schichtentrennung sich sofort aus.
2. Widerlegung: Der Interrupt pausiert nicht „das Web", sondern den **serverseitigen** Workflow; der Checkpointer hält den Zustand; der Browser fragt nur den Status ab und schickt irgendwann `resume`. Pausiert wird im Backend – das Web ist nur Fernbedienung.
3. Vor dem Internet-Betrieb: HTTPS erzwingen, Benutzer-Authentifizierung, Autorisierung pro Endpunkt, Rate-Limiting/Kostenbudgets, Logging/Monitoring (Stufe 9) – und ein Konzept für Freigabe-Benachrichtigungen (E-Mail/Webhook statt Warte-Schleife).
