"""Aufgabe 15.1 – Referenzloesung: FastAPI-Backend mit Chat-Endpunkt.

Start:  uvicorn 15-frontend.solutions.api_server:app --reload
        (vom Projektordner aus; oder Datei direkt: uvicorn api_server:app)
Doku:    http://localhost:8000/docs
Offline: laeuft komplett ohne Key – Modus wird im /status gemeldet.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from fastapi import FastAPI, HTTPException
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

from lernakademie.mock_llm import get_chat_model, is_offline_mode

app = FastAPI(title="Lernakademie-API", version="1.0")

# Vereinfachtes Session-Gedaechtnis: {session_id: [nachrichten]}
SESSIONS: dict[str, list[dict]] = {}


class ChatRequest(BaseModel):
    """Request-Schema – FastAPI validiert ALLE Anfragen dagegen (422 statt Crash)."""
    nachricht: str
    session_id: str = "default"
    temperature: float = 0.0


class ChatResponse(BaseModel):
    antwort: str
    modus: str


PROMPT = ChatPromptTemplate.from_messages([
    ("system", "Du bist ein hilfsbereiter Assistent der Lernakademie."),
    ("human", "{nachricht}"),
])


@app.get("/status")
def status() -> dict:
    """Lebenszeichen + Modus (offline/echt) – das Frontend zeigt das an."""
    modus = "offline" if is_offline_mode() else "mistral"
    return {"status": "ok", "modus": modus}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """Chat mit Sitzungs-Gedaechtnis (vereinfachtes Stufe-2.4-Muster im Server)."""
    text = request.nachricht.strip()
    if not text:
        # 400 = "inhaltlich ungueltig" (422 waere nur Schema-Verstoss)
        raise HTTPException(status_code=400, detail="Die Nachricht darf nicht leer sein.")

    verlauf = SESSIONS.setdefault(request.session_id, [])
    verlauf.append({"role": "user", "content": text})

    # Gedaechtnis in die Chain einspeisen (letzte 6 Nachrichten als Kontext):
    kontext = " | ".join(
        f"{e['role']}: {e['content'][:80]}" for e in verlauf[-6:])

    modell = get_chat_model(temperature=request.temperature)
    chain = (
        ChatPromptTemplate.from_messages([
            ("system", "Du bist ein Assistent. Bisheriger Verlauf: {kontext}"),
            ("human", "{nachricht}"),
        ])
        | modell
        | StrOutputParser()
    )
    antwort = chain.invoke({"kontext": kontext, "nachricht": text})

    verlauf.append({"role": "assistant", "content": antwort})
    return ChatResponse(antwort=antwort,
                        modus="offline" if is_offline_mode() else "mistral")


# ---------------------------------------------------------------------------
# Mini-Test (laeuft in der CI; zeigt das TestClient-Muster):
# ---------------------------------------------------------------------------

def test_api() -> None:
    from fastapi.testclient import TestClient

    client = TestClient(app)

    antwort = client.get("/status")
    assert antwort.status_code == 200
    assert antwort.json()["status"] == "ok"

    chat = client.post("/chat", json={"nachricht": "Hallo, ich heisse Alex!",
                                      "session_id": "test"})
    assert chat.status_code == 200
    assert "antwort" in chat.json()

    # Gedaechtnis: Nachfrage in derselben Session
    nachfrage = client.post("/chat", json={
        "nachricht": "Wie heisse ich?", "session_id": "test"})
    assert nachfrage.status_code == 200
    # (Offline spiegelt den Verlauf; mit Key wuerde das Modell ihn nutzen.)

    fehler = client.post("/chat", json={"nachricht": "   ", "session_id": "t2"})
    assert fehler.status_code == 400


if __name__ == "__main__":
    test_api()
    print("Alle Mini-Tests bestanden. Starte den Server mit: uvicorn api_server:app")
