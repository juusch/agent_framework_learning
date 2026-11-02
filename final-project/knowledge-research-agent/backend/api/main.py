"""Die FastAPI-Anwendung des Capstone-Projekts.

Start (aus dem Projektordner knowledge-research-agent):
    uvicorn backend.api.main:app --port 8000
Doku:  http://localhost:8000/docs

Alle Endpunkte laufen offline (ohne Key) – Modus per /status abfragbar.
"""

from __future__ import annotations

import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))  # Akademie-Wurzel
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # Projektordner

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient  # noqa: F401 (Doku)
from langgraph.types import Command

from backend.agents import approval
from backend.graphs.workflow import baue_workflow
from backend.models.schemas import (
    ChatRequest, ChatResponse, DokumentFundstelle, DokumentHochladen,
    FaktVorschlag, Freigabe, GraphResponse, PromptLaborRequest,
    PromptLaborResponse,
)
from backend.retrieval.graph_api import baue_wissens_graph, graph_als_dto
from backend.retrieval.vector import Wissensbasis
from backend.services.session import verlauf_anhaengen, verlauf_holen

from lernakademie.llm_client import get_chat_model, is_offline_mode
from lernakademie.config import llm_zusammenfassung

app = FastAPI(title="Knowledge & Research Agent", version="1.0")

# ---- Dienste (einmal beim Start gebaut – Stufe 6.3-Muster!) ---------------
WISSENSBASIS = Wissensbasis()
GRAPH = baue_wissens_graph()
WORKFLOW = baue_workflow(WISSENSBASIS, GRAPH)
FREIGABE_WORKFLOW = approval.baue_freigabe_workflow(GRAPH)


ANBIETER_LABEL = {
    "mistral": "Mistral Cloud",
    "openai_compatible": "OpenAI-kompatibler Server",
    "offline": "Offline-Modus (Simulation)",
}


