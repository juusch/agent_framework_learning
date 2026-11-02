"""Tests fuer die Graphen-Loesungen (Stufen 5, 7, 9) – komplett offline."""

import importlib.util
import os
from pathlib import Path

os.environ.setdefault("ACADEMY_OFFLINE", "1")

PROJEKT = Path(__file__).resolve().parents[1]


def lade_modul(relativer_pfad: str):
    datei = PROJEKT / relativer_pfad
    spec = importlib.util.spec_from_file_location(datei.stem, datei)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


def test_routing_klassifizierung():
    routing = lade_modul("05-build3-langgraph-graphrag/solutions/routing_graph.py")
    assert routing.klassifizieren({"eingabe": "Falscher Betrag auf der Rechnung"})["kategorie"] == "rechnung"
    assert routing.klassifizieren({"eingabe": "App stuerzt ab"})["kategorie"] == "technisch"
    assert routing.klassifizieren({"eingabe": "Guten Tag"})["kategorie"] == "allgemein"


def test_loop_terminiert_immer():
    loop = lade_modul("05-build3-langgraph-graphrag/solutions/loop_graph.py")
    app = loop.baue_graph()
    ergebnis = app.invoke({"text": "x", "bewertung": 0, "versuche": 0,
                           "max_versuche": 3, "historie": []})
    assert ergebnis["versuche"] <= 3
    assert len(ergebnis["historie"]) >= 1


def test_parallel_workflow():
    parallel = lade_modul("06-agents-und-tools/solutions/parallel_workflow.py")
    app = parallel.baue_graph()
    ergebnis = app.invoke({"text": "eins zwei drei", "befund_1": 0,
                           "befund_2": 0, "befund_3": 0.0, "bericht": ""})
    assert ergebnis["befund_1"] == 3
    assert "3 Woerter" in ergebnis["bericht"]


def test_subgraph_und_aeusserer_graph():
    sub = lade_modul("06-agents-und-tools/solutions/subgraph_workflow.py")
    loop = sub.baue_qualitaets_loop()
    solo = loop.invoke({"text": "test", "bewertung": 0, "versuche": 0, "max_versuche": 2})
    assert "Politur" in solo["text"]
    app = sub.baue_projekt_graph()
    ergebnis = app.invoke({"auftrag": "A", "freigegebenes_produkt": "", "status": ""})
    assert ergebnis["status"] == "versandbereit"
    assert "bewertung" not in ergebnis  # Kapselung: innere Felder fehlen aussen


def test_supervisor_delegation():
    sup = lade_modul("06-agents-und-tools/solutions/supervisor_workflow.py")
    app = sup.baue_supervisor_graph()
    ergebnis = app.invoke({"auftrag": "RAG", "naechster_schritt": "",
                           "stichpunkte": [], "bericht": "", "ergebnis_log": [],
                           "runden": 0, "max_runden": 5})
    assert any("recherche_agent" in e for e in ergebnis["ergebnis_log"])
    assert ergebnis["bericht"]


def test_logging_maskierung():
    demo = lade_modul("08-testing-und-produktion/solutions/logging_demo.py")
    maskiert = demo.maske_geheimnisse("key a1b2c3d4e5f6g7h8i9j0 gelesen")
    assert "a1b2c3d4" not in maskiert
    assert "***" in maskiert
    assert demo.schaetze_kosten(4000, 2000) > 0
