# Aufgabe 15.2 – Deine erste Chat-Oberfläche (Streamlit) 💬🖥️

## Schwierigkeit
Leicht · **Kosten: keine** (offline voll übbar)

## Lernziel
Du baust eine minimale Chat-Oberfläche mit Streamlit, die per HTTP mit deinem FastAPI-Backend (15.1) spricht – Buttons, Verlauf, Fehlermeldungen.

## Warum ist das wichtig?
Bislang war deine Schnittstelle `input()` im Terminal. Für echte Nutzer (und für dich beim Experimentieren!) braucht es: klickbare Oberflächen, sichtbaren Verlauf, verständliche Fehlermeldungen. Streamlit gibt dir das in **reinem Python** – ohne eine Zeile HTML/JS.

## Was du VERSTEHEN musst vs. BAUST

- **Verstehen:** Die UI schickt HTTP-Requests an dein Backend (genau wie Stufe 2 dein Code bei Mistral tat!) und rendert die JSON-Antwort als Text. Der Verlauf lebt in `st.session_state` – Streamlit läuft **bei jeder Interaktion das Skript neu ab**, deshalb ist Session-State dein Gedächtnis (gleiches Problem wie LLM-Verlauf, gleiche Lösung!).
- **Selbst bauen:** Diese Mini-Version – sie ist bewusst klein (~50 Zeilen).
- **Fertig nutzen:** Das Capstone-Frontend (Graph-Explorer, Agent-Playground, Freigaben) – dort schaust, konfigurierst und experimentierst du, ohne Frontend-Code zu schreiben.

## Das Konzept einfach erklärt
**Metapher – der Fahrkartenschalter mit Anzeigetafel:** Streamlit ist der Schalter (Widgets = Formulare: Textfeld, Button), `requests.post` ist der Bote zum Backend, und `st.chat_message` ist die Anzeigetafel, auf der das Gespräch sichtbar bleibt. Jede Interaktion „baut die Tafel neu" – deshalb muss der bisherige Verlauf im `session_state` gespeichert sein.

## Die technische Erklärung
- `st.session_state.verlauf` = Liste von `{"role": "user"/"assistant", "content": ...}` – auffällig identisch zu deiner Stufe-2.4-Nachrichtenliste!
- `st.chat_input("Frage ...")` → Eingabefeld unten; `st.chat_message("user")` → Sprechblase.
- `requests.post(f"{API_URL}/chat", json={"nachricht": ..., "session_id": ...})` → der Brückenschlag; die Antwort ist `response.json()["antwort"]`.
- **Fehler sichtbar machen:** Backend nicht erreichbar? `st.error(...)` statt stiller Absturz.

## Voraussetzungen
- Aufgabe 15.1 (Backend muss laufen!)

## Deine Mission
Baue `chat_app.py` (Streamlit):
1. Titel + Sidebar-Status: live `/status` abfragen und anzeigen („Backend: erreichbar, Modus: offline").
2. Chat-Verlauf über `st.session_state` ( initials: Begrüßung des Assistenten).
3. Eingabe über `st.chat_input` → POST an dein Backend → Antwort als Sprechblase (aus `st.chat_message("assistant")`).
4. Fehlerfall: Backend nicht erreichbar → `st.error` mit Anleitung („Hast du uvicorn gestartet?"), die App bleibt bedienbar.
5. Bonus-Widget: Slider „Temperatur" in der Sidebar, der als `payload` mitgeschickt wird (dein Backend darf ihn ignorieren – Konzept zählt: **UI steuert Backend-Verhalten**).

## Akzeptanzkriterien
- [ ] Die Oberfläche startet per `streamlit run chat_app.py`.
- [ ] Nachrichten werden im Verlauf sichtbar (nach Reload der Seite weg – okay, Capstone löst das!).
- [ ] Antworten kommen aus dem Backend (offline: `[OFFLINE]`-Antwort sichtbar).
- [ ] Backend-aus-Fall zeigt klare Fehlermeldung, kein White-Screen.

## Hinweise
1. Start-Reihenfolge: erst `uvicorn ... api_server:app`, dann `streamlit run chat_app.py`.
2. `st.session_state.setdefault("verlauf", [...])` – das ist dein „Gedächtnis-Boot".
3. Verhindere Doppel-Render: Die Antwort nur hinzufügen, wenn sie noch nicht drin ist (einfach: direkt nach POST anhängen – Streamlit rendert danach).

## Reflexionsfragen
1. Warum läuft Streamlit bei JEDEM Klick das ganze Skript neu – und warum ist session_state die einzige Rettung für Zustand? (Vergleich: Server-losen vs. dein Terminal-Programm!)
2. Was wäre der Vorteil, wenn das Frontend den Verlauf **nicht** speichert, sondern das Backend (Capstone macht das so!) – Stichwort: Mehrere Geräte/Neuladen?
3. Wo genau entsteht die Temperatur-Auswahl: Frontend, Transport, Backend-Validierung? Wer ist verantwortlich für Grenzwerte (0.0–1.0)?

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| Weißer Screen | Terminal-Ausgabe lesen (`streamlit run ...` zeigt Fehler) |
| Verbindung abgelehnt | Backend-URL/Port prüfen (localhost:8000) |
| Verlauf verschwindet | session_state verwenden, keine normalen Variablen |

## Referenzlösung
→ [`solutions/chat_app.py`](../solutions/chat_app.py)

## Code-Walkthrough
In der Lösungsdatei; besonders session_state-Boot und die requests-Brücke.

## Was haben wir gelernt?
Streamlit-Grundmuster, UI↔Backend-Brücke, Session-State als Gedächtnis, Fehler-UX.

## Was kommt als Nächstes?
15.3 vertieft die Architektur- und Sicherheits-Konzepte, die im Capstone in voller Größe laufen – dann baust du (bzw. nutzt) die Groß-Anwendung.