@app.get("/status")
def status() -> dict:
    """Lebenszeichen: Anbieter, Modell, Dokumente, Graph-Groesse.

    Zeigt NIE den API-Key – nur ob einer konfiguriert ist.
    """
    info = llm_zusammenfassung()
    return {
        "status": "ok",
        "modus": info["anbieter"],
        "anbieter": ANBIETER_LABEL.get(info["anbieter"], info["anbieter"]),
        "modell": info["modell"],
        "endpoint": info["base_url"].replace("https://", "").replace("http://", ""),
        "api_key": info["api_key"],
        "dokumente": len(WISSENSBASIS.liste()),
        "graph_knoten": len(GRAPH.nodes()),
        "graph_kanten": len(GRAPH.relationships()),
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """Die Hauptfrage: Agent klassifiziert und ruft nur noetige Quellen auf."""
    text = request.nachricht.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Die Nachricht ist leer.")

    ergebnis = WORKFLOW.invoke({
        "frage": text, "route": "", "dokumente": [],
        "graph_fakten": [], "antwort": "",
    })

    dokumente = [DokumentFundstelle(**d) for d in ergebnis["dokumente"]]
    verlauf_anhaengen(request.session_id, {
        "frage": text,
        "antwort": ergebnis["antwort"],
        "route": ergebnis["route"],
        "dokumente": ergebnis["dokumente"],
        "graph_fakten": ergebnis["graph_fakten"],
    })
    return ChatResponse(
        antwort=ergebnis["antwort"],
        route=ergebnis["route"],
        dokumente=dokumente,
        graph_fakten=ergebnis["graph_fakten"],
        modus="offline" if is_offline_mode() else "mistral",
    )


@app.get("/history")
def history(session_id: str = "default") -> dict:
    """Gespraechsverlauf einer Session (vom Backend verwaltet)."""
    return {"session_id": session_id, "eintraege": verlauf_holen(session_id)}


@app.get("/graph", response_model=GraphResponse)
def graph_ansicht() -> GraphResponse:
    """Kompletter Graph fuer den Explorer (Nodes + Edges)."""
    from backend.models.schemas import GraphEdgeDTO, GraphNodeDTO

    daten = graph_als_dto(GRAPH)
    return GraphResponse(
        nodes=[GraphNodeDTO(**n) for n in daten["nodes"]],
        edges=[GraphEdgeDTO(von=e["von"], zu=e["zu"], typ=e["typ"])
               for e in daten["edges"]],
    )


@app.get("/documents")
def dokumente() -> dict:
    """Liste der indexierten Dokumente."""
    return {"dokumente": WISSENSBASIS.liste()}


@app.post("/documents")
def dokument_hochladen(upload: DokumentHochladen) -> dict:
    """Neues Dokument in die Wissensbasis (Vektor-Index) aufnehmen."""
    chunks = WISSENSBASIS.hinzufuegen(upload.titel, upload.inhalt)
    return {"titel": upload.titel, "neue_chunks": chunks}


@app.post("/facts/propose")
def fakt_vorschlagen(vorschlag: FaktVorschlag) -> dict:
    """Fakt vorschlagen -> Workflow pausiert am Freigabe-Interrupt.

    Rueckgabe enthaelt thread_id + Interrupt-Daten; die Freigabe erfolgt
    per /facts/approve mit genau dieser thread_id (Stufe 6.4/14.2-Muster).
    """
    thread_id = vorschlag.von.lower() + "-" + uuid.uuid4().hex[:8]
    config = {"configurable": {"thread_id": thread_id}}
    ergebnis = FREIGABE_WORKFLOW.invoke({
        "von": vorschlag.von, "typ": vorschlag.typ.upper(),
        "zu": vorschlag.zu, "grund": vorschlag.grund,
        "thread_id": thread_id, "ergebnis": "",
    }, config)

    interrupts = ergebnis.get("__interrupt__")
    if interrupts:
        return {"thread_id": thread_id, "status": "wartet_auf_freigabe",
                "details": interrupts[0].value}
    return {"thread_id": thread_id, "status": ergebnis.get("ergebnis", "?")}


@app.post("/facts/approve")
def fakt_freigeben(freigabe: Freigabe) -> dict:
    """Freigabe/Ablehnung: setzt den pausierten Workflow fort."""
    config = {"configurable": {"thread_id": freigabe.thread_id}}
    try:
        fortsetzung = FREIGABE_WORKFLOW.invoke(
            Command(resume=freigabe.genehmigt), config)
    except Exception as fehler:
        raise HTTPException(status_code=404,
                            detail=f"Angehaltener Vorgang nicht gefunden: {fehler}")

    ergebnis = fortsetzung.get("ergebnis", "?")
    if freigabe.genehmigt and "GENEHMIGT" in ergebnis:
        von = GRAPH.find_node(None, name=fortsetzung.get("von", "?"))
        zu = GRAPH.find_node(None, name=fortsetzung.get("zu", "?"))
        if von and zu:  # Entity Resolution (Stufe 12.2)
            GRAPH.add_relationship(von.id, zu.id, fortsetzung.get("typ", "RELATES_TO"))
        else:
            return {"ergebnis": ergebnis + " – aber ein Node fehlt im Graph."}
    return {"ergebnis": ergebnis}


@app.get("/audit")
def audit() -> dict:
    """Audit-Log aller Freigaben und Ablehnungen (Stufe 14.2)."""
    return {"eintraege": list(approval.AUDIT_LOG)}


@app.post("/prompt-labor", response_model=PromptLaborResponse)
def prompt_labor(request: PromptLaborRequest) -> PromptLaborResponse:
    """Experimentier-Werkstatt: freie Prompts + Temperature wirken sichtbar."""
    modell = get_chat_model(temperature=request.temperature)
    antwort = modell.invoke([
        ("system", request.system_prompt),
        ("human", request.user_prompt),
    ])
    return PromptLaborResponse(
        antwort=antwort.content,
        modus="offline" if is_offline_mode() else "mistral",
    )
