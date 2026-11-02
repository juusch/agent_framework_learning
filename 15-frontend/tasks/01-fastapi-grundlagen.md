# Aufgabe 15.1 – Dein erster API-Endpunkt (FastAPI) 🌐

## Schwierigkeit
Leicht · **Kosten: keine**

## Lernziel
Du baust einen kleinen FastAPI-Server mit einem Chat-Endpunkt, der deinen Akademie-Agenten aufruft – und verstehst Request/Response, JSON, Endpunkte und die automatische Doku.

## Warum ist das wichtig?
Du kennst APIs als **Nutzer** (Stufe 2: dein Code ruft Mistral). Jetzt drehst du den Spieß um: **Dein Python wird der Dienst**, den andere aufrufen. Jede Web-Anwendung der Welt funktioniert nach diesem Muster – und dein Capstone-Frontend wird genau diesen Endpunkt benutzen.

## Das Konzept einfach erklärt
**Metapher – dein eigenes Restaurant:** Bislang warst du Gast bei Mistral (Stufe 2). Jetzt eröffnest du **selbst ein Restaurant**: Die Speisekarte sind deine **Endpunkte** (`/chat`, `/graph`), der Kellner ist FastAPI (nimmt Bestellungen = Requests, bringt Gerichte = Responses), die Küche ist dein LangGraph-Code. Der Browser (später: Streamlit) ist der Gast.

## Die technische Erklärung
- **Endpunkt** = URL + Methode: `@app.post("/chat")` – „schick mir JSON an diese Adresse".
- **Request-Modell** (Pydantic, Stufe 3.3!): `class ChatRequest(BaseModel): nachricht: str` – FastAPI **validiert automatisch**. Falsche Eingabe → klarer 422-Fehler statt Crash.
- **Response**: gibst ein Dict/Modell zurück → FastAPI serialisiert zu JSON.
- **Automatische Doku**: `/docs` – interaktive Swagger-Oberfläche (kostenlos dazugewonnen!).
- Testen **ohne Browser**: `fastapi.testclient.TestClient` – so prüfen wir das alles in CI.

## Voraussetzungen
- Stufe 3 (Chains), Stufe 6.4 (Verlauf) – hier nur als Grundlage; die Aufgabe ist Backend-fokussiert

## Deine Mission
Baue `api_server.py`:
1. FastAPI-App mit `@app.get("/status")` → `{"status": "ok", "modus": "offline/echt"}` (nutze `is_offline_mode()`!).
2. `@app.post("/chat")`: Request `{"nachricht": str}` → ruft deine Chain/Agent auf → Response `{"antwort": str, "modus": str}`.
3. **Sitzungs-Verlauf:** `ChatRequest` optional um `session_id: str = "default"` ergänzen; speichere Nachrichten pro Session in einem Dict (vereinfachtes Gedächtnis – das Capstone macht das sauberer).
4. **Fehlerfall:** Leere Nachricht → HTTP-Fehler 400 mit deutscher Meldung (nicht crashen!).
5. Teste per TestClient (mini-Test in derselben Datei oder als Kommentar) und per `/docs` im Browser.

## Akzeptanzkriterien
- [ ] `/status` liefert Modus-Info (offline ohne Key – erkennbar!).
- [ ] `/chat` antwortet auf Nachrichten (offline: `[OFFLINE]`-Antwort).
- [ ] Der Verlauf pro Session funktioniert (Nachfrage bezieht sich auf Früheres).
- [ ] Leere Nachrichten liefern 400, keine 500er.
- [ ] `/docs` zeigt beide Endpunkte.

## Hinweise
1. Imports: `from fastapi import FastAPI, HTTPException`, `from pydantic import BaseModel`.
2. Agent wiederverwenden: Die einfachste Variante nutzt `get_chat_model()` + Prompt-Chain aus Stufe 3 – fürs Verständnis reicht das; das Capstone bringt den vollen Hybrid-Agenten.
3. TestClient: `from fastapi.testclient import TestClient; client = TestClient(app); client.post("/chat", json={...})`.

## Reflexionsfragen
1. Warum NIEMALS der API-Key im Frontend landen darf (Stufe 9.2!) – was wäre das Äquivalent zum „Kellner, der seine Kreditkarte mitbringt"?
2. Was ist der Vorteil der Pydantic-Validierung AM ENDPUNKT statt „irgendwo im Code"?
3. Warum ist TestClient-gestütztes Testen CI-fähig, Browser-Testen nicht?

## Häufige Fehler
| Fehler | Lösung |
|---|---|
| 422 statt 400 bei leerer Nachricht | 422 = Schema-Verstoß; für „inhaltlich leer" prüfe im Endpunkt und wirf HTTPException(400) |
| Server startet nicht | `uvicorn datei:app` (ohne .py!) im richtigen Ordner |
| Verlauf „vergisst" | Sessions-Dict außerhalb des Endpunkts definieren (global) |

## Referenzlösung
→ [`solutions/api_server.py`](../solutions/api_server.py)

## Code-Walkthrough
In der Lösungsdatei; besonders Request-Modell, Sessions und Fehlerbehandlung.

## Was haben wir gelernt?
Endpunkte, Request/Response-Modelle, Status-Endpunkt, automatische Doku, API-Tests.

## Was kommt als Nächstes?
Jetzt der visuelle Teil: Aufgabe 15.2 koppelt eine Streamlit-Oberfläche an genau diesen Endpunkt – dein erster Chat mit Maus statt Tastatur-Prompt.
