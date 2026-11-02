"""Capstone-Tests: komplette API offline ueber den FastAPI-TestClient.

Laufen ohne Key, ohne laufende Server, ohne Docker – CI-faehig.
"""

import os
import sys
from pathlib import Path

os.environ.setdefault("ACADEMY_OFFLINE", "1")

PROJEKT = Path(__file__).resolve().parents[1]
AKADEMIE = PROJEKT.parents[1]
sys.path.insert(0, str(AKADEMIE))
sys.path.insert(0, str(PROJEKT))

from fastapi.testclient import TestClient  # noqa: E402

from backend.api.main import app  # noqa: E402

client = TestClient(app)


def test_status_offline():
    antwort = client.get("/status")
    assert antwort.status_code == 200
    daten = antwort.json()
    assert daten["status"] == "ok"
    assert daten["modus"] == "offline"
    assert daten["graph_knoten"] >= 5
    assert daten["dokumente"] >= 2  # Seed-Dokumente


def test_chat_vektor_route():
    antwort = client.post("/chat", json={
        "session_id": "test-session",
        "nachricht": "Was steht ueber die Abteilung Engineering?"})
    assert antwort.status_code == 200
    daten = antwort.json()
    assert daten["route"] in ("vektor", "hybrid", "graph")
    assert daten["antwort"]  # nie leer
    assert daten["modus"] == "offline"


def test_chat_graph_route():
    antwort = client.post("/chat", json={
        "session_id": "test-session",
        "nachricht": "Wer haengt am AI Assistant dran?"})
    daten = antwort.json()
    assert daten["route"] == "graph"
    assert any("AI Assistant" in fakt for fakt in daten["graph_fakten"])


def test_chat_hybrid_und_quellentrennung():
    antwort = client.post("/chat", json={
        "session_id": "test-session",
        "nachricht": "Was wissen wir gesamt ueber das Projekt?"})
    daten = antwort.json()
    assert daten["route"] == "hybrid"
    # Beide Quellen aktiv -> Quellentrennung gefordert:
    assert daten["dokumente"] or daten["graph_fakten"]


def test_chat_leere_nachricht_400():
    antwort = client.post("/chat", json={"nachricht": "  "})
    assert antwort.status_code == 400


def test_verlauf_pro_session():
    client.post("/chat", json={"session_id": "verlauf-test",
                               "nachricht": "Frage eins"})
    verlauf = client.get("/history", params={"session_id": "verlauf-test"}).json()
    assert len(verlauf["eintraege"]) == 1
    assert verlauf["eintraege"][0]["frage"] == "Frage eins"


def test_graph_ansicht():
    daten = client.get("/graph").json()
    namen = {node["name"] for node in daten["nodes"]}
    assert {"Anna", "Ben", "Acme", "AI Assistant"} <= namen
    assert any(edge["typ"] == "WORKS_FOR" for edge in daten["edges"])


def test_dokument_hochladen_und_suche():
    antwort = client.post("/documents", json={
        "titel": "test-notiz",
        "inhalt": "Dies ist eine Testnotiz ueber die Weiterbildung im Unternehmen."})
    assert antwort.status_code == 200
    assert antwort.json()["neue_chunks"] >= 1
    liste = client.get("/documents").json()["dokumente"]
    assert any(d["titel"] == "test-notiz" for d in liste)


def test_fakt_freigabe_roundtrip():
    """Vorschlag -> Interrupt -> Genehmigung -> Graph enthaelt den Fakt."""
    kanten_vorher = client.get("/status").json()["graph_kanten"]

    vorschlag = client.post("/facts/propose", json={
        "von": "Clara", "typ": "WORKS_FOR", "zu": "Acme",
        "grund": "Steht implizit im Firmenprofil."}).json()
    assert vorschlag["status"] == "wartet_auf_freigabe"
    assert vorschlag["details"]["frage"]

    freigabe = client.post("/facts/approve", json={
        "thread_id": vorschlag["thread_id"], "genehmigt": True}).json()
    assert "GENEHMIGT" in freigabe["ergebnis"]

    kanten_nachher = client.get("/status").json()["graph_kanten"]
    assert kanten_nachher == kanten_vorher + 1


def test_fakt_ablehnung_laesst_graph_unveraendert():
    kanten_vorher = client.get("/status").json()["graph_kanten"]

    vorschlag = client.post("/facts/propose", json={
        "von": "Ben", "typ": "MANAGES", "zu": "Acme",
        "grund": "Vermutung ohne Beleg."}).json()
    freigabe = client.post("/facts/approve", json={
        "thread_id": vorschlag["thread_id"], "genehmigt": False}).json()
    assert "ABGELEHNT" in freigabe["ergebnis"]

    assert client.get("/status").json()["graph_kanten"] == kanten_vorher
    audit = client.get("/audit").json()["eintraege"]
    assert any("ABGELEHNT" in e for e in audit)


def test_freigabe_unbekannter_thread_404():
    antwort = client.post("/facts/approve", json={
        "thread_id": "gibt-es-nicht", "genehmigt": True})
    assert antwort.status_code == 404


def test_prompt_labor():
    antwort = client.post("/prompt-labor", json={
        "system_prompt": "Du bist ein Tester.",
        "user_prompt": "Sag kurz Bescheid.",
        "temperature": 0.5}).json()
    assert antwort["modus"] == "offline"
    assert antwort["antwort"]
