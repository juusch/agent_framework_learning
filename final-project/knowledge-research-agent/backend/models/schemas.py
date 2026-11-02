"""Pydantic-Schemas: der Vertrag zwischen Frontend und Backend.

Jeder Endpunkt validiert Eingaben gegen diese Modelle (Stufe 3.3 + 15.1)
und liefert strukturierte Antworten – Grundlage fuer Testbarkeit und
die automatische API-Doku.
"""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    nachricht: str = Field(min_length=1, description="Die Frage des Nutzers")
    session_id: str = Field(default="default", description="Gespraechs-ID")
    temperature: float = Field(default=0.0, ge=0.0, le=1.0)


class DokumentFundstelle(BaseModel):
    quelle: str
    textstelle: str


class ChatResponse(BaseModel):
    antwort: str
    route: str
    dokumente: list[DokumentFundstelle] = []
    graph_fakten: list[str] = []
    modus: str


class GraphNodeDTO(BaseModel):
    id: int
    label: str
    name: str
    properties: dict


class GraphEdgeDTO(BaseModel):
    von: int
    zu: int
    typ: str


class GraphResponse(BaseModel):
    nodes: list[GraphNodeDTO]
    edges: list[GraphEdgeDTO]


class DokumentHochladen(BaseModel):
    titel: str = Field(min_length=1)
    inhalt: str = Field(min_length=20, description="Mind. 20 Zeichen")


class FaktVorschlag(BaseModel):
    von: str
    typ: str
    zu: str
    grund: str = ""


class Freigabe(BaseModel):
    thread_id: str
    genehmigt: bool


class PromptLaborRequest(BaseModel):
    system_prompt: str = "Du bist ein hilfreicher Assistent."
    user_prompt: str = Field(min_length=1)
    temperature: float = Field(default=0.0, ge=0.0, le=1.0)


class PromptLaborResponse(BaseModel):
    antwort: str
    modus: str
